# ============================================
# ROUTER - Calendário de Atividades PEI
# ============================================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime, timedelta
from pydantic import BaseModel

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.pei import PEI
from app.models.atividade_pei import AtividadePEI, TipoAtividade, StatusAtividade
from app.services.calendario_atividades_service import CalendarioAtividadesService


router = APIRouter(prefix="/calendario", tags=["Calendário de Atividades"])


# ============================================
# SCHEMAS
# ============================================

class GerarCalendarioRequest(BaseModel):
    pei_id: int
    data_inicio: Optional[date] = None


class AtualizarStatusRequest(BaseModel):
    status: str
    observacoes: Optional[str] = None


class AtividadeResponse(BaseModel):
    id: int
    pei_id: int
    objetivo_id: Optional[int]
    student_id: int
    tipo: str
    titulo: str
    descricao: Optional[str]
    data_programada: date
    status: str
    duracao_estimada_min: Optional[int]
    ordem_sequencial: Optional[int]
    instrucoes: Optional[str]
    material_id: Optional[int] = None
    prova_id: Optional[int] = None
    
    class Config:
        from_attributes = True


# ============================================
# ENDPOINTS - Geração de Calendário
# ============================================

@router.post("/gerar")
async def gerar_calendario_pei(
    request: GerarCalendarioRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera o calendário completo de atividades para um PEI.
    Cria automaticamente materiais, exercícios e provas para cada objetivo.
    """
    
    # Verificar se o PEI existe
    pei = db.query(PEI).filter(PEI.id == request.pei_id).first()
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Verificar se já existe calendário
    atividades_existentes = db.query(AtividadePEI).filter(
        AtividadePEI.pei_id == request.pei_id
    ).count()
    
    if atividades_existentes > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Este PEI já possui {atividades_existentes} atividades no calendário. Use o endpoint de regeneração se quiser substituir."
        )
    
    service = CalendarioAtividadesService(db)
    
    try:
        resultado = await service.gerar_calendario_completo(
            pei_id=request.pei_id,
            user_id=current_user.id,
            data_inicio=request.data_inicio
        )
        
        return {
            "success": True,
            "message": f"Calendário gerado com sucesso!",
            **resultado
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/regenerar/{pei_id}")
async def regenerar_calendario_pei(
    pei_id: int,
    data_inicio: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Regenera o calendário de um PEI, excluindo as atividades anteriores.
    """
    
    # Excluir atividades existentes
    db.query(AtividadePEI).filter(AtividadePEI.pei_id == pei_id).delete()
    db.commit()
    
    service = CalendarioAtividadesService(db)
    
    try:
        resultado = await service.gerar_calendario_completo(
            pei_id=pei_id,
            user_id=current_user.id,
            data_inicio=data_inicio
        )
        
        return {
            "success": True,
            "message": "Calendário regenerado com sucesso!",
            **resultado
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# ENDPOINTS - Consulta de Atividades
# ============================================

@router.get("/aluno/{student_id}")
async def listar_atividades_aluno(
    student_id: int,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    status: Optional[str] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todas as atividades de um aluno com filtros opcionais.
    """
    
    query = db.query(AtividadePEI).filter(AtividadePEI.student_id == student_id)
    
    if data_inicio:
        query = query.filter(AtividadePEI.data_programada >= data_inicio)
    
    if data_fim:
        query = query.filter(AtividadePEI.data_programada <= data_fim)
    
    if status:
        query = query.filter(AtividadePEI.status == status)
    
    if tipo:
        query = query.filter(AtividadePEI.tipo == tipo)
    
    atividades = query.order_by(AtividadePEI.data_programada).all()
    
    return {
        "total": len(atividades),
        "atividades": [
            {
                "id": a.id,
                "pei_id": a.pei_id,
                "objetivo_id": a.objetivo_id,
                "tipo": a.tipo.value if a.tipo else None,
                "titulo": a.titulo,
                "descricao": a.descricao,
                "data_programada": a.data_programada.isoformat() if a.data_programada else None,
                "status": a.status.value if a.status else None,
                "duracao_estimada_min": a.duracao_estimada_min,
                "material_id": a.material_id,
                "material_aluno_id": a.material_aluno_id,
                "prova_id": a.prova_id,
                "prova_aluno_id": a.prova_aluno_id,
                "instrucoes": a.instrucoes
            }
            for a in atividades
        ]
    }


@router.get("/aluno/{student_id}/semana")
async def listar_atividades_semana(
    student_id: int,
    data_referencia: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista as atividades da semana de um aluno.
    """
    
    service = CalendarioAtividadesService(db)
    return service.listar_atividades_semana(student_id, data_referencia)


@router.get("/aluno/{student_id}/hoje")
async def listar_atividades_hoje(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista as atividades de hoje de um aluno.
    """
    
    hoje = date.today()
    
    atividades = db.query(AtividadePEI).filter(
        AtividadePEI.student_id == student_id,
        AtividadePEI.data_programada == hoje
    ).order_by(AtividadePEI.ordem_sequencial).all()
    
    return {
        "data": hoje.isoformat(),
        "total": len(atividades),
        "pendentes": sum(1 for a in atividades if a.status == StatusAtividade.PENDENTE),
        "atividades": [
            {
                "id": a.id,
                "tipo": a.tipo.value,
                "titulo": a.titulo,
                "status": a.status.value,
                "duracao_min": a.duracao_estimada_min,
                "material_aluno_id": a.material_aluno_id,
                "prova_aluno_id": a.prova_aluno_id,
                "instrucoes": a.instrucoes
            }
            for a in atividades
        ]
    }


@router.get("/aluno/{student_id}/proximas")
async def listar_proximas_atividades(
    student_id: int,
    limite: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista as próximas atividades pendentes de um aluno.
    """
    
    hoje = date.today()
    
    atividades = db.query(AtividadePEI).filter(
        AtividadePEI.student_id == student_id,
        AtividadePEI.data_programada >= hoje,
        AtividadePEI.status.in_([StatusAtividade.PENDENTE, StatusAtividade.EM_ANDAMENTO])
    ).order_by(AtividadePEI.data_programada).limit(limite).all()
    
    return {
        "total": len(atividades),
        "atividades": [
            {
                "id": a.id,
                "tipo": a.tipo.value,
                "titulo": a.titulo,
                "data_programada": a.data_programada.isoformat(),
                "status": a.status.value,
                "duracao_min": a.duracao_estimada_min,
                "material_aluno_id": a.material_aluno_id,
                "prova_aluno_id": a.prova_aluno_id
            }
            for a in atividades
        ]
    }


@router.get("/aluno/{student_id}/atrasadas")
async def listar_atividades_atrasadas(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista atividades atrasadas de um aluno.
    """
    
    hoje = date.today()
    
    atividades = db.query(AtividadePEI).filter(
        AtividadePEI.student_id == student_id,
        AtividadePEI.data_programada < hoje,
        AtividadePEI.status.in_([StatusAtividade.PENDENTE, StatusAtividade.EM_ANDAMENTO])
    ).order_by(AtividadePEI.data_programada).all()
    
    # Marcar como atrasadas
    for a in atividades:
        if a.status == StatusAtividade.PENDENTE:
            a.status = StatusAtividade.ATRASADA
    db.commit()
    
    return {
        "total": len(atividades),
        "atividades": [
            {
                "id": a.id,
                "tipo": a.tipo.value,
                "titulo": a.titulo,
                "data_programada": a.data_programada.isoformat(),
                "dias_atraso": (hoje - a.data_programada).days,
                "status": a.status.value
            }
            for a in atividades
        ]
    }


@router.get("/pei/{pei_id}")
async def listar_atividades_pei(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todas as atividades de um PEI.
    """
    
    atividades = db.query(AtividadePEI).filter(
        AtividadePEI.pei_id == pei_id
    ).order_by(AtividadePEI.data_programada, AtividadePEI.ordem_sequencial).all()
    
    # Agrupar por objetivo
    por_objetivo = {}
    for a in atividades:
        obj_id = a.objetivo_id or 0
        if obj_id not in por_objetivo:
            por_objetivo[obj_id] = {
                "objetivo_id": obj_id,
                "atividades": []
            }
        por_objetivo[obj_id]["atividades"].append({
            "id": a.id,
            "tipo": a.tipo.value,
            "titulo": a.titulo,
            "data_programada": a.data_programada.isoformat() if a.data_programada else None,
            "status": a.status.value
        })
    
    return {
        "pei_id": pei_id,
        "total_atividades": len(atividades),
        "total_concluidas": sum(1 for a in atividades if a.status == StatusAtividade.CONCLUIDA),
        "total_pendentes": sum(1 for a in atividades if a.status == StatusAtividade.PENDENTE),
        "por_objetivo": list(por_objetivo.values())
    }


# ============================================
# ENDPOINTS - Gerenciamento de Atividades
# ============================================

@router.get("/atividade/{atividade_id}")
async def obter_atividade(
    atividade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtém detalhes de uma atividade específica.
    """
    
    atividade = db.query(AtividadePEI).filter(AtividadePEI.id == atividade_id).first()
    
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    return {
        "id": atividade.id,
        "pei_id": atividade.pei_id,
        "objetivo_id": atividade.objetivo_id,
        "student_id": atividade.student_id,
        "tipo": atividade.tipo.value,
        "titulo": atividade.titulo,
        "descricao": atividade.descricao,
        "data_programada": atividade.data_programada.isoformat() if atividade.data_programada else None,
        "data_inicio": atividade.data_inicio.isoformat() if atividade.data_inicio else None,
        "data_conclusao": atividade.data_conclusao.isoformat() if atividade.data_conclusao else None,
        "status": atividade.status.value,
        "duracao_estimada_min": atividade.duracao_estimada_min,
        "ordem_sequencial": atividade.ordem_sequencial,
        "instrucoes": atividade.instrucoes,
        "adaptacoes": atividade.adaptacoes,
        "material_id": atividade.material_id,
        "material_aluno_id": atividade.material_aluno_id,
        "prova_id": atividade.prova_id,
        "prova_aluno_id": atividade.prova_aluno_id,
        "resultado": atividade.resultado,
        "observacoes_professor": atividade.observacoes_professor
    }


@router.put("/atividade/{atividade_id}/status")
async def atualizar_status_atividade(
    atividade_id: int,
    request: AtualizarStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Atualiza o status de uma atividade.
    """
    
    atividade = db.query(AtividadePEI).filter(AtividadePEI.id == atividade_id).first()
    
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    try:
        novo_status = StatusAtividade(request.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Status inválido: {request.status}")
    
    atividade.status = novo_status
    
    if novo_status == StatusAtividade.EM_ANDAMENTO and not atividade.data_inicio:
        atividade.data_inicio = datetime.utcnow()
    
    if novo_status == StatusAtividade.CONCLUIDA:
        atividade.data_conclusao = datetime.utcnow()
    
    if request.observacoes:
        atividade.observacoes_professor = request.observacoes
    
    db.commit()
    db.refresh(atividade)
    
    return {
        "success": True,
        "message": f"Status atualizado para {novo_status.value}",
        "atividade_id": atividade_id,
        "novo_status": novo_status.value
    }


@router.put("/atividade/{atividade_id}/reagendar")
async def reagendar_atividade(
    atividade_id: int,
    nova_data: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Reagenda uma atividade para outra data.
    """
    
    atividade = db.query(AtividadePEI).filter(AtividadePEI.id == atividade_id).first()
    
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    data_anterior = atividade.data_programada
    atividade.data_programada = nova_data
    
    # Se estava atrasada e nova data é futura, volta para pendente
    if atividade.status == StatusAtividade.ATRASADA and nova_data >= date.today():
        atividade.status = StatusAtividade.PENDENTE
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Atividade reagendada de {data_anterior} para {nova_data}",
        "atividade_id": atividade_id,
        "nova_data": nova_data.isoformat()
    }


@router.delete("/atividade/{atividade_id}")
async def excluir_atividade(
    atividade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Exclui uma atividade do calendário.
    """
    
    atividade = db.query(AtividadePEI).filter(AtividadePEI.id == atividade_id).first()
    
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
    db.delete(atividade)
    db.commit()
    
    return {"success": True, "message": "Atividade excluída com sucesso"}


# ============================================
# ENDPOINTS - Calendário Visual (Mensal)
# ============================================

@router.get("/aluno/{student_id}/mensal/{ano}/{mes}")
async def calendario_mensal_aluno(
    student_id: int,
    ano: int,
    mes: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna o calendário mensal de um aluno para visualização.
    """
    
    # Calcular primeiro e último dia do mês
    primeiro_dia = date(ano, mes, 1)
    if mes == 12:
        ultimo_dia = date(ano + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = date(ano, mes + 1, 1) - timedelta(days=1)
    
    atividades = db.query(AtividadePEI).filter(
        AtividadePEI.student_id == student_id,
        AtividadePEI.data_programada >= primeiro_dia,
        AtividadePEI.data_programada <= ultimo_dia
    ).order_by(AtividadePEI.data_programada).all()
    
    # Organizar por dia
    calendario = {}
    for dia in range(1, ultimo_dia.day + 1):
        data_dia = date(ano, mes, dia)
        calendario[dia] = {
            "data": data_dia.isoformat(),
            "dia_semana": data_dia.strftime("%A"),
            "atividades": []
        }
    
    for a in atividades:
        dia = a.data_programada.day
        calendario[dia]["atividades"].append({
            "id": a.id,
            "tipo": a.tipo.value,
            "titulo": a.titulo[:30] + "..." if len(a.titulo) > 30 else a.titulo,
            "status": a.status.value,
            "cor": _cor_tipo(a.tipo)
        })
    
    # Estatísticas do mês
    total = len(atividades)
    concluidas = sum(1 for a in atividades if a.status == StatusAtividade.CONCLUIDA)
    pendentes = sum(1 for a in atividades if a.status == StatusAtividade.PENDENTE)
    atrasadas = sum(1 for a in atividades if a.status == StatusAtividade.ATRASADA)
    
    return {
        "ano": ano,
        "mes": mes,
        "nome_mes": primeiro_dia.strftime("%B"),
        "total_dias": ultimo_dia.day,
        "estatisticas": {
            "total": total,
            "concluidas": concluidas,
            "pendentes": pendentes,
            "atrasadas": atrasadas,
            "percentual_conclusao": round((concluidas / total * 100) if total > 0 else 0, 1)
        },
        "calendario": calendario
    }


def _cor_tipo(tipo: TipoAtividade) -> str:
    """Retorna a cor associada ao tipo de atividade"""
    cores = {
        TipoAtividade.MATERIAL: "#3B82F6",    # Azul
        TipoAtividade.EXERCICIO: "#10B981",   # Verde
        TipoAtividade.PROVA: "#EF4444",       # Vermelho
        TipoAtividade.REVISAO: "#F59E0B",     # Amarelo
        TipoAtividade.ATIVIDADE_PRATICA: "#8B5CF6"  # Roxo
    }
    return cores.get(tipo, "#6B7280")
