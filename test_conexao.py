"""
Script para testar conexão com MySQL e verificar variáveis de ambiente
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Força o carregamento do .env
load_dotenv(override=True)

print("=" * 60)
print("🔍 TESTE DE CONEXÃO MySQL - AdaptAI")
print("=" * 60)
print()

# 1. Verificar variáveis de ambiente
print("📋 1. VERIFICANDO VARIÁVEIS DE AMBIENTE:")
print("-" * 60)

vars_to_check = [
    "MYSQL_HOST",
    "MYSQL_PORT", 
    "MYSQL_USER",
    "MYSQL_PASSWORD",
    "MYSQL_DATABASE"
]

all_vars_ok = True
for var in vars_to_check:
    value = os.getenv(var)
    if value:
        # Oculta senha parcialmente
        if "PASSWORD" in var:
            display_value = value[:3] + "*" * (len(value) - 3)
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")
    else:
        print(f"❌ {var}: NÃO ENCONTRADO")
        all_vars_ok = False

print()

if not all_vars_ok:
    print("⚠️  ERRO: Algumas variáveis não foram encontradas!")
    print()
    print("SOLUÇÃO:")
    print("1. Verifique se o arquivo .env existe em: backend/.env")
    print("2. Verifique se as variáveis estão definidas corretamente")
    print("3. Execute: pip install python-dotenv")
    sys.exit(1)

# 2. Montar URL de conexão
print("🔗 2. MONTANDO URL DE CONEXÃO:")
print("-" * 60)

host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

# Codifica a senha para URL
encoded_password = quote_plus(password) if password else ""

db_url = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}?charset=utf8mb4"

# Mostra URL (sem senha completa)
safe_url = f"mysql+pymysql://{user}:***@{host}:{port}/{database}?charset=utf8mb4"
print(f"URL: {safe_url}")
print()

# 3. Testar conexão
print("🔌 3. TESTANDO CONEXÃO COM BANCO DE DADOS:")
print("-" * 60)

try:
    # Cria engine com timeout menor para teste
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 10,
            "charset": "utf8mb4"
        }
    )
    
    # Tenta conectar
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        
        if row and row[0] == 1:
            print("✅ CONEXÃO BEM-SUCEDIDA!")
            print()
            
            # Testa acesso ao banco
            result = conn.execute(text("SELECT DATABASE() as db_name"))
            db_name = result.fetchone()[0]
            print(f"✅ Banco de dados atual: {db_name}")
            
            # Lista algumas tabelas
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"✅ Tabelas encontradas: {len(tables)}")
                print(f"   Primeiras tabelas: {', '.join(tables[:5])}")
            else:
                print("⚠️  Nenhuma tabela encontrada no banco")
            
    print()
    print("=" * 60)
    print("✅ TUDO OK! Banco de dados está acessível.")
    print("=" * 60)
    print()
    print("Agora você pode iniciar o backend com:")
    print("  uvicorn app.main:app --reload")
    
except Exception as e:
    print(f"❌ ERRO AO CONECTAR: {str(e)}")
    print()
    print("POSSÍVEIS CAUSAS:")
    print("1. ❌ Host/porta incorretos")
    print("2. ❌ Usuário/senha inválidos") 
    print("3. ❌ Firewall bloqueando conexão")
    print("4. ❌ Banco de dados indisponível")
    print("5. ❌ IP não autorizado no servidor MySQL")
    print()
    print("VERIFIQUE:")
    print(f"- Host: {host}")
    print(f"- Porta: {port}")
    print(f"- Usuário: {user}")
    print(f"- Banco: {database}")
    sys.exit(1)
