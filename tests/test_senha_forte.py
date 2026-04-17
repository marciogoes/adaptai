"""
Testes unitarios para politica de senha forte (A13).
"""
import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, validar_senha_forte


class TestValidarSenhaForte:
    def test_senha_valida_passa(self):
        """Senha atendendo todos os requisitos deve passar."""
        assert validar_senha_forte("SenhaForte123") == "SenhaForte123"
    
    def test_senha_curta_falha(self):
        with pytest.raises(ValueError, match="pelo menos 10"):
            validar_senha_forte("Abc123")
    
    def test_senha_sem_maiuscula_falha(self):
        with pytest.raises(ValueError, match="maiuscula"):
            validar_senha_forte("senhaforte123")
    
    def test_senha_sem_minuscula_falha(self):
        with pytest.raises(ValueError, match="minuscula"):
            validar_senha_forte("SENHAFORTE123")
    
    def test_senha_sem_numero_falha(self):
        with pytest.raises(ValueError, match="numero"):
            validar_senha_forte("SenhaForteABC")
    
    def test_senha_muito_longa_falha(self):
        with pytest.raises(ValueError, match="muito longa"):
            validar_senha_forte("A" + "b" * 127 + "1")  # 129 chars
    
    def test_senha_obvia_bloqueada(self):
        with pytest.raises(ValueError, match="muito comum"):
            validar_senha_forte("Password123")  # sem bloqueio de caixa
        
        # variacoes case-insensitive tambem bloqueadas
        with pytest.raises(ValueError, match="muito comum"):
            validar_senha_forte("PASSWORD123")


class TestUserCreate:
    def test_usercreate_valida_senha(self):
        """UserCreate deve rejeitar senha fraca."""
        with pytest.raises(ValidationError):
            UserCreate(name="Teste", email="t@t.com", password="senha123")
    
    def test_usercreate_aceita_senha_forte(self):
        user = UserCreate(name="Teste", email="t@t.com", password="SenhaForte123")
        assert user.password == "SenhaForte123"
    
    def test_usercreate_nao_aceita_role(self):
        """UserCreate NAO deve ter campo role (evita escalacao - A4)."""
        # Se passar 'role' no dict, pydantic deve IGNORAR (nao adicionar ao modelo)
        user = UserCreate(
            name="Teste",
            email="t@t.com",
            password="SenhaForte123",
        )
        assert not hasattr(user, "role")
