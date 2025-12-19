"""
Script para listar todas as tabelas do banco de dados
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def listar_tabelas():
    print("\n" + "="*80)
    print("📊 LISTANDO TABELAS DO BANCO DE DADOS")
    print("="*80 + "\n")
    
    engine = create_engine(settings.db_url)
    
    try:
        with engine.connect() as conn:
            print("✅ Conectado ao banco!\n")
            
            # Listar todas as tabelas
            sql = "SHOW TABLES"
            result = conn.execute(text(sql))
            
            tabelas = [row[0] for row in result]
            
            print(f"📋 Total de tabelas: {len(tabelas)}\n")
            print("="*80)
            
            for idx, tabela in enumerate(sorted(tabelas), 1):
                print(f"{idx:2d}. {tabela}")
            
            print("="*80 + "\n")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
    
    finally:
        engine.dispose()


if __name__ == "__main__":
    listar_tabelas()
    input("\nPressione ENTER para sair...")
