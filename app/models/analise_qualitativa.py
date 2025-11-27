"""
Modelo de Análise Qualitativa
"""
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AnaliseQualitativa(Base):
    """Modelo de Análise Qualitativa das Provas"""
    __tablename__ = "analises_qualitativas"
    
    id = Column(Integer, primary_key=True, index=True)
    prova_aluno_id = Column(Integer, ForeignKey("provas_alunos.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Análise geral
    pontos_fortes = Column(Text)
    pontos_fracos = Column(Text)
    conteudos_revisar = Column(JSON)  # Lista de conteúdos
    recomendacoes = Column(Text)
    
    # Análise por conteúdo
    analise_por_conteudo = Column(JSON)  # {"Álgebra": {"acertos": 2, "erros": 3, ...}}
    
    # Métricas
    nivel_dominio = Column(String(50))  # excelente, bom, regular, precisa_melhorar
    areas_prioridade = Column(JSON)  # ["Álgebra", "Geometria"]
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    prova_aluno = relationship("ProvaAluno", back_populates="analise_qualitativa")
