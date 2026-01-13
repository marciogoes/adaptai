"""
🎓 ROTAS DE ESTUDANTES - AdaptAI
Gerenciamento de alunos com filtro por professor/escola
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.database import get_db
from app.models.student import Student
from app.models.user import User, UserRole
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/students", tags=["Students"])


def get_students_query(db: Session, current_user: User):
    """
    Retorna query base de alunos baseado no papel do usuário:
    - SUPER_ADMIN: Todos os alunos
    - ADMIN/COORDINATOR: Alunos da escola
    - TEACHER: Apenas seus próprios alunos
    """
    base_query = db.query(Student)
    
    if current_user.role == UserRole.SUPER_ADMIN:
        # Super admin vê todos
        return base_query
    
    elif current_user.role in [UserRole.ADMIN, UserRole.COORDINATOR]:
        # Admin/Coord vê alunos da sua escola
        if current_user.escola_id:
            return base_query.filter(Student.escola_id == current_user.escola_id)
        else:
            # Se não tem escola, vê só os seus
            return base_query.filter(Student.created_by_user_id == current_user.id)
    
    else:
        # Professor vê apenas seus alunos
        return base_query.filter(Student.created_by_user_id == current_user.id)


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    ➕ Criar um novo estudante (com ou sem login)
    
    O aluno será automaticamente associado ao professor que o criou
    e à escola do professor (se houver).
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
        turma=student_data.turma if hasattr(student_data, 'turma') else None,
        matricula=student_data.matricula if hasattr(student_data, 'matricula') else None,
        diagnosis=student_data.diagnosis,
        profile_data=student_data.profile_data,
        notes=student_data.notes,
        created_by_user_id=current_user.id,
        escola_id=current_user.escola_id  # Herda a escola do professor
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return new_student


@router.get("/", response_model=List[StudentListResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    grade_level: str = Query(None, description="Filtrar por ano escolar"),
    turma: str = Query(None, description="Filtrar por turma"),
    search: str = Query(None, description="Buscar por nome"),
    todos: bool = Query(False, description="Admin: listar todos da escola"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    📋 Listar estudantes
    
    - **Professor**: Vê apenas seus próprios alunos
    - **Coordenador/Admin**: Vê alunos da escola (ou só seus se `todos=False`)
    - **Super Admin**: Vê todos os alunos do sistema
    
    Filtros disponíveis:
    - `grade_level`: Filtrar por série (ex: "5º ano")
    - `turma`: Filtrar por turma (ex: "A", "Manhã")
    - `search`: Buscar por nome
    - `todos`: Admin pode ver todos da escola
    """
    # Obter query base baseada no papel
    if todos and current_user.role in [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.SUPER_ADMIN]:
        query = get_students_query(db, current_user)
    else:
        # Professor sempre vê só seus alunos
        query = db.query(Student).filter(Student.created_by_user_id == current_user.id)
    
    # Filtros
    if grade_level:
        query = query.filter(Student.grade_level == grade_level)
    
    if turma:
        query = query.filter(Student.turma == turma)
    
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    
    # Ordenar por nome
    query = query.order_by(Student.name)
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/meus", response_model=List[StudentListResponse])
def list_my_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: str = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    👨‍🏫 Listar APENAS meus alunos (professor)
    
    Útil para admins que também são professores e querem ver
    apenas os alunos que eles mesmos cadastraram.
    """
    query = db.query(Student).filter(Student.created_by_user_id == current_user.id)
    
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    
    query = query.order_by(Student.name)
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/escola", response_model=List[StudentListResponse])
def list_school_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    grade_level: str = Query(None, description="Filtrar por ano escolar"),
    turma: str = Query(None, description="Filtrar por turma"),
    professor_id: int = Query(None, description="Filtrar por professor"),
    search: str = Query(None, description="Buscar por nome"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    🏫 Listar todos os alunos da escola (Admin/Coordenador)
    
    Apenas Admin, Coordenador e Super Admin podem acessar.
    """
    # Verificar permissão
    if current_user.role not in [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Admin ou Coordenador podem ver todos os alunos da escola"
        )
    
    query = get_students_query(db, current_user)
    
    # Filtros
    if grade_level:
        query = query.filter(Student.grade_level == grade_level)
    
    if turma:
        query = query.filter(Student.turma == turma)
    
    if professor_id:
        query = query.filter(Student.created_by_user_id == professor_id)
    
    if search:
        query = query.filter(Student.name.ilike(f"%{search}%"))
    
    query = query.order_by(Student.name)
    
    students = query.offset(skip).limit(limit).all()
    return students


@router.get("/stats")
def get_students_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    📊 Estatísticas dos alunos
    """
    from sqlalchemy import func
    
    # Meus alunos
    meus_alunos = db.query(func.count(Student.id)).filter(
        Student.created_by_user_id == current_user.id
    ).scalar()
    
    # Total da escola (se admin)
    total_escola = 0
    if current_user.role in [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.SUPER_ADMIN]:
        query = get_students_query(db, current_user)
        total_escola = query.count()
    
    # Por série (meus alunos)
    por_serie = db.query(
        Student.grade_level,
        func.count(Student.id)
    ).filter(
        Student.created_by_user_id == current_user.id
    ).group_by(Student.grade_level).all()
    
    # Por turma (meus alunos)
    por_turma = db.query(
        Student.turma,
        func.count(Student.id)
    ).filter(
        Student.created_by_user_id == current_user.id,
        Student.turma.isnot(None)
    ).group_by(Student.turma).all()
    
    return {
        "meus_alunos": meus_alunos,
        "total_escola": total_escola,
        "por_serie": {serie: count for serie, count in por_serie if serie},
        "por_turma": {turma: count for turma, count in por_turma if turma}
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    🔍 Obter detalhes de um estudante específico
    """
    # Verificar acesso baseado no papel
    query = get_students_query(db, current_user)
    student = query.filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado ou você não tem permissão para acessá-lo"
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
    ✏️ Atualizar dados de um estudante (incluindo email e senha)
    """
    from app.core.security import get_password_hash
    
    # Verificar acesso
    query = get_students_query(db, current_user)
    student = query.filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado ou você não tem permissão"
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
    🗑️ Deletar um estudante
    
    Apenas o professor que criou ou Admin pode deletar.
    """
    # Verificar se é o criador ou admin
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    # Verificar permissão
    pode_deletar = (
        student.created_by_user_id == current_user.id or
        current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
    )
    
    if not pode_deletar:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este aluno"
        )
    
    db.delete(student)
    db.commit()
    
    return None


@router.post("/{student_id}/transferir")
def transfer_student(
    student_id: int,
    novo_professor_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    🔄 Transferir aluno para outro professor (Admin/Coordenador)
    """
    # Verificar permissão
    if current_user.role not in [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Admin ou Coordenador podem transferir alunos"
        )
    
    # Buscar aluno
    query = get_students_query(db, current_user)
    student = query.filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    # Verificar novo professor
    novo_professor = db.query(User).filter(User.id == novo_professor_id).first()
    
    if not novo_professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor não encontrado"
        )
    
    # Verificar se professor é da mesma escola (se não for super admin)
    if current_user.role != UserRole.SUPER_ADMIN:
        if novo_professor.escola_id != current_user.escola_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O professor deve ser da mesma escola"
            )
    
    # Transferir
    professor_anterior = student.created_by_user_id
    student.created_by_user_id = novo_professor_id
    db.commit()
    
    return {
        "success": True,
        "message": f"Aluno {student.name} transferido com sucesso",
        "professor_anterior_id": professor_anterior,
        "novo_professor_id": novo_professor_id
    }


@router.get("/{student_id}/applications")
def get_student_applications(
    student_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    📋 Obter todas as aplicações de um estudante
    """
    from app.models.application import Application
    
    # Verificar acesso
    query = get_students_query(db, current_user)
    student = query.filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado ou você não tem permissão"
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
    📊 Obter histórico de performance de um estudante
    """
    from app.models.performance import PerformanceAnalysis
    
    # Verificar acesso
    query = get_students_query(db, current_user)
    student = query.filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado ou você não tem permissão"
        )
    
    analyses = db.query(PerformanceAnalysis).filter(
        PerformanceAnalysis.student_id == student_id
    ).order_by(PerformanceAnalysis.analyzed_at.desc()).all()
    
    return analyses
