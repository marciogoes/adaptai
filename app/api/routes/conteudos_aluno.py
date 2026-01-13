# ============================================
# ROTAS - Conteúdos do Aluno (Integração)
# ============================================
"""
Endpoints para buscar conteúdos estudados por aluno.
Usado como insumo para materiais adaptados e provas.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List, Optional
from datetime import date, timedelta

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.registro_diario import RegistroDiario, AulaRegistrada


router = APIRouter(prefix="/conteudos-aluno", tags=["📚 Conteúdos do Aluno"])


@router.get("/{student_id}/recentes")
async def conteudos_recentes_aluno(
    student_id: int,
    dias: int = Query(30, description="Últimos X dias"),
    disciplina: Optional[str] = Query(None, description="Filtrar por disciplina"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📚 Buscar conteúdos recentes estudados por um aluno
    
    Retorna lista de conteúdos dos últimos X dias, agrupados por disciplina.
    Útil para sugerir temas ao criar materiais ou provas.
    """
    # Verificar acesso ao aluno
    aluno = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    data_inicio = date.today() - timedelta(days=dias)
    
    # Buscar aulas do aluno
    query = db.query(AulaRegistrada).join(RegistroDiario).filter(
        RegistroDiario.student_id == student_id,
        RegistroDiario.data_aula >= data_inicio
    )
    
    if disciplina:
        query = query.filter(AulaRegistrada.disciplina.ilike(f"%{disciplina}%"))
    
    aulas = query.order_by(RegistroDiario.data_aula.desc()).all()
    
    # Agrupar por disciplina
    por_disciplina = {}
    for aula in aulas:
        disc = aula.disciplina
        if disc not in por_disciplina:
            por_disciplina[disc] = {
                "disciplina": disc,
                "total_aulas": 0,
                "conteudos": [],
                "ultima_aula": None
            }
        
        por_disciplina[disc]["total_aulas"] += 1
        por_disciplina[disc]["conteudos"].append({
            "id": aula.id,
            "data": aula.registro.data_aula.isoformat(),
            "conteudo": aula.conteudo,
            "professor": aula.professor_nome,
            "paginas": aula.paginas,
            "modulo": aula.modulo,
            "tem_dever": aula.tem_dever_casa,
            "tem_avaliacao": aula.tem_atividade_avaliativa
        })
        
        if not por_disciplina[disc]["ultima_aula"]:
            por_disciplina[disc]["ultima_aula"] = aula.registro.data_aula.isoformat()
    
    return {
        "aluno": {
            "id": aluno.id,
            "nome": aluno.name,
            "serie": aluno.grade_level
        },
        "periodo": f"Últimos {dias} dias",
        "total_disciplinas": len(por_disciplina),
        "total_aulas": len(aulas),
        "por_disciplina": list(por_disciplina.values())
    }


@router.get("/{student_id}/disciplinas")
async def disciplinas_aluno(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📋 Listar todas as disciplinas registradas para um aluno
    """
    # Verificar acesso
    aluno = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    disciplinas = db.query(distinct(AulaRegistrada.disciplina)).join(RegistroDiario).filter(
        RegistroDiario.student_id == student_id
    ).all()
    
    return {
        "aluno_id": student_id,
        "disciplinas": [d[0] for d in disciplinas if d[0]]
    }


@router.get("/{student_id}/sugestoes-prova")
async def sugestoes_para_prova(
    student_id: int,
    disciplina: str = Query(..., description="Disciplina da prova"),
    dias: int = Query(30, description="Considerar últimos X dias"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🎯 Sugestões de conteúdos para criar uma prova
    
    Retorna conteúdos recentes de uma disciplina formatados
    como sugestão para criação de prova.
    """
    # Verificar acesso
    aluno = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    data_inicio = date.today() - timedelta(days=dias)
    
    aulas = db.query(AulaRegistrada).join(RegistroDiario).filter(
        RegistroDiario.student_id == student_id,
        RegistroDiario.data_aula >= data_inicio,
        AulaRegistrada.disciplina.ilike(f"%{disciplina}%")
    ).order_by(RegistroDiario.data_aula.desc()).all()
    
    # Formatar como sugestão de conteúdo para prova
    conteudos_unicos = []
    conteudos_set = set()
    
    for aula in aulas:
        if aula.conteudo not in conteudos_set:
            conteudos_set.add(aula.conteudo)
            conteudos_unicos.append({
                "conteudo": aula.conteudo,
                "data": aula.registro.data_aula.isoformat(),
                "paginas": aula.paginas,
                "relevancia": "alta" if aula.tem_avaliacao else "normal"
            })
    
    # Gerar texto sugerido para o campo de conteúdo da prova
    texto_sugerido = f"Conteúdos de {disciplina} estudados recentemente:\n"
    for c in conteudos_unicos[:5]:  # Top 5
        texto_sugerido += f"- {c['conteudo']}"
        if c['paginas']:
            texto_sugerido += f" (pág. {c['paginas']})"
        texto_sugerido += "\n"
    
    return {
        "aluno": aluno.name,
        "disciplina": disciplina,
        "periodo": f"Últimos {dias} dias",
        "total_aulas": len(aulas),
        "conteudos": conteudos_unicos,
        "texto_sugerido": texto_sugerido.strip()
    }


@router.get("/{student_id}/sugestoes-material")
async def sugestoes_para_material(
    student_id: int,
    disciplina: str = Query(..., description="Disciplina do material"),
    dias: int = Query(14, description="Considerar últimos X dias"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📖 Sugestões de conteúdos para criar material adaptado
    
    Retorna conteúdos recentes formatados como sugestão
    para criação de material de estudo.
    """
    # Verificar acesso
    aluno = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    data_inicio = date.today() - timedelta(days=dias)
    
    aulas = db.query(AulaRegistrada).join(RegistroDiario).filter(
        RegistroDiario.student_id == student_id,
        RegistroDiario.data_aula >= data_inicio,
        AulaRegistrada.disciplina.ilike(f"%{disciplina}%")
    ).order_by(RegistroDiario.data_aula.desc()).all()
    
    # Identificar conteúdos com dever de casa (prioridade para estudo)
    com_dever = [a for a in aulas if a.tem_dever_casa]
    com_avaliacao = [a for a in aulas if a.tem_atividade_avaliativa]
    
    # Gerar texto sugerido
    texto_sugerido = ""
    if com_avaliacao:
        texto_sugerido = f"⚠️ Conteúdo com avaliação marcada: {com_avaliacao[0].conteudo}\n\n"
    elif com_dever:
        texto_sugerido = f"📝 Conteúdo com dever de casa: {com_dever[0].conteudo}\n\n"
    elif aulas:
        texto_sugerido = f"📚 Último conteúdo estudado: {aulas[0].conteudo}\n\n"
    
    return {
        "aluno": {
            "id": aluno.id,
            "nome": aluno.name,
            "serie": aluno.grade_level,
            "diagnostico": aluno.diagnosis
        },
        "disciplina": disciplina,
        "periodo": f"Últimos {dias} dias",
        "total_aulas": len(aulas),
        "com_dever_casa": len(com_dever),
        "com_avaliacao": len(com_avaliacao),
        "conteudos": [
            {
                "conteudo": a.conteudo,
                "data": a.registro.data_aula.isoformat(),
                "tem_dever": a.tem_dever_casa,
                "tem_avaliacao": a.tem_atividade_avaliativa,
                "prioridade": "alta" if a.tem_avaliacao else ("media" if a.tem_dever_casa else "normal")
            }
            for a in aulas
        ],
        "texto_sugerido": texto_sugerido.strip()
    }
