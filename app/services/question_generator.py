from sqlalchemy.orm import Session
from app.models.question import QuestionSet, Question, DifficultyLevel
from app.services.ai_service import AIService
from typing import Dict

class QuestionGeneratorService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    async def generate_question_set(
        self,
        user_id: int,
        title: str,
        subject: str,
        grade_level: str,
        raw_content: str,
        level_1_qty: int = 0,
        level_2_qty: int = 0,
        level_3_qty: int = 0,
        level_4_qty: int = 0,
        adaptations: list = [],
        tags: list = []
    ) -> QuestionSet:
        """
        Gera um conjunto completo de questões
        """
        
        # Criar config
        config = {
            "level_1_qty": level_1_qty,
            "level_2_qty": level_2_qty,
            "level_3_qty": level_3_qty,
            "level_4_qty": level_4_qty,
            "adaptations": adaptations
        }
        
        # Criar o QuestionSet
        question_set = QuestionSet(
            user_id=user_id,
            title=title,
            subject=subject,
            grade_level=grade_level,
            raw_content=raw_content,
            config=config,
            tags=tags
        )
        
        self.db.add(question_set)
        self.db.commit()
        self.db.refresh(question_set)
        
        # Gerar questões por nível
        all_questions = []
        order_number = 1
        
        levels_to_generate = [
            (1, level_1_qty),
            (2, level_2_qty),
            (3, level_3_qty),
            (4, level_4_qty)
        ]
        
        for level, quantity in levels_to_generate:
            if quantity > 0:
                questions_data = self.ai_service.generate_questions(
                    content=raw_content,
                    subject=subject,
                    grade_level=grade_level,
                    difficulty_level=level,
                    quantity=quantity,
                    adaptations=adaptations
                )
                
                for q_data in questions_data:
                    question = Question(
                        question_set_id=question_set.id,
                        difficulty_level=DifficultyLevel(level),
                        question_text=q_data["question_text"],
                        option_a=q_data["option_a"],
                        option_b=q_data["option_b"],
                        option_c=q_data["option_c"],
                        option_d=q_data["option_d"],
                        correct_answer=q_data["correct_answer"],
                        explanation=q_data.get("explanation"),
                        skill=q_data.get("skill"),
                        order_number=order_number
                    )
                    all_questions.append(question)
                    order_number += 1
        
        # Salvar todas as questões
        self.db.add_all(all_questions)
        self.db.commit()
        
        # Refresh para pegar as questões
        self.db.refresh(question_set)
        
        return question_set
    
    def get_question_set_with_questions(self, question_set_id: int, user_id: int = None) -> QuestionSet:
        """
        Retorna o conjunto de questões com todas as questões
        """
        query = self.db.query(QuestionSet).filter(QuestionSet.id == question_set_id)
        
        if user_id:
            query = query.filter(QuestionSet.user_id == user_id)
        
        return query.first()
    
    def list_question_sets(self, user_id: int, skip: int = 0, limit: int = 20):
        """
        Lista todos os conjuntos de questões do usuário
        """
        return self.db.query(QuestionSet).filter(
            QuestionSet.user_id == user_id
        ).offset(skip).limit(limit).all()
