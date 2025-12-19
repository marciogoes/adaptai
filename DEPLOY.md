# 🚀 AdaptAI Backend - Deploy Guide

## 📋 Arquivos de Deploy

- `Procfile` - Comando de inicialização para Railway/Heroku
- `railway.json` - Configurações do Railway
- `runtime.txt` - Versão do Python
- `requirements.txt` - Dependências Python
- `.env.example` - Template de variáveis de ambiente

## 🔧 Variáveis de Ambiente Necessárias

Configure estas variáveis no Railway:

```
DATABASE_URL=mysql+pymysql://usuario:senha@host:porta/banco
SECRET_KEY=sua-chave-secreta-minimo-32-caracteres
ANTHROPIC_API_KEY=sk-ant-api03-sua-chave
CLAUDE_MODEL=claude-3-haiku-20240307
ENVIRONMENT=production
DEBUG=false
BACKEND_CORS_ORIGINS=https://seu-frontend.vercel.app,http://localhost:3000
```

## 🚀 Deploy no Railway

### 1. Criar conta
- Acesse https://railway.app
- Faça login com GitHub

### 2. Novo projeto
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Escolha o repositório do backend

### 3. Configurar variáveis
- Clique no serviço criado
- Vá em "Variables"
- Adicione todas as variáveis listadas acima

### 4. Deploy automático
- Railway fará deploy automaticamente
- Acompanhe os logs em "Deployments"

### 5. Obter URL
- Após deploy, vá em "Settings"
- Copie a URL pública (ex: https://adaptai-backend.up.railway.app)

## 📝 Endpoints Principais

- `GET /` - Info da API
- `GET /health` - Health check
- `GET /docs` - Documentação Swagger
- `POST /api/v1/auth/login` - Login

## 🔒 Segurança

- Nunca comite o arquivo `.env`
- Use SECRET_KEY forte em produção
- Configure CORS apenas para domínios necessários
