from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db, SessionLocal
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_from_token(token: str) -> User:
    """
    Busca usuario pelo token usando conexao propria que fecha imediatamente.
    Ideal para endpoints que demoram muito (IA).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Abre conexao, busca e FECHA imediatamente
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        
        # Forca carregamento dos atributos antes de fechar
        _ = user.id, user.email, user.name, user.role, user.is_active
        
        return user
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Retorna o usuário atual baseado no token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Retorna o usuario atual se estiver ativo.
    Bloqueia usuarios com is_active=False.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desativado. Entre em contato com o administrador."
        )
    return current_user

def require_teacher(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Requer que o usuário seja pelo menos professor
    """
    from app.models.user import UserRole
    
    if current_user.role not in [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Teacher role required."
        )
    return current_user

def require_coordinator(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Requer que o usuário seja coordenador ou admin
    """
    from app.models.user import UserRole
    
    if current_user.role not in [UserRole.COORDINATOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Coordinator role required."
        )
    return current_user

def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Requer que o usuário seja admin ou super_admin
    """
    from app.models.user import UserRole
    
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    return current_user


# ============================================
# HELPERS DE OWNERSHIP (para evitar IDOR)
# ============================================

def verificar_acesso_aluno(db, student_id: int, current_user: User):
    """
    Verifica se o current_user tem acesso ao aluno (student_id).
    Retorna o Student se tiver acesso, levanta 403/404 caso contrario.
    
    Regras:
    - SUPER_ADMIN: acesso a todos
    - ADMIN/COORDINATOR: acesso a alunos da mesma escola
    - TEACHER: acesso apenas a alunos que ele mesmo criou
    
    Uso tipico em endpoints:
        aluno = verificar_acesso_aluno(db, request.student_id, current_user)
    """
    from app.models.student import Student
    from app.models.user import UserRole
    
    aluno = db.query(Student).filter(Student.id == student_id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno nao encontrado"
        )
    
    if current_user.role == UserRole.SUPER_ADMIN:
        return aluno
    
    if current_user.role in [UserRole.ADMIN, UserRole.COORDINATOR]:
        if aluno.escola_id != current_user.escola_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Voce nao tem permissao para acessar este aluno"
            )
        return aluno
    
    # TEACHER
    if aluno.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Voce nao tem permissao para acessar este aluno"
        )
    return aluno


def verificar_acesso_aos_alunos(db, student_ids: list, current_user: User):
    """
    Versao em lote de verificar_acesso_aluno.
    Retorna lista de Students validos, levanta 403 se QUALQUER aluno for inacessivel.
    Uso: ao atribuir tema de redacao/prova a multiplos alunos.
    """
    return [verificar_acesso_aluno(db, sid, current_user) for sid in student_ids]


def verificar_acesso_pei(db, pei_id: int, current_user: User):
    """
    Verifica acesso ao PEI via ownership do aluno dono.
    Retorna o PEI se tiver acesso, levanta 404/403 caso contrario.
    
    Uso tipico em endpoints:
        pei = verificar_acesso_pei(db, pei_id, current_user)
    """
    from app.models.pei import PEI
    
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    if not pei:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PEI nao encontrado"
        )
    
    # Valida acesso ao aluno dono do PEI - se falhar, levanta 403/404
    verificar_acesso_aluno(db, pei.student_id, current_user)
    return pei


def verificar_acesso_objetivo_pei(db, objetivo_id: int, current_user: User):
    """
    Verifica acesso a um PEIObjetivo via ownership do aluno (atraves do PEI pai).
    Retorna o objetivo se tiver acesso, levanta 404/403 caso contrario.
    
    Uso tipico em endpoints:
        objetivo = verificar_acesso_objetivo_pei(db, objetivo_id, current_user)
    """
    from app.models.pei import PEI, PEIObjetivo
    
    objetivo = db.query(PEIObjetivo).filter(PEIObjetivo.id == objetivo_id).first()
    if not objetivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo nao encontrado"
        )
    
    pei = db.query(PEI).filter(PEI.id == objetivo.pei_id).first()
    if not pei:
        # PEI orfao - nao deveria acontecer mas protege contra DB inconsistente
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PEI do objetivo nao encontrado"
        )
    
    verificar_acesso_aluno(db, pei.student_id, current_user)
    return objetivo


# ============================================
# AUTENTICACAO DE ESTUDANTES (C4 - centralizado)
# ============================================

# OAuth2 scheme compartilhado com auth.py (mesmo tokenUrl)
_student_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_student(
    token: str = Depends(_student_oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency para obter estudante autenticado a partir do token JWT.
    
    CENTRALIZADO: antes esta funcao estava duplicada em 4 arquivos de rotas
    (student_provas, student_materiais, student_pei, auth). Agora todas
    as rotas de estudante devem usar esta dependencia unica.
    
    Requisitos:
    - Token valido
    - Subject comeca com "student:"
    - Estudante existe no banco
    - Estudante esta ativo (is_active=True)
    
    Raises:
        401 se token invalido ou nao for de estudante
        403 se estudante estiver inativo
        404 se estudante nao existir
    """
    # Import aqui para evitar ciclo em tempo de import
    from app.models.student import Student
    from app.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub", "")
    if not email or not email.startswith("student:"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token nao e de estudante",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remover prefixo student:
    student_email = email.replace("student:", "")
    student = db.query(Student).filter(Student.email == student_email).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudante nao encontrado"
        )
    
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta de estudante desativada. Entre em contato com seu professor."
        )
    
    return student
