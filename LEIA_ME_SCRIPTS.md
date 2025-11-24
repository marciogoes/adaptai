# 🚀 Scripts de Inicialização - AdaptAI Backend

## 📋 Scripts Disponíveis

### 1️⃣ **RECRIAR_VENV_E_INICIAR.bat** ⭐ (PRINCIPAL)
Script completo que:
- ✅ Remove o venv antigo (Python 3.14)
- ✅ Cria novo venv com Python 3.12
- ✅ Instala todas as dependências
- ✅ Inicia o servidor automaticamente

**Quando usar:** 
- Primeira vez configurando o projeto
- Quando houver problemas com o ambiente virtual
- Após atualizar Python

**Como usar:**
```
1. Clique duas vezes em: RECRIAR_VENV_E_INICIAR.bat
2. Aguarde (pode levar 2-3 minutos)
3. Pronto! Servidor iniciado!
```

---

### 2️⃣ **RECRIAR_VENV_E_INICIAR.ps1** (PowerShell)
Mesma função que o .bat, mas em PowerShell (mais moderno).

**Como usar:**
```
1. Clique com botão direito em: RECRIAR_VENV_E_INICIAR.ps1
2. Selecione "Executar com PowerShell"
3. Se der erro de permissão, abra PowerShell como Admin e execute:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 3️⃣ **INICIAR_BACKEND.bat** (Rápido)
Script simples para iniciar o servidor quando o venv já está configurado.

**Quando usar:**
- Depois que você já usou o RECRIAR_VENV_E_INICIAR.bat
- No dia a dia para iniciar o servidor rapidamente

**Como usar:**
```
1. Clique duas vezes em: INICIAR_BACKEND.bat
2. Servidor inicia imediatamente!
```

---

## 🎯 Fluxo Recomendado

### **PRIMEIRA VEZ:**
```
1. Execute: RECRIAR_VENV_E_INICIAR.bat
2. Aguarde instalação completa
3. Servidor inicia automaticamente
4. Acesse: http://localhost:8000/docs
```

### **PRÓXIMAS VEZES:**
```
1. Execute: INICIAR_BACKEND.bat
2. Servidor inicia rapidamente
3. Acesse: http://localhost:8000/docs
```

### **SE DER PROBLEMA:**
```
1. Execute novamente: RECRIAR_VENV_E_INICIAR.bat
2. Isso vai recriar todo o ambiente
```

---

## 📊 O Que Cada Script Faz

### RECRIAR_VENV_E_INICIAR.bat
```
[1/8] ✅ Verifica Python 3.12
[2/8] ✅ Desativa venv antigo
[3/8] ✅ Remove venv antigo
[4/8] ✅ Cria novo venv
[5/8] ✅ Ativa venv
[6/8] ✅ Atualiza pip
[7/8] ✅ Instala dependências:
      - fastapi
      - uvicorn
      - sqlalchemy
      - pymysql
      - python-dotenv
      - python-jose
      - passlib
      - python-multipart
      - anthropic (IA)
      - pydantic
[8/8] ✅ Verifica instalação
[...] 🚀 Inicia servidor
```

---

## 🆘 Troubleshooting

### ❌ Erro: "Python 3.12 não encontrado"
**Solução:** Instale Python 3.12 de https://www.python.org/downloads/

### ❌ Erro: "Ambiente virtual não encontrado"
**Solução:** Execute primeiro: `RECRIAR_VENV_E_INICIAR.bat`

### ❌ Erro: "pip install falhou"
**Solução:** 
1. Verifique sua conexão com internet
2. Execute novamente o script

### ❌ Erro PowerShell: "não pode ser carregado"
**Solução:** 
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 Dependências Instaladas

```
fastapi              → Framework web
uvicorn              → Servidor ASGI
sqlalchemy           → ORM para banco de dados
pymysql              → Driver MySQL
python-dotenv        → Variáveis de ambiente
python-jose          → JWT para autenticação
passlib              → Hash de senhas
python-multipart     → Upload de arquivos
anthropic            → API Claude (IA)
pydantic             → Validação de dados
```

---

## 🎉 Resultado Esperado

Quando tudo funcionar, você verá:

```
============================================================
🎓 AdaptAI Backend Starting...
📌 Version: 1.0.0
🐍 Python: 3.12.x
🗄️  Database: MySQL 8.0 DBaaS
🤖 AI Model: claude-sonnet-4-20250514
✨ Novo: Sistema de Provas com IA ativado!
============================================================

INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## 🔗 Links Úteis

- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000 (execute separadamente)

---

## 💡 Dicas

1. ✅ **Use sempre Python 3.12** (não 3.14)
2. ✅ **Execute scripts clicando duas vezes** (mais fácil)
3. ✅ **Primeira vez:** Use `RECRIAR_VENV_E_INICIAR.bat`
4. ✅ **Próximas vezes:** Use `INICIAR_BACKEND.bat`
5. ✅ **Mantenha o terminal aberto** enquanto usa o sistema

---

## 🎯 Próximo Passo

Depois de iniciar o backend:
1. ✅ Acesse: http://localhost:8000/docs
2. ✅ Teste os endpoints
3. ✅ Inicie o frontend (em outro terminal)
4. ✅ Comece a usar o AdaptAI!

---

**Feito com ❤️ pelo AdaptAI Team**
