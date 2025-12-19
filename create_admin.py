import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext
from datetime import datetime

# Configurar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_user():
    db = SessionLocal()
    
    try:
        # Verificar se já existe um usuário com este email
        existing_user = db.query(User).filter(User.email == "admin@adaptai.com").first()
        
        if existing_user:
            print("[INFO] Usuario admin@adaptai.com ja existe!")
            print(f"      Nome: {existing_user.name}")
            print(f"      Email: {existing_user.email}")
            print(f"      Role: {existing_user.role}")
            return
        
        # Criar senha hasheada
        hashed_password = pwd_context.hash("admin123")
        
        # Criar usuário
        admin_user = User(
            name="Administrador",
            email="admin@adaptai.com",
            hashed_password=hashed_password,
            role="admin",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("="*60)
        print("USUARIO CRIADO COM SUCESSO!")
        print("="*60)
        print()
        print("Credenciais de acesso:")
        print(f"  Email:    admin@adaptai.com")
        print(f"  Senha:    admin123")
        print(f"  Nome:     {admin_user.name}")
        print(f"  Role:     {admin_user.role}")
        print()
        print("Use estas credenciais para fazer login no sistema!")
        print("="*60)
        
    except Exception as e:
        print(f"[ERRO] Falha ao criar usuario: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
