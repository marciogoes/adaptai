"""
📋 Listar Todos os Usuários - AdaptAI
"""
import sys
import os
from urllib.parse import quote_plus

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Configuração do banco
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

MYSQL_PASSWORD_ESCAPED = quote_plus(MYSQL_PASSWORD) if MYSQL_PASSWORD else ""
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD_ESCAPED}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print()
print("=" * 80)
print("📋 LISTANDO TODOS OS USUÁRIOS DO ADAPTAI")
print("=" * 80)
print()

try:
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Lista todos os usuários
    result = db.execute(text("""
        SELECT id, name, email, role, is_active, created_at 
        FROM users 
        ORDER BY role, name
    """))
    
    usuarios = result.fetchall()
    
    if not usuarios:
        print("❌ Nenhum usuário encontrado no banco de dados!")
    else:
        print(f"Total de usuários: {len(usuarios)}")
        print()
        print("┌─────┬────────────────────────────────┬────────────────────────────────────┬──────────────┬────────┐")
        print("│ ID  │ NOME                           │ EMAIL                              │ PERFIL       │ ATIVO  │")
        print("├─────┼────────────────────────────────┼────────────────────────────────────┼──────────────┼────────┤")
        
        for user in usuarios:
            id_str = str(user[0]).ljust(3)
            nome = (user[1] or "")[:30].ljust(30)
            email = (user[2] or "")[:34].ljust(34)
            role = (user[3] or "").upper()[:12].ljust(12)
            ativo = "✅ Sim" if user[4] else "❌ Não"
            ativo = ativo.ljust(6)
            print(f"│ {id_str} │ {nome} │ {email} │ {role} │ {ativo} │")
        
        print("└─────┴────────────────────────────────┴────────────────────────────────────┴──────────────┴────────┘")
        
        # Resumo por perfil
        print()
        print("📊 RESUMO POR PERFIL:")
        print("-" * 40)
        
        result_resumo = db.execute(text("""
            SELECT role, COUNT(*) as total 
            FROM users 
            GROUP BY role 
            ORDER BY total DESC
        """))
        
        for row in result_resumo.fetchall():
            print(f"   • {row[0].upper()}: {row[1]} usuário(s)")
    
    db.close()
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
