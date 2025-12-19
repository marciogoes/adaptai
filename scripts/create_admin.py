"""
Script para criar um usuário administrador inicial
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_admin():
    db: Session = SessionLocal()
    
    try:
        print("🔐 Criando usuário administrador...")
        
        # Verificar se já existe admin
        existing_admin = db.query(User).filter(User.email == "admin@adaptai.com").first()
        
        if existing_admin:
            print("❌ Usuário admin já existe!")
            print(f"   Email: {existing_admin.email}")
            print(f"   Nome: {existing_admin.name}")
            return
        
        # Criar admin
        admin = User(
            name="Administrador AdaptAI",
            email="admin@adaptai.com",
            hashed_password=get_password_hash("admin123"),  # MUDAR EM PRODUÇÃO!
            role=UserRole.ADMIN
        )
        
        db.add(admin)
        db.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print("\n📧 Credenciais de acesso:")
        print("   Email: admin@adaptai.com")
        print("   Senha: admin123")
        print("\n⚠️  IMPORTANTE: MUDE A SENHA EM PRODUÇÃO!")
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
