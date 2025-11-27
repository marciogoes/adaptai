from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    TEACHER = "teacher"
    COORDINATOR = "coordinator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TEACHER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    students = relationship("Student", back_populates="teacher")
    question_sets = relationship("QuestionSet", back_populates="creator")
    applications = relationship("Application", back_populates="applied_by")
    provas_criadas = relationship("Prova", back_populates="criado_por")
    materiais_criados = relationship("Material", back_populates="criado_por")
