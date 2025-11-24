from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class PerformanceByLevel(BaseModel):
    correct: int
    total: int
    percentage: float

class PerformanceBySkill(BaseModel):
    correct: int
    total: int
    percentage: float
    mastery: str  # "excellent", "good", "developing", "needs_work"

class WeakPoint(BaseModel):
    skill: str
    description: str
    questions_missed: List[int]
    recommendation: str

class StrongPoint(BaseModel):
    skill: str
    description: str

class PerformanceAnalysisResponse(BaseModel):
    id: int
    student_id: int
    application_id: int
    overall_score: float
    by_difficulty_level: Dict[str, Dict[str, float]]
    by_skill: Dict[str, Dict[str, float]]
    weak_points: List[Dict]
    strong_points: List[Dict]
    recommendations: Optional[str] = None
    analyzed_at: datetime
    
    class Config:
        from_attributes = True

class PerformanceSummary(BaseModel):
    """Resumo rápido de desempenho"""
    student_id: int
    student_name: str
    overall_score: float
    total_questions: int
    correct_answers: int
    status: str  # "excellent", "good", "needs_improvement"

class StudentProgressReport(BaseModel):
    """Relatório de progresso do aluno"""
    student_id: int
    student_name: str
    period: str
    total_applications: int
    average_score: float
    improvement_trend: str  # "improving", "stable", "declining"
    strong_skills: List[str]
    weak_skills: List[str]
    recommendations: str
