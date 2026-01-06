# ============================================
# SINCRONIZAR BANCO REMOTO - Adicionar colunas faltantes
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

def sincronizar_banco():
    print("=" * 60)
    print("🔄 SINCRONIZANDO BANCO DE DADOS REMOTO")
    print("=" * 60)
    print(f"📡 Host: {settings.MYSQL_HOST}")
    print(f"📦 Database: {settings.MYSQL_DATABASE}")
    print("=" * 60)
    
    alteracoes = [
        # Tabela USERS
        ("users", "escola_id", "ALTER TABLE users ADD COLUMN escola_id INT NULL"),
        
        # Tabela STUDENTS
        ("students", "escola_id", "ALTER TABLE students ADD COLUMN escola_id INT NULL"),
        ("students", "email", "ALTER TABLE students ADD COLUMN email VARCHAR(255) NULL"),
        ("students", "hashed_password", "ALTER TABLE students ADD COLUMN hashed_password VARCHAR(255) NULL"),
        ("students", "is_active", "ALTER TABLE students ADD COLUMN is_active BOOLEAN DEFAULT TRUE"),
        ("students", "turma", "ALTER TABLE students ADD COLUMN turma VARCHAR(50) NULL"),
        ("students", "matricula", "ALTER TABLE students ADD COLUMN matricula VARCHAR(50) NULL"),
        ("students", "profile_data", "ALTER TABLE students ADD COLUMN profile_data JSON NULL"),
    ]
    
    with engine.connect() as conn:
        for tabela, coluna, sql in alteracoes:
            # Verificar se coluna existe
            result = conn.execute(text(f"""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{settings.MYSQL_DATABASE}'
                AND TABLE_NAME = '{tabela}' 
                AND COLUMN_NAME = '{coluna}'
            """))
            
            if result.fetchone():
                print(f"✅ {tabela}.{coluna} já existe")
            else:
                print(f"➕ Adicionando {tabela}.{coluna}...")
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"   ✅ Adicionado!")
                except Exception as e:
                    print(f"   ⚠️  Erro: {e}")
        
        # Mostrar estrutura das tabelas principais
        print("\n" + "=" * 60)
        print("📋 ESTRUTURA ATUAL DAS TABELAS")
        print("=" * 60)
        
        for tabela in ["users", "students"]:
            print(f"\n🔹 Tabela: {tabela}")
            try:
                result = conn.execute(text(f"DESCRIBE {tabela}"))
                for row in result.fetchall():
                    print(f"   • {row[0]}: {row[1]}")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SINCRONIZAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n🔄 Reinicie o backend agora!")


if __name__ == "__main__":
    sincronizar_banco()
