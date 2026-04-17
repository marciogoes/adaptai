"""
Endpoints administrativos para monitoramento do sistema.

Acesso restrito a ADMIN ou SUPER_ADMIN.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.api.dependencies import require_admin
from app.models.user import User
from app.models.background_task import BackgroundTask, BackgroundTaskStatus
from app.services.ai_cache_service import cache_stats, cleanup_old_cache
from app.services.background_tasks import task_manager


router = APIRouter(prefix="/admin", tags=["Admin - Monitoramento"])


@router.get("/ai-cache/stats")
def obter_stats_cache_ia(current_user: User = Depends(require_admin)):
    """
    Retorna estatisticas do cache de IA.
    
    Util para acompanhar economia de creditos Anthropic:
    - total_entries: quantas respostas unicas foram cacheadas
    - total_hits: quantas vezes o cache foi reutilizado (= chamadas economizadas)
    - top_types: quais tipos de material mais se beneficiam
    """
    return cache_stats()


@router.post("/ai-cache/cleanup")
def limpar_cache_ia_antigo(
    ttl_hours: int = 672,
    current_user: User = Depends(require_admin),
):
    """
    Remove entradas de cache nao usadas ha mais de ttl_hours.
    Default: 4 semanas (672h).
    """
    removidos = cleanup_old_cache(ttl_hours=ttl_hours)
    return {
        "removidos": removidos,
        "ttl_hours": ttl_hours,
    }


@router.get("/background-tasks/stats")
def obter_stats_background_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Retorna estatisticas de tarefas em background.
    Util para ver se ha tasks travadas, taxa de falhas, etc.
    """
    por_status = (
        db.query(BackgroundTask.status, func.count(BackgroundTask.id))
        .group_by(BackgroundTask.status)
        .all()
    )
    
    por_tipo = (
        db.query(BackgroundTask.task_type, func.count(BackgroundTask.id))
        .group_by(BackgroundTask.task_type)
        .limit(20)
        .all()
    )
    
    # Ultimas 10 tasks falhas (debugging)
    falhas_recentes = (
        db.query(BackgroundTask)
        .filter(BackgroundTask.status == BackgroundTaskStatus.FAILED)
        .order_by(BackgroundTask.created_at.desc())
        .limit(10)
        .all()
    )
    
    return {
        "por_status": [
            {"status": s.value if s else "null", "count": c}
            for s, c in por_status
        ],
        "por_tipo": [
            {"tipo": t or "null", "count": c}
            for t, c in por_tipo
        ],
        "falhas_recentes": [
            {
                "task_id": t.task_id,
                "task_type": t.task_type,
                "error": (t.error or "")[:200],
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in falhas_recentes
        ],
    }


@router.post("/background-tasks/cleanup")
def limpar_background_tasks_antigas(current_user: User = Depends(require_admin)):
    """Remove tasks mais antigas que o TTL configurado (default 7 dias)."""
    removidos = task_manager.cleanup_old_tasks()
    return {"removidos": removidos or 0}
