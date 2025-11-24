from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base

# Importar rotas
from app.api.routes import auth, students, questions, applications, analytics
from app.api.routes import provas  # NOVA ROTA DE PROVAS
from app.api.routes import student_provas  # ROTAS ESTUDANTES

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    🎓 **AdaptAI API - Sistema de Educação Inclusiva com IA**
    
    Sistema inteligente para geração automática de provas e questões adaptadas.
    
    ## 🚀 Funcionalidades Principais
    
    * **Geração Automática de Provas com IA**: Administrador define conteúdo, IA gera questões
    * **Associação Aluno-Prova**: Administrador libera provas para alunos específicos
    * **Múltiplos Níveis de Dificuldade**: 4 níveis customizáveis
    * **Adaptações Personalizadas**: Para TEA, TDAH, dislexia, etc
    * **Armazenamento Completo**: Provas, questões, respostas, resultados
    * **Análise de Desempenho**: Com IA para identificar pontos fortes e fracos
    
    ## 📊 Tecnologias
    
    * Python 3.14 + FastAPI
    * MySQL 8.0 DBaaS
    * Claude AI (Anthropic)
    * SQLAlchemy ORM
    * JWT Authentication
    """,
    contact={
        "name": "AdaptAI Team",
        "email": "contact@adaptai.com",
    },
    license_info={
        "name": "MIT",
    }
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth.router, prefix="/api/v1", tags=["🔐 Authentication"])
app.include_router(students.router, prefix="/api/v1", tags=["👥 Students"])
app.include_router(questions.router, prefix="/api/v1", tags=["📝 Questions"])
app.include_router(applications.router, prefix="/api/v1", tags=["📋 Applications"])
app.include_router(analytics.router, prefix="/api/v1", tags=["📊 Analytics"])
app.include_router(provas.router, prefix="/api/v1", tags=["🎓 Provas (NOVO)"])  # NOVA ROTA!
app.include_router(student_provas.router, prefix="/api/v1", tags=["🎓 Provas Estudantes"])  # ROTAS ESTUDANTES!

# Rotas principais
@app.get("/", tags=["Root"])
def root():
    """
    🏠 Endpoint raiz da API
    """
    return {
        "message": "🎓 AdaptAI API - Sistema de Educação Inclusiva com IA",
        "version": settings.VERSION,
        "status": "running",
        "novo": "🎓 Sistema de Provas com IA ativado!",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "Geração automática de provas com IA",
            "Administrador define conteúdo/tema",
            "IA gera questões automaticamente",
            "Associação prova-aluno",
            "Aluno faz prova online",
            "Armazenamento completo de dados",
            "Análise de desempenho com IA"
        ],
        "endpoints": {
            "auth": "/api/v1/auth",
            "students": "/api/v1/students",
            "questions": "/api/v1/questions",
            "applications": "/api/v1/applications",
            "analytics": "/api/v1/analytics",
            "provas": "/api/v1/provas"  # NOVO!
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    💚 Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "AdaptAI Backend",
        "version": settings.VERSION,
        "database": "MySQL 8.0 DBaaS",
        "ai_engine": "Claude API (Anthropic)",
        "features_enabled": ["prova_generation", "student_management", "analytics"]
    }

@app.get("/info", tags=["Info"])
def info():
    """
    ℹ️ Informações sobre a API
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": "Sistema de educação inclusiva com geração automática de provas usando IA",
        "tech_stack": {
            "framework": "FastAPI",
            "python_version": "3.14",
            "database": "MySQL 8.0 DBaaS",
            "ai_model": settings.CLAUDE_MODEL,
            "orm": "SQLAlchemy"
        },
        "features": {
            "auto_prova_generation": "✅ Enabled",
            "ai_powered": "✅ Claude AI",
            "student_assignment": "✅ Enabled",
            "online_exam": "✅ Enabled",
            "performance_analysis": "✅ Enabled",
            "adaptive_difficulty": "✅ 4 levels"
        }
    }

# Event handlers
@app.on_event("startup")
async def startup_event():
    """
    Executado ao iniciar a aplicacao
    """
    print("="*60)
    print("[ADAPTAI] Backend Starting...")
    print(f"[VERSION] {settings.VERSION}")
    print(f"[PYTHON] 3.12")
    print(f"[DATABASE] MySQL 8.0 DBaaS")
    print(f"[AI MODEL] {settings.CLAUDE_MODEL}")
    print(f"[FEATURE] Sistema de Provas com IA ativado!")
    print("="*60)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado ao desligar a aplicacao
    """
    print("\n[ADAPTAI] Backend Shutting down...")
    print("Goodbye!\n")
