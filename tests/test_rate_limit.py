"""
Testes do rate limit (in-memory).
"""
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.core.rate_limit import check_rate_limit, _RateLimitStore, _get_client_ip


def _fake_request(ip: str = "1.2.3.4", forwarded: str = None):
    """Monta um Request do FastAPI fake para testar rate_limit."""
    req = MagicMock()
    headers = {}
    if forwarded:
        headers["X-Forwarded-For"] = forwarded
    req.headers = headers
    req.client = MagicMock()
    req.client.host = ip
    return req


class TestRateLimitStore:
    def test_aceita_dentro_do_limite(self):
        store = _RateLimitStore()
        # 3 requests em janela de 60s com limite 5
        for _ in range(3):
            assert store.check("1.1.1.1", "endpoint", max_requests=5, window_seconds=60)
    
    def test_bloqueia_ao_estourar_limite(self):
        store = _RateLimitStore()
        # 5 OKs, 6o bloqueia
        for _ in range(5):
            assert store.check("1.1.1.1", "endpoint", max_requests=5, window_seconds=60)
        assert not store.check("1.1.1.1", "endpoint", max_requests=5, window_seconds=60)
    
    def test_ips_diferentes_sao_independentes(self):
        store = _RateLimitStore()
        # IP A estoura
        for _ in range(5):
            store.check("1.1.1.1", "ep", max_requests=5, window_seconds=60)
        assert not store.check("1.1.1.1", "ep", max_requests=5, window_seconds=60)
        # IP B continua livre
        assert store.check("2.2.2.2", "ep", max_requests=5, window_seconds=60)
    
    def test_chaves_diferentes_sao_independentes(self):
        store = _RateLimitStore()
        # Endpoint A estoura
        for _ in range(3):
            store.check("1.1.1.1", "login", max_requests=3, window_seconds=60)
        assert not store.check("1.1.1.1", "login", max_requests=3, window_seconds=60)
        # Endpoint B continua livre
        assert store.check("1.1.1.1", "register", max_requests=3, window_seconds=60)


class TestGetClientIP:
    def test_usa_x_forwarded_for_quando_presente(self):
        req = _fake_request(ip="127.0.0.1", forwarded="203.0.113.1, 10.0.0.1")
        # Deve pegar o PRIMEIRO IP (cliente original), nao o ultimo
        assert _get_client_ip(req) == "203.0.113.1"
    
    def test_usa_client_host_sem_forwarded(self):
        req = _fake_request(ip="203.0.113.2")
        assert _get_client_ip(req) == "203.0.113.2"


class TestCheckRateLimit:
    def test_levanta_429_quando_estoura(self):
        req = _fake_request(ip="3.3.3.3")
        # Chamar ate estourar - usa chave diferente para nao colidir com outros testes
        for _ in range(2):
            check_rate_limit(req, key="test_429", max_requests=2, window_seconds=60)
        
        with pytest.raises(HTTPException) as exc_info:
            check_rate_limit(req, key="test_429", max_requests=2, window_seconds=60)
        
        assert exc_info.value.status_code == 429
        assert "Retry-After" in exc_info.value.headers
