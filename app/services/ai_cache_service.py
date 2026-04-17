"""
Service de cache para chamadas a IA.

Uso tipico: envolve o client.messages.create() com lookup+salvamento automatico.

    from app.services.ai_cache_service import cached_completion
    
    response = cached_completion(
        prompt="Gere um mapa mental de fotossintese para 7o ano",
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        cache_type="mapa_mental",
        ttl_hours=168,  # 7 dias
    )

Se prompt identico (mesmo hash) foi chamado antes no mesmo modelo e ainda
nao expirou, retorna resposta cacheada SEM chamar Claude. Caso contrario,
chama Claude, salva no cache e retorna.

Economia tipica em cenarios educacionais: 40-70% das chamadas sao cache hit,
ja que conteudo curricular e repetido entre professores/turmas.
"""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List

from app.database import SessionLocal
from app.models.ai_cache import AICache
from app.core.anthropic_client import get_anthropic_client, get_default_model
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def _hash_prompt(prompt: str, extra: Optional[Dict[str, Any]] = None) -> str:
    """
    Gera hash SHA-256 estavel do prompt + parametros que afetam a resposta.
    
    'extra' pode conter system prompt, tools, etc - qualquer coisa que
    mude o comportamento da IA mesmo com o mesmo user prompt.
    """
    # Normaliza: remove whitespace inconsistente mas preserva quebras intencionais
    normalized = prompt.strip()
    
    if extra:
        # Serializa extra de forma deterministica (sort_keys)
        extra_str = json.dumps(extra, sort_keys=True, ensure_ascii=False)
        normalized += "||" + extra_str
    
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _parse_response_text(response) -> str:
    """Extrai texto da resposta do Claude (pode ter multiplos content blocks)."""
    if not response or not hasattr(response, "content"):
        return ""
    
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts)


def lookup_cache(
    prompt_hash: str,
    model: str,
    ttl_hours: int = 168,
) -> Optional[Dict[str, Any]]:
    """
    Busca resposta cacheada. Retorna None se nao existir ou expirada.
    Se encontrar, incrementa hit_count e atualiza last_hit_at.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)
        
        row = (
            db.query(AICache)
            .filter(
                AICache.prompt_hash == prompt_hash,
                AICache.model == model,
                AICache.created_at >= cutoff,
            )
            .first()
        )
        
        if not row:
            return None
        
        # Incrementar hit_count
        row.hit_count += 1
        row.last_hit_at = datetime.now(timezone.utc)
        db.commit()
        
        logger.info(
            "AI cache hit",
            extra={
                "cache_id": row.id,
                "cache_type": row.cache_type,
                "hit_count": row.hit_count,
            },
        )
        
        return row.response
    except Exception:
        db.rollback()
        logger.warning("Erro ao consultar cache de IA", exc_info=True)
        return None
    finally:
        db.close()


def save_cache(
    prompt_hash: str,
    model: str,
    response: Dict[str, Any],
    cache_type: Optional[str] = None,
):
    """Salva resposta no cache (ignora se falhar - nao deve quebrar fluxo principal)."""
    db = SessionLocal()
    try:
        # Verificar se ja existe (race condition em multi-worker)
        existing = (
            db.query(AICache)
            .filter(
                AICache.prompt_hash == prompt_hash,
                AICache.model == model,
            )
            .first()
        )
        
        if existing:
            # Ja existe - atualiza response (pode ter expirado e estamos salvando novo)
            existing.response = response
            existing.created_at = datetime.now(timezone.utc)
            existing.last_hit_at = datetime.now(timezone.utc)
            db.commit()
            return
        
        entry = AICache(
            prompt_hash=prompt_hash,
            model=model,
            cache_type=cache_type,
            response=response,
            hit_count=0,
        )
        db.add(entry)
        db.commit()
        
        logger.info(
            "Resposta salva em cache de IA",
            extra={"cache_type": cache_type, "prompt_hash": prompt_hash[:12]},
        )
    except Exception:
        db.rollback()
        logger.warning("Erro ao salvar cache de IA", exc_info=True)
    finally:
        db.close()


def cached_completion(
    prompt: str,
    model: Optional[str] = None,
    max_tokens: int = 2048,
    system: Optional[str] = None,
    cache_type: Optional[str] = None,
    ttl_hours: int = 168,
    use_cache: bool = True,
) -> str:
    """
    Wrapper que faz cache automatico de chamadas Claude.
    
    Args:
        prompt: texto do usuario
        model: modelo Claude (default: get_default_model())
        max_tokens: limite de tokens da resposta
        system: system prompt opcional
        cache_type: identificador do tipo de chamada (ex: "mapa_mental")
        ttl_hours: quanto tempo considerar cache valido (default 7 dias)
        use_cache: se False, pula cache (sempre chama Claude)
    
    Returns:
        texto da resposta (string). Para estrutura completa, use client diretamente.
    """
    model = model or get_default_model()
    
    extra = {}
    if system:
        extra["system"] = system
    if max_tokens != 2048:
        extra["max_tokens"] = max_tokens
    
    prompt_hash = _hash_prompt(prompt, extra if extra else None)
    
    # 1. Tentar cache
    if use_cache:
        cached = lookup_cache(prompt_hash, model, ttl_hours)
        if cached and isinstance(cached, dict) and "text" in cached:
            return cached["text"]
    
    # 2. Cache miss - chamar Claude
    client = get_anthropic_client()
    
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system
    
    response = client.messages.create(**kwargs)
    text = _parse_response_text(response)
    
    # 3. Salvar no cache (best effort)
    if use_cache and text:
        try:
            save_cache(
                prompt_hash=prompt_hash,
                model=model,
                response={"text": text},
                cache_type=cache_type,
            )
        except Exception:
            pass  # cache save nunca deve falhar o fluxo principal
    
    return text


def cleanup_old_cache(ttl_hours: int = 168 * 4) -> int:
    """
    Remove entradas de cache mais antigas que ttl_hours.
    Default: 4 semanas - mantem historico mais longo que o TTL de hit (1 semana)
    para poder ver padroes de uso.
    
    Retorna numero de entradas removidas.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=ttl_hours)
        deleted = (
            db.query(AICache)
            .filter(AICache.last_hit_at < cutoff)
            .delete(synchronize_session=False)
        )
        db.commit()
        if deleted:
            logger.info("Cache de IA: entradas antigas removidas", extra={"count": deleted})
        return deleted
    except Exception:
        db.rollback()
        logger.error("Erro no cleanup de cache de IA", exc_info=True)
        return 0
    finally:
        db.close()


def cache_stats() -> Dict[str, Any]:
    """
    Retorna estatisticas do cache para monitoramento.
    """
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        total = db.query(func.count(AICache.id)).scalar() or 0
        total_hits = db.query(func.sum(AICache.hit_count)).scalar() or 0
        
        # Top tipos de cache
        top_types = (
            db.query(AICache.cache_type, func.count(AICache.id), func.sum(AICache.hit_count))
            .group_by(AICache.cache_type)
            .order_by(func.sum(AICache.hit_count).desc())
            .limit(10)
            .all()
        )
        
        return {
            "total_entries": total,
            "total_hits": total_hits,
            "economia_estimada_chamadas": total_hits,  # cada hit = 1 chamada a Claude economizada
            "top_types": [
                {"type": t, "entries": c, "hits": h or 0}
                for t, c, h in top_types
            ],
        }
    finally:
        db.close()
