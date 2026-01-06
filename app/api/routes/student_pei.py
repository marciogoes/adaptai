# ============================================
# ROTAS - PEI do Estudante (Portal do Aluno)
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

from app.database import get_db
from app.models.student import Student
from app.models.pei import PEI, PEIObjetivo
from app.api.routes.student_provas import get_current_student

router = APIRouter()


# ============================================
# SCHEMAS
# ============================================

class ObjetivoResumo(BaseModel):
    id: int
    area: str
    titulo: str
    descricao: Optional[str]
    trimestre: Optional[int]
    status: str
    valor_atual: Optional[float]
    valor_alvo: Optional[float]
    prazo: Optional[date]
    codigo_bncc: Optional[str]
    
    class Config:
        from_attributes = True


class PEIResumo(BaseModel):
    id: int
    ano_letivo: str
    status: str
    data_inicio: Optional[date]
    data_fim: Optional[date]
    total_objetivos: int
    objetivos_por_area: dict
    objetivos_por_status: dict
    progresso_geral: float
    objetivos: List[ObjetivoResumo]
    
    class Config:
        from_attributes = True


# ============================================
# ROTAS
# ============================================

@router.get("/meu-pei", response_model=Optional[PEIResumo])
def get_meu_pei(
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Retorna o PEI ativo do estudante logado
    """
    # Buscar PEI ativo do aluno
    pei = db.query(PEI).filter(
        PEI.student_id == current_student.id,
        PEI.status.in_(["ativo", "rascunho"])  # Mostrar rascunho também por enquanto
    ).order_by(PEI.created_at.desc()).first()
    
    if not pei:
        return None
    
    # Buscar objetivos
    objetivos = db.query(PEIObjetivo).filter(
        PEIObjetivo.pei_id == pei.id
    ).order_by(PEIObjetivo.trimestre, PEIObjetivo.area).all()
    
    # Calcular estatísticas
    objetivos_por_area = {}
    objetivos_por_status = {}
    total_progresso = 0
    
    for obj in objetivos:
        # Por área
        area = obj.area or "outro"
        if area not in objetivos_por_area:
            objetivos_por_area[area] = 0
        objetivos_por_area[area] += 1
        
        # Por status
        status = obj.status or "nao_iniciado"
        if status not in objetivos_por_status:
            objetivos_por_status[status] = 0
        objetivos_por_status[status] += 1
        
        # Progresso
        if obj.valor_atual and obj.valor_alvo and obj.valor_alvo > 0:
            total_progresso += (float(obj.valor_atual) / float(obj.valor_alvo)) * 100
    
    progresso_geral = total_progresso / len(objetivos) if objetivos else 0
    
    # Montar resposta
    objetivos_lista = []
    for obj in objetivos:
        objetivos_lista.append(ObjetivoResumo(
            id=obj.id,
            area=obj.area or "outro",
            titulo=obj.titulo or "",
            descricao=obj.descricao,
            trimestre=obj.trimestre,
            status=obj.status or "nao_iniciado",
            valor_atual=float(obj.valor_atual) if obj.valor_atual else 0,
            valor_alvo=float(obj.valor_alvo) if obj.valor_alvo else 100,
            prazo=obj.prazo,
            codigo_bncc=obj.codigo_bncc
        ))
    
    return PEIResumo(
        id=pei.id,
        ano_letivo=pei.ano_letivo or "2025",
        status=pei.status or "rascunho",
        data_inicio=pei.data_inicio,
        data_fim=pei.data_fim,
        total_objetivos=len(objetivos),
        objetivos_por_area=objetivos_por_area,
        objetivos_por_status=objetivos_por_status,
        progresso_geral=progresso_geral,
        objetivos=objetivos_lista
    )


@router.get("/meu-pei/objetivos")
def get_meus_objetivos(
    trimestre: Optional[int] = None,
    area: Optional[str] = None,
    db: Session = Depends(get_db),
    current_student: Student = Depends(get_current_student)
):
    """
    Lista os objetivos do PEI com filtros opcionais
    """
    # Buscar PEI ativo
    pei = db.query(PEI).filter(
        PEI.student_id == current_student.id,
        PEI.status.in_(["ativo", "rascunho"])
    ).order_by(PEI.created_at.desc()).first()
    
    if not pei:
        return []
    
    # Query de objetivos
    query = db.query(PEIObjetivo).filter(PEIObjetivo.pei_id == pei.id)
    
    if trimestre:
        query = query.filter(PEIObjetivo.trimestre == trimestre)
    
    if area:
        query = query.filter(PEIObjetivo.area == area)
    
    objetivos = query.order_by(PEIObjetivo.trimestre, PEIObjetivo.area).all()
    
    return [
        {
            "id": obj.id,
            "area": obj.area,
            "titulo": obj.titulo,
            "descricao": obj.descricao,
            "trimestre": obj.trimestre,
            "status": obj.status,
            "valor_atual": float(obj.valor_atual) if obj.valor_atual else 0,
            "valor_alvo": float(obj.valor_alvo) if obj.valor_alvo else 100,
            "prazo": obj.prazo.isoformat() if obj.prazo else None,
            "codigo_bncc": obj.codigo_bncc,
            "estrategias": obj.estrategias,
            "adaptacoes": obj.adaptacoes
        }
        for obj in objetivos
    ]
