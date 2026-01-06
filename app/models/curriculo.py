# ============================================
# MODELOS - Currículo Nacional (BNCC)
# ============================================

from sqlalchemy import Column, Integer, String, Text, JSON, Enum, DateTime, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class DificuldadeCurriculo(str, enum.Enum):
    FUNDAMENTAL = "fundamental"
    INTERMEDIARIO = "intermediario"
    AVANCADO = "avancado"


class CurriculoNacional(Base):
    """
    Tabela que armazena as habilidades da BNCC
    """
    __tablename__ = "curriculo_nacional"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação BNCC
    codigo_bncc = Column(String(20), unique=True, index=True)
    ano_escolar = Column(String(10), index=True)  # "1º ano", "2º ano", etc
    componente = Column(String(50), index=True)   # Matemática, Português, etc
    
    # Organização
    campo_experiencia = Column(String(100))       # "Números e Álgebra"
    eixo_tematico = Column(String(100))           # "Operações"
    
    # Conteúdo
    habilidade_codigo = Column(String(20))
    habilidade_descricao = Column(Text)
    objeto_conhecimento = Column(Text)
    
    # Extras
    exemplos_atividades = Column(JSON, nullable=True)  # Lista de exemplos
    prerequisitos = Column(JSON, nullable=True)        # Lista de códigos BNCC pré-requisitos
    
    # Classificação
    dificuldade = Column(String(20), default="intermediario")
    trimestre_sugerido = Column(Integer, nullable=True)  # 1, 2, 3 ou 4
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    objetivos_pei = relationship("PEIObjetivo", back_populates="curriculo_nacional")


class MapeamentoPrerequisitos(Base):
    """
    Mapeia os pré-requisitos entre habilidades
    """
    __tablename__ = "mapeamento_prerequisitos"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Habilidade principal
    habilidade_codigo = Column(String(20), index=True)
    habilidade_titulo = Column(String(255))
    ano_escolar = Column(String(10))
    
    # Pré-requisito
    prerequisito_codigo = Column(String(20), index=True)
    prerequisito_titulo = Column(String(255))
    ano_prerequisito = Column(String(10))
    
    # Relevância
    essencial = Column(Boolean, default=True)
    peso = Column(DECIMAL(3, 2), default=1.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CurriculoEscola(Base):
    """
    Currículo personalizado da escola (opcional)
    """
    __tablename__ = "curriculo_escola"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Vínculo com currículo nacional
    curriculo_nacional_id = Column(Integer, ForeignKey("curriculo_nacional.id"), nullable=True)
    
    # Identificação
    ano_escolar = Column(String(10))
    disciplina = Column(String(50))
    unidade_tematica = Column(String(100))
    
    # Conteúdo
    titulo = Column(String(255))
    descricao = Column(Text)
    objetivos_aprendizagem = Column(JSON)
    
    # Período
    periodo = Column(String(20))  # bimestre_1, bimestre_2, etc
    carga_horaria_estimada = Column(Integer)
    
    # Recursos
    materiais_necessarios = Column(JSON)
    avaliacoes_sugeridas = Column(JSON)
    
    # Criação
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
