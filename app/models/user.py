from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    TEACHER = "teacher"
    COORDINATOR = "coordinator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"  # Admin do sistema (acessa todas as escolas)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Multi-tenant: vinculação com escola
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=True, index=True)
    
    # Dados básicos
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TEACHER)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    escola = relationship("Escola", back_populates="usuarios")
    students = relationship("Student", back_populates="teacher")
    question_sets = relationship("QuestionSet", back_populates="creator")
    applications = relationship("Application", back_populates="applied_by")
    provas_criadas = relationship("Prova", back_populates="criado_por")
    materiais_criados = relationship("Material", back_populates="criado_por")
    temas_redacao_criados = relationship("TemaRedacao", back_populates="criado_por")
    
    @property
    def is_super_admin(self) -> bool:
        """Verifica se é super admin (acessa todas as escolas)"""
        return self.role == UserRole.SUPER_ADMIN
    
    @property
    def pode_gerenciar_escola(self) -> bool:
        """Verifica se pode gerenciar configurações da escola"""
        return self.role in [UserRole.ADMIN, UserRole.COORDINATOR, UserRole.SUPER_ADMIN]
