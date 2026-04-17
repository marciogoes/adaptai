"""
Testes do dispatcher do rate_limit: validam que quando Redis esta offline,
o sistema degrade graceful para o backend de memoria, sem propagar erro.

NAO testa conectividade real com Redis - isso requer container vivo, o que
faz mais sentido em testes de integracao (fora daqui).
"""
from unittest.mock import MagicMock, patch

import pytest

from app.core import rate_limit


def _fake_request(ip: str = "7.7.7.7"):
    req = MagicMock()
    req.headers = {}
    req.client = MagicMock()
    req.client.host = ip
    return req


class TestDispatcher:
    def setup_method(self):
        """Reset estado global antes de cada teste."""
        rate_limit._redis_backend = None
        rate_limit._memory_backend = rate_limit._MemoryBackend()

    def test_usa_memoria_quando_redis_url_nao_setado(self, monkeypatch):
        monkeypatch.delenv("REDIS_URL", raising=False)
        monkeypatch.delenv("RAILWAY_REDIS_URL", raising=False)

        assert rate_limit.get_active_backend_name() == "memory"

    def test_degrade_graceful_se_redis_falha_ao_conectar(self, monkeypatch):
        """Se Redis estiver configurado mas nao responder, deve cair para memoria."""
        monkeypatch.setenv("REDIS_URL", "redis://host-que-nao-existe-lala:6379")

        # Forca reinicializacao do backend
        rate_limit._redis_backend = None
        rate_limit._init_backends()

        # Antes de tentar conectar, backend redis existe mas nao foi testado
        assert rate_limit._redis_backend is not None

        # Primeira chamada deve falhar internamente e cair para memoria.
        # O dispatcher NAO deve propagar excecao.
        req = _fake_request()
        try:
            rate_limit.check_rate_limit(req, key="x", max_requests=100, window_seconds=60)
        except Exception as e:
            # Unica excecao aceitavel seria 429, e nao pode vir de rede
            pytest.fail(f"Rate limit propagou excecao em vez de degrade: {e}")

        # Apos falhar, deve estar marcado como offline por 30s
        assert rate_limit._redis_backend.is_offline()
        assert rate_limit.get_active_backend_name() == "memory"

    def test_limite_funciona_em_memoria_mesmo_com_redis_offline(self, monkeypatch):
        """Regression: rate limit nao pode deixar de funcionar em fallback."""
        monkeypatch.setenv("REDIS_URL", "redis://host-inexistente:6379")
        rate_limit._redis_backend = None

        req = _fake_request(ip="8.8.8.8")
        # Limite de 2 em 60s
        rate_limit.check_rate_limit(req, key="fallback_test", max_requests=2, window_seconds=60)
        rate_limit.check_rate_limit(req, key="fallback_test", max_requests=2, window_seconds=60)

        with pytest.raises(Exception) as exc:
            rate_limit.check_rate_limit(req, key="fallback_test", max_requests=2, window_seconds=60)
        # Deve ser HTTPException 429, nao erro de rede
        assert getattr(exc.value, "status_code", None) == 429


class TestUrlRedacted:
    def test_url_com_senha_e_ofuscada(self):
        url = "redis://default:super-secret-pass@redis.internal:6379/0"
        redacted = rate_limit._redacted_url(url)
        assert "super-secret-pass" not in redacted
        assert "redis.internal" in redacted
        assert "6379" in redacted

    def test_url_malformada_nao_explode(self):
        assert rate_limit._redacted_url("lixo-que-nao-e-url") == "redis://***"
