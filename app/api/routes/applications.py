from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.application import Application, StudentAnswer, ApplicationStatus
from app.models.question import Question
from app.schemas.application import (
    ApplicationCreate, ApplicationResponse, StudentAnswerCreate,
    StudentAnswerResponse, AnswerSubmitBatch, ApplicationWithAnswers
)
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Aplicar uma atividade a um estudante
    """
    from app.models.student import Student
    from app.models.question import QuestionSet
    
    # Verificar se o estudante existe e pertence ao usuário
    student = db.query(Student).filter(
        Student.id == application_data.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Verificar se o question_set existe e pertence ao usuário
    question_set = db.query(QuestionSet).filter(
        QuestionSet.id == application_data.question_set_id,
        QuestionSet.user_id == current_user.id
    ).first()
    
    if not question_set:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question set not found"
        )
    
    # Criar aplicação
    new_application = Application(
        question_set_id=application_data.question_set_id,
        student_id=application_data.student_id,
        applied_by_user_id=current_user.id,
        applied_date=application_data.applied_date,
        time_limit_minutes=application_data.time_limit_minutes,
        status=ApplicationStatus.PENDING
    )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    
    return new_application

@router.get("/", response_model=List[ApplicationResponse])
def list_applications(
    student_id: int = None,
    status: ApplicationStatus = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Listar aplicações
    """
    query = db.query(Application).filter(
        Application.applied_by_user_id == current_user.id
    )
    
    if student_id:
        query = query.filter(Application.student_id == student_id)
    
    if status:
        query = query.filter(Application.status == status)
    
    applications = query.order_by(Application.created_at.desc()).all()
    return applications

@router.get("/{application_id}", response_model=ApplicationWithAnswers)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter detalhes de uma aplicação com respostas
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.applied_by_user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Contar questões
    total_questions = len(application.question_set.questions)
    answered_questions = len(application.answers)
    
    result = {
        **application.__dict__,
        "total_questions": total_questions,
        "answered_questions": answered_questions
    }
    
    return result

@router.post("/{application_id}/start")
def start_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Iniciar uma aplicação (aluno começou a responder)
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.applied_by_user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if application.status != ApplicationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already started"
        )
    
    application.status = ApplicationStatus.IN_PROGRESS
    application.started_at = datetime.now()
    
    db.commit()
    db.refresh(application)
    
    return application

@router.post("/{application_id}/answers", response_model=StudentAnswerResponse)
def submit_answer(
    application_id: int,
    answer_data: StudentAnswerCreate,
    db: Session = Depends(get_db)
):
    """
    Submeter uma resposta do aluno
    """
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Verificar se a questão pertence a este question_set
    question = db.query(Question).filter(
        Question.id == answer_data.question_id,
        Question.question_set_id == application.question_set_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found in this application"
        )
    
    # Verificar se já existe resposta para esta questão
    existing_answer = db.query(StudentAnswer).filter(
        StudentAnswer.application_id == application_id,
        StudentAnswer.question_id == answer_data.question_id
    ).first()
    
    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer already submitted for this question"
        )
    
    # Verificar se a resposta está correta
    is_correct = (answer_data.selected_answer == question.correct_answer) if answer_data.selected_answer else None
    
    # Criar resposta
    new_answer = StudentAnswer(
        application_id=application_id,
        question_id=answer_data.question_id,
        student_id=application.student_id,
        selected_answer=answer_data.selected_answer,
        is_correct=is_correct,
        time_spent_seconds=answer_data.time_spent_seconds
    )
    
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    
    return new_answer

@router.post("/{application_id}/answers/batch", response_model=List[StudentAnswerResponse])
def submit_answers_batch(
    application_id: int,
    batch_data: AnswerSubmitBatch,
    db: Session = Depends(get_db)
):
    """
    Submeter múltiplas respostas de uma vez
    """
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    new_answers = []
    
    for answer_data in batch_data.answers:
        # Verificar se a questão pertence a este question_set
        question = db.query(Question).filter(
            Question.id == answer_data.question_id,
            Question.question_set_id == application.question_set_id
        ).first()
        
        if not question:
            continue  # Pula questões inválidas
        
        # Verificar se já existe resposta
        existing_answer = db.query(StudentAnswer).filter(
            StudentAnswer.application_id == application_id,
            StudentAnswer.question_id == answer_data.question_id
        ).first()
        
        if existing_answer:
            continue  # Pula respostas já existentes
        
        # Verificar correção
        is_correct = (answer_data.selected_answer == question.correct_answer) if answer_data.selected_answer else None
        
        # Criar resposta
        new_answer = StudentAnswer(
            application_id=application_id,
            question_id=answer_data.question_id,
            student_id=application.student_id,
            selected_answer=answer_data.selected_answer,
            is_correct=is_correct,
            time_spent_seconds=answer_data.time_spent_seconds
        )
        
        db.add(new_answer)
        new_answers.append(new_answer)
    
    db.commit()
    
    for answer in new_answers:
        db.refresh(answer)
    
    return new_answers

@router.post("/{application_id}/complete")
def complete_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Finalizar aplicação e gerar análise de desempenho automática
    """
    from app.services.performance_analyzer import PerformanceAnalyzerService
    
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.applied_by_user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if application.status == ApplicationStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already completed"
        )
    
    # Atualizar status
    application.status = ApplicationStatus.COMPLETED
    application.completed_at = datetime.now()
    db.commit()
    
    # Gerar análise de desempenho
    try:
        analyzer = PerformanceAnalyzerService(db)
        performance_analysis = analyzer.analyze_application(application_id)
        
        return {
            "message": "Application completed successfully",
            "application": application,
            "performance_analysis": performance_analysis
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing performance: {str(e)}"
        )

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deletar uma aplicação
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.applied_by_user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    db.delete(application)
    db.commit()
    
    return None
