#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=======================================================
ADAPTAI - TESTE ETAPA 2: AUTENTICAÇÃO
=======================================================
Testa: Login Admin, Login Estudante, JWT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🧪 TESTE ETAPA 2 - AUTENTICAÇÃO")
print("=" * 60)
print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# Configuração - altere se necessário
BASE_URL = "http://localhost:8000/api/v1"

# Contadores
testes_ok = 0
testes_falha = 0

def registrar_teste(nome, sucesso, mensagem=""):
    global testes_ok, testes_falha
    if sucesso:
        testes_ok += 1
        status = "✅ PASSOU"
    else:
        testes_falha += 1
        status = "❌ FALHOU"
    print(f"{status} - {nome}")
    if mensagem:
        print(f"        └─ {mensagem}")

def testar_endpoint(url, timeout=10):
    """Testa se um endpoint está acessível"""
    try:
        response = requests.get(url, timeout=timeout)
        return True, response.status_code
    except requests.exceptions.ConnectionError:
        return False, "Conexão recusada"
    except Exception as e:
        return False, str(e)

# ==================================================
# TESTE 1: Backend Acessível
# ==================================================
print("📋 TESTE 1: Verificando se backend está rodando...")
print("-" * 50)

sucesso, status = testar_endpoint("http://localhost:8000/health")
if sucesso:
    registrar_teste("Backend acessível", True, f"Status: {status}")
else:
    registrar_teste("Backend acessível", False, f"Erro: {status}")
    print("\n⚠️ IMPORTANTE: O backend precisa estar rodando!")
    print("   Execute: INICIAR_BACKEND.bat ou python -m uvicorn app.main:app --reload")
    print("\n" + "=" * 60)
    exit(1)

# ==================================================
# TESTE 2: Login de Administrador
# ==================================================
print("\n📋 TESTE 2: Testando login de administrador...")
print("-" * 50)

# Credenciais de teste (ajuste conforme seu sistema)
admin_credentials = [
    {"username": "admin", "password": "admin123"},
    {"username": "marcio", "password": "marcio123"},
]

admin_token = None
for cred in admin_credentials:
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": cred["username"], "password": cred["password"]},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            admin_token = data.get("access_token")
            registrar_teste(f"Login admin ({cred['username']})", True, "Token JWT recebido")
            break
        else:
            registrar_teste(f"Login admin ({cred['username']})", False, f"Status: {response.status_code}")
    except Exception as e:
        registrar_teste(f"Login admin ({cred['username']})", False, str(e))

if not admin_token:
    print("\n⚠️ Nenhum login de admin funcionou!")
    print("   Verifique as credenciais no banco de dados.")

# ==================================================
# TESTE 3: Validar Token JWT
# ==================================================
if admin_token:
    print("\n📋 TESTE 3: Validando token JWT...")
    print("-" * 50)
    
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            user_data = response.json()
            registrar_teste("Validar token JWT", True, f"Usuário: {user_data.get('username', 'N/A')}")
        else:
            registrar_teste("Validar token JWT", False, f"Status: {response.status_code}")
    except Exception as e:
        registrar_teste("Validar token JWT", False, str(e))

# ==================================================
# TESTE 4: Acesso a Endpoints Protegidos
# ==================================================
if admin_token:
    print("\n📋 TESTE 4: Testando endpoints protegidos...")
    print("-" * 50)
    
    endpoints_protegidos = [
        "/students",
        "/provas",
        "/materiais",
    ]
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    for endpoint in endpoints_protegidos:
        try:
            response = requests.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else "OK"
                registrar_teste(f"Endpoint {endpoint}", True, f"Resposta: {count}")
            else:
                registrar_teste(f"Endpoint {endpoint}", False, f"Status: {response.status_code}")
        except Exception as e:
            registrar_teste(f"Endpoint {endpoint}", False, str(e))

# ==================================================
# TESTE 5: Login de Estudante (se houver)
# ==================================================
print("\n📋 TESTE 5: Testando login de estudante...")
print("-" * 50)

# Buscar estudantes do banco para tentar login
try:
    import mysql.connector
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nome, login_username 
        FROM teamarcionovo_students 
        WHERE login_username IS NOT NULL 
        LIMIT 1
    """)
    estudante = cursor.fetchone()
    
    if estudante and estudante.get("login_username"):
        # Tentar login do estudante
        try:
            response = requests.post(
                f"{BASE_URL}/auth/student-login",
                data={
                    "username": estudante["login_username"],
                    "password": "123456"  # senha padrão
                },
                timeout=10
            )
            if response.status_code == 200:
                registrar_teste(f"Login estudante ({estudante['nome']})", True, "OK")
            else:
                registrar_teste(f"Login estudante ({estudante['nome']})", False, f"Status: {response.status_code}")
        except Exception as e:
            registrar_teste("Login estudante", False, str(e))
    else:
        registrar_teste("Login estudante", False, "Nenhum estudante com login configurado")
    
    conn.close()
except Exception as e:
    registrar_teste("Login estudante", False, f"Erro ao buscar estudantes: {e}")

# ==================================================
# RESUMO FINAL
# ==================================================
print("\n" + "=" * 60)
print("📊 RESUMO ETAPA 2 - AUTENTICAÇÃO")
print("=" * 60)
print(f"✅ Testes OK:     {testes_ok}")
print(f"❌ Testes Falha:  {testes_falha}")
print(f"📈 Taxa Sucesso:  {(testes_ok/(testes_ok+testes_falha)*100):.1f}%" if (testes_ok+testes_falha) > 0 else "N/A")
print("=" * 60)

if testes_falha == 0:
    print("\n🎉 ETAPA 2 CONCLUÍDA COM SUCESSO!")
else:
    print(f"\n⚠️ ATENÇÃO: {testes_falha} problema(s) encontrado(s)!")

print("\n" + "=" * 60)
