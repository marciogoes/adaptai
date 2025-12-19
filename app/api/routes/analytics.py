from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.performance import PerformanceAnalysis
from app.models.student import Student
from app.schemas.performance import PerformanceAnalysisResponse, PerformanceSummary
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/student/{student_id}/performance", response_model=List[PerformanceAnalysisResponse])
def get_student_performance(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter histórico completo de análises de desempenho de um estudante
    """
    # Verificar se o estudante pertence ao usuário
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Buscar análises
    analyses = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.student_id == student_id
    ).order_by(PerformanceAnalysis.analyzed_at.desc()).all()
    
    return analyses

@router.get("/application/{application_id}/performance", response_model=PerformanceAnalysisResponse)
def get_application_performance(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter análise de desempenho de uma aplicação específica
    """
    from app.models.application import Application
    
    # Verificar se a aplicação pertence ao usuário
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.applied_by_user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Buscar análise
    analysis = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.application_id == application_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Performance analysis not found. Complete the application first."
        )
    
    return analysis

@router.get("/student/{student_id}/summary", response_model=PerformanceSummary)
def get_student_summary(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter resumo rápido do desempenho do estudante
    """
    # Verificar se o estudante pertence ao usuário
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Buscar última análise
    latest_analysis = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.student_id == student_id
    ).order_by(PerformanceAnalysis.analyzed_at.desc()).first()
    
    if not latest_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No performance data available for this student"
        )
    
    # Calcular total de questões e acertos
    from app.models.application import Application, StudentAnswer
    
    application = db.query(Application).filter(
        Application.id == latest_analysis.application_id
    ).first()
    
    total_questions = len(application.question_set.questions)
    correct_answers = db.query(StudentAnswer).filter(
        StudentAnswer.application_id == application.id,
        StudentAnswer.is_correct == True
    ).count()
    
    # Determinar status
    score = latest_analysis.overall_score
    if score >= 90:
        status_text = "excellent"
    elif score >= 75:
        status_text = "good"
    else:
        status_text = "needs_improvement"
    
    return {
        "student_id": student.id,
        "student_name": student.name,
        "overall_score": latest_analysis.overall_score,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "status": status_text
    }

@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas gerais para o dashboard do professor
    """
    from app.models.application import Application
    from app.models.question import QuestionSet
    from sqlalchemy import func
    
    # Total de estudantes
    total_students = db.query(func.count(Student.id)).filter(
        Student.created_by_user_id == current_user.id
    ).scalar()
    
    # Total de conjuntos de questões
    total_question_sets = db.query(func.count(QuestionSet.id)).filter(
        QuestionSet.user_id == current_user.id
    ).scalar()
    
    # Total de aplicações
    total_applications = db.query(func.count(Application.id)).filter(
        Application.applied_by_user_id == current_user.id
    ).scalar()
    
    # Aplicações completadas
    completed_applications = db.query(func.count(Application.id)).filter(
        Application.applied_by_user_id == current_user.id,
        Application.status == "completed"
    ).scalar()
    
    # Média geral de desempenho
    avg_score = db.query(func.avg(PerformanceAnalysis.overall_score)).join(
        Application
    ).filter(
        Application.applied_by_user_id == current_user.id
    ).scalar()
    
    # Aplicações recentes (últimas 5)
    recent_applications = db.query(Application).filter(
        Application.applied_by_user_id == current_user.id
    ).order_by(Application.created_at.desc()).limit(5).all()
    
    return {
        "total_students": total_students,
        "total_question_sets": total_question_sets,
        "total_applications": total_applications,
        "completed_applications": completed_applications,
        "average_score": round(avg_score, 2) if avg_score else 0,
        "recent_applications": [
            {
                "id": app.id,
                "student_id": app.student_id,
                "question_set_id": app.question_set_id,
                "status": app.status,
                "created_at": app.created_at
            }
            for app in recent_applications
        ]
    }

@router.get("/compare")
def compare_students_performance(
    student_ids: str,  # Ex: "1,2,3"
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Comparar desempenho de múltiplos estudantes
    """
    # Parse IDs
    try:
        ids = [int(id.strip()) for id in student_ids.split(",")]
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student IDs format. Use comma-separated numbers."
        )
    
    comparisons = []
    
    for student_id in ids:
        # Verificar se o estudante pertence ao usuário
        student = db.query(Student).filter(
            Student.id == student_id,
            Student.created_by_user_id == current_user.id
        ).first()
        
        if not student:
            continue
        
        # Buscar última análise
        latest_analysis = db.query(PerformanceAnalysis).filter(
            PerformanceAnalysis.student_id == student_id
        ).order_by(PerformanceAnalysis.analyzed_at.desc()).first()
        
        if latest_analysis:
            comparisons.append({
                "student_id": student.id,
                "student_name": student.name,
                "overall_score": latest_analysis.overall_score,
                "by_difficulty_level": latest_analysis.by_difficulty_level,
                "by_skill": latest_analysis.by_skill,
                "strong_points": latest_analysis.strong_points,
                "weak_points": latest_analysis.weak_points
            })
    
    return {
        "total_students": len(comparisons),
        "comparisons": comparisons
    }
