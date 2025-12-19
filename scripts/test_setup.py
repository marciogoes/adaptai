"""
Script de teste para validar a configuração do AdaptAI
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🧪 Testando imports...")
    
    try:
        from app.core.config import settings
        print("  ✅ Config importado")
        
        from app.database import engine, Base
        print("  ✅ Database importado")
        
        from app.models import User, Student, Question
        print("  ✅ Models importados")
        
        from app.core.security import get_password_hash
        print("  ✅ Security importado")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro no import: {e}")
        return False

def test_config():
    """Testa se as configurações estão corretas"""
    print("\n⚙️  Testando configurações...")
    
    try:
        from app.core.config import settings
        
        print(f"  📱 App Name: {settings.APP_NAME}")
        print(f"  🔢 Version: {settings.VERSION}")
        print(f"  🐛 Debug: {settings.DEBUG}")
        print(f"  🗄️  Database: {settings.MYSQL_DATABASE}")
        print(f"  🤖 Claude Model: {settings.CLAUDE_MODEL}")
        
        if not settings.ANTHROPIC_API_KEY or settings.ANTHROPIC_API_KEY.startswith("sk-ant-api03-your"):
            print("  ⚠️  ATENÇÃO: Configure a ANTHROPIC_API_KEY no arquivo .env")
        else:
            print("  ✅ API Key configurada")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro na configuração: {e}")
        return False

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("\n🗄️  Testando conexão com banco de dados...")
    
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("  ✅ Conexão com MySQL estabelecida")
            return True
    except Exception as e:
        print(f"  ❌ Erro ao conectar com MySQL: {e}")
        print("  💡 Dica: Verifique se o MySQL está rodando e as credenciais no .env")
        return False

def test_tables():
    """Testa se as tabelas foram criadas"""
    print("\n📊 Testando tabelas do banco de dados...")
    
    try:
        from app.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'users', 'students', 'question_sets', 'questions',
            'applications', 'student_answers', 'performance_analyses'
        ]
        
        for table in expected_tables:
            if table in tables:
                print(f"  ✅ Tabela '{table}' existe")
            else:
                print(f"  ❌ Tabela '{table}' não encontrada")
        
        if len(tables) == 0:
            print("\n  💡 Execute: python scripts/init_db.py")
        
        return len(tables) > 0
    except Exception as e:
        print(f"  ❌ Erro ao verificar tabelas: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🎓 AdaptAI - Teste de Configuração")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Config": test_config(),
        "Database": test_database_connection(),
        "Tables": test_tables()
    }
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 O AdaptAI está pronto para uso!")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("📖 Verifique as mensagens acima para resolver os problemas")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
