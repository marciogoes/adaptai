from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class DifficultyLevel(int, Enum):
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    CHALLENGE = 4

class QuestionGenerationConfig(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Título da atividade")
    subject: str = Field(..., max_length=100, description="Disciplina: Matemática, Português, Ciências, etc")
    grade_level: str = Field(..., max_length=50, description="Ano escolar: 1º ano, 2º ano, etc")
    raw_content: str = Field(..., min_length=50, description="Conteúdo base para gerar as questões")
    
    level_1_qty: int = Field(default=0, ge=0, le=50, description="Quantidade de questões nível 1 (Básico)")
    level_2_qty: int = Field(default=0, ge=0, le=50, description="Quantidade de questões nível 2 (Intermediário)")
    level_3_qty: int = Field(default=0, ge=0, le=50, description="Quantidade de questões nível 3 (Avançado)")
    level_4_qty: int = Field(default=0, ge=0, le=50, description="Quantidade de questões nível 4 (Desafio)")
    
    adaptations: List[str] = Field(
        default=[],
        description="Adaptações: simple_language, short_sentences, avoid_double_negative, visual_support, highlight_keywords"
    )
    tags: List[str] = Field(default=[], description="Tags para categorização")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Avaliação de Fotossíntese",
                "subject": "Ciências",
                "grade_level": "5º ano",
                "raw_content": "A fotossíntese é o processo pelo qual plantas verdes usam luz solar para transformar água e gás carbônico em glicose e oxigênio...",
                "level_1_qty": 10,
                "level_2_qty": 8,
                "level_3_qty": 5,
                "level_4_qty": 0,
                "adaptations": ["simple_language", "short_sentences"],
                "tags": ["fotossíntese", "plantas", "ciências"]
            }
        }

class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str = Field(..., pattern="^[a-d]$")
    explanation: Optional[str] = None
    skill: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: int
    difficulty_level: DifficultyLevel
    order_number: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionSetBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade_level: str

class QuestionSetResponse(QuestionSetBase):
    id: int
    user_id: int
    config: Dict
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    questions: List[QuestionResponse] = []
    
    class Config:
        from_attributes = True

class QuestionSetListResponse(QuestionSetBase):
    id: int
    config: Dict
    tags: Optional[List[str]] = None
    created_at: datetime
    total_questions: int
    
    class Config:
        from_attributes = True

class QuestionSetWithStats(QuestionSetResponse):
    total_questions: int
    questions_by_level: Dict[int, int]
    
    class Config:
        from_attributes = True
