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
    Retorna o usuário atual se estiver ativo
    """
    # Por enquanto todos os usuários são ativos
    # Futuramente pode adicionar campo 'is_active' no model
    return current_user

def require_teacher(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Requer que o usuário seja pelo menos professor
    """
    from app.models.user import UserRole
    
    if current_user.role not in [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]:
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
    
    if current_user.role not in [UserRole.COORDINATOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Coordinator role required."
        )
    return current_user

def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Requer que o usuário seja admin
    """
    from app.models.user import UserRole
    
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    return current_user
