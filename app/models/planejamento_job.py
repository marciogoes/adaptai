# ============================================
# MODEL - Jobs de Planejamento (Persistência)
# ============================================
# Armazena o estado de jobs de planejamento para
# permitir retomada em caso de interrupção

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"  # Pausado para retomar depois


class PlanejamentoJob(Base):
    """
    Armazena o estado de um job de geração de planejamento.
    Permite retomar processamento em caso de interrupção.
    """
    __tablename__ = "planejamento_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação
    task_id = Column(String(100), unique=True, index=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ano_letivo = Column(String(10), nullable=False)
    
    # Status
    status = Column(String(20), default=JobStatus.PENDING.value)
    progress = Column(Integer, default=0)  # 0-100
    message = Column(String(500))
    
    # Configuração
    componentes_solicitados = Column(JSON)  # Lista de componentes para processar
    
    # Progresso detalhado
    componentes_processados = Column(JSON, default=list)  # Componentes já concluídos
    componente_atual = Column(String(100))  # Componente sendo processado agora
    lote_atual = Column(Integer, default=0)  # Lote dentro do componente atual
    
    # Resultados parciais (salvos conforme processa)
    resultados_parciais = Column(JSON, default=dict)  # {componente: {objetivos: [...]}}
    
    # Resultado final
    resultado_final = Column(JSON)
    pei_id = Column(Integer, ForeignKey("pei.id"), nullable=True)  # PEI criado ao final
    
    # Controle de erros
    tentativas = Column(Integer, default=0)
    ultimo_erro = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Heartbeat - para detectar jobs travados
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    heartbeat_count = Column(Integer, default=0)
    
    # Controle de concorrência
    lock_token = Column(String(100), nullable=True)  # Token único para evitar duplicação
    lock_expires_at = Column(DateTime, nullable=True)  # Expiração do lock
    
    # Relacionamentos
    student = relationship("Student", backref="planejamento_jobs")
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "student_id": self.student_id,
            "ano_letivo": self.ano_letivo,
            "status": self.status,
            "progress": self.progress,
            "message": self.message,
            "componentes_solicitados": self.componentes_solicitados,
            "componentes_processados": self.componentes_processados,
            "componente_atual": self.componente_atual,
            "lote_atual": self.lote_atual,
            "tentativas": self.tentativas,
            "ultimo_erro": self.ultimo_erro,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "pei_id": self.pei_id
        }


class PlanejamentoJobLog(Base):
    """
    Log detalhado de cada etapa do processamento.
    Útil para debug e auditoria.
    """
    __tablename__ = "planejamento_job_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("planejamento_jobs.id"), nullable=False)
    
    # Detalhes
    evento = Column(String(50))  # started, lote_processado, erro, completed, etc.
    componente = Column(String(100))
    lote = Column(Integer)
    mensagem = Column(Text)
    dados = Column(JSON)  # Dados adicionais (ex: quantidade de objetivos gerados)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    job = relationship("PlanejamentoJob", backref="logs")
