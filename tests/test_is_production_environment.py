"""
Testes do helper is_production_environment().

Motivacao: o deploy de 17/04/2026 quebrou porque os checks de producao eram
inconsistentes entre config.py e main.py. Este helper centraliza a logica,
entao precisa estar bem coberto.

Testamos a funcao pura - nao reimportamos config para evitar interagir com
conftest.py (que seta DATABASE_URL/SECRET_KEY globalmente).
"""
import pytest

from app.core.config import is_production_environment


class TestIsProductionEnvironment:
    def setup_method(self):
        """Limpa sinais de producao de testes anteriores."""
        # Usa pytest monkeypatch no lugar seria melhor, mas como nao temos
        # acesso a ele fora de metodos de teste, fazemos manual via fixture.
        pass

    def _limpar(self, monkeypatch):
        for k in ("RAILWAY_ENVIRONMENT", "RAILWAY_PROJECT_ID", "RAILWAY_SERVICE_ID",
                  "PRODUCTION", "ENVIRONMENT"):
            monkeypatch.delenv(k, raising=False)

    def test_sem_sinais_retorna_false(self, monkeypatch):
        self._limpar(monkeypatch)
        assert is_production_environment() is False

    def test_railway_environment_set_retorna_true(self, monkeypatch):
        self._limpar(monkeypatch)
        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
        assert is_production_environment() is True

    def test_railway_project_id_set_retorna_true(self, monkeypatch):
        """Railway moderno nao seta RAILWAY_ENVIRONMENT mas sempre seta PROJECT_ID."""
        self._limpar(monkeypatch)
        monkeypatch.setenv("RAILWAY_PROJECT_ID", "some-uuid-abc")
        assert is_production_environment() is True

    @pytest.mark.parametrize("valor", ["1", "true", "TRUE", "yes", "on"])
    def test_production_flag_variantes_true(self, monkeypatch, valor):
        self._limpar(monkeypatch)
        monkeypatch.setenv("PRODUCTION", valor)
        assert is_production_environment() is True

    @pytest.mark.parametrize("valor", ["0", "false", "no", "off", ""])
    def test_production_flag_falsy(self, monkeypatch, valor):
        self._limpar(monkeypatch)
        monkeypatch.setenv("PRODUCTION", valor)
        assert is_production_environment() is False

    def test_environment_production_retorna_true(self, monkeypatch):
        """Caso do railway.toml: [env] ENVIRONMENT = 'production'."""
        self._limpar(monkeypatch)
        monkeypatch.setenv("ENVIRONMENT", "production")
        assert is_production_environment() is True

    def test_environment_staging_retorna_false(self, monkeypatch):
        """Staging nao e producao - permite testes isolados."""
        self._limpar(monkeypatch)
        monkeypatch.setenv("ENVIRONMENT", "staging")
        assert is_production_environment() is False

    def test_whitespace_so_retorna_false(self, monkeypatch):
        """RAILWAY_ENVIRONMENT=' ' nao deve contar."""
        self._limpar(monkeypatch)
        monkeypatch.setenv("RAILWAY_ENVIRONMENT", "   ")
        assert is_production_environment() is False
