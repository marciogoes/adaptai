"""
Script para resetar a senha e corrigir o role do Super Admin do AdaptAI
Execute na pasta backend: venv\Scripts\python.exe resetar_superadmin.py
"""

import bcrypt
import pymysql

# Configurações do banco
DB_CONFIG = {
    "host": "teamarcionovo.mysql.dbaas.com.br",
    "port": 3306,
    "user": "teamarcionovo",
    "password": "MarcioGo1003@@",
    "database": "teamarcionovo",
    "charset": "utf8mb4",
}

NOVA_SENHA = "admin123"
EMAIL_ADMIN = "admin@adaptai.com.br"
ROLE_CORRETO = "admin"


def resetar_senha():
    print("=" * 60)
    print("🔐 RESET DE SENHA + ROLE - SUPER ADMIN AdaptAI")
    print("=" * 60)

    # Gerar hash da nova senha
    senha_bytes = NOVA_SENHA.encode("utf-8")
    salt = bcrypt.gensalt()
    novo_hash = bcrypt.hashpw(senha_bytes, salt).decode("utf-8")

    print(f"\n📧 Email: {EMAIL_ADMIN}")
    print(f"🔑 Nova senha: {NOVA_SENHA}")
    print(f"👤 Role: {ROLE_CORRETO}")

    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Verifica o usuário atual
        cursor.execute(
            "SELECT id, name, email, role FROM users WHERE email = %s", (EMAIL_ADMIN,)
        )
        user = cursor.fetchone()

        if not user:
            print(f"\n❌ Usuário '{EMAIL_ADMIN}' NÃO encontrado!")
            print("\n📋 Usuários admin existentes no banco:")
            cursor.execute(
                "SELECT id, name, email, role FROM users WHERE role IN ('admin', 'super_admin', '') LIMIT 10"
            )
            admins = cursor.fetchall()
            for a in admins:
                print(f"   ID {a[0]}: {a[2]} | role='{a[3]}'")
        else:
            print(f"\n✅ Usuário encontrado: {user[1]} (ID: {user[0]})")
            print(f"   Role atual: '{user[3]}' → será corrigido para '{ROLE_CORRETO}'")

            # Atualiza senha E role
            cursor.execute(
                "UPDATE users SET hashed_password = %s, role = %s WHERE email = %s",
                (novo_hash, ROLE_CORRETO, EMAIL_ADMIN),
            )
            conn.commit()

            # Confirma no banco
            cursor.execute(
                "SELECT id, name, email, role FROM users WHERE email = %s", (EMAIL_ADMIN,)
            )
            updated = cursor.fetchone()

            print(f"\n✅ ATUALIZADO COM SUCESSO!")
            print(f"   Role agora: '{updated[3]}'")
            print("\n" + "=" * 60)
            print("🎉 Faça login com:")
            print(f"   Email: {EMAIL_ADMIN}")
            print(f"   Senha: {NOVA_SENHA}")
            print("=" * 60)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique se os módulos estão instalados:")
        print("   pip install pymysql bcrypt")


if __name__ == "__main__":
    resetar_senha()
