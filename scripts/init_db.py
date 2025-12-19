"""
Script para inicializar o banco de dados
Cria todas as tabelas necessárias
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import user, student, question, application, performance

def init_db():
    print("🚀 Iniciando criação das tabelas no banco de dados...")
    print(f"📊 Database URL: {engine.url}")
    
    try:
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        print("\nTabelas criadas:")
        print("  - users")
        print("  - students")
        print("  - question_sets")
        print("  - questions")
        print("  - applications")
        print("  - student_answers")
        print("  - performance_analyses")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
