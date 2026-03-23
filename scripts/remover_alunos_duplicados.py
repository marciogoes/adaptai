#!/usr/bin/env python3
"""
Script para remover alunos duplicados (nomes que não estão em caixa alta)
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Credenciais do MySQL
MYSQL_HOST = "teamarcionovo.mysql.dbaas.com.br"
MYSQL_PORT = 3306
MYSQL_USER = "teamarcionovo"
MYSQL_PASSWORD = "MarcioGo1003@@"
MYSQL_DATABASE = "teamarcionovo"

encoded_password = quote_plus(MYSQL_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

def main():
    print("=" * 70)
    print("  ADAPTAI - Remover Alunos Duplicados (caixa baixa/mista)")
    print("=" * 70)
    print()
    
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
        
        print("🔍 Conectando ao banco de dados...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ Conectado! MySQL Version: {version}")
        
        print()
        print("-" * 70)
        print("ANTES: Lista de alunos")
        print("-" * 70)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, grade_level, email
                FROM students 
                ORDER BY id
            """))
            students = result.fetchall()
            
            print(f"\n📋 {len(students)} alunos encontrados:\n")
            for s in students:
                # Verificar se o nome está em caixa alta
                is_upper = s[1] == s[1].upper()
                status = "✅ CAIXA ALTA" if is_upper else "❌ caixa mista"
                print(f"   ID: {s[0]:3} | {status} | Nome: {s[1][:45]:45} | Série: {s[2]}")
        
        print()
        print("-" * 70)
        print("Removendo alunos que NÃO estão em caixa alta...")
        print("-" * 70)
        
        # IDs dos alunos em caixa mista/baixa (4, 5, 6)
        ids_para_remover = [4, 5, 6]
        
        with engine.begin() as conn:
            # Listar os que serão removidos
            result = conn.execute(text("""
                SELECT id, name FROM students 
                WHERE id IN :ids
            """), {"ids": tuple(ids_para_remover)})
            
            alunos_remover = result.fetchall()
            
            if alunos_remover:
                print(f"\n🗑️  Removendo {len(alunos_remover)} alunos:")
                for a in alunos_remover:
                    print(f"   - ID {a[0]}: {a[1]}")
                
                # Remover (CASCADE vai apagar dados relacionados)
                result = conn.execute(text("""
                    DELETE FROM students 
                    WHERE id IN :ids
                """), {"ids": tuple(ids_para_remover)})
                
                print(f"\n✅ {result.rowcount} aluno(s) removido(s)!")
            else:
                print("\n✅ Nenhum aluno para remover.")
        
        print()
        print("-" * 70)
        print("DEPOIS: Lista de alunos atualizada")
        print("-" * 70)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, grade_level, email
                FROM students 
                ORDER BY id
            """))
            students = result.fetchall()
            
            print(f"\n📋 {len(students)} alunos no sistema:\n")
            for s in students:
                print(f"   ID: {s[0]:3} | Nome: {s[1][:50]:50} | Série: {s[2]:12} | Email: {s[3] or 'N/A'}")
        
        print()
        print("=" * 70)
        print("  🎉 OPERAÇÃO CONCLUÍDA!")
        print("=" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
