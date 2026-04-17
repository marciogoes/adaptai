"""
Cliente Anthropic centralizado (singleton lazy).

MOTIVACAO: antes deste modulo, o projeto instanciava Anthropic() em 8+ lugares:
- services/ai_materiais_service.py
- services/redacao_ai_service.py
- services/diario_ai_service.py
- services/planejamento_bncc_completo_service.py
- services/relatorio_processor.py (novo processar_relatorio_com_progresso)
- api/routes/pei.py
- api/routes/relatorios.py
- e outros

Cada instanciacao:
- Faz um novo handshake TLS com api.anthropic.com
- Dificulta trocar modelo globalmente
- Impede rate limiting central
- Nao permite rotacao de API key em runtime

Este modulo resolve centralizando em uma unica instancia lazy.

Uso:

    from app.core.anthropic_client import get_anthropic_client, get_default_model
    
    client = get_anthropic_client()
    response = client.messages.create(
        model=get_default_model(),
        max_tokens=2048,
        messages=[{"role": "user", "content": "Ola"}]
    )

Para tarefas rapidas/baratas (classificacao, extracao simples), use o modelo rapido:

    from app.core.anthropic_client import get_fast_model
    client.messages.create(model=get_fast_model(), ...)

Para cache automatico (ECONOMIA DE CREDITOS), use:

    from app.services.ai_cache_service import cached_completion
    text = cached_completion(prompt="...", cache_type="mapa_mental")
"""
from typing import Optional
from threading import Lock
from app.core.config import settings


# Instancia singleton - inicializada sob demanda
_client = None
_client_lock = Lock()


def get_anthropic_client():
    """
    Retorna a instancia unica do cliente Anthropic.
    Inicializacao lazy + thread-safe (primeira chamada), segura em multi-thread.
    
    Raises:
        RuntimeError: se ANTHROPIC_API_KEY nao estiver configurada.
    """
    global _client
    if _client is not None:
        return _client
    
    with _client_lock:
        # Double-check apos obter lock
        if _client is not None:
            return _client
        
        if not settings.ANTHROPIC_API_KEY or not settings.ANTHROPIC_API_KEY.strip():
            raise RuntimeError(
                "ANTHROPIC_API_KEY nao configurada. "
                "Defina no .env ou nas variaveis de ambiente do Railway."
            )
        # Import lazy - evita erro na inicializacao se anthropic nao estiver instalado
        from anthropic import Anthropic
        _client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    return _client


def reset_anthropic_client():
    """
    Reseta o singleton. Util para testes ou rotacao de API key.
    """
    global _client
    with _client_lock:
        _client = None


def get_default_model() -> str:
    """
    Retorna o modelo Claude padrao para tarefas complexas.
    Controlado por settings.CLAUDE_MODEL.
    
    Fallback: claude-3-5-sonnet-20241022 (modelo mais capaz estavel).
    """
    return settings.CLAUDE_MODEL or "claude-3-5-sonnet-20241022"


def get_fast_model() -> str:
    """
    Retorna um modelo Claude rapido/barato para tarefas simples
    (classificacao, extracao de campos, resumos curtos).
    
    Nao e sobrescrito por config - sempre usa Haiku por ser o mais rapido.
    """
    return "claude-3-haiku-20240307"
