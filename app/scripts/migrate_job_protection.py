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
        
        # Criar índice para busca de jobs travados
        print("\n📊 Verificando índices...")
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_jobs_heartbeat 
                ON planejamento_jobs (status, last_heartbeat)
            """))
            conn.commit()
            print("   ✅ Índice idx_jobs_heartbeat criado/verificado")
        except Exception as e:
            # MySQL não suporta IF NOT EXISTS em índices
            print(f"   ⚠️ Índice pode já existir: {e}")
        
        try:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_jobs_student_status 
                ON planejamento_jobs (student_id, ano_letivo, status)
            """))
            conn.commit()
            print("   ✅ Índice idx_jobs_student_status criado/verificado")
        except Exception as e:
            print(f"   ⚠️ Índice pode já existir: {e}")
        
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
