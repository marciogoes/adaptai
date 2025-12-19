# 🔧 AdaptAI Backend

API FastAPI para sistema educacional com IA para avaliações adaptativas.

## 🚀 Tecnologias

- **Python 3.12+**
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para MySQL
- **MySQL** - Banco de dados
- **Anthropic Claude API** - IA para geração de conteúdo
- **JWT** - Autenticação
- **Pydantic** - Validação de dados

---

## 📦 Instalação

### 1. Clonar repositório
```bash
git clone https://github.com/marciogoesn/adaptai.git
cd adaptai
```

### 2. Criar ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas credenciais
```

**Importante:** Edite o arquivo `.env` com suas credenciais reais:
- Database MySQL (host, user, password)
- Anthropic API Key
- JWT Secret Key

### 5. Iniciar servidor
```bash
uvicorn app.main:app --reload
```

Servidor rodando em: http://localhost:8000

---

## 📚 API Documentation

Acesse a documentação interativa:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🗂️ Estrutura do Projeto

```
backend/
├── app/
│   ├── api/              # Endpoints da API
│   │   └── v1/           
│   │       ├── auth.py   # Autenticação
│   │       ├── questions.py
│   │       ├── materials.py
│   │       └── ...
│   ├── models/           # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── prova.py
│   │   └── ...
│   ├── services/         # Lógica de negócio + IA
│   │   ├── ai_question_service.py
│   │   ├── prova_adaptativa_service.py
│   │   └── ...
│   ├── core/             # Configurações
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   └── main.py           # Aplicação FastAPI
├── storage/              # Arquivos gerados (HTML, JSON)
├── .env.example          # Template de configuração
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

---

## 🔐 Segurança

- ✅ **JWT** para autenticação
- ✅ **Bcrypt** para hash de senhas
- ✅ **CORS** configurado
- ✅ Variáveis de ambiente protegidas (.env não vai pro Git)
- ✅ Validação de dados com Pydantic

---

## ✨ Funcionalidades Principais

### 🎯 Para Professores
- Criar provas automaticamente com IA
- Correção automática de provas
- Análise qualitativa com IA
- Gerar provas de reforço adaptativas
- Criar materiais personalizados
- Dashboard com analytics

### 👨‍🎓 Para Alunos
- Realizar provas online
- Receber feedback imediato
- Acessar provas de reforço personalizadas
- Visualizar materiais adaptativos

---

## 🧪 Testes

```bash
# Rodar testes
pytest

# Com coverage
pytest --cov=app tests/
```

---

## 🚀 Deploy

### Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Docker
```bash
docker build -t adaptai-backend .
docker run -p 8000:8000 adaptai-backend
```

---

## 🔧 Variáveis de Ambiente

Veja `.env.example` para todas as configurações disponíveis.

**Essenciais:**
- `DATABASE_URL` - Conexão MySQL
- `ANTHROPIC_API_KEY` - API Key do Claude
- `SECRET_KEY` - Chave JWT
- `FRONTEND_URL` - URL do frontend (CORS)

---

## 📞 Suporte

- 📧 Email: goes.nascimento@gmail.com
- 🐛 Issues: https://github.com/marciogoesn/adaptai/issues
- 📚 Frontend: https://github.com/marciogoesn/adaptai-frontend

---

## 📄 Licença

MIT License - Veja [LICENSE](../LICENSE) para detalhes.

---

**Desenvolvido com 💜 para educação inclusiva**
