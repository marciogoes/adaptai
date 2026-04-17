"""
Rate limiting por IP com backend Redis e fallback em memoria.

Arquitetura:
    - Se REDIS_URL estiver configurada, usa Redis (sliding window via ZSET + Lua).
    - Senao, usa dict em memoria (como antes).
    - Se Redis estiver configurado mas ficar offline, degrade graceful para
      memoria e loga WARNING (uma vez por janela de 60s para nao poluir).

Garantias:
    - Atomicidade em Redis via script Lua (sem TOCTOU entre check e add).
    - Thread-safe em memoria via Lock.
    - Rate limiter nao pode derrubar o app: erros de Redis nunca propagam.

Uso em rotas FastAPI (nao muda):

    from app.core.rate_limit import check_rate_limit

    @router.post("/endpoint-caro")
    async def endpoint(request: Request, ...):
        check_rate_limit(request, key="checkout", max_requests=3, window_seconds=3600)
        # ... resto
"""
from __future__ import annotations

import os
import time
import uuid
import logging
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from threading import Lock
from typing import Optional

from fastapi import Request, HTTPException, status

logger = logging.getLogger(__name__)


# ============================================================
# BACKEND INTERFACE
# ============================================================

class _RateLimitBackend(ABC):
    """Interface comum para backends de rate limiting."""

    @abstractmethod
    def check(self, ip: str, key: str, max_requests: int, window_seconds: int) -> bool:
        """Retorna True se a request esta dentro do limite."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...


# ============================================================
# BACKEND EM MEMORIA (deque por (ip, key))
# ============================================================

class _MemoryBackend(_RateLimitBackend):
    """
    Sliding window em memoria usando deque.
    Apropriado para dev (1 worker) ou fallback quando Redis cair.
    """

    name = "memory"

    def __init__(self):
        self._buckets: dict[tuple[str, str], deque] = defaultdict(deque)
        self._lock = Lock()

    def check(self, ip: str, key: str, max_requests: int, window_seconds: int) -> bool:
        now = time.time()
        cutoff = now - window_seconds
        bucket_key = (ip, key)

        with self._lock:
            bucket = self._buckets[bucket_key]
            # Expira timestamps fora da janela (O(k) amortizado)
            while bucket and bucket[0] < cutoff:
                bucket.popleft()

            if len(bucket) >= max_requests:
                return False
            bucket.append(now)
            return True

    def cleanup(self):
        """Remove buckets vazios para nao crescer memoria indefinidamente."""
        with self._lock:
            empty = [k for k, v in self._buckets.items() if not v]
            for k in empty:
                del self._buckets[k]


# ============================================================
# BACKEND REDIS (sliding window atomico via Lua)
# ============================================================

# Script Lua: atomico, sem race entre check e add.
#   KEYS[1] = bucket key
#   ARGV[1] = now (epoch float como string)
#   ARGV[2] = cutoff (now - window)
#   ARGV[3] = max_requests
#   ARGV[4] = window_seconds (para EXPIRE)
#   ARGV[5] = member unico (ex: uuid+now) para nao colidir
# Retorna 1 se aceito, 0 se excedeu.
_LUA_SLIDING_WINDOW = """
redis.call('ZREMRANGEBYSCORE', KEYS[1], 0, ARGV[2])
local count = redis.call('ZCARD', KEYS[1])
if count >= tonumber(ARGV[3]) then
    return 0
end
redis.call('ZADD', KEYS[1], ARGV[1], ARGV[5])
redis.call('EXPIRE', KEYS[1], ARGV[4])
return 1
"""


class _RedisBackend(_RateLimitBackend):
    """
    Sliding window via Redis ZSET + Lua script atomico.

    Conecta no primeiro uso (lazy). Em caso de erro, marca como offline
    por OFFLINE_COOLDOWN segundos e delega para fallback externo.
    """

    name = "redis"
    OFFLINE_COOLDOWN = 30  # segundos antes de tentar reconectar

    def __init__(self, redis_url: str):
        self._url = redis_url
        self._client = None
        self._script_sha: Optional[str] = None
        self._offline_until: float = 0.0
        self._lock = Lock()
        self._last_warn_logged: float = 0.0

    def _ensure_client(self):
        if self._client is not None:
            return self._client

        with self._lock:
            if self._client is not None:
                return self._client
            try:
                import redis  # noqa
                client = redis.Redis.from_url(
                    self._url,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                    decode_responses=True,
                    health_check_interval=30,
                )
                # Testa conexao
                client.ping()
                # Pre-carrega script Lua
                self._script_sha = client.script_load(_LUA_SLIDING_WINDOW)
                self._client = client
                logger.info("Rate limiter: Redis conectado")
            except Exception as e:
                self._mark_offline(e)
                raise
        return self._client

    def _mark_offline(self, err: Exception):
        self._offline_until = time.time() + self.OFFLINE_COOLDOWN
        self._client = None
        self._script_sha = None
        # Loga uma vez a cada cooldown - evita poluicao em rajadas
        now = time.time()
        if now - self._last_warn_logged > self.OFFLINE_COOLDOWN:
            logger.warning(
                "Rate limiter Redis offline, usando fallback em memoria por %ds: %s",
                self.OFFLINE_COOLDOWN, err,
            )
            self._last_warn_logged = now

    def is_offline(self) -> bool:
        return time.time() < self._offline_until

    def check(self, ip: str, key: str, max_requests: int, window_seconds: int) -> bool:
        if self.is_offline():
            raise _RedisUnavailable()

        try:
            client = self._ensure_client()
        except Exception:
            raise _RedisUnavailable()

        now = time.time()
        cutoff = now - window_seconds
        bucket_key = f"rl:{ip}:{key}"
        # Member unico para nao colidir quando dois requests chegam no mesmo microssegundo
        member = f"{now}:{uuid.uuid4().hex[:8]}"

        try:
            result = client.evalsha(
                self._script_sha,
                1,
                bucket_key,
                str(now),
                str(cutoff),
                str(max_requests),
                str(window_seconds + 1),
                member,
            )
            return bool(int(result))
        except Exception as e:
            # Qualquer erro de Redis -> degrade graceful
            self._mark_offline(e)
            raise _RedisUnavailable()


class _RedisUnavailable(Exception):
    """Sinalizador interno: backend Redis indisponivel, usar fallback."""


# ============================================================
# FACTORY + DISPATCHER
# ============================================================

_memory_backend = _MemoryBackend()
_redis_backend: Optional[_RedisBackend] = None


def _init_backends():
    """Inicializa o backend Redis se REDIS_URL estiver setada."""
    global _redis_backend
    if _redis_backend is not None:
        return

    redis_url = os.getenv("REDIS_URL") or os.getenv("RAILWAY_REDIS_URL")
    if redis_url and redis_url.strip():
        _redis_backend = _RedisBackend(redis_url.strip())
        logger.info("Rate limiter configurado com Redis (%s)", _redacted_url(redis_url))
    else:
        logger.info("Rate limiter usando apenas memoria (REDIS_URL nao definido)")


def _redacted_url(url: str) -> str:
    """Ofusca credenciais de uma URL tipo redis://user:pass@host:port/0 para log."""
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        host = p.hostname or "?"
        port = p.port or ""
        return f"{p.scheme}://***@{host}:{port}"
    except Exception:
        return "redis://***"


def _check(ip: str, key: str, max_requests: int, window_seconds: int) -> bool:
    """Dispatcher: tenta Redis, cai para memoria se offline."""
    _init_backends()

    if _redis_backend is not None and not _redis_backend.is_offline():
        try:
            return _redis_backend.check(ip, key, max_requests, window_seconds)
        except _RedisUnavailable:
            pass  # Fallback abaixo

    return _memory_backend.check(ip, key, max_requests, window_seconds)


# ============================================================
# API PUBLICA (compativel com versao anterior)
# ============================================================

def _get_client_ip(request: Request) -> str:
    """
    Extrai IP do cliente, levando em conta proxy reverso.
    Railway e Vercel colocam IP real em X-Forwarded-For.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # Pega o PRIMEIRO IP (cliente original), nao o ultimo
        return forwarded.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"


def check_rate_limit(
    request: Request,
    key: str,
    max_requests: int,
    window_seconds: int,
    error_message: str = None,
):
    """
    Verifica se o IP atingiu o limite de requests para a chave `key`.
    Se sim, levanta HTTPException 429.

    Args:
        request: FastAPI Request (para extrair IP)
        key: identificador do endpoint (ex: "checkout", "login", "gerar_material")
        max_requests: numero maximo de requests na janela
        window_seconds: tamanho da janela em segundos
        error_message: mensagem customizada (opcional)

    Exemplos:
        check_rate_limit(request, "checkout", 3, 3600)  # 3 por hora
        check_rate_limit(request, "login", 10, 60)      # 10 por minuto
        check_rate_limit(request, "gerar_ia", 20, 3600) # 20 por hora
    """
    ip = _get_client_ip(request)

    if not _check(ip, key, max_requests, window_seconds):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_message or "Muitas requisicoes. Tente novamente em alguns minutos.",
            headers={"Retry-After": str(window_seconds)},
        )


def get_store():
    """
    Compat: retorna o backend de memoria (ainda usado por algum teste/cleanup).
    """
    return _memory_backend


def get_active_backend_name() -> str:
    """Util para /health e testes: nome do backend em uso agora."""
    _init_backends()
    if _redis_backend is not None and not _redis_backend.is_offline():
        return "redis"
    return "memory"


# ============================================================
# Compatibilidade retroativa
# ============================================================
# A API antiga expunha `_RateLimitStore`. Mantido como alias para nao quebrar
# testes e imports existentes (tests/test_rate_limit.py).
_RateLimitStore = _MemoryBackend
