"""
Modelo SQLAlchemy para cache de respostas de IA.

MOTIVACAO: geracao de material educacional (25+ tipos) e corrcoes de
redacao fazem muitas chamadas identicas a Anthropic Claude.
Exemplo: professor gera "mapa mental de fotossintese para 7o ano" varias
vezes - o resultado da IA e praticamente o mesmo, mas cada chamada
queima credito Anthropic.

Este cache armazena (hash_prompt, modelo) -> resposta com TTL configuravel.
Hit -> retorna resposta salva; miss -> chama IA, salva e retorna.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Index
from datetime import datetime, timezone

from app.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class AICache(Base):
    """
    Cache de respostas da IA Claude.
    Indexado por (prompt_hash, modelo) para lookup rapido.
    """
    __tablename__ = "ai_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Hash SHA-256 do prompt normalizado (chave de lookup)
    prompt_hash = Column(String(64), nullable=False, index=True)
    
    # Modelo usado (importante: mesmo prompt em modelos diferentes = cache diferente)
    model = Column(String(100), nullable=False)
    
    # Tipo/categoria opcional para debugging (ex: "gerar_material_flashcards")
    cache_type = Column(String(100), nullable=True, index=True)
    
    # Resposta completa da IA (JSON)
    response = Column(JSON, nullable=False)
    
    # Contador de hits (para monitorar eficacia)
    hit_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=_utcnow, nullable=False)
    last_hit_at = Column(DateTime, default=_utcnow, nullable=False)
    
    # Index composto para lookup rapido
    __table_args__ = (
        Index("idx_ai_cache_lookup", "prompt_hash", "model"),
    )
