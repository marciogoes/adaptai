# ============================================
# DIAGNÓSTICO COMPLETO DE LOGIN (sem requests)
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings
import bcrypt

# Criar engine
engine = create_engine(settings.db_url, echo=False)

def diagnostico():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO COMPLETO DE LOGIN")
    print("=" * 60)
    
    # 1. Verificar usuário no banco
    print("\n📋 PASSO 1: Verificando usuário no banco...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, email, hashed_password, role, is_active FROM users WHERE email = 'admin@adaptai.com'"))
        user = result.fetchone()
        
        if not user:
            print("❌ Usuário admin@adaptai.com NÃO EXISTE no banco!")
            print("\n🔧 Criando usuário...")
            
            senha = "senha123"
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')
            
            conn.execute(text("""
                INSERT INTO users (name, email, hashed_password, role, is_active)
                VALUES ('Administrador', 'admin@adaptai.com', :senha, 'admin', 1)
            """), {"senha": senha_hash})
            conn.commit()
            print("✅ Usuário criado!")
            
            # Buscar novamente
            result = conn.execute(text("SELECT id, name, email, hashed_password, role, is_active FROM users WHERE email = 'admin@adaptai.com'"))
            user = result.fetchone()
        
        print(f"   ID: {user[0]}")
        print(f"   Nome: {user[1]}")
        print(f"   Email: {user[2]}")
        print(f"   Hash: {user[3][:40]}...")
        print(f"   Role: {user[4]}")
        print(f"   Ativo: {user[5]}")
        
        # 2. Testar senha
        print("\n📋 PASSO 2: Testando senha...")
        senha_teste = "senha123"
        hash_banco = user[3]
        
        try:
            senha_valida = bcrypt.checkpw(senha_teste.encode('utf-8'), hash_banco.encode('utf-8'))
            if senha_valida:
                print(f"✅ Senha 'senha123' está CORRETA!")
            else:
                print(f"❌ Senha 'senha123' está INCORRETA!")
                print("\n🔧 Atualizando senha...")
                
                salt = bcrypt.gensalt()
                novo_hash = bcrypt.hashpw(senha_teste.encode('utf-8'), salt).decode('utf-8')
                
                conn.execute(text("""
                    UPDATE users SET hashed_password = :senha WHERE email = 'admin@adaptai.com'
                """), {"senha": novo_hash})
                conn.commit()
                print("✅ Senha atualizada!")
        except Exception as e:
            print(f"❌ Erro ao verificar senha: {e}")
            print("\n🔧 Recriando hash da senha...")
            
            salt = bcrypt.gensalt()
            novo_hash = bcrypt.hashpw(senha_teste.encode('utf-8'), salt).decode('utf-8')
            
            conn.execute(text("""
                UPDATE users SET hashed_password = :senha WHERE email = 'admin@adaptai.com'
            """), {"senha": novo_hash})
            conn.commit()
            print("✅ Senha recriada!")
    
    # 3. Listar todos os usuários
    print("\n📋 PASSO 3: Todos os usuários no banco:")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, email, role, is_active FROM users"))
        users = result.fetchall()
        
        if not users:
            print("   ⚠️  Nenhum usuário encontrado!")
        else:
            for u in users:
                status = "✅" if u[3] else "❌"
                print(f"   {status} ID:{u[0]} | {u[1]} | {u[2]}")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO CONCLUÍDO!")
    print("=" * 60)
    print("\n🔐 CREDENCIAIS PARA LOGIN:")
    print("   Email: admin@adaptai.com")
    print("   Senha: senha123")
    print("   URL: http://localhost:5173/login")
    print("\n⚠️  Certifique-se que o BACKEND está rodando:")
    print("   python -m uvicorn app.main:app --reload")
    print("=" * 60)


if __name__ == "__main__":
    diagnostico()
