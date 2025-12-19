# 🔧 INSTALAÇÃO MANUAL - PASSO A PASSO

Se os scripts não funcionarem, siga estas instruções manualmente:

## ⚠️ IMPORTANTE

Abra o **CMD** ou **PowerShell** como ADMINISTRADOR

---

## 📋 PASSO A PASSO

### 1️⃣ Navegue até a pasta backend:

```bash
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
```

### 2️⃣ Verifique se tem Python 3.12:

```bash
py -3.12 --version
```

**Deve mostrar:** `Python 3.12.x`

Se não tiver, baixe em: https://www.python.org/downloads/

---

### 3️⃣ Remova o venv antigo:

```bash
rmdir /s venv
```

Quando perguntar, digite `S` e Enter.

---

### 4️⃣ Crie novo venv com Python 3.12:

```bash
py -3.12 -m venv venv
```

**Aguarde:** ~10 segundos

---

### 5️⃣ Ative o venv:

```bash
venv\Scripts\activate
```

Deve aparecer `(venv)` no início da linha.

---

### 6️⃣ Atualize o pip:

```bash
python -m pip install --upgrade pip
```

---

### 7️⃣ Instale as dependências (UMA POR VEZ):

```bash
pip install fastapi
```

```bash
pip install uvicorn
```

```bash
pip install sqlalchemy
```

```bash
pip install pymysql
```

```bash
pip install python-dotenv
```

```bash
pip install "python-jose[cryptography]"
```

```bash
pip install "passlib[bcrypt]"
```

```bash
pip install python-multipart
```

```bash
pip install anthropic
```

```bash
pip install pydantic pydantic-settings
```

**Aguarde:** Cada comando leva ~10-30 segundos

---

### 8️⃣ Verifique a instalação:

```bash
python --version
```

Deve mostrar: `Python 3.12.x`

```bash
pip list
```

Deve listar todas as bibliotecas instaladas.

---

### 9️⃣ Inicie o servidor:

```bash
uvicorn app.main:app --reload
```

---

## ✅ RESULTADO ESPERADO

Você deve ver:

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

## 🌐 Teste o Backend

Abra no navegador:
```
http://localhost:8000/docs
```

---

## 🆘 SE DER ERRO

### Erro: "py não é reconhecido"

Tente:
```bash
python -m venv venv
```

### Erro: "pip install falhou"

Tente com --user:
```bash
pip install --user nome-do-pacote
```

### Erro: "Permission denied"

Execute o CMD/PowerShell como **Administrador**

---

## 💾 ARQUIVO PARA SALVAR COMANDOS

Crie um arquivo `instalar.txt` com todos os comandos:

```
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
rmdir /s venv
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
pip install "python-jose[cryptography]" "passlib[bcrypt]"
pip install python-multipart anthropic pydantic pydantic-settings
uvicorn app.main:app --reload
```

E copie/cole linha por linha no terminal.

---

## 📝 PRÓXIMOS PASSOS

Depois do backend funcionando:

1. ✅ Teste: http://localhost:8000/docs
2. ✅ Inicie o frontend em outro terminal
3. ✅ Acesse: http://localhost:3000

---

**Se continuar com problemas, me envie o ERRO COMPLETO que aparece!**
