from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    
    # Credenciais de acesso
    email = Column(String(255), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    birth_date = Column(Date, nullable=True)
    grade_level = Column(String(50), nullable=False)  # "1º ano", "2º ano", etc
    
    # Diagnóstico e perfil em JSON
    diagnosis = Column(JSON, nullable=True)
    # Ex: {"tea": {"level": 1}, "tdah": true, "dislexia": false}
    
    profile_data = Column(JSON, nullable=True)
    # Ex: {"learning_style": "visual", "support_level": "medium", 
    #      "interests": ["dinossauros", "espaço"]}
    
    notes = Column(Text, nullable=True)  # Observações gerais
    
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teacher = relationship("User", back_populates="students")
    applications = relationship("Application", back_populates="student")
    answers = relationship("StudentAnswer", back_populates="student")
    performance_analyses = relationship("PerformanceAnalysis", back_populates="student")
    provas = relationship("ProvaAluno", back_populates="aluno")
    materiais = relationship("MaterialAluno", back_populates="aluno")
    relatorios = relationship("Relatorio", back_populates="student", cascade="all, delete-orphan")
