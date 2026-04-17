"""
Modelo SQLAlchemy para tarefas em background persistidas no DB.

MOTIVACAO (E2): antes, BackgroundTaskManager armazenava tudo em dict Python
em memoria. Isso tem tres problemas:
1. Tarefas perdidas em deploy / restart do container (Railway faz isso frequentemente).
2. Em multi-worker (uvicorn com --workers>1), cada worker tem seu proprio dict;
   request de status pode cair em worker diferente e retornar 404.
3. Sem historico durave - impossivel debugar "qual prompt foi enviado para aquela geracao
   que falhou ha 2 dias".

Esta tabela resolve os tres.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum, ForeignKey
from datetime import datetime, timezone
import enum

from app.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class BackgroundTaskStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BackgroundTask(Base):
    """
    Tarefa em background persistida.
    
    Uso tipico:
    - Request chega, cria-se uma tarefa -> retorna task_id
    - BackgroundTaskManager processa em async
    - Cliente faz polling em GET /tasks/{task_id} para ver status
    """
    __tablename__ = "background_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # task_id publico (UUID) - exposto ao cliente, separado do id numerico interno
    task_id = Column(String(36), unique=True, index=True, nullable=False)
    
    # Status e progresso
    status = Column(
        Enum(BackgroundTaskStatus, values_callable=lambda x: [e.value for e in x]),
        default=BackgroundTaskStatus.PENDING,
        nullable=False,
        index=True
    )
    progress = Column(Integer, default=0)  # 0-100
    message = Column(String(500), default="Aguardando inicio...")
    
    # Metadados opcionais (tipo de tarefa, payload de entrada, etc)
    task_type = Column(String(100), index=True)  # ex: "gerar_material", "analise_laudo"
    input_data = Column(JSON, nullable=True)      # parametros originais
    
    # Resultado ou erro
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    
    # Auditoria
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by_student_id = Column(Integer, ForeignKey("students.id", ondelete="SET NULL"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=_utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        duration = None
        if self.completed_at and self.started_at:
            duration = (self.completed_at - self.started_at).total_seconds()
        
        return {
            "task_id": self.task_id,
            "status": self.status.value if self.status else None,
            "progress": self.progress or 0,
            "message": self.message or "",
            "task_type": self.task_type,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": duration,
        }
