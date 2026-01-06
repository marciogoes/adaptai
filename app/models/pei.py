# ============================================
# MODELOS - PEI (Plano Educacional Individualizado)
# ============================================

from sqlalchemy import Column, Integer, String, Text, JSON, Enum, DateTime, ForeignKey, Date, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class StatusPEI(str, enum.Enum):
    RASCUNHO = "rascunho"
    ATIVO = "ativo"
    EM_REVISAO = "em_revisao"
    CONCLUIDO = "concluido"
    ARQUIVADO = "arquivado"


class TipoPeriodo(str, enum.Enum):
    ANUAL = "anual"
    SEMESTRAL = "semestral"


class AreaPEI(str, enum.Enum):
    MATEMATICA = "matematica"
    PORTUGUES = "portugues"
    CIENCIAS = "ciencias"
    HISTORIA = "historia"
    GEOGRAFIA = "geografia"
    SOCIOEMOCIONAL = "socioemocional"
    AUTONOMIA = "autonomia"
    OUTRO = "outro"


class StatusObjetivo(str, enum.Enum):
    NAO_INICIADO = "nao_iniciado"
    EM_PROGRESSO = "em_progresso"
    ATINGIDO = "atingido"
    PARCIALMENTE_ATINGIDO = "parcialmente_atingido"
    NAO_ATINGIDO = "nao_atingido"
    CANCELADO = "cancelado"


class OrigemObjetivo(str, enum.Enum):
    IA_SUGESTAO = "ia_sugestao"
    PROFESSOR_MANUAL = "professor_manual"
    IA_AJUSTADO = "ia_ajustado"
    DIAGNOSTICO = "diagnostico"


class PEI(Base):
    """
    Plano Educacional Individualizado
    """
    __tablename__ = "peis"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Período
    ano_letivo = Column(String(10))  # "2025"
    tipo_periodo = Column(String(20), default="anual")
    semestre = Column(Integer, nullable=True)
    
    # Datas
    data_inicio = Column(Date)
    data_fim = Column(Date)
    data_proxima_revisao = Column(Date)
    
    # Perfil consolidado
    diagnosticos = Column(JSON, nullable=True)
    pontos_fortes = Column(JSON, nullable=True)
    desafios = Column(JSON, nullable=True)
    estilo_aprendizagem = Column(JSON, nullable=True)
    desempenho_atual = Column(JSON, nullable=True)
    adaptacoes_atuais = Column(JSON, nullable=True)
    contexto_familiar = Column(Text, nullable=True)
    
    # Avaliação diagnóstica vinculada
    avaliacao_diagnostica_id = Column(Integer, nullable=True)
    baseline_estabelecido = Column(Boolean, default=False)
    
    # Sugestões da IA
    ia_sugestoes_originais = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(20), default="rascunho", index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="peis")
    created_by_user = relationship("User", foreign_keys=[created_by])
    objetivos = relationship("PEIObjetivo", back_populates="pei", cascade="all, delete-orphan")
    ajustes = relationship("PEIAjuste", back_populates="pei", cascade="all, delete-orphan")
    atividades = relationship("AtividadePEI", back_populates="pei", cascade="all, delete-orphan")


class PEIObjetivo(Base):
    """
    Objetivo específico dentro de um PEI
    """
    __tablename__ = "pei_objetivos"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    pei_id = Column(Integer, ForeignKey("peis.id"), nullable=False, index=True)
    
    # Área
    area = Column(String(50), index=True)  # matematica, portugues, etc
    
    # Vínculo com currículo
    curriculo_nacional_id = Column(Integer, ForeignKey("curriculo_nacional.id"), nullable=True)
    codigo_bncc = Column(String(20), nullable=True)
    
    # Conteúdo
    titulo = Column(String(255))
    descricao = Column(Text)
    
    # Meta SMART
    meta_especifica = Column(Text)
    criterio_medicao = Column(String(255))
    valor_alvo = Column(DECIMAL(5, 2))
    prazo = Column(Date)
    trimestre = Column(Integer, index=True)
    
    # Detalhes pedagógicos
    adaptacoes = Column(JSON, nullable=True)
    estrategias = Column(JSON, nullable=True)
    materiais_recursos = Column(JSON, nullable=True)
    criterios_avaliacao = Column(JSON, nullable=True)
    
    # Progresso
    valor_atual = Column(DECIMAL(5, 2), default=0)
    status = Column(String(30), default="nao_iniciado", index=True)
    
    # Origem
    origem = Column(String(30), default="ia_sugestao")
    ia_sugestao_original = Column(JSON, nullable=True)
    
    # Justificativa
    justificativa = Column(JSON, nullable=True)
    
    # Timestamps
    ultima_atualizacao = Column(DateTime(timezone=True))
    observacoes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    pei = relationship("PEI", back_populates="objetivos")
    curriculo_nacional = relationship("CurriculoNacional", back_populates="objetivos_pei")
    registros_progresso = relationship("PEIProgressLog", back_populates="objetivo", cascade="all, delete-orphan")
    atividades = relationship("AtividadePEI", back_populates="objetivo", cascade="all, delete-orphan")
    sequencia = relationship("SequenciaObjetivo", back_populates="objetivo", uselist=False, cascade="all, delete-orphan")


class PEIProgressLog(Base):
    """
    Registro de progresso em um objetivo
    """
    __tablename__ = "pei_progress_logs"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("pei_objetivos.id"), nullable=False, index=True)
    assessment_id = Column(Integer, nullable=True)
    
    observation = Column(Text)
    progress_value = Column(DECIMAL(5, 2))
    
    ai_analysis = Column(Text, nullable=True)
    ai_suggestions = Column(JSON, nullable=True)
    
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    objetivo = relationship("PEIObjetivo", back_populates="registros_progresso")
    professor = relationship("User", foreign_keys=[recorded_by])


class PEIAjuste(Base):
    """
    Histórico de ajustes no PEI
    """
    __tablename__ = "pei_adjustments"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    pei_id = Column(Integer, ForeignKey("peis.id"), nullable=False, index=True)
    
    adjustment_type = Column(String(50))  # goal_added, goal_modified, etc
    description = Column(Text)
    reason = Column(Text)
    
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    
    adjusted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    adjusted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    pei = relationship("PEI", back_populates="ajustes")
    professor = relationship("User", foreign_keys=[adjusted_by])
