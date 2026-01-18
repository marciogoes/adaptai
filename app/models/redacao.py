"""
📝 AdaptAI - Modelo de Redação
Sistema de redações estilo ENEM com correção por IA
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

from app.database import Base


class StatusRedacao(str, Enum):
    """Status da redação"""
    RASCUNHO = "rascunho"           # Aluno ainda está escrevendo
    SUBMETIDA = "submetida"         # Aguardando correção
    CORRIGINDO = "corrigindo"       # IA está corrigindo
    CORRIGIDA = "corrigida"         # Correção finalizada
    ERRO = "erro"                   # Erro na correção


class TemaRedacao(Base):
    """
    Tema de redação gerado pela IA
    Baseado em temas atuais e relevantes
    """
    __tablename__ = "temas_redacao"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Tema principal
    titulo = Column(String(500), nullable=False)
    tema_completo = Column(Text, nullable=False)  # Proposta completa estilo ENEM
    
    # Textos motivadores (como no ENEM)
    textos_motivadores = Column(JSON, nullable=True)  # Lista de textos
    
    # Contexto
    area_tematica = Column(String(100), nullable=True)  # Saúde, Tecnologia, Meio Ambiente, etc.
    palavras_chave = Column(JSON, nullable=True)
    
    # Metadados
    fonte_inspiracao = Column(String(255), nullable=True)  # Notícia que inspirou
    nivel_dificuldade = Column(String(20), default="medio")  # facil, medio, dificil
    
    # Controle
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    criado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    criado_por = relationship("User", back_populates="temas_criados")
    redacoes = relationship("Redacao", back_populates="tema")


class Redacao(Base):
    """
    Redação do aluno
    """
    __tablename__ = "redacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Vínculo com tema e aluno
    tema_id = Column(Integer, ForeignKey("temas_redacao.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Texto da redação
    titulo_redacao = Column(String(255), nullable=True)  # Título dado pelo aluno
    texto = Column(Text, nullable=True)  # Texto completo da redação
    
    # Contadores
    quantidade_palavras = Column(Integer, default=0)
    quantidade_linhas = Column(Integer, default=0)
    quantidade_paragrafos = Column(Integer, default=0)
    
    # Status
    status = Column(SQLEnum(StatusRedacao), default=StatusRedacao.RASCUNHO)
    
    # Datas
    iniciada_em = Column(DateTime(timezone=True), server_default=func.now())
    submetida_em = Column(DateTime(timezone=True), nullable=True)
    corrigida_em = Column(DateTime(timezone=True), nullable=True)
    
    # Tempo
    tempo_escrita_minutos = Column(Integer, nullable=True)
    
    # Relacionamentos
    tema = relationship("TemaRedacao", back_populates="redacoes")
    aluno = relationship("Student", back_populates="redacoes")
    correcao = relationship("CorrecaoRedacao", back_populates="redacao", uselist=False)


class CorrecaoRedacao(Base):
    """
    Correção da redação no padrão ENEM
    5 competências, cada uma valendo 0-200 pontos
    Total: 0-1000 pontos
    """
    __tablename__ = "correcoes_redacao"
    
    id = Column(Integer, primary_key=True, index=True)
    redacao_id = Column(Integer, ForeignKey("redacoes.id"), nullable=False, unique=True)
    
    # ========================================
    # COMPETÊNCIA 1: Domínio da escrita formal
    # ========================================
    # Demonstrar domínio da modalidade escrita formal da língua portuguesa
    comp1_nota = Column(Integer, default=0)  # 0-200
    comp1_nivel = Column(Integer, default=0)  # 0-5 (níveis do ENEM)
    comp1_comentario = Column(Text, nullable=True)
    comp1_erros = Column(JSON, nullable=True)  # Lista de erros encontrados
    
    # ========================================
    # COMPETÊNCIA 2: Compreensão da proposta
    # ========================================
    # Compreender a proposta e aplicar conceitos para desenvolver o tema
    comp2_nota = Column(Integer, default=0)
    comp2_nivel = Column(Integer, default=0)
    comp2_comentario = Column(Text, nullable=True)
    comp2_analise = Column(JSON, nullable=True)  # Análise da abordagem
    
    # ========================================
    # COMPETÊNCIA 3: Argumentação
    # ========================================
    # Selecionar, relacionar, organizar e interpretar informações
    comp3_nota = Column(Integer, default=0)
    comp3_nivel = Column(Integer, default=0)
    comp3_comentario = Column(Text, nullable=True)
    comp3_argumentos = Column(JSON, nullable=True)  # Argumentos identificados
    
    # ========================================
    # COMPETÊNCIA 4: Coesão textual
    # ========================================
    # Demonstrar conhecimento dos mecanismos linguísticos necessários
    comp4_nota = Column(Integer, default=0)
    comp4_nivel = Column(Integer, default=0)
    comp4_comentario = Column(Text, nullable=True)
    comp4_conectivos = Column(JSON, nullable=True)  # Uso de conectivos
    
    # ========================================
    # COMPETÊNCIA 5: Proposta de intervenção
    # ========================================
    # Elaborar proposta de intervenção respeitando os direitos humanos
    comp5_nota = Column(Integer, default=0)
    comp5_nivel = Column(Integer, default=0)
    comp5_comentario = Column(Text, nullable=True)
    comp5_elementos = Column(JSON, nullable=True)  # Elementos da proposta
    
    # ========================================
    # NOTA FINAL E FEEDBACK
    # ========================================
    nota_total = Column(Integer, default=0)  # 0-1000
    
    # Feedback geral
    feedback_geral = Column(Text, nullable=True)
    pontos_fortes = Column(JSON, nullable=True)
    pontos_melhorar = Column(JSON, nullable=True)
    sugestoes_estudo = Column(JSON, nullable=True)
    
    # Texto corrigido (com marcações)
    texto_corrigido_html = Column(Text, nullable=True)
    
    # Metadados da correção
    modelo_ia = Column(String(50), default="claude")
    tempo_correcao_segundos = Column(Integer, nullable=True)
    corrigida_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    redacao = relationship("Redacao", back_populates="correcao")
