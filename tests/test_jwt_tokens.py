"""
Testes do sistema de JWT (access + refresh tokens - A10).
"""
import pytest
from datetime import timedelta
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    verify_password,
    get_password_hash,
)


class TestPasswordHashing:
    def test_hash_e_verify_funcionam(self):
        senha = "SenhaForte123"
        hashed = get_password_hash(senha)
        assert hashed != senha
        assert verify_password(senha, hashed)
    
    def test_senha_errada_falha(self):
        hashed = get_password_hash("SenhaForte123")
        assert not verify_password("SenhaErrada456", hashed)


class TestAccessToken:
    def test_cria_e_decodifica(self):
        token = create_access_token({"sub": "user@test.com"})
        payload = decode_access_token(token)
        
        assert payload is not None
        assert payload["sub"] == "user@test.com"
        assert payload["type"] == "access"
        assert "exp" in payload
    
    def test_token_invalido_retorna_none(self):
        assert decode_access_token("nao-e-um-jwt-valido") is None
        assert decode_access_token("") is None
    
    def test_expires_delta_customizado(self):
        token = create_access_token(
            {"sub": "user@test.com"},
            expires_delta=timedelta(seconds=1),
        )
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["type"] == "access"


class TestRefreshToken:
    def test_cria_refresh_com_type_correto(self):
        token = create_refresh_token({"sub": "user@test.com"})
        payload = decode_access_token(token)  # usa decode generico
        
        assert payload is not None
        assert payload["sub"] == "user@test.com"
        assert payload["type"] == "refresh"
    
    def test_decode_refresh_valida_type(self):
        refresh = create_refresh_token({"sub": "user@test.com"})
        payload = decode_refresh_token(refresh)
        
        assert payload is not None
        assert payload["type"] == "refresh"
    
    def test_decode_refresh_rejeita_access_token(self):
        """Access token passado em endpoint de refresh deve ser rejeitado."""
        access = create_access_token({"sub": "user@test.com"})
        assert decode_refresh_token(access) is None
    
    def test_decode_refresh_rejeita_token_invalido(self):
        assert decode_refresh_token("lixo") is None
        assert decode_refresh_token("") is None
