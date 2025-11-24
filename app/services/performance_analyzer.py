from sqlalchemy.orm import Session
from app.models.application import Application, StudentAnswer
from app.models.performance import PerformanceAnalysis
from app.models.student import Student
from app.services.ai_service import AIService
from typing import Dict, List
from collections import defaultdict

class PerformanceAnalyzerService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
    
    def analyze_application(self, application_id: int) -> PerformanceAnalysis:
        """
        Analisa o desempenho de um aluno em uma aplicação
        """
        
        # Buscar a aplicação com respostas
        application = self.db.query(Application).filter(
            Application.id == application_id
        ).first()
        
        if not application:
            raise ValueError("Application not found")
        
        answers = self.db.query(StudentAnswer).filter(
            StudentAnswer.application_id == application_id
        ).all()
        
        # Buscar o aluno
        student = self.db.query(Student).filter(
            Student.id == application.student_id
        ).first()
        
        # Calcular estatísticas básicas
        total_questions = len(answers)
        correct_answers = sum(1 for a in answers if a.is_correct)
        overall_score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Análise por nível de dificuldade
        by_difficulty = defaultdict(lambda: {"correct": 0, "total": 0})
        
        for answer in answers:
            question = answer.question
            level = str(question.difficulty_level.value)
            by_difficulty[level]["total"] += 1
            if answer.is_correct:
                by_difficulty[level]["correct"] += 1
        
        # Calcular porcentagens
        by_difficulty_with_percentage = {}
        for level, stats in by_difficulty.items():
            percentage = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            by_difficulty_with_percentage[level] = {
                "correct": stats["correct"],
                "total": stats["total"],
                "percentage": round(percentage, 2)
            }
        
        # Análise por habilidade/skill
        by_skill = defaultdict(lambda: {"correct": 0, "total": 0})
        
        for answer in answers:
            question = answer.question
            if question.skill:
                by_skill[question.skill]["total"] += 1
                if answer.is_correct:
                    by_skill[question.skill]["correct"] += 1
        
        # Calcular mastery level por skill
        by_skill_with_mastery = {}
        for skill, stats in by_skill.items():
            percentage = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            
            if percentage >= 90:
                mastery = "excellent"
            elif percentage >= 75:
                mastery = "good"
            elif percentage >= 60:
                mastery = "developing"
            else:
                mastery = "needs_work"
            
            by_skill_with_mastery[skill] = {
                "correct": stats["correct"],
                "total": stats["total"],
                "percentage": round(percentage, 2),
                "mastery": mastery
            }
        
        # Identificar pontos fracos (questões erradas)
        weak_points = []
        questions_by_skill = defaultdict(list)
        
        for answer in answers:
            if not answer.is_correct and answer.question.skill:
                questions_by_skill[answer.question.skill].append(answer.question.id)
        
        for skill, question_ids in questions_by_skill.items():
            if len(question_ids) >= 2:  # Pelo menos 2 erros na mesma habilidade
                weak_points.append({
                    "skill": skill,
                    "description": f"Dificuldade em {skill.replace('_', ' ')}",
                    "questions_missed": question_ids,
                    "recommendation": self._get_skill_recommendation(skill)
                })
        
        # Identificar pontos fortes
        strong_points = []
        for skill, stats in by_skill_with_mastery.items():
            if stats["mastery"] in ["excellent", "good"]:
                strong_points.append({
                    "skill": skill,
                    "description": f"Bom desempenho em {skill.replace('_', ' ')}"
                })
        
        # Preparar dados para análise da IA
        answers_data = []
        for answer in answers:
            answers_data.append({
                "question_id": answer.question.id,
                "question_text": answer.question.question_text,
                "selected_answer": answer.selected_answer,
                "correct_answer": answer.question.correct_answer,
                "is_correct": answer.is_correct,
                "skill": answer.question.skill,
                "difficulty_level": answer.question.difficulty_level.value
            })
        
        # Gerar recomendações com IA
        ai_analysis = self.ai_service.analyze_performance(
            student_name=student.name,
            answers_data=answers_data,
            student_profile=student.profile_data
        )
        
        recommendations_text = f"""
{ai_analysis.get('summary', '')}

PONTOS FORTES:
{ai_analysis.get('strong_points_analysis', '')}

ÁREAS PARA MELHORAR:
{ai_analysis.get('weak_points_analysis', '')}

RECOMENDAÇÕES:
{ai_analysis.get('recommendations', '')}

PRÓXIMOS PASSOS:
{chr(10).join('• ' + step for step in ai_analysis.get('next_steps', []))}
"""
        
        # Criar a análise de desempenho
        performance_analysis = PerformanceAnalysis(
            student_id=application.student_id,
            application_id=application_id,
            overall_score=round(overall_score, 2),
            by_difficulty_level=by_difficulty_with_percentage,
            by_skill=by_skill_with_mastery,
            weak_points=weak_points,
            strong_points=strong_points,
            recommendations=recommendations_text
        )
        
        self.db.add(performance_analysis)
        self.db.commit()
        self.db.refresh(performance_analysis)
        
        return performance_analysis
    
    def _get_skill_recommendation(self, skill: str) -> str:
        """
        Retorna recomendação baseada na habilidade
        """
        recommendations = {
            "identificar_conceitos": "Revisar definições básicas com exemplos visuais",
            "interpretar_relacoes": "Usar organizadores gráficos e mapas conceituais",
            "aplicar_conhecimento": "Praticar com situações do cotidiano",
            "analisar_informacoes": "Trabalhar com textos curtos e questões direcionadas",
            "comparar_e_contrastar": "Usar tabelas comparativas e diagramas de Venn"
        }
        
        return recommendations.get(skill, "Praticar mais exercícios sobre este tópico")
