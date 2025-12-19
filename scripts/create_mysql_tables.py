#!/usr/bin/env python3
"""
Script para criar tabelas do AdaptAI no MySQL remoto
Versão com limpeza profunda do banco
"""
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Credenciais do MySQL
MYSQL_HOST = "teamarcionovo.mysql.dbaas.com.br"
MYSQL_PORT = 3306
MYSQL_USER = "teamarcionovo"
MYSQL_PASSWORD = "MarcioGo1003@@"
MYSQL_DATABASE = "teamarcionovo"

# Criar URL de conexão
encoded_password = quote_plus(MYSQL_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

def create_tables():
    """Cria todas as tabelas no MySQL"""
    print("=" * 70)
    print("  ADAPTAI - Criação de Tabelas MySQL")
    print("=" * 70)
    print()
    
    try:
        # Criar engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
        
        # Testar conexão
        print("🔍 Testando conexão...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ Conectado! MySQL Version: {version}")
        
        print()
        print("🗑️  LIMPEZA PROFUNDA - Removendo TUDO...")
        
        with engine.connect() as conn:
            # Desabilitar verificação de foreign keys
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.commit()
            
            # Listar e dropar TODAS as tabelas do database
            result = conn.execute(text(
                f"SELECT TABLE_NAME FROM information_schema.TABLES "
                f"WHERE TABLE_SCHEMA = '{MYSQL_DATABASE}' AND TABLE_TYPE = 'BASE TABLE'"
            ))
            all_tables = [row[0] for row in result.fetchall()]
            
            if all_tables:
                print(f"   Encontradas {len(all_tables)} tabelas existentes:")
                for table in all_tables:
                    try:
                        conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                        print(f"   ✓ Removida: {table}")
                    except Exception as e:
                        print(f"   ⚠ Erro ao remover {table}: {e}")
                conn.commit()
            else:
                print("   ℹ Nenhuma tabela existente encontrada")
            
            # Reabilitar foreign keys
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
        
        print()
        print("📦 Criando tabelas novas (SEM foreign keys primeiro)...")
        print()
        
        with engine.begin() as conn:
            
            # 1. USERS (sem FK)
            print("   [1/5] Criando 'users'...")
            conn.execute(text("""
                CREATE TABLE `users` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `email` VARCHAR(255) NOT NULL,
                    `hashed_password` VARCHAR(255) NOT NULL,
                    `full_name` VARCHAR(255) NOT NULL,
                    `is_active` TINYINT(1) DEFAULT 1,
                    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`),
                    UNIQUE KEY `unique_email` (`email`),
                    KEY `idx_email` (`email`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # 2. STUDENTS (sem FK)
            print("   [2/5] Criando 'students'...")
            conn.execute(text("""
                CREATE TABLE `students` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `name` VARCHAR(255) NOT NULL,
                    `email` VARCHAR(255) NULL,
                    `grade` VARCHAR(50) NULL,
                    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`),
                    KEY `idx_name` (`name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # 3. QUESTIONS (sem FK)
            print("   [3/5] Criando 'questions'...")
            conn.execute(text("""
                CREATE TABLE `questions` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `text` TEXT NOT NULL,
                    `subject` VARCHAR(100) NOT NULL,
                    `grade` VARCHAR(50) NULL,
                    `difficulty` VARCHAR(20) NOT NULL,
                    `options` JSON NOT NULL,
                    `correct_answer` INT NOT NULL,
                    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`),
                    KEY `idx_subject` (`subject`),
                    KEY `idx_difficulty` (`difficulty`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # 4. APPLICATIONS (sem FK)
            print("   [4/5] Criando 'applications'...")
            conn.execute(text("""
                CREATE TABLE `applications` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `student_id` INT NOT NULL,
                    `question_ids` JSON NOT NULL,
                    `status` VARCHAR(20) DEFAULT 'pending',
                    `total_questions` INT NOT NULL,
                    `correct_answers` INT NULL,
                    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`),
                    KEY `idx_student` (`student_id`),
                    KEY `idx_status` (`status`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # 5. ANSWERS (sem FK)
            print("   [5/5] Criando 'answers'...")
            conn.execute(text("""
                CREATE TABLE `answers` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `application_id` INT NOT NULL,
                    `question_id` INT NOT NULL,
                    `user_answer` INT NOT NULL,
                    `is_correct` TINYINT(1) NOT NULL,
                    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (`id`),
                    KEY `idx_application` (`application_id`),
                    KEY `idx_question` (`question_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
        
        print()
        print("🔗 Adicionando foreign keys...")
        
        with engine.begin() as conn:
            try:
                print("   [1/3] FK: applications -> students...")
                conn.execute(text("""
                    ALTER TABLE `applications` 
                    ADD CONSTRAINT `fk_applications_student`
                    FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) 
                    ON DELETE CASCADE
                """))
            except Exception as e:
                print(f"   ⚠ Aviso FK applications: {e}")
            
            try:
                print("   [2/3] FK: answers -> applications...")
                conn.execute(text("""
                    ALTER TABLE `answers` 
                    ADD CONSTRAINT `fk_answers_application`
                    FOREIGN KEY (`application_id`) REFERENCES `applications`(`id`) 
                    ON DELETE CASCADE
                """))
            except Exception as e:
                print(f"   ⚠ Aviso FK answers->applications: {e}")
            
            try:
                print("   [3/3] FK: answers -> questions...")
                conn.execute(text("""
                    ALTER TABLE `answers` 
                    ADD CONSTRAINT `fk_answers_question`
                    FOREIGN KEY (`question_id`) REFERENCES `questions`(`id`) 
                    ON DELETE CASCADE
                """))
            except Exception as e:
                print(f"   ⚠ Aviso FK answers->questions: {e}")
        
        print()
        print("✅ Todas as tabelas criadas!")
        print()
        
        # Verificar tabelas
        print("🔍 Verificando resultado final...")
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT TABLE_NAME FROM information_schema.TABLES "
                f"WHERE TABLE_SCHEMA = '{MYSQL_DATABASE}' "
                "ORDER BY TABLE_NAME"
            ))
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ {len(tables)} tabelas criadas:")
            for table in tables:
                result2 = conn.execute(text(f"SELECT COUNT(*) FROM `{table}`"))
                count = result2.fetchone()[0]
                print(f"   - {table:20s} ({count} registros)")
        
        print()
        print("=" * 70)
        print("  🎉 SUCESSO! BANCO DE DADOS PRONTO!")
        print("=" * 70)
        print()
        print("📝 Próximos passos:")
        print()
        print("1. Inicie o backend:")
        print("   uvicorn app.main:app --reload")
        print()
        print("2. Acesse: http://localhost:8000/docs")
        print()
        print("3. Crie primeiro usuário:")
        print("   POST /api/auth/register")
        print('   {"email": "admin@adaptai.com", "password": "senha123", "full_name": "Admin"}')
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERRO:", str(e))
        print("=" * 70)
        import traceback
        print()
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = create_tables()
    exit(0 if success else 1)
