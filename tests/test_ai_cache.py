"""
Testes do helper de cache de IA.
"""
import hashlib
from unittest.mock import patch, MagicMock

from app.services.ai_cache_service import _hash_prompt


class TestHashPrompt:
    def test_hash_deterministico(self):
        """Mesmo prompt deve gerar mesmo hash."""
        h1 = _hash_prompt("Teste prompt")
        h2 = _hash_prompt("Teste prompt")
        assert h1 == h2
    
    def test_prompts_diferentes_hashes_diferentes(self):
        h1 = _hash_prompt("Prompt A")
        h2 = _hash_prompt("Prompt B")
        assert h1 != h2
    
    def test_normaliza_whitespace_beiradas(self):
        """Trim nas pontas nao deve alterar hash."""
        h1 = _hash_prompt("  Prompt com espacos  ")
        h2 = _hash_prompt("Prompt com espacos")
        assert h1 == h2
    
    def test_preserva_whitespace_interno(self):
        """Quebras de linha intencionais DEVEM afetar hash (prompt diferente)."""
        h1 = _hash_prompt("linha 1\nlinha 2")
        h2 = _hash_prompt("linha 1 linha 2")
        assert h1 != h2
    
    def test_extra_afeta_hash(self):
        """Parametros extras devem mudar o hash."""
        h1 = _hash_prompt("Teste", extra={"system": "voce eh professor"})
        h2 = _hash_prompt("Teste", extra={"system": "voce eh aluno"})
        h3 = _hash_prompt("Teste")
        assert h1 != h2
        assert h1 != h3
    
    def test_extra_sort_keys_deterministico(self):
        """Ordem das chaves do extra nao deve afetar hash."""
        h1 = _hash_prompt("Teste", extra={"a": 1, "b": 2})
        h2 = _hash_prompt("Teste", extra={"b": 2, "a": 1})
        assert h1 == h2
    
    def test_hash_e_sha256_hex(self):
        """Deve produzir hex de SHA-256 (64 chars)."""
        h = _hash_prompt("teste")
        assert len(h) == 64
        # Deve ser hexadecimal valido
        int(h, 16)  # nao levanta ValueError
