# 🛠️ GUIA: MATERIAIS TRAVADOS EM "GERANDO"

## 🎯 PROBLEMA:
Materiais ficaram travados em status "GERANDO" devido a falha anterior no MySQL.

---

## ✅ SOLUÇÃO RÁPIDA (30 segundos):

### Clique duplo em:
```
backend\LIMPAR_MATERIAIS_TRAVADOS.bat
```

### Escolha uma opção:

**Opção 1: Marcar como ERRO** ⚡ (Recomendado)
- Mais rápido (instantâneo)
- Marca os materiais como ERRO
- Você pode deletá-los no frontend
- Criar novos materiais limpos

**Opção 2: Re-gerar automaticamente** 🔄
- Demora ~1 minuto por material
- Tenta gerar o conteúdo novamente
- Use se quiser aproveitar os materiais

**Opção 3: Cancelar** ❌
- Não faz nada
- Materiais continuam travados

---

## 🎬 PASSO A PASSO:

### 1️⃣ Execute o script:
```bash
# Clique duplo em:
backend\LIMPAR_MATERIAIS_TRAVADOS.bat

# OU manualmente:
cd backend
venv\Scripts\activate
python limpar_materiais_travados.py
```

### 2️⃣ O script mostra os materiais travados:
```
🔍 Encontrados 2 materiais travados:

   ID 1: Recuperação de Química Material 01 (VISUAL)
   ID 2: Funções orgânicas com carbonila (MAPA_MENTAL)

OPÇÕES:
1. Marcar TODOS como ERRO (rápido)
2. Re-gerar TODOS automaticamente (demora ~1 min por material)
3. Cancelar

Escolha uma opção (1/2/3):
```

### 3️⃣ Digite sua escolha:
- Digite `1` e pressione Enter (marcar como erro)
- OU `2` (re-gerar)
- OU `3` (cancelar)

### 4️⃣ Depois no Frontend:
- Recarregue a página (F5)
- Se escolheu opção 1: materiais aparecem como ERRO (pode deletar)
- Se escolheu opção 2: materiais aparecem como DISPONÍVEL

---

## 💡 RECOMENDAÇÃO:

**Use OPÇÃO 1** (Marcar como ERRO):
1. Mais rápido
2. Você deleta os materiais com problema
3. Cria novos materiais limpos
4. Sistema funcionando 100%

---

## 🚀 DEPOIS DE LIMPAR:

**Teste criando um novo material:**
1. Vá para: http://localhost:5173/materiais/criar
2. Crie um material de teste
3. Aguarde 10-30 segundos
4. Deve aparecer DISPONÍVEL ✅

---

## 🐛 SE DER ERRO:

**Erro: "No module named 'app'"**
- Certifique-se de estar na pasta `backend`
- Execute: `cd backend` antes

**Erro: "venv não encontrado"**
- Execute: `python -m venv venv`
- Depois rode o script novamente

**Materiais não aparecem:**
- Verifique se backend está rodando
- Recarregue a página no frontend (F5)

---

**Execute agora e me diga qual opção escolheu!** 🚀
