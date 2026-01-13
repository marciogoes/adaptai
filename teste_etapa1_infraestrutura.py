#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=======================================================
ADAPTAI - TESTE ETAPA 1: INFRAESTRUTURA BÁSICA
=======================================================
Testa: Banco de dados, tabelas, configurações
"""

import sys
import os

# Adicionar path do app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

print("=" * 60)
print("🧪 TESTE ETAPA 1 - INFRAESTRUTURA ADAPTAI")
print("=" * 60)
print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print()

# Contadores
testes_ok = 0
testes_falha = 0
resultados = []

def registrar_teste(nome, sucesso, mensagem=""):
    global testes_ok, testes_falha
    if sucesso:
        testes_ok += 1
        status = "✅ PASSOU"
    else:
        testes_falha += 1
        status = "❌ FALHOU"
    resultados.append({
        "nome": nome,
        "sucesso": sucesso,
        "status": status,
        "mensagem": mensagem
    })
    print(f"{status} - {nome}")
    if mensagem:
        print(f"        └─ {mensagem}")

# ==================================================
# TESTE 1: Variáveis de Ambiente
# ==================================================
print("\n📋 TESTE 1: Verificando variáveis de ambiente...")
print("-" * 50)

variaveis_obrigatorias = [
    "MYSQL_HOST", "MYSQL_PORT", "MYSQL_USER", 
    "MYSQL_PASSWORD", "MYSQL_DATABASE",
    "SECRET_KEY", "ANTHROPIC_API_KEY"
]

for var in variaveis_obrigatorias:
    valor = os.getenv(var)
    if valor:
        # Mascarar valores sensíveis
        if "KEY" in var or "PASSWORD" in var:
            valor_display = valor[:8] + "..." if len(valor) > 8 else "***"
        else:
            valor_display = valor
        registrar_teste(f"ENV: {var}", True, f"Valor: {valor_display}")
    else:
        registrar_teste(f"ENV: {var}", False, "Variável não encontrada!")

# ==================================================
# TESTE 2: Conexão com MySQL
# ==================================================
print("\n📋 TESTE 2: Testando conexão MySQL...")
print("-" * 50)

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        connect_timeout=10
    )
    registrar_teste("Conexão MySQL", True, f"Host: {os.getenv('MYSQL_HOST')}")
    
    cursor = conn.cursor()
    
    # Testar versão do MySQL
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    registrar_teste("Versão MySQL", True, f"Versão: {version}")
    
except Exception as e:
    registrar_teste("Conexão MySQL", False, str(e))
    conn = None

# ==================================================
# TESTE 3: Verificar Tabelas do Sistema
# ==================================================
if conn:
    print("\n📋 TESTE 3: Verificando tabelas do banco...")
    print("-" * 50)
    
    tabelas_esperadas = [
        "teamarcionovo_users",
        "teamarcionovo_students", 
        "teamarcionovo_provas",
        "teamarcionovo_questoes_prova",
        "teamarcionovo_materiais_estudo",
        "teamarcionovo_pei",
        "teamarcionovo_relatorios",
        "teamarcionovo_bncc_habilidades",
        "teamarcionovo_calendario_atividades",
        "teamarcionovo_planos"
    ]
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tabelas_existentes = [t[0] for t in cursor.fetchall()]
        
        registrar_teste("Total de tabelas", True, f"Encontradas: {len(tabelas_existentes)} tabelas")
        
        # Verificar tabelas críticas
        for tabela in tabelas_esperadas:
            if tabela in tabelas_existentes:
                # Contar registros
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                    count = cursor.fetchone()[0]
                    registrar_teste(f"Tabela: {tabela}", True, f"{count} registros")
                except Exception as e:
                    registrar_teste(f"Tabela: {tabela}", True, "Existe (erro ao contar)")
            else:
                registrar_teste(f"Tabela: {tabela}", False, "NÃO ENCONTRADA!")
        
    except Exception as e:
        registrar_teste("Verificar tabelas", False, str(e))

# ==================================================
# TESTE 4: Verificar Usuários Cadastrados
# ==================================================
if conn:
    print("\n📋 TESTE 4: Verificando usuários do sistema...")
    print("-" * 50)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, email, role, is_active 
            FROM teamarcionovo_users 
            LIMIT 10
        """)
        usuarios = cursor.fetchall()
        
        if usuarios:
            registrar_teste("Usuários cadastrados", True, f"{len(usuarios)} usuário(s) encontrado(s)")
            print("\n    👥 Usuários:")
            for u in usuarios:
                status = "🟢 Ativo" if u.get('is_active', True) else "🔴 Inativo"
                print(f"       - {u['username']} ({u['role']}) {status}")
        else:
            registrar_teste("Usuários cadastrados", False, "Nenhum usuário encontrado!")
            
    except Exception as e:
        registrar_teste("Verificar usuários", False, str(e))

# ==================================================
# TESTE 5: Verificar Estudantes
# ==================================================
if conn:
    print("\n📋 TESTE 5: Verificando estudantes cadastrados...")
    print("-" * 50)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nome, serie, necessidades_especiais, created_at
            FROM teamarcionovo_students 
            LIMIT 10
        """)
        estudantes = cursor.fetchall()
        
        if estudantes:
            registrar_teste("Estudantes cadastrados", True, f"{len(estudantes)} estudante(s)")
            print("\n    🎓 Estudantes:")
            for e in estudantes:
                print(f"       - {e['nome']} ({e['serie']}) - {e.get('necessidades_especiais', 'N/A')}")
        else:
            registrar_teste("Estudantes cadastrados", False, "Nenhum estudante encontrado!")
            
    except Exception as e:
        registrar_teste("Verificar estudantes", False, str(e))

# ==================================================
# TESTE 6: Verificar Configuração Claude API
# ==================================================
print("\n📋 TESTE 6: Verificando Claude API...")
print("-" * 50)

api_key = os.getenv("ANTHROPIC_API_KEY")
claude_model = os.getenv("CLAUDE_MODEL")

if api_key and api_key.startswith("sk-ant-"):
    registrar_teste("API Key Anthropic", True, "Formato correto (sk-ant-...)")
else:
    registrar_teste("API Key Anthropic", False, "Key inválida ou não configurada!")

if claude_model:
    registrar_teste("Modelo Claude", True, f"Modelo: {claude_model}")
else:
    registrar_teste("Modelo Claude", False, "Modelo não configurado!")

# ==================================================
# TESTE 7: Verificar Integridade das Tabelas Principais
# ==================================================
if conn:
    print("\n📋 TESTE 7: Verificando integridade de dados...")
    print("-" * 50)
    
    try:
        cursor = conn.cursor()
        
        # Verificar provas
        cursor.execute("SELECT COUNT(*) FROM teamarcionovo_provas")
        provas = cursor.fetchone()[0]
        registrar_teste("Provas no sistema", True, f"{provas} prova(s)")
        
        # Verificar materiais
        cursor.execute("SELECT COUNT(*) FROM teamarcionovo_materiais_estudo")
        materiais = cursor.fetchone()[0]
        registrar_teste("Materiais de estudo", True, f"{materiais} material(is)")
        
        # Verificar PEIs
        cursor.execute("SELECT COUNT(*) FROM teamarcionovo_pei")
        peis = cursor.fetchone()[0]
        registrar_teste("PEIs cadastrados", True, f"{peis} PEI(s)")
        
        # Verificar relatórios
        cursor.execute("SELECT COUNT(*) FROM teamarcionovo_relatorios")
        relatorios = cursor.fetchone()[0]
        registrar_teste("Relatórios", True, f"{relatorios} relatório(s)")
        
    except Exception as e:
        registrar_teste("Integridade de dados", False, str(e))

# Fechar conexão
if conn:
    conn.close()

# ==================================================
# RESUMO FINAL
# ==================================================
print("\n" + "=" * 60)
print("📊 RESUMO ETAPA 1 - INFRAESTRUTURA")
print("=" * 60)
print(f"✅ Testes OK:     {testes_ok}")
print(f"❌ Testes Falha:  {testes_falha}")
print(f"📈 Taxa Sucesso:  {(testes_ok/(testes_ok+testes_falha)*100):.1f}%")
print("=" * 60)

if testes_falha == 0:
    print("\n🎉 ETAPA 1 CONCLUÍDA COM SUCESSO!")
    print("   Infraestrutura OK - Pronto para próximos testes.")
else:
    print(f"\n⚠️ ATENÇÃO: {testes_falha} problema(s) encontrado(s)!")
    print("   Corrija os itens marcados com ❌ antes de prosseguir.")

print("\n" + "=" * 60)
