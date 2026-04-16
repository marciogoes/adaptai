"""
Script para listar todos os usuários cadastrados no banco do AdaptAI
Execute na pasta backend: venv\Scripts\python.exe listar_usuarios.py
"""

import pymysql

DB_CONFIG = {
    "host": "teamarcionovo.mysql.dbaas.com.br",
    "port": 3306,
    "user": "teamarcionovo",
    "password": "MarcioGo1003@@",
    "database": "teamarcionovo",
    "charset": "utf8mb4",
}

def listar_usuarios():
    print("=" * 70)
    print("👥 USUÁRIOS CADASTRADOS - AdaptAI")
    print("=" * 70)

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, role, is_active
            FROM users
            ORDER BY role, name
        """)
        users = cursor.fetchall()

        if not users:
            print("\n❌ Nenhum usuário encontrado!")
        else:
            print(f"\n{'ID':<5} {'Nome':<30} {'Email':<45} {'Role':<15} {'Ativo'}")
            print("-" * 100)
            for u in users:
                ativo = "✅" if u[4] else "❌"
                print(f"{u[0]:<5} {u[1]:<30} {u[2]:<45} {u[3]:<15} {ativo}")

        print(f"\nTotal: {len(users)} usuário(s)")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ ERRO: {e}")

if __name__ == "__main__":
    listar_usuarios()
