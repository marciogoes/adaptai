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

def associar_estudante_professor():
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("ASSOCIAR ESTUDANTE A PROFESSOR")
        print("=" * 60)
        print()
        
        # Listar professores/admins disponíveis
        print("Professores/Admins disponíveis:")
        print("-" * 60)
        users = db.query(User).filter(User.role.in_(["admin", "teacher"])).all()
        
        if not users:
            print("❌ ERRO: Nenhum professor ou admin encontrado!")
            print("   Crie um usuário admin primeiro!")
            return
        
        for user in users:
            print(f"ID: {user.id} | Nome: {user.name} | Email: {user.email} | Role: {user.role}")
        print()
        
        # Listar estudantes
        print("Estudantes disponíveis:")
        print("-" * 60)
        students = db.query(Student).all()
        
        if not students:
            print("❌ ERRO: Nenhum estudante encontrado!")
            return
        
        for student in students:
            professor_info = "Sem professor"
            if student.created_by_user_id:
                professor = db.query(User).filter(User.id == student.created_by_user_id).first()
                if professor:
                    professor_info = f"Professor: {professor.name}"
            print(f"ID: {student.id} | Nome: {student.name} | {professor_info}")
        print()
        
        # Pedir IDs
        student_id = input("Digite o ID do ESTUDANTE: ").strip()
        professor_id = input("Digite o ID do PROFESSOR/ADMIN: ").strip()
        
        # Validar
        try:
            student_id = int(student_id)
            professor_id = int(professor_id)
        except ValueError:
            print("❌ ERRO: IDs devem ser números!")
            return
        
        # Buscar estudante
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            print(f"❌ ERRO: Estudante com ID {student_id} não encontrado!")
            return
        
        # Buscar professor
        professor = db.query(User).filter(User.id == professor_id).first()
        if not professor:
            print(f"❌ ERRO: Professor com ID {professor_id} não encontrado!")
            return
        
        # Confirmar
        print()
        print("=" * 60)
        print("CONFIRMAÇÃO:")
        print("=" * 60)
        print(f"Estudante: {student.name}")
        print(f"Será associado a: {professor.name} ({professor.role})")
        print()
        
        confirma = input("Confirma? (S/N): ").strip().upper()
        if confirma != 'S':
            print("❌ Operação cancelada!")
            return
        
        # Associar
        print()
        print("Associando...")
        student.created_by_user_id = professor_id
        db.commit()
        
        print()
        print("=" * 60)
        print("✅ ESTUDANTE ASSOCIADO COM SUCESSO!")
        print("=" * 60)
        print(f"{student.name} agora está associado a {professor.name}")
        print()
        print("O estudante deve aparecer agora no dashboard do professor!")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    associar_estudante_professor()
