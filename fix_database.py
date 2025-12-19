import sys
sys.path.append('.')

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings
from app.database import Base, SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_database():
    print("="*70)
    print("CORRIGINDO BANCO DE DADOS - REMOCAO TOTAL E RECRIACAO")
    print("="*70)
    print()
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        print("[1/5] Descobrindo TODAS as tabelas existentes...")
        inspector = inspect(engine)
        all_tables = inspector.get_table_names()
        
        if all_tables:
            print(f"  Encontradas {len(all_tables)} tabelas:")
            for table in sorted(all_tables):
                print(f"    - {table}")
        else:
            print("  Nenhuma tabela encontrada")
        print()
        
        print("[2/5] REMOVENDO TODAS AS TABELAS...")
        with engine.connect() as conn:
            # Desabilitar foreign key checks temporariamente
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # Dropar cada tabela
            for table in all_tables:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                    print(f"  ✓ {table} removida")
                except Exception as e:
                    print(f"  ✗ {table}: {e}")
            
            # Reabilitar foreign key checks
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
        
        print("[OK] Todas as tabelas removidas!")
        print()
        
        print("[3/5] Verificando se banco esta vazio...")
        inspector = inspect(engine)
        remaining = inspector.get_table_names()
        
        if remaining:
            print(f"  ⚠ AVISO: Ainda existem {len(remaining)} tabelas!")
            for table in remaining:
                print(f"    - {table}")
        else:
            print("  ✓ Banco completamente vazio!")
        print()
        
        print("[4/5] CRIANDO TABELAS NOVAS com nomes corretos...")
        Base.metadata.create_all(bind=engine)
        print("[OK] Tabelas criadas!")
        print()
        
        print("[5/5] Verificando tabelas criadas...")
        inspector = inspect(engine)
        new_tables = inspector.get_table_names()
        
        print(f"  Total de tabelas criadas: {len(new_tables)}")
        for table in sorted(new_tables):
            if table.startswith('teamarcionovo'):
                print(f"    ❌ {table} (NOME ERRADO!)")
            else:
                print(f"    ✓ {table}")
        print()
        
        # Criar usuario administrador
        print("[BONUS] Criando usuario administrador...")
        db = SessionLocal()
        
        try:
            existing = db.query(User).filter(User.email == "admin@adaptai.com").first()
            if existing:
                print("  ! Usuario admin ja existe")
            else:
                admin = User(
                    name="Administrador",
                    email="admin@adaptai.com",
                    hashed_password=pwd_context.hash("admin123"),
                    role="admin",
                    is_active=True
                )
                db.add(admin)
                db.commit()
                print("  ✓ Usuario admin criado")
        except Exception as e:
            print(f"  ✗ Erro ao criar usuario: {e}")
        finally:
            db.close()
        
        print()
        print("="*70)
        print("SUCESSO! BANCO TOTALMENTE RECRIADO!")
        print("="*70)
        print()
        print("Tabelas no banco agora:")
        for table in sorted(new_tables):
            print(f"  - {table}")
        print()
        print("Credenciais de acesso:")
        print("  Email: admin@adaptai.com")
        print("  Senha: admin123")
        print()
        print("="*70)
        
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = fix_database()
    sys.exit(0 if success else 1)
