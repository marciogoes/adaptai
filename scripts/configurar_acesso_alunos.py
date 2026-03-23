#!/usr/bin/env python3
"""
Script para criar usuários de acesso para os alunos:
- Marcio (aluno)
- Cassio (aluno)  
- Enrico (aluno)

E vincular a professora Debora Santana como responsável
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import bcrypt

# Credenciais do MySQL
MYSQL_HOST = "teamarcionovo.mysql.dbaas.com.br"
MYSQL_PORT = 3306
MYSQL_USER = "teamarcionovo"
MYSQL_PASSWORD = "MarcioGo1003@@"
MYSQL_DATABASE = "teamarcionovo"

# Criar URL de conexão
encoded_password = quote_plus(MYSQL_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

def get_password_hash(password: str) -> str:
    """Gera hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def main():
    print("=" * 70)
    print("  ADAPTAI - Configurar Acesso dos Alunos")
    print("=" * 70)
    print()
    
    try:
        # Criar engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
        
        # Testar conexão
        print("🔍 Conectando ao banco de dados...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ Conectado! MySQL Version: {version}")
        
        print()
        print("-" * 70)
        print("PASSO 1: Listando alunos existentes (tabela students)")
        print("-" * 70)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, email, grade_level, created_by_user_id, escola_id, is_active
                FROM students 
                ORDER BY name
            """))
            students = result.fetchall()
            
            print(f"\n📋 {len(students)} alunos encontrados:\n")
            for s in students:
                print(f"   ID: {s[0]:3} | Nome: {s[1]:25} | Email: {s[2] or 'N/A':30} | Série: {s[3]:15} | Prof ID: {s[4]} | Escola: {s[5]} | Ativo: {s[6]}")
        
        print()
        print("-" * 70)
        print("PASSO 2: Obtendo ID da professora Debora Santana")
        print("-" * 70)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, email FROM users 
                WHERE name = 'Debora Santana'
            """))
            debora = result.fetchone()
            
            if debora:
                debora_id = debora[0]
                print(f"\n✅ Professora encontrada:")
                print(f"   ID: {debora[0]}")
                print(f"   Nome: {debora[1]}")
                print(f"   Email: {debora[2]}")
            else:
                print("\n⚠️  Professora Debora Santana não encontrada!")
                debora_id = None
        
        print()
        print("-" * 70)
        print("PASSO 3: Configurando acesso dos alunos")
        print("-" * 70)
        
        # Senha padrão para alunos
        senha_aluno = "Aluno@2024"
        hashed_password = get_password_hash(senha_aluno)
        
        # Lista de alunos para configurar
        alunos_config = [
            {"nome_busca": "Marcio", "email": "marcio.aluno@adaptai.com"},
            {"nome_busca": "Cassio", "email": "cassio.aluno@adaptai.com"},
            {"nome_busca": "Enrico", "email": "enrico.aluno@adaptai.com"},
        ]
        
        with engine.begin() as conn:
            for aluno in alunos_config:
                # Buscar aluno pelo nome (case insensitive para pegar variações)
                result = conn.execute(text("""
                    SELECT id, name, email FROM students 
                    WHERE name LIKE :nome
                """), {"nome": f"%{aluno['nome_busca']}%"})
                
                student = result.fetchone()
                
                if student:
                    print(f"\n📝 Configurando aluno: {student[1]} (ID: {student[0]})")
                    
                    # Atualizar email, senha e professor responsável
                    update_params = {
                        "email": aluno["email"],
                        "hashed_password": hashed_password,
                        "is_active": 1,
                        "student_id": student[0]
                    }
                    
                    if debora_id:
                        update_params["created_by_user_id"] = debora_id
                        conn.execute(text("""
                            UPDATE students 
                            SET email = :email,
                                hashed_password = :hashed_password,
                                is_active = :is_active,
                                created_by_user_id = :created_by_user_id
                            WHERE id = :student_id
                        """), update_params)
                    else:
                        conn.execute(text("""
                            UPDATE students 
                            SET email = :email,
                                hashed_password = :hashed_password,
                                is_active = :is_active
                            WHERE id = :student_id
                        """), update_params)
                    
                    print(f"   ✅ Email: {aluno['email']}")
                    print(f"   ✅ Senha: {senha_aluno}")
                    if debora_id:
                        print(f"   ✅ Professora: Debora Santana (ID: {debora_id})")
                else:
                    print(f"\n⚠️  Aluno '{aluno['nome_busca']}' não encontrado na tabela students")
        
        print()
        print("-" * 70)
        print("RESULTADO FINAL: Lista de alunos atualizada")
        print("-" * 70)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT s.id, s.name, s.email, s.grade_level, s.is_active,
                       u.name as professor_nome
                FROM students s
                LEFT JOIN users u ON s.created_by_user_id = u.id
                ORDER BY s.name
            """))
            students = result.fetchall()
            
            print(f"\n📋 {len(students)} alunos no sistema:\n")
            for s in students:
                print(f"   ID: {s[0]:3} | Nome: {s[1]:25} | Email: {s[2] or 'N/A':30} | Série: {s[3]:15} | Ativo: {s[4]} | Professor: {s[5] or 'N/A'}")
        
        print()
        print("=" * 70)
        print("  CREDENCIAIS DE ACESSO DOS ALUNOS")
        print("=" * 70)
        print()
        print("  📧 Marcio:")
        print("     Email: marcio.aluno@adaptai.com")
        print("     Senha: Aluno@2024")
        print()
        print("  📧 Cassio:")
        print("     Email: cassio.aluno@adaptai.com")
        print("     Senha: Aluno@2024")
        print()
        print("  📧 Enrico:")
        print("     Email: enrico.aluno@adaptai.com")
        print("     Senha: Aluno@2024")
        print()
        print("  👩‍🏫 Professora responsável: Debora Santana")
        print()
        print("=" * 70)
        print("  🎉 OPERAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
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
    success = main()
    exit(0 if success else 1)
