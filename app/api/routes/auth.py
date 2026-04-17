from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.core.config import settings
from app.core.rate_limit import check_rate_limit
from app.api.dependencies import get_current_active_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# SEGURANCA: hash dummy para garantir tempo constante no login.
# Quando o email nao existe, ainda verificamos a senha contra este hash para
# evitar enumeracao de usuarios por timing attack.
_DUMMY_PASSWORD_HASH = get_password_hash("dummy-password-for-timing-safety-never-used")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    Registrar um novo usuario (PUBLICO).
    
    SEGURANCA: 
    - Rate limited a 5 registros por hora por IP.
    - Este endpoint SEMPRE cria usuario com role=TEACHER.
    - Nao aceita 'role' do cliente para evitar escalacao de privilegio.
    Para criar admin/coordenador, use endpoint protegido separado.
    """
    check_rate_limit(
        request, key="register", max_requests=5, window_seconds=3600,
        error_message="Muitos registros a partir deste IP. Aguarde 1 hora."
    )
    
    # Verificar se o email ja existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Criar novo usuario - role HARDCODED para TEACHER por seguranca
    from app.models.user import UserRole
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=UserRole.TEACHER  # NUNCA aceitar role do request publico
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login e obtencao de token JWT.
    
    SEGURANCA: 
    - Rate limited a 10 tentativas por minuto por IP (anti brute-force).
    - Usa tempo constante para evitar enumeracao de usuarios.
    - Mesma mensagem de erro e mesmo tempo de resposta para email invalido e senha errada.
    """
    check_rate_limit(
        request, key="login", max_requests=10, window_seconds=60,
        error_message="Muitas tentativas de login. Aguarde um minuto."
    )
    
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # SEGURANCA: SEMPRE executar verify_password (mesmo quando user nao existe)
    # contra um hash dummy, para manter tempo de resposta constante.
    if user:
        valid = verify_password(form_data.password, user.hashed_password)
    else:
        verify_password(form_data.password, _DUMMY_PASSWORD_HASH)
        valid = False
    
    if not valid or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Bloquear login de usuario desativado
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desativado. Entre em contato com o administrador."
        )
    
    # Criar tokens (A10: access curto + refresh longo)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

@router.post("/login/json", response_model=Token)
def login_json(user_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    Login com JSON (alternativa ao form).
    
    SEGURANCA: rate limited + tempo constante (mesmas protecoes do /login).
    """
    check_rate_limit(
        request, key="login", max_requests=10, window_seconds=60,
        error_message="Muitas tentativas de login. Aguarde um minuto."
    )
    
    user = db.query(User).filter(User.email == user_data.email).first()
    
    # Tempo constante - ver comentario em login()
    if user:
        valid = verify_password(user_data.password, user.hashed_password)
    else:
        verify_password(user_data.password, _DUMMY_PASSWORD_HASH)
        valid = False
    
    if not valid or not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desativado. Entre em contato com o administrador."
        )
    
    # Criar tokens (A10)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user_data.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """
    Obter informações do usuário atual
    """
    return current_user

@router.get("/test-token")
def test_token(current_user: User = Depends(get_current_active_user)):
    """
    Testar se o token e valido
    """
    return {
        "message": "Token is valid",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


# ============================================
# REFRESH TOKEN (A10)
# ============================================

class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/refresh", response_model=RefreshResponse)
def refresh_access_token(
    payload: RefreshRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Troca um refresh token valido por um novo access token.
    
    Fluxo esperado:
    1. Cliente detecta que access token expirou (401)
    2. Cliente chama POST /auth/refresh com o refresh_token guardado
    3. Se valido, recebe novo access_token e continua
    4. Se invalido (expirado ou malformado), cliente precisa fazer login de novo
    """
    # Rate limit - impede abuso do endpoint de refresh
    check_rate_limit(
        request, key="refresh", max_requests=30, window_seconds=60,
        error_message="Muitas renovacoes de token. Aguarde um minuto."
    )
    
    refresh_payload = decode_refresh_token(payload.refresh_token)
    if not refresh_payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalido ou expirado. Faca login novamente.",
        )
    
    email: str = refresh_payload.get("sub", "")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token malformado.",
        )
    
    # Verificar se o usuario/aluno ainda existe e esta ativo
    if email.startswith("student:"):
        from app.models.student import Student
        student_email = email.replace("student:", "")
        student = db.query(Student).filter(Student.email == student_email).first()
        if not student or not student.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta desativada. Faca login novamente.",
            )
        
        new_access = create_access_token(
            data={"sub": email, "student_id": student.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    else:
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Conta desativada. Faca login novamente.",
            )
        
        new_access = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    
    return RefreshResponse(access_token=new_access)

# ============= ENDPOINTS PARA ESTUDANTES =============

@router.post("/student/login", response_model=Token)
def student_login(user_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    Login para estudantes.
    
    SEGURANCA: rate limited + tempo constante.
    """
    from app.models.student import Student
    
    check_rate_limit(
        request, key="student_login", max_requests=10, window_seconds=60,
        error_message="Muitas tentativas de login. Aguarde um minuto."
    )
    
    student = db.query(Student).filter(Student.email == user_data.email).first()
    
    # SEGURANCA: tempo constante - ver comentario em login()
    if student and student.hashed_password:
        valid = verify_password(user_data.password, student.hashed_password)
    else:
        verify_password(user_data.password, _DUMMY_PASSWORD_HASH)
        valid = False
    
    if not valid or not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Estudante inativo. Entre em contato com o professor.",
        )
    
    # Criar tokens com prefixo student: para diferenciar (A10)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": f"student:{student.email}", "student_id": student.id},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": f"student:{student.email}", "student_id": student.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }

@router.get("/student/me")
def get_current_student_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obter informações do estudante atual
    """
    from app.models.student import Student
    from app.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if not email or not email.startswith("student:"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não é de estudante",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remover prefixo student:
    email = email.replace("student:", "")
    student = db.query(Student).filter(Student.email == email).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudante não encontrado"
        )
    
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "grade_level": student.grade_level,
        "birth_date": student.birth_date,
        "diagnosis": student.diagnosis,
        "profile_data": student.profile_data,
        "is_active": student.is_active
    }
