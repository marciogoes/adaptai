"""
Script para inicializar o banco de dados MySQL remoto
Cria todas as tabelas necessárias
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from app.database import engine, Base
from app.models import user, student, question, application, answer
from app.core.config import settings

def init_db():
    """Cria todas as tabelas no banco de dados"""
    print("🚀 Iniciando conexão com MySQL remoto...")
    print(f"📍 Host: {settings.MYSQL_HOST}")
    print(f"👤 User: {settings.MYSQL_USER}")
    print(f"💾 Database: {settings.MYSQL_DATABASE}")
    print()
    
    try:
        # Testa a conexão
        with engine.connect() as connection:
            print("✅ Conexão com MySQL estabelecida com sucesso!")
        
        print("\n📦 Criando tabelas...")
        
        # Cria todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tabelas criadas com sucesso!")
        print("\n📋 Tabelas criadas:")
        print("  - users (usuários do sistema)")
        print("  - students (estudantes)")
        print("  - questions (questões)")
        print("  - applications (aplicações de questões)")
        print("  - answers (respostas dos estudantes)")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("\n📝 Próximos passos:")
        print("  1. Inicie o servidor: uvicorn app.main:app --reload")
        print("  2. Acesse: http://localhost:8000")
        print("  3. Documentação API: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Erro ao inicializar banco de dados:")
        print(f"   {str(e)}")
        print("\n🔍 Verifique:")
        print("  - Credenciais do MySQL no arquivo .env")
        print("  - Conexão com a internet")
        print("  - Firewall/Permissões do servidor MySQL")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("  ADAPTAI - Inicialização do Banco de Dados MySQL")
    print("=" * 60)
    print()
    
    init_db()
