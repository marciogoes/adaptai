"""
Migration: Corrigir tabela relatorios
Adiciona arquivo_path e permite NULL em arquivo_base64
"""
import sys
from pathlib import Path

# Adicionar path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine

def run_migration():
    """Executa migration da tabela relatorios"""
    
    print("=" * 60)
    print("MIGRATION: Corrigir tabela relatorios")
    print("=" * 60)
    
    with engine.connect() as conn:
        try:
            # 1. Verificar se coluna arquivo_path já existe
            print("\n[1/3] Verificando coluna arquivo_path...")
            result = conn.execute(text("SHOW COLUMNS FROM relatorios LIKE 'arquivo_path'"))
            if result.fetchone():
                print("✅ Coluna arquivo_path já existe!")
            else:
                print("➕ Adicionando coluna arquivo_path...")
                conn.execute(text("""
                    ALTER TABLE relatorios 
                    ADD COLUMN arquivo_path VARCHAR(500) NULL
                    AFTER arquivo_tipo
                """))
                conn.commit()
                print("✅ Coluna arquivo_path adicionada!")
            
            # 2. Permitir NULL em arquivo_base64
            print("\n[2/3] Permitindo NULL em arquivo_base64...")
            conn.execute(text("""
                ALTER TABLE relatorios 
                MODIFY COLUMN arquivo_base64 LONGTEXT NULL
            """))
            conn.commit()
            print("✅ arquivo_base64 agora aceita NULL!")
            
            # 3. Verificar estrutura
            print("\n[3/3] Verificando estrutura final...")
            result = conn.execute(text("DESCRIBE relatorios"))
            rows = result.fetchall()
            
            print("\n📊 Estrutura da tabela relatorios:")
            print("-" * 80)
            for row in rows:
                if row[0] in ['arquivo_path', 'arquivo_base64']:
                    print(f"  {row[0]}: {row[1]} - NULL: {row[2]}")
            print("-" * 80)
            
            print("\n" + "=" * 60)
            print("✅ MIGRATION CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("\nAgora você pode fazer upload de relatórios! 🎉")
            
        except Exception as e:
            print(f"\n❌ ERRO na migration: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    run_migration()
