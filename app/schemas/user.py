from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re

class UserRole(str, Enum):
    TEACHER = "teacher"
    COORDINATOR = "coordinator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"  # Admin global do sistema


# ============================================
# VALIDACAO DE SENHA (A13 - politica forte)
# ============================================

def validar_senha_forte(senha: str) -> str:
    """
    Valida senha segundo politica forte.
    
    Requisitos:
    - Minimo 10 caracteres (era 8 antes - ainda aceitavel pela maioria mas facil de bruteforcear)
    - Pelo menos 1 letra maiuscula
    - Pelo menos 1 letra minuscula
    - Pelo menos 1 numero
    - Nao pode ser uma senha obvia (lista de senhas comuns)
    
    Nao exige caractere especial (UX: frustra usuarios, e o ganho em entropia
    e compensado pelo tamanho minimo de 10 caracteres).
    """
    if len(senha) < 10:
        raise ValueError("Senha deve ter pelo menos 10 caracteres")
    
    if len(senha) > 128:
        raise ValueError("Senha muito longa (max 128 caracteres)")
    
    # FIX: lista de senhas obvias checada ANTES das validacoes de caracteres.
    # Caso contrario, 'PASSWORD123' era rejeitado por "falta minuscula" em vez
    # de por "muito comum" - mensagem pior pro usuario, e o teste
    # test_senha_obvia_bloqueada esperava a mensagem especifica case-insensitive.
    # Lista curta de senhas obvias para bloquear
    senhas_proibidas = {
        "12345678901", "1234567890", "abcd1234ab", "senha12345",
        "password123", "123456abc", "qwerty12345", "admin12345",
        "adaptai2024", "adaptai2025", "adaptai2026",
    }
    if senha.lower() in senhas_proibidas:
        raise ValueError("Esta senha e muito comum. Escolha uma mais segura.")
    
    if not re.search(r"[A-Z]", senha):
        raise ValueError("Senha deve conter pelo menos uma letra maiuscula")
    
    if not re.search(r"[a-z]", senha):
        raise ValueError("Senha deve conter pelo menos uma letra minuscula")
    
    if not re.search(r"\d", senha):
        raise ValueError("Senha deve conter pelo menos um numero")
    
    return senha


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema para registro PUBLICO de usuarios.
    NAO aceita 'role' do cliente - sempre sera TEACHER (ver auth.py /register).
    Para criar usuarios com outras roles, use UserCreateAdmin em endpoint protegido.
    
    Senha deve seguir politica forte (ver validar_senha_forte).
    """
    password: str = Field(..., min_length=10, max_length=128)
    
    @field_validator("password")
    @classmethod
    def _validar_senha(cls, v: str) -> str:
        return validar_senha_forte(v)

class UserCreateAdmin(UserBase):
    """
    Schema para criacao de usuario por admin/coordenador.
    Aceita 'role' mas o endpoint que usa este schema DEVE ser protegido por require_admin.
    """
    password: str = Field(..., min_length=10, max_length=128)
    role: UserRole = UserRole.TEACHER
    
    @field_validator("password")
    @classmethod
    def _validar_senha(cls, v: str) -> str:
        return validar_senha_forte(v)

class UserLogin(BaseModel):
    email: EmailStr
    password: str  # Login nao valida forca - aceita qualquer string para verificar

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool = True
    escola_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    # A10: refresh_token e opcional para backward-compat com clientes antigos
    # que esperam apenas access_token. Novos clientes devem guardar ambos.
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
