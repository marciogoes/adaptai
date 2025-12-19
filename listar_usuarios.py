import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# IMPORTAR TODOS OS MODELOS para SQLAlchemy resolver relacionamentos
from app.database import SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.question import QuestionSet, Question
from app.models.application import Application
from app.models.performance import PerformanceAnalysis
from app.models.material import Material, MaterialAluno
from app.models.prova import Prova, QuestaoGerada, ProvaAluno, RespostaAluno, StatusProvaAluno
from app.models.analise_qualitativa import AnaliseQualitativa

def listar_usuarios():
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("USUÁRIOS NO SISTEMA")
        print("=" * 60)
        print()
        
        # Listar Users
        users = db.query(User).all()
        
        if not users:
            print("❌ Nenhum usuário encontrado!")
        else:
            print(f"Total de usuários: {len(users)}")
            print()
            for user in users:
                print(f"ID: {user.id}")
                print(f"Nome: {user.name}")
                print(f"Email: {user.email}")
                print(f"Role: {user.role}")
                print(f"Ativo: {user.is_active}")
                print("-" * 60)
        
        print()
        print("=" * 60)
        print("ESTUDANTES NO SISTEMA")
        print("=" * 60)
        print()
        
        # Listar Students
        students = db.query(Student).all()
        
        if not students:
            print("❌ Nenhum estudante encontrado!")
        else:
            print(f"Total de estudantes: {len(students)}")
            print()
            for student in students:
                print(f"ID: {student.id}")
                print(f"Nome: {student.name}")
                print(f"Email: {student.email}")
                print(f"Série: {student.grade_level}")
                print(f"Criado por (user_id): {student.created_by_user_id}")
                print(f"Ativo: {student.is_active}")
                print("-" * 60)
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    listar_usuarios()
