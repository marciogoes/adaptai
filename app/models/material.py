"""
Modelos para Materiais de Estudo
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base


class TipoMaterial(str, Enum):
    """Tipos de materiais disponíveis"""
    VISUAL = "visual"
    MAPA_MENTAL = "mapa_mental"


class StatusMaterial(str, Enum):
    """Status de geração do material"""
    GERANDO = "gerando"
    DISPONIVEL = "disponivel"
    ERRO = "erro"


class Material(Base):
    """Material de estudo gerado por IA"""
    __tablename__ = "materiais"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    conteudo_prompt = Column(Text, nullable=False)
    tipo = Column(SQLEnum(TipoMaterial), nullable=False)
    materia = Column(String(100), nullable=False)
    serie_nivel = Column(String(50), nullable=True)
    tags = Column(JSON, nullable=True)
    
    # Caminho do arquivo no storage
    arquivo_path = Column(String(255), nullable=True)  # Ex: "123_visual.html"
    
    # Metadados
    metadados = Column(JSON, nullable=True)  # Tokens usados, tempo de geração, etc
    status = Column(SQLEnum(StatusMaterial), default=StatusMaterial.GERANDO)
    
    # Timestamps
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    criado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    criado_por = relationship("User", back_populates="materiais_criados")
    materiais_alunos = relationship("MaterialAluno", back_populates="material", cascade="all, delete-orphan")


class MaterialAluno(Base):
    """Associação entre material e aluno"""
    __tablename__ = "materiais_alunos"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Datas de acesso
    data_disponibilizacao = Column(DateTime(timezone=True), server_default=func.now())
    data_primeira_visualizacao = Column(DateTime(timezone=True), nullable=True)
    data_ultima_visualizacao = Column(DateTime(timezone=True), nullable=True)
    total_visualizacoes = Column(Integer, default=0)
    
    # Interações do aluno
    favorito = Column(Integer, default=0)  # 0 = não, 1 = sim
    anotacoes_aluno = Column(Text, nullable=True)
    
    # Relacionamentos
    material = relationship("Material", back_populates="materiais_alunos")
    aluno = relationship("Student", back_populates="materiais")
