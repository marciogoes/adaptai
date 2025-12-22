from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import settings
from app.database import engine, Base

# Importar TODOS os modelos para o SQLAlchemy criar as tabelas
from app.models import *  # Isso importa todos os modelos
from app.models.relatorio import Relatorio  # Garantir que Relatorio seja importado

# Importar rotas
from app.api.routes import auth, students, questions, applications, analytics
from app.api.routes import provas  # NOVA ROTA DE PROVAS
from app.api.routes import student_provas  # ROTAS ESTUDANTES
from app.api.routes import professor_analytics  # ANALYTICS DE PROVAS PARA PROFESSORES
from app.api.routes import materiais, student_materiais  # MATERIAIS DE ESTUDO COM IA
from app.api.routes import analise_qualitativa  # ANÁLISE QUALITATIVA COM IA
from app.api.routes import prova_adaptativa  # PROVA ADAPTATIVA (REFORÇO)
from app.api.routes import pei  # PEI COM IA
from app.api.routes import relatorios  # RELATÓRIOS DE TERAPIAS
from app.api.routes import relatorios_analise  # ANÁLISE CONSOLIDADA DE RELATÓRIOS
from app.api.routes import materiais_adaptados  # MATERIAIS ADAPTADOS COM IA

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

# CORS - Permitir origens de desenvolvimento E produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://adaptai-frontend.vercel.app",  # PRODUÇÃO VERCEL ✅
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175", 
        "http://localhost:5176", 
        "http://localhost:5177", 
        "http://localhost:5178", 
        "http://localhost:5179", 
        "http://localhost:5180", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173", 
        "http://127.0.0.1:5174", 
        "http://127.0.0.1:5175", 
        "http://127.0.0.1:5176", 
        "http://127.0.0.1:5177", 
        "http://127.0.0.1:5178", 
        "http://127.0.0.1:5179", 
        "http://127.0.0.1:5180"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configurar pastas de storage para arquivos estáticos
storage_materiais_path = Path(__file__).parent.parent / "storage" / "materiais"
storage_materiais_path.mkdir(parents=True, exist_ok=True)
app.mount("/storage/materiais", StaticFiles(directory=str(storage_materiais_path)), name="materiais_storage")
print(f"📁 Storage Materiais configurado: {storage_materiais_path}")

storage_relatorios_path = Path(__file__).parent.parent / "storage" / "relatorios"
storage_relatorios_path.mkdir(parents=True, exist_ok=True)
app.mount("/storage/relatorios", StaticFiles(directory=str(storage_relatorios_path)), name="relatorios_storage")
print(f"📁 Storage Relatórios configurado: {storage_relatorios_path}")

# Incluir rotas
app.include_router(auth.router, prefix="/api/v1", tags=["🔐 Authentication"])
app.include_router(students.router, prefix="/api/v1", tags=["👥 Students"])
app.include_router(questions.router, prefix="/api/v1", tags=["📝 Questions"])
app.include_router(applications.router, prefix="/api/v1", tags=["📋 Applications"])
app.include_router(analytics.router, prefix="/api/v1", tags=["📊 Analytics"])
app.include_router(provas.router, prefix="/api/v1", tags=["🎓 Provas (NOVO)"])  # NOVA ROTA!
app.include_router(student_provas.router, prefix="/api/v1", tags=["🎓 Provas Estudantes"])  # ROTAS ESTUDANTES!
app.include_router(professor_analytics.router, prefix="/api/v1", tags=["📊 Analytics Provas"])  # ANALYTICS PARA PROFESSORES!
app.include_router(materiais.router, prefix="/api/v1", tags=["📚 Materiais"])  # MATERIAIS DE ESTUDO COM IA!
app.include_router(student_materiais.router, prefix="/api/v1", tags=["📚 Student Materiais"])  # ALUNO VER MATERIAIS!
app.include_router(analise_qualitativa.router, prefix="/api/v1", tags=["🤖 Análise Qualitativa IA"])  # ANÁLISE COM IA!
app.include_router(prova_adaptativa.router, prefix="/api/v1", tags=["🎯 Prova Adaptativa (Reforço)"])  # PROVA DE REFORÇO!
app.include_router(pei.router, prefix="/api/v1", tags=["❤️ PEI com IA"])  # PEI COM IA!
app.include_router(relatorios.router, prefix="/api/v1", tags=["📋 Relatórios de Terapias"])  # RELATÓRIOS!
app.include_router(relatorios_analise.router, prefix="/api/v1", tags=["🎨 Jornada Terapêutica"])  # ANÁLISE CONSOLIDADA!
app.include_router(materiais_adaptados.router, prefix="/api/v1", tags=["🎨 Materiais Adaptados"])  # MATERIAIS ADAPTADOS!

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
