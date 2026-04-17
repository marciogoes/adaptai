"""
SERVICE - Tarefas em Background (persistidas no DB)

E2 MIGRADO: antes usava dict em memoria, agora usa tabela background_tasks.

API publica mantem compatibilidade: create_task(), get_task(), update_task(),
run_task() continuam funcionando como antes.

Diferencas internas:
- Tarefas persistem atraves de deploys e restarts
- Funciona em multi-worker (todos os workers veem as mesmas tarefas)
- Pode-se fazer SELECT ad-hoc no MySQL para debugar estado de tarefas antigas
"""
import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Callable
from enum import Enum
import traceback

from app.database import SessionLocal
from app.models.background_task import BackgroundTask, BackgroundTaskStatus
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def _utcnow():
    return datetime.now(timezone.utc)


# Re-exporta o enum com nome antigo para compatibilidade
class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResult:
    """
    Objeto leve em memoria que espelha um registro de BackgroundTask do DB.
    Mantido por compatibilidade com callers que usam task.to_dict().
    """
    def __init__(self, row: BackgroundTask):
        self.task_id = row.task_id
        self.status = TaskStatus(row.status.value if row.status else "pending")
        self.progress = row.progress or 0
        self.message = row.message or ""
        self.result = row.result
        self.error = row.error
        self.created_at = row.created_at
        self.started_at = row.started_at
        self.completed_at = row.completed_at
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "progress": self.progress,
            "message": self.message,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": (self.completed_at - self.started_at).total_seconds() if self.completed_at and self.started_at else None
        }


class BackgroundTaskManager:
    """
    Gerenciador de tarefas em background persistidas no DB.
    Cada operacao abre sua propria sessao e fecha imediatamente.
    """
    
    def __init__(self, task_ttl_hours: int = 24 * 7):
        # TTL default: 7 dias (antes era 24h, mas agora que persiste no DB
        # podemos manter mais tempo para audit trail)
        self._task_ttl = timedelta(hours=task_ttl_hours)
    
    def create_task(
        self,
        task_type: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
        student_id: Optional[int] = None,
    ) -> str:
        """
        Cria nova tarefa e retorna o task_id publico (UUID).
        
        Args opcionais novos (nao obrigatorios - codigo antigo continua funcionando):
        - task_type: classificacao da tarefa para filtros ("gerar_material", etc)
        - input_data: JSON com parametros de entrada
        - user_id / student_id: quem criou
        """
        task_id = str(uuid.uuid4())
        db = SessionLocal()
        try:
            task = BackgroundTask(
                task_id=task_id,
                status=BackgroundTaskStatus.PENDING,
                progress=0,
                message="Aguardando inicio...",
                task_type=task_type,
                input_data=input_data,
                created_by_user_id=user_id,
                created_by_student_id=student_id,
            )
            db.add(task)
            db.commit()
            return task_id
        finally:
            db.close()
    
    def get_task(self, task_id: str) -> Optional[TaskResult]:
        """Busca tarefa pelo task_id publico (UUID)."""
        db = SessionLocal()
        try:
            row = db.query(BackgroundTask).filter(BackgroundTask.task_id == task_id).first()
            if not row:
                return None
            return TaskResult(row)
        finally:
            db.close()
    
    def update_task(
        self,
        task_id: str,
        status: Optional[TaskStatus] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result: Optional[Any] = None,
        error: Optional[str] = None,
    ):
        """Atualiza status de uma tarefa no DB."""
        db = SessionLocal()
        try:
            row = db.query(BackgroundTask).filter(BackgroundTask.task_id == task_id).first()
            if not row:
                return
            
            if status:
                row.status = BackgroundTaskStatus(status.value)
                if status == TaskStatus.PROCESSING and not row.started_at:
                    row.started_at = _utcnow()
                elif status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
                    row.completed_at = _utcnow()
            
            if progress is not None:
                # clamp 0-100
                row.progress = max(0, min(100, int(progress)))
            if message:
                row.message = message[:500]  # respeitar limite da coluna
            if result is not None:
                row.result = result
            if error:
                row.error = error
            
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error("Erro ao atualizar task", extra={"task_id": task_id}, exc_info=True)
        finally:
            db.close()
    
    def cleanup_old_tasks(self):
        """
        Remove tarefas antigas (mais velhas que task_ttl).
        Pode ser chamado periodicamente em background ou no startup.
        """
        db = SessionLocal()
        try:
            cutoff = _utcnow() - self._task_ttl
            deleted = db.query(BackgroundTask).filter(
                BackgroundTask.created_at < cutoff
            ).delete(synchronize_session=False)
            db.commit()
            if deleted:
                logger.info("Tarefas antigas removidas", extra={"count": deleted})
            return deleted
        except Exception as e:
            db.rollback()
            logger.error("Erro no cleanup de tasks", exc_info=True)
            return 0
        finally:
            db.close()
    
    async def run_task(
        self,
        task_id: str,
        func: Callable,
        *args,
        **kwargs,
    ):
        """
        Executa uma funcao como tarefa em background.
        A funcao recebe task_id e task_manager como kwargs e pode chamar
        update_task() para atualizar progresso.
        """
        try:
            self.update_task(
                task_id,
                status=TaskStatus.PROCESSING,
                progress=0,
                message="Iniciando processamento...",
            )
            
            result = await func(
                *args,
                task_id=task_id,
                task_manager=self,
                **kwargs,
            )
            
            self.update_task(
                task_id,
                status=TaskStatus.COMPLETED,
                progress=100,
                message="Concluido com sucesso!",
                result=result,
            )
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            logger.error(
                "Task falhou com excecao",
                extra={"task_id": task_id},
                exc_info=True,
            )
            
            self.update_task(
                task_id,
                status=TaskStatus.FAILED,
                message="Erro no processamento",
                error=error_msg,
            )


# Instancia global do gerenciador (stateless agora - seguro em multi-worker)
task_manager = BackgroundTaskManager()


def get_task_manager() -> BackgroundTaskManager:
    """Retorna a instancia do gerenciador de tarefas"""
    return task_manager
