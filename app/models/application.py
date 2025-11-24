from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    question_set_id = Column(Integer, ForeignKey("question_sets.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    applied_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    applied_date = Column(DateTime(timezone=True), nullable=False)
    time_limit_minutes = Column(Integer, nullable=True)
    
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    question_set = relationship("QuestionSet", back_populates="applications")
    student = relationship("Student", back_populates="applications")
    applied_by = relationship("User", back_populates="applications")
    answers = relationship("StudentAnswer", back_populates="application", cascade="all, delete-orphan")
    performance_analysis = relationship("PerformanceAnalysis", back_populates="application", uselist=False)

class StudentAnswer(Base):
    __tablename__ = "student_answers"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    selected_answer = Column(String(1), nullable=True)  # 'a', 'b', 'c', 'd', ou null
    is_correct = Column(Boolean, nullable=True)
    
    time_spent_seconds = Column(Integer, nullable=True)
    attempts = Column(Integer, default=1)
    
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    student = relationship("Student", back_populates="answers")
