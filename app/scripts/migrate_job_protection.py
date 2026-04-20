# ============================================
# MIGRATION - Adicionar colunas de proteção a jobs
# ============================================
# Execute: python -m app.scripts.migrate_job_protection
#
# Adiciona colunas para:
# - Heartbeat (detectar jobs travados)
# - Lock de concorrência (evitar duplicação)

import sys
import os

# Adicionar path do projeto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text
from app.core.config import settings


def run_migration():
    """Executa a migração para adicionar colunas de proteção"""
    
    print("=" * 60)
    print("MIGRATION: Adicionar colunas de proteção a planejamento_jobs")
    print("=" * 60)
    
    engine = create_engine(settings.db_url, echo=False)
    
    with engine.connect() as conn:
        # Verificar se tabela existe
        result = conn.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'planejamento_jobs'
        """))
        
        if result.scalar() == 0:
            print("❌ Tabela planejamento_jobs não existe!")
            print("   Execute as migrations iniciais primeiro.")
            return False
        
        # Verificar colunas existentes
        result = conn.execute(text("""
            SELECT COLUMN_NAME 
            FROM information_schema.columns 
            WHERE table_name = 'planejamento_jobs'
        """))
        colunas_existentes = [row[0] for row in result.fetchall()]
        
        # Colunas a adicionar
        colunas_novas = {
            "last_heartbeat": "DATETIME DEFAULT CURRENT_TIMESTAMP",
            "heartbeat_count": "INT DEFAULT 0",
            "lock_token": "VARCHAR(100) NULL",
            "lock_expires_at": "DATETIME NULL"
        }
        
        for coluna, definicao in colunas_novas.items():
            if coluna in colunas_existentes:
                print(f"✓ Coluna '{coluna}' já existe")
            else:
                print(f"➕ Adicionando coluna '{coluna}'...")
                try:
                    conn.execute(text(f"""
                        ALTER TABLE planejamento_jobs 
                        ADD COLUMN {coluna} {definicao}
                    """))
                    conn.commit()
                    print(f"   ✅ Coluna '{coluna}' adicionada com sucesso!")
                except Exception as e:
                    print(f"   ❌ Erro ao adicionar '{coluna}': {e}")
        
        # Criar índices para busca de jobs travados e lookup por aluno.
        # FIX: MySQL nao suporta CREATE INDEX IF NOT EXISTS (so MariaDB/Postgres).
        # A versao anterior mascarava o erro de sintaxe como "indice pode ja existir",
        # entao os indices nunca eram criados de fato. Agora checamos antes via
        # information_schema, mesmo padrao usado para colunas acima.
        print("\n📊 Verificando índices...")
        
        result = conn.execute(text("""
            SELECT INDEX_NAME 
            FROM information_schema.statistics 
            WHERE table_schema = DATABASE()
            AND table_name = 'planejamento_jobs'
        """))
        indices_existentes = {row[0] for row in result.fetchall()}
        
        indices_novos = {
            "idx_jobs_heartbeat": "planejamento_jobs (status, last_heartbeat)",
            "idx_jobs_student_status": "planejamento_jobs (student_id, ano_letivo, status)",
        }
        
        for nome, definicao in indices_novos.items():
            if nome in indices_existentes:
                print(f"   ✓ Índice '{nome}' já existe")
                continue
            print(f"   ➕ Criando índice '{nome}'...")
            try:
                conn.execute(text(f"CREATE INDEX {nome} ON {definicao}"))
                conn.commit()
                print(f"      ✅ Índice '{nome}' criado com sucesso!")
            except Exception as e:
                print(f"      ❌ Erro ao criar índice '{nome}': {e}")
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION CONCLUÍDA!")
        print("=" * 60)
        
        return True


def verificar_e_limpar_jobs_travados():
    """Verifica e limpa jobs que ficaram travados"""
    
    print("\n🔍 Verificando jobs travados...")
    
    engine = create_engine(settings.db_url, echo=False)
    
    with engine.connect() as conn:
        # Buscar jobs em PROCESSING há mais de 10 minutos
        result = conn.execute(text("""
            SELECT id, task_id, student_id, status, updated_at, last_heartbeat
            FROM planejamento_jobs 
            WHERE status = 'processing'
            AND (
                last_heartbeat < DATE_SUB(NOW(), INTERVAL 5 MINUTE)
                OR last_heartbeat IS NULL
            )
        """))
        
        jobs_travados = result.fetchall()
        
        if not jobs_travados:
            print("   ✅ Nenhum job travado encontrado!")
            return
        
        print(f"   ⚠️ Encontrados {len(jobs_travados)} jobs travados:")
        
        for job in jobs_travados:
            print(f"      - Job {job[0]} (task: {job[1][:8]}...) - Aluno {job[2]}")
            
            # Marcar como FAILED
            conn.execute(text("""
                UPDATE planejamento_jobs 
                SET status = 'failed',
                    ultimo_erro = 'Job marcado como travado pelo sistema de cleanup',
                    completed_at = NOW()
                WHERE id = :job_id
            """), {"job_id": job[0]})
        
        conn.commit()
        print(f"   ✅ {len(jobs_travados)} jobs marcados como FAILED")


if __name__ == "__main__":
    success = run_migration()
    
    if success:
        verificar_e_limpar_jobs_travados()
