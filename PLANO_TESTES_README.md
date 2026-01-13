# 🧪 PLANO DE TESTES - ADAPTAI

## 📋 Visão Geral

Este plano divide os testes do AdaptAI em **8 etapas independentes**, permitindo:
- Executar uma etapa por vez
- Identificar problemas específicos
- Evitar timeout por projetos grandes

---

## 🚀 Como Usar

### Opção 1: Menu Interativo (RECOMENDADO)
```bash
# Na pasta backend, execute:
MENU_TESTES.bat
```

### Opção 2: Executar Etapa Específica
```bash
TESTE_ETAPA1.bat   # Infraestrutura
TESTE_ETAPA2.bat   # Autenticação
TESTE_ETAPA3.bat   # Estudantes
```

---

## 📊 Etapas de Teste

| Etapa | Módulo | Descrição | Requer Backend |
|-------|--------|-----------|----------------|
| **1** | Infraestrutura | Banco de dados, tabelas, configurações | ❌ Não |
| **2** | Autenticação | Login, JWT, endpoints protegidos | ✅ Sim |
| **3** | Estudantes | CRUD de estudantes | ✅ Sim |
| **4** | Provas | Criar, listar, associar provas | ✅ Sim |
| **5** | Materiais | CRUD de materiais de estudo | ✅ Sim |
| **6** | PEI | Plano Educacional Individualizado | ✅ Sim |
| **7** | Relatórios | Upload, listagem, análise | ✅ Sim |
| **8** | BNCC/Calendário | Planejamento e calendário | ✅ Sim |

---

## 📁 Arquivos Criados

```
backend/
├── MENU_TESTES.bat              # Menu principal interativo
├── TESTE_ETAPA1.bat             # Executor da Etapa 1
├── TESTE_ETAPA2.bat             # Executor da Etapa 2
├── TESTE_ETAPA3.bat             # Executor da Etapa 3
├── teste_etapa1_infraestrutura.py
├── teste_etapa2_autenticacao.py
└── teste_etapa3_estudantes.py
```

---

## 🔄 Ordem Recomendada de Execução

1. **ETAPA 1** - Verificar infraestrutura (pode rodar sem backend)
2. **Iniciar o backend** (opção B no menu ou INICIAR_BACKEND.bat)
3. **ETAPA 2** - Testar autenticação
4. **ETAPA 3** - Testar estudantes
5. Continuar com as demais etapas...

---

## ⚠️ Pré-requisitos

- Python 3.12+ instalado
- Ambiente virtual configurado (venv)
- Variáveis de ambiente configuradas (.env)
- MySQL acessível
- Para etapas 2-8: Backend rodando

---

## 📈 Interpretando Resultados

```
✅ PASSOU - Teste executado com sucesso
❌ FALHOU - Problema encontrado (ver mensagem)
```

### Exemplo de Saída:
```
📊 RESUMO ETAPA 1 - INFRAESTRUTURA
════════════════════════════════════════
✅ Testes OK:     15
❌ Testes Falha:  2
📈 Taxa Sucesso:  88.2%
```

---

## 🛠️ Solução de Problemas

### "Conexão recusada"
- O backend não está rodando
- Execute: `INICIAR_BACKEND.bat` ou opção B no menu

### "Variável não encontrada"
- Arquivo .env não existe ou incompleto
- Verifique: `backend/.env`

### "Tabela não encontrada"
- Banco de dados não foi inicializado
- Execute as migrações ou scripts de criação de tabelas

### "Login falhou"
- Credenciais incorretas
- Verifique usuários no banco: `LISTAR_USUARIOS.bat`

---

## 📞 Suporte

Se encontrar problemas persistentes:
1. Execute a ETAPA 1 primeiro para verificar infraestrutura
2. Verifique os logs do backend
3. Confirme as credenciais no arquivo .env

---

*Documento gerado automaticamente para o projeto AdaptAI*
