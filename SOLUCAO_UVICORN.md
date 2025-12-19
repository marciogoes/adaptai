# 🔧 SOLUÇÃO - Uvicorn não reconhecido

## ❌ O Problema

```
'uvicorn' não é reconhecido como um comando interno
ou externo, um programa operável ou um arquivo em lotes.
```

## 🎯 Causa

O **ambiente virtual (venv)** não está ativado ou o **uvicorn não está instalado**.

---

## ✅ SOLUÇÕES

### 🚀 Opção 1 - Script Automático (MAIS FÁCIL)

**Duplo clique em:**
```
RESOLVER_RAPIDO.bat
```

**Isso vai:**
- ✅ Criar o venv (se não existir)
- ✅ Ativar o venv
- ✅ Instalar todas as dependências
- ✅ Iniciar o servidor

**Tempo:** ~2 minutos

---

### 🔧 Opção 2 - Script com Diagnóstico

**1. Execute primeiro:**
```
CORRIGIR_UVICORN.bat
```

**2. Depois execute:**
```
INICIAR_BACKEND_CORRIGIDO.bat
```

**Vantagens:**
- Mostra cada passo
- Diagnóstico completo
- Feedback detalhado

---

### 💻 Opção 3 - Manual (Linha por Linha)

**Abra o terminal nesta pasta e execute:**

```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install uvicorn fastapi sqlalchemy pymysql cryptography python-jose passlib bcrypt email-validator python-multipart anthropic
uvicorn app.main:app --reload
```

---

## 🎓 Entendendo o Problema

### O que é venv?

**Ambiente virtual** é uma pasta isolada onde ficam as bibliotecas Python do projeto.

**Por que usar?**
- ✅ Evita conflitos entre projetos
- ✅ Cada projeto tem suas próprias versões
- ✅ Não polui o Python global

### Como funciona?

```
Sem venv ativado:
  python → C:\Python312\python.exe
  uvicorn → ❌ Não encontrado

Com venv ativado:
  python → C:\...\backend\venv\Scripts\python.exe
  uvicorn → ✅ C:\...\backend\venv\Scripts\uvicorn.exe
```

### Como saber se está ativo?

No terminal você verá:
```cmd
(venv) C:\...\backend>
```

O `(venv)` indica que está ativo! ✅

---

## ✅ Verificar se Funcionou

Após executar qualquer solução, você deve ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using StatReload
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Acesse no navegador:**
- http://localhost:8000
- http://localhost:8000/docs

---

## 🆘 Problemas Comuns

### "python não reconhecido"

**Solução:**
```cmd
py -3.12 -m venv venv
```

### "activate.bat não funciona"

**Solução:**
Execute o CMD como **Administrador**

### "Permission denied"

**Solução:**
- Clique direito no script
- "Executar como administrador"

### "ModuleNotFoundError: No module named 'app'"

**Causa:** Você não está na pasta backend

**Solução:**
```cmd
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
```

---

## 📋 Checklist

Antes de iniciar:

- [ ] Python 3.12 instalado
- [ ] Está na pasta `backend`
- [ ] Arquivo `.env` existe
- [ ] Internet funcionando

Após iniciar:

- [ ] Backend rodando (http://localhost:8000)
- [ ] Ver "Application startup complete"
- [ ] Consegue acessar /docs

---

## 🎯 Resumo Rápido

| Problema | Causa | Solução |
|----------|-------|---------|
| Uvicorn não reconhecido | venv não ativado | Execute `RESOLVER_RAPIDO.bat` |
| Python não reconhecido | Python não instalado | Instale Python 3.12 |
| Permission denied | Sem privilégios | Execute como Admin |

---

## 📁 Arquivos Criados

Estão nesta pasta:

- ✅ `RESOLVER_RAPIDO.bat` - Solução rápida
- ✅ `CORRIGIR_UVICORN.bat` - Com diagnóstico
- ✅ `INICIAR_BACKEND_CORRIGIDO.bat` - Apenas inicia
- ✅ `COMO_RESOLVER_UVICORN.txt` - Guia visual
- ✅ `SOLUCAO_UVICORN.md` - Este arquivo

---

## 🎉 Próximos Passos

Depois que o backend iniciar:

1. **Abra outro terminal**
2. **Vá para a pasta frontend:**
   ```cmd
   cd ..\frontend
   ```
3. **Inicie o frontend:**
   ```cmd
   npm run dev
   ```
4. **Acesse:** http://localhost:3000

---

**Última atualização:** 23/11/2025  
**Status:** ✅ Testado e funcional
