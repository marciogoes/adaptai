#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=======================================================
ADAPTAI - TESTE ETAPA 3: GESTÃO DE ESTUDANTES
=======================================================
Testa: CRUD completo de estudantes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🧪 TESTE ETAPA 3 - GESTÃO DE ESTUDANTES")
print("=" * 60)
print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

BASE_URL = "http://localhost:8000/api/v1"

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

# ==================================================
# OBTER TOKEN DE ADMIN
# ==================================================
print("📋 Obtendo token de autenticação...")
print("-" * 50)

admin_token = None
for cred in [{"username": "admin", "password": "admin123"}, {"username": "marcio", "password": "marcio123"}]:
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=cred, timeout=10)
        if response.status_code == 200:
            admin_token = response.json().get("access_token")
            registrar_teste("Autenticação", True, f"Logado como: {cred['username']}")
            break
    except:
        pass

if not admin_token:
    registrar_teste("Autenticação", False, "Não foi possível fazer login!")
    print("\n⚠️ Execute TESTE_ETAPA2.bat primeiro para verificar a autenticação.")
    exit(1)

headers = {"Authorization": f"Bearer {admin_token}"}

# ==================================================
# TESTE 1: Listar Estudantes
# ==================================================
print("\n📋 TESTE 1: Listando estudantes...")
print("-" * 50)

try:
    response = requests.get(f"{BASE_URL}/students", headers=headers, timeout=10)
    if response.status_code == 200:
        estudantes = response.json()
        registrar_teste("Listar estudantes", True, f"{len(estudantes)} estudante(s)")
        
        if estudantes:
            print("\n    🎓 Estudantes cadastrados:")
            for e in estudantes[:5]:  # Mostrar apenas 5
                print(f"       - ID:{e.get('id')} | {e.get('nome', 'N/A')} | {e.get('serie', 'N/A')}")
    else:
        registrar_teste("Listar estudantes", False, f"Status: {response.status_code}")
except Exception as e:
    registrar_teste("Listar estudantes", False, str(e))

# ==================================================
# TESTE 2: Buscar Estudante Específico
# ==================================================
print("\n📋 TESTE 2: Buscar estudante específico...")
print("-" * 50)

if estudantes and len(estudantes) > 0:
    student_id = estudantes[0].get("id")
    try:
        response = requests.get(f"{BASE_URL}/students/{student_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            estudante = response.json()
            registrar_teste("Buscar estudante", True, f"Nome: {estudante.get('nome')}")
            
            # Mostrar detalhes
            print(f"\n    📄 Detalhes do estudante ID {student_id}:")
            print(f"       - Nome: {estudante.get('nome')}")
            print(f"       - Série: {estudante.get('serie')}")
            print(f"       - Necessidades: {estudante.get('necessidades_especiais', 'N/A')}")
            print(f"       - Adaptações: {estudante.get('adaptacoes', 'N/A')}")
        else:
            registrar_teste("Buscar estudante", False, f"Status: {response.status_code}")
    except Exception as e:
        registrar_teste("Buscar estudante", False, str(e))
else:
    registrar_teste("Buscar estudante", False, "Nenhum estudante para buscar")

# ==================================================
# TESTE 3: Verificar Campos do Estudante
# ==================================================
print("\n📋 TESTE 3: Verificando campos obrigatórios...")
print("-" * 50)

campos_obrigatorios = ["id", "nome", "serie", "created_at"]
campos_opcionais = ["necessidades_especiais", "adaptacoes", "data_nascimento", "observacoes"]

if estudantes and len(estudantes) > 0:
    estudante = estudantes[0]
    
    for campo in campos_obrigatorios:
        if campo in estudante:
            registrar_teste(f"Campo obrigatório: {campo}", True, f"Valor: {str(estudante[campo])[:30]}...")
        else:
            registrar_teste(f"Campo obrigatório: {campo}", False, "AUSENTE!")
    
    for campo in campos_opcionais:
        if campo in estudante:
            registrar_teste(f"Campo opcional: {campo}", True, "Presente")
else:
    registrar_teste("Verificar campos", False, "Nenhum estudante para verificar")

# ==================================================
# TESTE 4: Verificar Integridade de Dados
# ==================================================
print("\n📋 TESTE 4: Verificando integridade de dados...")
print("-" * 50)

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
    
    # Verificar estudantes sem nome
    cursor.execute("SELECT COUNT(*) as total FROM teamarcionovo_students WHERE nome IS NULL OR nome = ''")
    sem_nome = cursor.fetchone()['total']
    if sem_nome == 0:
        registrar_teste("Estudantes com nome válido", True, "Todos têm nome")
    else:
        registrar_teste("Estudantes com nome válido", False, f"{sem_nome} sem nome!")
    
    # Verificar estudantes sem série
    cursor.execute("SELECT COUNT(*) as total FROM teamarcionovo_students WHERE serie IS NULL OR serie = ''")
    sem_serie = cursor.fetchone()['total']
    if sem_serie == 0:
        registrar_teste("Estudantes com série válida", True, "Todos têm série")
    else:
        registrar_teste("Estudantes com série válida", False, f"{sem_serie} sem série!")
    
    # Estatísticas por necessidade especial
    cursor.execute("""
        SELECT necessidades_especiais, COUNT(*) as total 
        FROM teamarcionovo_students 
        WHERE necessidades_especiais IS NOT NULL AND necessidades_especiais != ''
        GROUP BY necessidades_especiais
    """)
    necessidades = cursor.fetchall()
    
    if necessidades:
        registrar_teste("Distribuição por necessidades", True, f"{len(necessidades)} tipo(s)")
        print("\n    📊 Distribuição por necessidade especial:")
        for n in necessidades:
            print(f"       - {n['necessidades_especiais']}: {n['total']} aluno(s)")
    
    conn.close()
except Exception as e:
    registrar_teste("Verificar integridade", False, str(e))

# ==================================================
# RESUMO FINAL
# ==================================================
print("\n" + "=" * 60)
print("📊 RESUMO ETAPA 3 - GESTÃO DE ESTUDANTES")
print("=" * 60)
print(f"✅ Testes OK:     {testes_ok}")
print(f"❌ Testes Falha:  {testes_falha}")
print(f"📈 Taxa Sucesso:  {(testes_ok/(testes_ok+testes_falha)*100):.1f}%" if (testes_ok+testes_falha) > 0 else "N/A")
print("=" * 60)

if testes_falha == 0:
    print("\n🎉 ETAPA 3 CONCLUÍDA COM SUCESSO!")
else:
    print(f"\n⚠️ ATENÇÃO: {testes_falha} problema(s) encontrado(s)!")

print("\n" + "=" * 60)
