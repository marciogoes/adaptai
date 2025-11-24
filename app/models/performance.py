from sqlalchemy import Column, Integer, Float, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PerformanceAnalysis(Base):
    __tablename__ = "performance_analyses"
    __table_args__ = {'schema': None}  # FORÇAR: SEM SCHEMA!

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    
    overall_score = Column(Float, nullable=False)  # Porcentagem
    
    # Análise por nível de dificuldade
    by_difficulty_level = Column(JSON, nullable=False)
    # Ex: {"1": {"correct": 9, "total": 10, "percentage": 90}, "2": {"correct": 6, "total": 8, "percentage": 75}}
    
    # Análise por habilidade/tópico
    by_skill = Column(JSON, nullable=False)
    # Ex: {"identificar_conceitos": {"correct": 10, "total": 10, "percentage": 100, "mastery": "excellent"}}
    
    # Pontos fracos identificados
    weak_points = Column(JSON, nullable=False)
    # Ex: [{"skill": "interpretar_relacoes", "description": "...", "questions_missed": [12, 15], "recommendation": "..."}]
    
    # Pontos fortes
    strong_points = Column(JSON, nullable=False)
    # Ex: [{"skill": "identificar_conceitos", "description": "..."}]
    
    # Recomendações geradas pela IA
    recommendations = Column(Text, nullable=True)
    
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student", back_populates="performance_analyses")
    application = relationship("Application", back_populates="performance_analysis")
