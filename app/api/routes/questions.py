from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.question import QuestionSet, Question
from app.schemas.question import (
    QuestionGenerationConfig, QuestionSetResponse,
    QuestionSetListResponse, QuestionSetWithStats
)
from app.services.question_generator import QuestionGeneratorService
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.post("/generate", response_model=QuestionSetResponse, status_code=status.HTTP_201_CREATED)
async def generate_questions(
    config: QuestionGenerationConfig,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    🎯 Gerar questões usando IA (Claude)
    
    Esta é a funcionalidade principal do AdaptAI!
    Gera questões de múltipla escolha adaptadas baseadas no conteúdo fornecido.
    
    Parâmetros:
    - **title**: Título da atividade
    - **subject**: Disciplina (Matemática, Português, etc)
    - **grade_level**: Ano escolar
    - **raw_content**: Conteúdo base (mínimo 50 caracteres)
    - **level_1_qty** a **level_4_qty**: Quantidade por nível
    - **adaptations**: Lista de adaptações (opcional)
    - **tags**: Tags para categorização (opcional)
    """
    try:
        generator = QuestionGeneratorService(db)
        
        question_set = await generator.generate_question_set(
            user_id=current_user.id,
            title=config.title,
            subject=config.subject,
            grade_level=config.grade_level,
            raw_content=config.raw_content,
            level_1_qty=config.level_1_qty,
            level_2_qty=config.level_2_qty,
            level_3_qty=config.level_3_qty,
            level_4_qty=config.level_4_qty,
            adaptations=config.adaptations,
            tags=config.tags
        )
        
        return question_set
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating questions: {str(e)}"
        )

@router.get("/", response_model=List[QuestionSetListResponse])
def list_question_sets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    subject: str = Query(None, description="Filtrar por disciplina"),
    grade_level: str = Query(None, description="Filtrar por ano escolar"),
    search: str = Query(None, description="Buscar no título"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos os conjuntos de questões do usuário
    """
    query = db.query(QuestionSet).filter(QuestionSet.user_id == current_user.id)
    
    # Filtros
    if subject:
        query = query.filter(QuestionSet.subject == subject)
    
    if grade_level:
        query = query.filter(QuestionSet.grade_level == grade_level)
    
    if search:
        query = query.filter(QuestionSet.title.ilike(f"%{search}%"))
    
    question_sets = query.order_by(QuestionSet.created_at.desc()).offset(skip).limit(limit).all()
    
    # Adicionar total_questions
    result = []
    for qs in question_sets:
        qs_dict = {
            "id": qs.id,
            "title": qs.title,
            "description": qs.description,
            "subject": qs.subject,
            "grade_level": qs.grade_level,
            "config": qs.config,
            "tags": qs.tags,
            "created_at": qs.created_at,
            "total_questions": len(qs.questions)
        }
        result.append(qs_dict)
    
    return result

@router.get("/{question_set_id}", response_model=QuestionSetResponse)
def get_question_set(
    question_set_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter um conjunto de questões específico com todas as questões
    """
    question_set = db.query(QuestionSet).filter(
        QuestionSet.id == question_set_id,
        QuestionSet.user_id == current_user.id
    ).first()
    
    if not question_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question set not found"
        )
    
    return question_set

@router.get("/{question_set_id}/stats", response_model=QuestionSetWithStats)
def get_question_set_stats(
    question_set_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas de um conjunto de questões
    """
    question_set = db.query(QuestionSet).filter(
        QuestionSet.id == question_set_id,
        QuestionSet.user_id == current_user.id
    ).first()
    
    if not question_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question set not found"
        )
    
    # Calcular estatísticas
    questions_by_level = {}
    for question in question_set.questions:
        level = question.difficulty_level.value
        questions_by_level[level] = questions_by_level.get(level, 0) + 1
    
    result = {
        **question_set.__dict__,
        "total_questions": len(question_set.questions),
        "questions_by_level": questions_by_level
    }
    
    return result

@router.delete("/{question_set_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question_set(
    question_set_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deletar um conjunto de questões
    """
    question_set = db.query(QuestionSet).filter(
        QuestionSet.id == question_set_id,
        QuestionSet.user_id == current_user.id
    ).first()
    
    if not question_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question set not found"
        )
    
    db.delete(question_set)
    db.commit()
    
    return None

@router.get("/{question_set_id}/export/json")
def export_questions_json(
    question_set_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Exportar questões em formato JSON
    """
    question_set = db.query(QuestionSet).filter(
        QuestionSet.id == question_set_id,
        QuestionSet.user_id == current_user.id
    ).first()
    
    if not question_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question set not found"
        )
    
    # Formatar para exportação
    export_data = {
        "title": question_set.title,
        "subject": question_set.subject,
        "grade_level": question_set.grade_level,
        "created_at": question_set.created_at.isoformat(),
        "total_questions": len(question_set.questions),
        "questions": []
    }
    
    for q in question_set.questions:
        export_data["questions"].append({
            "number": q.order_number,
            "difficulty_level": q.difficulty_level.value,
            "question": q.question_text,
            "options": {
                "a": q.option_a,
                "b": q.option_b,
                "c": q.option_c,
                "d": q.option_d
            },
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "skill": q.skill
        })
    
    return export_data
