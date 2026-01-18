"""
📝 AdaptAI - Modelo de Redação ENEM
Sistema de redações com correção por IA nas 5 competências
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

from app.database import Base


class StatusRedacao(str, Enum):
    """Status da redação do aluno"""
    RASCUNHO = "rascunho"           # Aluno ainda está escrevendo
    SUBMETIDA = "submetida"         # Aguardando correção pela IA
    CORRIGIDA = "corrigida"         # Correção finalizada
    ANULADA = "anulada"             # Redação anulada (fuga do tema, etc.)


class TemaRedacao(Base):
    """
    Tema de redação gerado pela IA ou criado manualmente
    Formato completo no estilo ENEM com textos motivadores
    """
    __tablename__ = "temas_redacao"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Tema e proposta
    titulo = Column(String(300), nullable=False)  # Título curto
    tema = Column(Text, nullable=False)           # Tema completo
    proposta = Column(Text, nullable=False)       # Proposta de redação
    
    # Textos motivadores (como no ENEM - até 4 textos)
    texto_motivador_1 = Column(Text, nullable=True)
    texto_motivador_2 = Column(Text, nullable=True)
    texto_motivador_3 = Column(Text, nullable=True)
    texto_motivador_4 = Column(Text, nullable=True)
    
    # Contexto
    area_tematica = Column(String(100), nullable=True)  # Saúde, Tecnologia, Meio Ambiente, etc.
    palavras_chave = Column(JSON, nullable=True)        # Lista de palavras-chave
    
    # Configuração
    nivel_dificuldade = Column(String(20), default="medio")  # facil, medio, dificil
    ativo = Column(Boolean, default=True)
    
    # Controle
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    criado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    criado_por = relationship("User", back_populates="temas_redacao_criados")
    redacoes = relationship("RedacaoAluno", back_populates="tema", cascade="all, delete-orphan")


class RedacaoAluno(Base):
    """
    Redação do aluno com correção nas 5 competências do ENEM
    Nota final de 0 a 1000 pontos
    """
    __tablename__ = "redacoes_alunos"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Vínculo com tema e aluno
    tema_id = Column(Integer, ForeignKey("temas_redacao.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Texto da redação
    titulo_redacao = Column(String(200), nullable=True)  # Título dado pelo aluno
    texto = Column(Text, nullable=True)                   # Texto completo da redação
    
    # Contadores
    quantidade_linhas = Column(Integer, default=0)
    quantidade_palavras = Column(Integer, default=0)
    
    # Status
    status = Column(SQLEnum(StatusRedacao), default=StatusRedacao.RASCUNHO)
    
    # Datas
    iniciado_em = Column(DateTime(timezone=True), server_default=func.now())
    submetido_em = Column(DateTime(timezone=True), nullable=True)
    corrigido_em = Column(DateTime(timezone=True), nullable=True)
    
    # ========================================
    # NOTAS POR COMPETÊNCIA (0-200 cada)
    # ========================================
    # Competência 1: Domínio da norma culta
    nota_competencia_1 = Column(Integer, nullable=True)
    feedback_competencia_1 = Column(Text, nullable=True)
    
    # Competência 2: Compreensão da proposta
    nota_competencia_2 = Column(Integer, nullable=True)
    feedback_competencia_2 = Column(Text, nullable=True)
    
    # Competência 3: Argumentação
    nota_competencia_3 = Column(Integer, nullable=True)
    feedback_competencia_3 = Column(Text, nullable=True)
    
    # Competência 4: Coesão textual
    nota_competencia_4 = Column(Integer, nullable=True)
    feedback_competencia_4 = Column(Text, nullable=True)
    
    # Competência 5: Proposta de intervenção
    nota_competencia_5 = Column(Integer, nullable=True)
    feedback_competencia_5 = Column(Text, nullable=True)
    
    # ========================================
    # NOTA FINAL E FEEDBACK GERAL
    # ========================================
    nota_final = Column(Integer, nullable=True)  # 0-1000 (soma das 5 competências)
    feedback_geral = Column(Text, nullable=True)
    
    # Análise detalhada
    pontos_fortes = Column(JSON, nullable=True)    # Lista de pontos positivos
    pontos_melhoria = Column(JSON, nullable=True)  # Lista de pontos a melhorar
    sugestoes = Column(JSON, nullable=True)        # Sugestões de estudo
    analise_detalhada = Column(JSON, nullable=True)  # Dados completos da correção
    
    # Relacionamentos
    tema = relationship("TemaRedacao", back_populates="redacoes")
    aluno = relationship("Student", back_populates="redacoes")
    
    # Unique constraint: cada aluno só pode ter uma redação por tema
    __table_args__ = (
        {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'},
    )
