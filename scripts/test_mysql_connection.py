"""
Script para testar a conexão com o MySQL remoto
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from sqlalchemy import text
from app.database import engine
from app.core.config import settings

def test_connection():
    """Testa a conexão com o MySQL"""
    print("🔍 Testando conexão com MySQL remoto...")
    print()
    print("📋 Configurações:")
    print(f"   Host: {settings.MYSQL_HOST}")
    print(f"   Port: {settings.MYSQL_PORT}")
    print(f"   User: {settings.MYSQL_USER}")
    print(f"   Database: {settings.MYSQL_DATABASE}")
    print()
    
    try:
        # Testa conexão básica
        print("1️⃣ Testando conexão básica...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print(f"   ✅ Conexão estabelecida! Resultado: {result.fetchone()}")
        
        # Verifica versão do MySQL
        print("\n2️⃣ Verificando versão do MySQL...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION() as version"))
            version = result.fetchone()[0]
            print(f"   ✅ MySQL Version: {version}")
        
        # Lista databases
        print("\n3️⃣ Listando databases disponíveis...")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result.fetchall()]
            print(f"   ✅ Databases encontrados: {', '.join(databases)}")
            
            if settings.MYSQL_DATABASE in databases:
                print(f"   ✅ Database '{settings.MYSQL_DATABASE}' encontrado!")
            else:
                print(f"   ⚠️  Database '{settings.MYSQL_DATABASE}' NÃO encontrado!")
                print(f"   📝 Você pode precisar criar o database manualmente.")
        
        # Lista tabelas no database
        print(f"\n4️⃣ Verificando tabelas no database '{settings.MYSQL_DATABASE}'...")
        with engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT TABLE_NAME FROM information_schema.TABLES "
                f"WHERE TABLE_SCHEMA = '{settings.MYSQL_DATABASE}'"
            ))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"   ✅ Tabelas encontradas ({len(tables)}):")
                for table in tables:
                    print(f"      - {table}")
            else:
                print(f"   ℹ️  Nenhuma tabela encontrada ainda.")
                print(f"   📝 Execute: python scripts/init_mysql_db.py")
        
        # Verifica charset
        print("\n5️⃣ Verificando charset do database...")
        with engine.connect() as conn:
            result = conn.execute(text(
                f"SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME "
                f"FROM information_schema.SCHEMATA "
                f"WHERE SCHEMA_NAME = '{settings.MYSQL_DATABASE}'"
            ))
            row = result.fetchone()
            if row:
                print(f"   ✅ Charset: {row[0]}")
                print(f"   ✅ Collation: {row[1]}")
        
        print("\n" + "=" * 60)
        print("🎉 CONEXÃO COM MYSQL FUNCIONANDO PERFEITAMENTE!")
        print("=" * 60)
        print("\n📝 Próximos passos:")
        
        if not tables:
            print("   1. Execute: python scripts/init_mysql_db.py")
            print("   2. Inicie o servidor: uvicorn app.main:app --reload")
        else:
            print("   1. Inicie o servidor: uvicorn app.main:app --reload")
            print("   2. Acesse: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERRO NA CONEXÃO COM MYSQL!")
        print("=" * 60)
        print(f"\nErro: {str(e)}")
        print("\n🔍 Possíveis causas:")
        print("   1. Credenciais incorretas no arquivo .env")
        print("   2. Servidor MySQL inacessível")
        print("   3. Firewall bloqueando conexão na porta 3306")
        print("   4. Database não existe")
        print("\n📝 Verifique:")
        print("   - Arquivo .env existe e está correto")
        print("   - Conexão com internet está funcionando")
        print("   - Credenciais estão corretas")
        
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  ADAPTAI - Teste de Conexão MySQL")
    print("=" * 60)
    print()
    
    success = test_connection()
    sys.exit(0 if success else 1)
