"""
Security helpers: bcrypt + JWT.

A10: introduz distincao access vs refresh token via claim 'type'.
- access: TTL curto (padrao settings.ACCESS_TOKEN_EXPIRE_MINUTES, ~60min)
- refresh: TTL longo (7 dias), usado APENAS no endpoint /refresh para obter novo access

Nota sobre revogacao: como nao temos Redis/blacklist, logout do lado cliente
e apenas limpeza do storage - token continua tecnicamente valido ate expirar.
Para revogacao server-side real, seria necessario adicionar tabela de tokens_revogados
ou integrar Redis. Deixado para bloco futuro.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings


REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha esta correta usando bcrypt diretamente"""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Gera hash da senha usando bcrypt diretamente"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria access token JWT.
    
    Inclui claim 'type': 'access' para distinguir de refresh tokens.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Cria refresh token JWT com TTL longo (7 dias).
    
    Deve ser usado APENAS para chamar POST /auth/refresh e obter novo access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica e valida token JWT.
    
    NAO valida o claim 'type' - permite decodificar tanto access quanto refresh.
    Endpoints que precisam distinguir devem verificar payload.get('type') explicitamente.
    
    Retorna None se invalido ou expirado.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str) -> Optional[dict]:
    """
    Decodifica refresh token e valida que eh do tipo 'refresh'.
    Retorna None se invalido, expirado, ou se for access token passado no lugar.
    """
    payload = decode_access_token(token)
    if not payload:
        return None
    if payload.get("type") != "refresh":
        return None
    return payload
