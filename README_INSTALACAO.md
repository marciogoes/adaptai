# 🚀 COMO INSTALAR O ADAPTAI BACKEND

## ⭐ SCRIPTS DISPONÍVEIS (Do mais simples ao mais complexo)

### 1. **INSTALAR.bat** ⭐ RECOMENDADO!
- Versão MAIS SIMPLES
- Muitas pausas (você controla)
- Sem caracteres especiais
- Mostra cada passo claramente

**COMO USAR:**
```
1. Clique 2x em: INSTALAR.bat
2. Leia cada mensagem
3. Pressione qualquer tecla quando pedir
4. Aguarde a instalação
```

---

### 2. **INSTALACAO_SIMPLES.bat**
- Versão intermediária
- Algumas pausas
- Feedback claro

---

### 3. **RECRIAR_VENV_E_INICIAR.bat**
- Versão automática
- Menos pausas
- Pode piscar rápido

---

## 🔧 SE OS SCRIPTS NÃO FUNCIONAREM

Abra o **CMD** e digite MANUALMENTE:

```bash
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv python-jose[cryptography] passlib[bcrypt] python-multipart anthropic pydantic pydantic-settings
uvicorn app.main:app --reload
```

Leia: **INSTALACAO_MANUAL.md** para instruções detalhadas.

---

## ✅ CHECKLIST

Antes de executar qualquer script:

- [ ] Python 3.12 instalado
- [ ] Está na pasta `backend`
- [ ] Tem conexão com internet
- [ ] CMD/PowerShell aberto

---

## 🎯 ORDEM RECOMENDADA

1. Tente: **INSTALAR.bat** (mais simples)
2. Se não funcionar: Siga **INSTALACAO_MANUAL.md**
3. Se continuar com problema: Me envie o erro!

---

## 📊 RESULTADO ESPERADO

Quando funcionar, você verá:

```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

Então acesse: http://localhost:8000/docs

---

## 🆘 PROBLEMAS COMUNS

### "Script pisca e fecha"
- Use: **INSTALAR.bat** (tem pausas)

### "Python 3.12 não encontrado"
- Instale: https://www.python.org/downloads/

### "Caracteres estranhos"
- Use: **INSTALAR.bat** (sem caracteres especiais)

### "Erro ao instalar bibliotecas"
- Verifique internet
- Tente instalar uma por vez (veja INSTALACAO_MANUAL.md)

---

## 💡 DICA IMPORTANTE

**O script INSTALAR.bat tem PAUSAS em cada passo!**

Isso significa que você vê TUDO que está acontecendo e controla quando avançar.

---

**Boa sorte! 🚀**
