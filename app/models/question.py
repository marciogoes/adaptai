from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class DifficultyLevel(int, enum.Enum):
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    CHALLENGE = 4

class QuestionSet(Base):
    __tablename__ = "question_sets"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)  # Matemática, Português, etc
    grade_level = Column(String(50), nullable=False)
    
    # Conteúdo original usado para gerar
    raw_content = Column(Text, nullable=False)
    
    # Configurações usadas na geração
    config = Column(JSON, nullable=False)
    # Ex: {"level_1_qty": 10, "level_2_qty": 8, "level_3_qty": 5, 
    #      "adaptations": ["visual_support", "simple_language"]}
    
    tags = Column(JSON, nullable=True)  # ["fotossíntese", "plantas", "ciências"]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="question_sets")
    questions = relationship("Question", back_populates="question_set", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="question_set")

class Question(Base):
    __tablename__ = "questions"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    question_set_id = Column(Integer, ForeignKey("question_sets.id"), nullable=False)
    
    difficulty_level = Column(Enum(DifficultyLevel), nullable=False)
    question_text = Column(Text, nullable=False)
    
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    
    correct_answer = Column(String(1), nullable=False)  # 'a', 'b', 'c', ou 'd'
    explanation = Column(Text, nullable=True)
    
    # Habilidade/tópico que a questão avalia
    skill = Column(String(100), nullable=True)  # "identificar_conceitos", "interpretar_relacoes"
    
    order_number = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    question_set = relationship("QuestionSet", back_populates="questions")
    answers = relationship("StudentAnswer", back_populates="question")
