import sys
sys.path.append('.')

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def listar_tabelas():
    print("="*60)
    print("LISTANDO TABELAS NO BANCO")
    print("="*60)
    print()
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        inspector = inspect(engine)
        
        tables = inspector.get_table_names()
        
        if not tables:
            print("Nenhuma tabela encontrada no banco!")
        else:
            print(f"Total de tabelas: {len(tables)}")
            print()
            
            # Separar tabelas corretas e erradas
            corretas = []
            erradas = []
            
            for table in sorted(tables):
                if table.startswith('teamarcionovo'):
                    erradas.append(table)
                else:
                    corretas.append(table)
            
            if erradas:
                print("❌ TABELAS COM NOMES ERRADOS:")
                for table in erradas:
                    print(f"   - {table}")
                print()
            
            if corretas:
                print("✓ TABELAS COM NOMES CORRETOS:")
                for table in corretas:
                    print(f"   - {table}")
                print()
            
            if not corretas:
                print("⚠ PROBLEMA: Nao ha tabelas com nomes corretos!")
                print("   Execute fix_database.py para corrigir!")
        
        print("="*60)
        
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    listar_tabelas()
