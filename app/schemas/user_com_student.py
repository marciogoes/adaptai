from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    TEACHER = "teacher"
    COORDINATOR = "coordinator"
    ADMIN = "admin"
    STUDENT = "student"  # ADICIONADO: Role de estudante

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole = UserRole.TEACHER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
