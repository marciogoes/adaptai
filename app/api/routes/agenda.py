# ============================================
# ROTAS DE AGENDA DO PROFESSOR - AdaptAI
# ============================================
"""
Endpoints para gerenciamento da agenda do professor.
Permite criar, editar, listar e gerenciar eventos.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, Field
from enum import Enum

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.agenda import AgendaProfessor, TipoEvento, StatusEvento, Recorrencia


router = APIRouter(prefix="/agenda", tags=["📅 Agenda do Professor"])


# ============================================
# SCHEMAS
# ============================================

class EventoCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=255)
    descricao: Optional[str] = None
    tipo: TipoEvento = TipoEvento.AULA
    student_id: Optional[int] = None
    data: date
    hora_inicio: time
    hora_fim: Optional[time] = None
    duracao_minutos: int = 50
    local: Optional[str] = None
    link_online: Optional[str] = None
    cor: str = "#8B5CF6"
    recorrencia: Recorrencia = Recorrencia.UNICO
    recorrencia_fim: Optional[date] = None
    notificar_aluno: bool = True
    notificar_responsavel: bool = True
    lembrete_minutos: int = 30
    notas_privadas: Optional[str] = None
    notas_compartilhadas: Optional[str] = None


class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[TipoEvento] = None
    student_id: Optional[int] = None
    data: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    duracao_minutos: Optional[int] = None
    local: Optional[str] = None
    link_online: Optional[str] = None
    status: Optional[StatusEvento] = None
    cor: Optional[str] = None
    notas_privadas: Optional[str] = None
    notas_compartilhadas: Optional[str] = None


class EventoResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    tipo: str
    student_id: Optional[int]
    student_name: Optional[str]
    data: date
    hora_inicio: time
    hora_fim: Optional[time]
    duracao_minutos: int
    local: Optional[str]
    link_online: Optional[str]
    status: str
    cor: str
    recorrencia: str
    notas_privadas: Optional[str]
    notas_compartilhadas: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# ENDPOINTS
# ============================================

@router.get("/")
async def listar_eventos(
    data_inicio: Optional[date] = Query(None, description="Data inicial"),
    data_fim: Optional[date] = Query(None, description="Data final"),
    tipo: Optional[TipoEvento] = Query(None, description="Filtrar por tipo"),
    student_id: Optional[int] = Query(None, description="Filtrar por aluno"),
    status: Optional[StatusEvento] = Query(None, description="Filtrar por status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📅 Lista eventos da agenda do professor
    
    Filtros disponíveis:
    - data_inicio/data_fim: Período de busca
    - tipo: Tipo de evento (aula, atendimento, reunião, etc)
    - student_id: Eventos de um aluno específico
    - status: Status do evento
    """
    
    # Base query - apenas eventos do professor logado
    query = db.query(AgendaProfessor).filter(
        AgendaProfessor.professor_id == current_user.id
    )
    
    # Filtros
    if data_inicio:
        query = query.filter(AgendaProfessor.data >= data_inicio)
    if data_fim:
        query = query.filter(AgendaProfessor.data <= data_fim)
    if tipo:
        query = query.filter(AgendaProfessor.tipo == tipo)
    if student_id:
        query = query.filter(AgendaProfessor.student_id == student_id)
    if status:
        query = query.filter(AgendaProfessor.status == status)
    
    # Se não especificou período, pega próximos 30 dias
    if not data_inicio and not data_fim:
        hoje = date.today()
        query = query.filter(
            AgendaProfessor.data >= hoje,
            AgendaProfessor.data <= hoje + timedelta(days=30)
        )
    
    eventos = query.order_by(AgendaProfessor.data, AgendaProfessor.hora_inicio).all()
    
    # Montar resposta com nome do aluno
    resultado = []
    for evento in eventos:
        resultado.append({
            "id": evento.id,
            "titulo": evento.titulo,
            "descricao": evento.descricao,
            "tipo": evento.tipo.value,
            "student_id": evento.student_id,
            "student_name": evento.student.name if evento.student else None,
            "data": evento.data.isoformat(),
            "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
            "hora_fim": evento.hora_fim.isoformat() if evento.hora_fim else None,
            "duracao_minutos": evento.duracao_minutos,
            "local": evento.local,
            "link_online": evento.link_online,
            "status": evento.status.value,
            "cor": evento.cor,
            "recorrencia": evento.recorrencia.value,
            "notas_privadas": evento.notas_privadas,
            "notas_compartilhadas": evento.notas_compartilhadas,
            "created_at": evento.created_at.isoformat() if evento.created_at else None
        })
    
    return {
        "total": len(resultado),
        "eventos": resultado
    }


@router.get("/hoje")
async def eventos_hoje(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📌 Lista eventos de hoje
    """
    hoje = date.today()
    
    eventos = db.query(AgendaProfessor).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data == hoje,
        AgendaProfessor.status.in_([StatusEvento.AGENDADO, StatusEvento.CONFIRMADO, StatusEvento.EM_ANDAMENTO])
    ).order_by(AgendaProfessor.hora_inicio).all()
    
    resultado = []
    for evento in eventos:
        resultado.append({
            "id": evento.id,
            "titulo": evento.titulo,
            "tipo": evento.tipo.value,
            "student_name": evento.student.name if evento.student else None,
            "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
            "hora_fim": evento.hora_fim.isoformat() if evento.hora_fim else None,
            "local": evento.local,
            "status": evento.status.value,
            "cor": evento.cor
        })
    
    return {
        "data": hoje.isoformat(),
        "total": len(resultado),
        "eventos": resultado
    }


@router.get("/semana")
async def eventos_semana(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📆 Lista eventos da semana atual
    """
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())  # Segunda
    fim_semana = inicio_semana + timedelta(days=6)  # Domingo
    
    eventos = db.query(AgendaProfessor).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= inicio_semana,
        AgendaProfessor.data <= fim_semana
    ).order_by(AgendaProfessor.data, AgendaProfessor.hora_inicio).all()
    
    # Agrupar por dia
    por_dia = {}
    for evento in eventos:
        dia_str = evento.data.isoformat()
        if dia_str not in por_dia:
            por_dia[dia_str] = []
        por_dia[dia_str].append({
            "id": evento.id,
            "titulo": evento.titulo,
            "tipo": evento.tipo.value,
            "student_name": evento.student.name if evento.student else None,
            "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
            "hora_fim": evento.hora_fim.isoformat() if evento.hora_fim else None,
            "status": evento.status.value,
            "cor": evento.cor
        })
    
    return {
        "inicio_semana": inicio_semana.isoformat(),
        "fim_semana": fim_semana.isoformat(),
        "total_eventos": len(eventos),
        "eventos_por_dia": por_dia
    }


@router.get("/mes/{ano}/{mes}")
async def eventos_mes(
    ano: int,
    mes: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗓️ Lista eventos de um mês específico
    """
    from calendar import monthrange
    
    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, monthrange(ano, mes)[1])
    
    eventos = db.query(AgendaProfessor).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= primeiro_dia,
        AgendaProfessor.data <= ultimo_dia
    ).order_by(AgendaProfessor.data, AgendaProfessor.hora_inicio).all()
    
    # Agrupar por dia
    por_dia = {}
    for evento in eventos:
        dia = evento.data.day
        if dia not in por_dia:
            por_dia[dia] = []
        por_dia[dia].append({
            "id": evento.id,
            "titulo": evento.titulo,
            "tipo": evento.tipo.value,
            "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
            "cor": evento.cor
        })
    
    return {
        "ano": ano,
        "mes": mes,
        "total_eventos": len(eventos),
        "dias_com_eventos": list(por_dia.keys()),
        "eventos_por_dia": por_dia
    }


@router.get("/{evento_id}")
async def obter_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔍 Obtém detalhes de um evento específico
    """
    evento = db.query(AgendaProfessor).filter(
        AgendaProfessor.id == evento_id,
        AgendaProfessor.professor_id == current_user.id
    ).first()
    
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    return {
        "id": evento.id,
        "titulo": evento.titulo,
        "descricao": evento.descricao,
        "tipo": evento.tipo.value,
        "student_id": evento.student_id,
        "student_name": evento.student.name if evento.student else None,
        "data": evento.data.isoformat(),
        "hora_inicio": evento.hora_inicio.isoformat() if evento.hora_inicio else None,
        "hora_fim": evento.hora_fim.isoformat() if evento.hora_fim else None,
        "duracao_minutos": evento.duracao_minutos,
        "local": evento.local,
        "link_online": evento.link_online,
        "status": evento.status.value,
        "cor": evento.cor,
        "recorrencia": evento.recorrencia.value,
        "recorrencia_fim": evento.recorrencia_fim.isoformat() if evento.recorrencia_fim else None,
        "notificar_aluno": evento.notificar_aluno,
        "notificar_responsavel": evento.notificar_responsavel,
        "lembrete_minutos": evento.lembrete_minutos,
        "notas_privadas": evento.notas_privadas,
        "notas_compartilhadas": evento.notas_compartilhadas,
        "created_at": evento.created_at.isoformat() if evento.created_at else None
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def criar_evento(
    evento_data: EventoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ➕ Cria um novo evento na agenda
    """
    
    # Verificar se aluno existe e pertence ao professor
    if evento_data.student_id:
        student = db.query(Student).filter(
            Student.id == evento_data.student_id,
            Student.created_by_user_id == current_user.id
        ).first()
        
        if not student:
            raise HTTPException(
                status_code=404, 
                detail="Aluno não encontrado ou não pertence a você"
            )
    
    # Criar evento
    novo_evento = AgendaProfessor(
        professor_id=current_user.id,
        titulo=evento_data.titulo,
        descricao=evento_data.descricao,
        tipo=evento_data.tipo,
        student_id=evento_data.student_id,
        data=evento_data.data,
        hora_inicio=evento_data.hora_inicio,
        hora_fim=evento_data.hora_fim,
        duracao_minutos=evento_data.duracao_minutos,
        local=evento_data.local,
        link_online=evento_data.link_online,
        cor=evento_data.cor,
        recorrencia=evento_data.recorrencia,
        recorrencia_fim=evento_data.recorrencia_fim,
        notificar_aluno=evento_data.notificar_aluno,
        notificar_responsavel=evento_data.notificar_responsavel,
        lembrete_minutos=evento_data.lembrete_minutos,
        notas_privadas=evento_data.notas_privadas,
        notas_compartilhadas=evento_data.notas_compartilhadas,
        status=StatusEvento.AGENDADO
    )
    
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)
    
    # Se for recorrente, criar eventos futuros
    if evento_data.recorrencia != Recorrencia.UNICO and evento_data.recorrencia_fim:
        criar_eventos_recorrentes(db, novo_evento, evento_data)
    
    return {
        "success": True,
        "message": "Evento criado com sucesso",
        "evento_id": novo_evento.id
    }


@router.put("/{evento_id}")
async def atualizar_evento(
    evento_id: int,
    evento_data: EventoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ✏️ Atualiza um evento existente
    """
    evento = db.query(AgendaProfessor).filter(
        AgendaProfessor.id == evento_id,
        AgendaProfessor.professor_id == current_user.id
    ).first()
    
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    # Verificar aluno se alterado
    if evento_data.student_id:
        student = db.query(Student).filter(
            Student.id == evento_data.student_id,
            Student.created_by_user_id == current_user.id
        ).first()
        
        if not student:
            raise HTTPException(
                status_code=404, 
                detail="Aluno não encontrado ou não pertence a você"
            )
    
    # Atualizar campos
    update_data = evento_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(evento, field, value)
    
    db.commit()
    db.refresh(evento)
    
    return {
        "success": True,
        "message": "Evento atualizado com sucesso"
    }


@router.delete("/{evento_id}")
async def deletar_evento(
    evento_id: int,
    deletar_recorrentes: bool = Query(False, description="Deletar eventos recorrentes também"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗑️ Deleta um evento
    """
    evento = db.query(AgendaProfessor).filter(
        AgendaProfessor.id == evento_id,
        AgendaProfessor.professor_id == current_user.id
    ).first()
    
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    # Se for evento pai e quiser deletar recorrentes
    if deletar_recorrentes and evento.recorrencia != Recorrencia.UNICO:
        db.query(AgendaProfessor).filter(
            AgendaProfessor.evento_pai_id == evento_id
        ).delete()
    
    db.delete(evento)
    db.commit()
    
    return {
        "success": True,
        "message": "Evento deletado com sucesso"
    }


@router.put("/{evento_id}/status")
async def atualizar_status_evento(
    evento_id: int,
    novo_status: StatusEvento,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔄 Atualiza apenas o status de um evento
    """
    evento = db.query(AgendaProfessor).filter(
        AgendaProfessor.id == evento_id,
        AgendaProfessor.professor_id == current_user.id
    ).first()
    
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    evento.status = novo_status
    db.commit()
    
    return {
        "success": True,
        "message": f"Status atualizado para {novo_status.value}"
    }


@router.get("/stats/resumo")
async def estatisticas_agenda(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📊 Estatísticas da agenda do professor
    """
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    
    # Contadores
    total_mes = db.query(func.count(AgendaProfessor.id)).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= inicio_mes
    ).scalar()
    
    eventos_hoje = db.query(func.count(AgendaProfessor.id)).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data == hoje
    ).scalar()
    
    proximos_7_dias = db.query(func.count(AgendaProfessor.id)).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= hoje,
        AgendaProfessor.data <= hoje + timedelta(days=7)
    ).scalar()
    
    # Por tipo
    por_tipo = db.query(
        AgendaProfessor.tipo,
        func.count(AgendaProfessor.id)
    ).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= inicio_mes
    ).group_by(AgendaProfessor.tipo).all()
    
    # Por aluno
    por_aluno = db.query(
        Student.name,
        func.count(AgendaProfessor.id)
    ).join(Student, AgendaProfessor.student_id == Student.id).filter(
        AgendaProfessor.professor_id == current_user.id,
        AgendaProfessor.data >= inicio_mes
    ).group_by(Student.name).order_by(func.count(AgendaProfessor.id).desc()).limit(5).all()
    
    return {
        "eventos_hoje": eventos_hoje,
        "eventos_proximos_7_dias": proximos_7_dias,
        "eventos_mes": total_mes,
        "por_tipo": {tipo.value: count for tipo, count in por_tipo},
        "top_alunos": {nome: count for nome, count in por_aluno}
    }


# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def criar_eventos_recorrentes(db: Session, evento_pai: AgendaProfessor, evento_data: EventoCreate):
    """Cria eventos recorrentes baseados no evento pai"""
    
    delta_dias = {
        Recorrencia.DIARIO: 1,
        Recorrencia.SEMANAL: 7,
        Recorrencia.QUINZENAL: 14,
        Recorrencia.MENSAL: 30  # Aproximado
    }
    
    dias = delta_dias.get(evento_data.recorrencia, 7)
    data_atual = evento_pai.data + timedelta(days=dias)
    
    while data_atual <= evento_data.recorrencia_fim:
        evento_filho = AgendaProfessor(
            professor_id=evento_pai.professor_id,
            titulo=evento_pai.titulo,
            descricao=evento_pai.descricao,
            tipo=evento_pai.tipo,
            student_id=evento_pai.student_id,
            data=data_atual,
            hora_inicio=evento_pai.hora_inicio,
            hora_fim=evento_pai.hora_fim,
            duracao_minutos=evento_pai.duracao_minutos,
            local=evento_pai.local,
            link_online=evento_pai.link_online,
            cor=evento_pai.cor,
            recorrencia=Recorrencia.UNICO,  # Filhos não são recorrentes
            evento_pai_id=evento_pai.id,
            notificar_aluno=evento_pai.notificar_aluno,
            notificar_responsavel=evento_pai.notificar_responsavel,
            lembrete_minutos=evento_pai.lembrete_minutos,
            status=StatusEvento.AGENDADO
        )
        
        db.add(evento_filho)
        data_atual += timedelta(days=dias)
    
    db.commit()
