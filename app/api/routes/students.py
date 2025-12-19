from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Criar um novo estudante (com ou sem login)
    """
    from app.core.security import get_password_hash
    
    # Verificar se email já existe
    if student_data.email:
        existing = db.query(Student).filter(Student.email == student_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
    
    # Hash da senha se fornecida
    hashed_password = None
    if student_data.password:
        hashed_password = get_password_hash(student_data.password)
    
    new_student = Student(
        name=student_data.name,
        email=student_data.email,
        hashed_password=hashed_password,
        is_active=True,
        birth_date=student_data.birth_date,
        grade_level=student_data.grade_level or "Não especificado",
        diagnosis=student_data.diagnosis,
        profile_data=student_data.profile_data,
        notes=student_data.notes,
        created_by_user_id=current_user.id
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student

@router.get("/", response_model=List[StudentListResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    grade_level: str = Query(None, description="Filtrar por ano escolar"),
    search: str = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos os estudantes do usuário
    """
    query = db.query(Student).filter(Student.created_by_user_id == current_user.id)
    
    # Filtros
    if grade_level:
        query = query.filter(Student.grade_level == grade_level)
    
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    
    students = query.offset(skip).limit(limit).all()
    return students

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter detalhes de um estudante específico
    """
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Atualizar dados de um estudante (incluindo email e senha)
    """
    from app.core.security import get_password_hash
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Verificar se o novo email já existe (se estiver alterando)
    if student_data.email and student_data.email != student.email:
        existing = db.query(Student).filter(
            Student.email == student_data.email,
            Student.id != student_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado por outro estudante"
            )
    
    # Atualizar campos (exceto password que precisa de hash)
    update_data = student_data.model_dump(exclude_unset=True)
    
    # Tratar senha separadamente
    if 'password' in update_data:
        password = update_data.pop('password')
        if password:  # Só atualiza se não for vazio
            student.hashed_password = get_password_hash(password)
    
    # Atualizar outros campos
    for field, value in update_data.items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)
    
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deletar um estudante
    """
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    db.delete(student)
    db.commit()
    
    return None

@router.get("/{student_id}/applications")
def get_student_applications(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter todas as aplicações de um estudante
    """
    from app.models.application import Application
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    applications = db.query(Application).filter(
        Application.student_id == student_id
    ).all()
    
    return applications

@router.get("/{student_id}/performance")
def get_student_performance_history(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter histórico de performance de um estudante
    """
    from app.models.performance import PerformanceAnalysis
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    analyses = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.student_id == student_id
    ).order_by(PerformanceAnalysis.analyzed_at.desc()).all()
    
    return analyses
