# 👨‍🎓 CRIAR ESTUDANTES NO SISTEMA

## 🎯 OPÇÃO 1: CRIAR ENRICO (AUTOMÁTICO)

Execute este script para criar o estudante Enrico automaticamente:

```cmd
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
CRIAR_ESTUDANTE_ENRICO.bat
```

**Dados do Enrico:**
- Nome: ENRICO MELO MOTA AZEVEDO
- Email: fazevedo1980@gmail.com
- Senha: Enrico
- Data Nascimento: 09/07/2015
- Série: 5º
- Diagnóstico: Neurotipico

---

## 🎯 OPÇÃO 2: CRIAR QUALQUER ESTUDANTE (INTERATIVO)

Execute este script e preencha os dados quando solicitado:

```cmd
cd C:\Users\marci\OneDrive\Documentos\Projetos\AdaptAI\backend
CRIAR_ESTUDANTE_INTERATIVO.bat
```

O script vai pedir:
- Nome completo
- Email
- Senha
- Data de nascimento (DD/MM/AAAA)
- Série/Ano
- Diagnóstico
- Observações (opcional)

---

## ✅ RESULTADO

Após a execução, você verá:

```
============================================================
✅ ESTUDANTE CRIADO COM SUCESSO!
============================================================

Credenciais de acesso:
  Email: fazevedo1980@gmail.com
  Senha: Enrico

O aluno já pode fazer login no sistema!
============================================================
```

---

## 🔐 LOGIN DO ALUNO

Após criar, o aluno pode acessar:
- URL: http://localhost:5173
- Email: fazevedo1980@gmail.com
- Senha: Enrico

---

## ⚠️ ERROS COMUNS

### "Email já está cadastrado"
O email já existe no sistema. Use outro email ou verifique se o aluno já foi criado.

### "Data inválida"
Use o formato DD/MM/AAAA (exemplo: 09/07/2015)

### "Erro de conexão"
Verifique se o backend está rodando e se o .env está configurado corretamente.

---

## 📝 DIAGNÓSTICOS COMUNS

Use um destes diagnósticos padrão:
- Neurotipico
- TEA (Transtorno do Espectro Autista)
- TDAH (Transtorno do Déficit de Atenção)
- Dislexia
- Discalculia
- Outro (especificar nas observações)

---

## 🎓 SÉRIES/ANOS

Exemplos:
- 1º ano, 2º ano, 3º ano (Ensino Fundamental I)
- 4º ano, 5º ano (Ensino Fundamental I)
- 6º ano até 9º ano (Ensino Fundamental II)
- 1º EM, 2º EM, 3º EM (Ensino Médio)

---

**Pronto! Scripts criados e prontos para usar! 🚀**
