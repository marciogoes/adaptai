# ============================================
# SERVICE - Tarefas em Background
# ============================================
# Sistema simples de processamento assíncrono
# Ideal para operações longas como geração de IA

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
from enum import Enum
import threading
import traceback

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskResult:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = TaskStatus.PENDING
        self.progress = 0
        self.message = "Aguardando início..."
        self.result = None
        self.error = None
        self.created_at = datetime.utcnow()
        self.started_at = None
        self.completed_at = None
    
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
    Gerenciador de tarefas em background.
    Armazena tarefas em memória (para produção com múltiplas instâncias, usar Redis)
    """
    
    def __init__(self, max_tasks: int = 100, task_ttl_hours: int = 24):
        self._tasks: Dict[str, TaskResult] = {}
        self._max_tasks = max_tasks
        self._task_ttl = timedelta(hours=task_ttl_hours)
        self._lock = threading.Lock()
    
    def create_task(self) -> str:
        """Cria uma nova tarefa e retorna o ID"""
        task_id = str(uuid.uuid4())
        
        with self._lock:
            # Limpar tarefas antigas
            self._cleanup_old_tasks()
            
            # Criar nova tarefa
            self._tasks[task_id] = TaskResult(task_id)
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[TaskResult]:
        """Obtém uma tarefa pelo ID"""
        return self._tasks.get(task_id)
    
    def update_task(
        self, 
        task_id: str, 
        status: Optional[TaskStatus] = None,
        progress: Optional[int] = None,
        message: Optional[str] = None,
        result: Optional[Any] = None,
        error: Optional[str] = None
    ):
        """Atualiza o status de uma tarefa"""
        task = self._tasks.get(task_id)
        if not task:
            return
        
        with self._lock:
            if status:
                task.status = status
                if status == TaskStatus.PROCESSING and not task.started_at:
                    task.started_at = datetime.utcnow()
                elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    task.completed_at = datetime.utcnow()
            
            if progress is not None:
                task.progress = progress
            if message:
                task.message = message
            if result is not None:
                task.result = result
            if error:
                task.error = error
    
    def _cleanup_old_tasks(self):
        """Remove tarefas antigas"""
        now = datetime.utcnow()
        expired_ids = [
            task_id for task_id, task in self._tasks.items()
            if now - task.created_at > self._task_ttl
        ]
        for task_id in expired_ids:
            del self._tasks[task_id]
        
        # Se ainda tiver muitas, remove as mais antigas completadas
        if len(self._tasks) >= self._max_tasks:
            completed = [
                (task_id, task) for task_id, task in self._tasks.items()
                if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]
            ]
            completed.sort(key=lambda x: x[1].created_at)
            for task_id, _ in completed[:len(completed)//2]:
                del self._tasks[task_id]
    
    async def run_task(
        self, 
        task_id: str, 
        func: Callable,
        *args, 
        **kwargs
    ):
        """
        Executa uma função como tarefa em background.
        A função deve ser async e pode chamar update_progress() para atualizar o progresso.
        """
        try:
            self.update_task(
                task_id, 
                status=TaskStatus.PROCESSING,
                progress=0,
                message="Iniciando processamento..."
            )
            
            # Executa a função passando o task_manager para updates
            result = await func(
                *args, 
                task_id=task_id,
                task_manager=self,
                **kwargs
            )
            
            self.update_task(
                task_id,
                status=TaskStatus.COMPLETED,
                progress=100,
                message="Concluído com sucesso!",
                result=result
            )
            
        except Exception as e:
            error_msg = str(e)
            traceback_str = traceback.format_exc()
            print(f"[TASK ERROR] {task_id}: {error_msg}\n{traceback_str}")
            
            self.update_task(
                task_id,
                status=TaskStatus.FAILED,
                message="Erro no processamento",
                error=error_msg
            )


# Instância global do gerenciador
task_manager = BackgroundTaskManager()


def get_task_manager() -> BackgroundTaskManager:
    """Retorna a instância do gerenciador de tarefas"""
    return task_manager
