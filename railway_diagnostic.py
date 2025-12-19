"""
Script de diagnóstico para Railway - Adicione ao seu projeto
"""
import os
import sys

print("=" * 80)
print("🔍 RAILWAY DIAGNOSTIC - AdaptAI")
print("=" * 80)
print()

# 1. Verificar se está no Railway
print("📍 AMBIENTE:")
print("-" * 80)
is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None
print(f"Railway: {'✅ SIM' if is_railway else '❌ NÃO'}")
print(f"Environment: {os.getenv('RAILWAY_ENVIRONMENT', 'N/A')}")
print(f"Service: {os.getenv('RAILWAY_SERVICE_NAME', 'N/A')}")
print()

# 2. Verificar variáveis MySQL
print("🗄️ VARIÁVEIS MYSQL:")
print("-" * 80)
mysql_vars = {
    "MYSQL_HOST": os.getenv("MYSQL_HOST"),
    "MYSQL_PORT": os.getenv("MYSQL_PORT"),
    "MYSQL_USER": os.getenv("MYSQL_USER"),
    "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
    "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE"),
}

for key, value in mysql_vars.items():
    if value:
        if "PASSWORD" in key:
            print(f"✅ {key}: {value[:3]}***")
        else:
            print(f"✅ {key}: {value}")
    else:
        print(f"❌ {key}: NÃO DEFINIDO")
print()

# 3. Verificar outras variáveis importantes
print("🔐 VARIÁVEIS DE SEGURANÇA:")
print("-" * 80)
print(f"SECRET_KEY: {'✅ DEFINIDO' if os.getenv('SECRET_KEY') else '❌ NÃO DEFINIDO'}")
print(f"ANTHROPIC_API_KEY: {'✅ DEFINIDO' if os.getenv('ANTHROPIC_API_KEY') else '❌ NÃO DEFINIDO'}")
print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'N/A')}")
print()

# 4. Tentar importar config
print("⚙️ TESTE DE IMPORTAÇÃO:")
print("-" * 80)
try:
    from app.core.config import settings
    print("✅ Config importado com sucesso!")
    print(f"   - MYSQL_HOST do settings: {settings.MYSQL_HOST}")
    print(f"   - MYSQL_DATABASE do settings: {settings.MYSQL_DATABASE}")
    print(f"   - db_url: {settings.db_url[:50]}...")
except Exception as e:
    print(f"❌ ERRO ao importar config: {e}")
    sys.exit(1)
print()

# 5. Tentar construir URL do banco
print("🔗 URL DO BANCO DE DADOS:")
print("-" * 80)
try:
    print(f"Host usado: {settings.MYSQL_HOST}")
    if settings.MYSQL_HOST == "localhost":
        print("❌ PROBLEMA: Usando 'localhost'!")
        print("   As variáveis de ambiente NÃO estão sendo lidas!")
    else:
        print(f"✅ URL OK: Conectando em {settings.MYSQL_HOST}")
except Exception as e:
    print(f"❌ ERRO: {e}")
print()

# 6. Testar conexão
print("🔌 TESTE DE CONEXÃO:")
print("-" * 80)
try:
    from sqlalchemy import create_engine, text
    
    engine = create_engine(
        settings.db_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 10}
    )
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ CONEXÃO OK!")
        
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()[0]
        print(f"✅ Banco: {db_name}")
        
except Exception as e:
    print(f"❌ ERRO DE CONEXÃO: {str(e)[:200]}")
    if "localhost" in str(e):
        print("\n⚠️  PROBLEMA IDENTIFICADO:")
        print("   O erro menciona 'localhost' - variáveis não estão sendo lidas!")
        print("\n   SOLUÇÃO:")
        print("   1. Verifique se TODAS as variáveis estão no Railway")
        print("   2. Faça REDEPLOY")
        print("   3. Aguarde build completo")

print()
print("=" * 80)
print("FIM DO DIAGNÓSTICO")
print("=" * 80)
