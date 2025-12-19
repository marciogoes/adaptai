import sys
sys.path.append('.')

import pymysql

def renomear_tabelas():
    print("="*70)
    print("SOLUCAO DEFINITIVA: RENOMEAR TABELAS COM PREFIXO")
    print("="*70)
    print()
    print("O SQLAlchemy INSISTE em usar 'teamarcionovo' como prefixo.")
    print("Entao vamos renomear as tabelas para ter esse prefixo!")
    print()
    
    # Conectar ao banco
    conn = pymysql.connect(
        host='teamarcionovo.mysql.dbaas.com.br',
        user='teamarcionovo',
        password='MarcioGo1003@@',
        database='teamarcionovo'
    )
    
    cursor = conn.cursor()
    
    try:
        # Listar tabelas atuais
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        
        print("Tabelas atuais:")
        for t in tables:
            print(f"  - {t}")
        print()
        
        # Mapa de renomeação
        rename_map = {
            'users': 'teamarcionovousers',
            'students': 'teamarcionovostudents',
            'questions': 'teamarcionovoquestions',
            'question_sets': 'teamarcionovoquestion_sets',
            'applications': 'teamarcionovoapplications',
            'student_answers': 'teamarcionovostudent_answers',
            'performance_analyses': 'teamarcionovoperformance_analyses'
        }
        
        print("Renomeando tabelas...")
        for old_name, new_name in rename_map.items():
            if old_name in tables:
                try:
                    cursor.execute(f"RENAME TABLE `{old_name}` TO `{new_name}`")
                    print(f"  ✓ {old_name} → {new_name}")
                except Exception as e:
                    print(f"  ✗ {old_name}: {e}")
        
        conn.commit()
        print("[OK] Tabelas renomeadas!")
        print()
        
        # Verificar
        cursor.execute("SHOW TABLES")
        new_tables = [t[0] for t in cursor.fetchall()]
        
        print("Tabelas finais:")
        for t in sorted(new_tables):
            print(f"  - {t}")
        print()
        
        print("="*70)
        print("SUCESSO! Agora o SQLAlchemy vai encontrar as tabelas!")
        print("="*70)
        
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    renomear_tabelas()
