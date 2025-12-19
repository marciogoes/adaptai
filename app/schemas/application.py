from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ApplicationCreate(BaseModel):
    question_set_id: int
    student_id: int
    applied_date: datetime = Field(default_factory=datetime.now)
    time_limit_minutes: Optional[int] = Field(default=None, ge=1, le=480, description="Tempo limite em minutos")

class ApplicationResponse(BaseModel):
    id: int
    question_set_id: int
    student_id: int
    applied_by_user_id: int
    applied_date: datetime
    time_limit_minutes: Optional[int] = None
    status: ApplicationStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentAnswerCreate(BaseModel):
    question_id: int
    selected_answer: Optional[str] = Field(None, pattern="^[a-d]$")
    time_spent_seconds: Optional[int] = Field(None, ge=0)

class StudentAnswerResponse(BaseModel):
    id: int
    application_id: int
    question_id: int
    student_id: int
    selected_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    time_spent_seconds: Optional[int] = None
    answered_at: datetime
    
    class Config:
        from_attributes = True

class AnswerSubmitBatch(BaseModel):
    """Submeter múltiplas respostas de uma vez"""
    answers: List[StudentAnswerCreate]

class ApplicationWithAnswers(ApplicationResponse):
    answers: List[StudentAnswerResponse] = []
    total_questions: int
    answered_questions: int
    
    class Config:
        from_attributes = True
