import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
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
from app.api.routes import planos  # PLANOS E ASSINATURAS MULTI-TENANT
from app.api.routes import escolas  # ESCOLAS (TENANTS)
from app.api.routes import planejamento_bncc  # PLANEJAMENTO BNCC E PEI
from app.api.routes import calendario_atividades  # CALENDÁRIO DE ATIVIDADES PEI
from app.api.routes import student_pei  # PEI PARA PORTAL DO ALUNO
from app.api.routes import diario_aprendizagem  # DIÁRIO DE APRENDIZAGEM COM IA
from app.api.routes import agenda  # AGENDA DO PROFESSOR
from app.api.routes import registro_diario  # REGISTRO DIÁRIO DE AULAS
from app.api.routes import conteudos_aluno  # CONTEÚDOS DO ALUNO (INTEGRAÇÃO)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    🎓 **AdaptAI API - Sistema de Educação Inclusiva com IA**
    
    Sistema inteligente para geração automática de provas e questões adaptadas.
    """,
    contact={
        "name": "AdaptAI Team",
        "email": "contact@adaptai.com",
    },
    license_info={
        "name": "MIT",
    }
)

# ============================================
# CORS - Configuração robusta para produção
# ============================================

ALLOWED_ORIGINS = [
    "https://adaptai-frontend.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:5177",
    "http://localhost:5178",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

IS_PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PRODUCTION")

if IS_PRODUCTION:
    print("[CORS] Modo de produção - permitindo todas origens")
    origins = ["*"]
else:
    origins = ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if not IS_PRODUCTION else False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    response = JSONResponse(content={"status": "ok"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Max-Age"] = "86400"
    return response

# ============================================
# Storage para arquivos estáticos
# ============================================

storage_materiais_path = Path(__file__).parent.parent / "storage" / "materiais"
storage_materiais_path.mkdir(parents=True, exist_ok=True)
app.mount("/storage/materiais", StaticFiles(directory=str(storage_materiais_path)), name="materiais_storage")

storage_relatorios_path = Path(__file__).parent.parent / "storage" / "relatorios"
storage_relatorios_path.mkdir(parents=True, exist_ok=True)
app.mount("/storage/relatorios", StaticFiles(directory=str(storage_relatorios_path)), name="relatorios_storage")

storage_registros_path = Path(__file__).parent.parent / "storage" / "registros_diarios"
storage_registros_path.mkdir(parents=True, exist_ok=True)

# ============================================
# Incluir rotas
# ============================================

app.include_router(auth.router, prefix="/api/v1", tags=["🔐 Authentication"])
app.include_router(students.router, prefix="/api/v1", tags=["👥 Students"])
app.include_router(questions.router, prefix="/api/v1", tags=["📝 Questions"])
app.include_router(applications.router, prefix="/api/v1", tags=["📋 Applications"])
app.include_router(analytics.router, prefix="/api/v1", tags=["📊 Analytics"])
app.include_router(provas.router, prefix="/api/v1", tags=["🎓 Provas"])
app.include_router(student_provas.router, prefix="/api/v1", tags=["🎓 Provas Estudantes"])
app.include_router(professor_analytics.router, prefix="/api/v1", tags=["📊 Analytics Provas"])
app.include_router(materiais.router, prefix="/api/v1", tags=["📚 Materiais"])
app.include_router(student_materiais.router, prefix="/api/v1", tags=["📚 Student Materiais"])
app.include_router(analise_qualitativa.router, prefix="/api/v1", tags=["🤖 Análise Qualitativa IA"])
app.include_router(prova_adaptativa.router, prefix="/api/v1", tags=["🎯 Prova Adaptativa"])
app.include_router(pei.router, prefix="/api/v1", tags=["❤️ PEI com IA"])
app.include_router(relatorios.router, prefix="/api/v1", tags=["📋 Relatórios"])
app.include_router(relatorios_analise.router, prefix="/api/v1", tags=["🎨 Jornada Terapêutica"])
app.include_router(materiais_adaptados.router, prefix="/api/v1", tags=["🎨 Materiais Adaptados"])
app.include_router(planos.router, prefix="/api/v1", tags=["💳 Planos"])
app.include_router(escolas.router, prefix="/api/v1", tags=["🏫 Escolas"])
app.include_router(planejamento_bncc.router, prefix="/api/v1", tags=["📚 Planejamento BNCC"])
app.include_router(calendario_atividades.router, prefix="/api/v1", tags=["📅 Calendário"])
app.include_router(student_pei.router, prefix="/api/v1/student", tags=["🎯 PEI Estudante"])
app.include_router(diario_aprendizagem.router, prefix="/api/v1", tags=["📔 Diário"])
app.include_router(agenda.router, prefix="/api/v1", tags=["📅 Agenda"])
app.include_router(registro_diario.router, prefix="/api/v1", tags=["📚 Registro Diário"])
app.include_router(conteudos_aluno.router, prefix="/api/v1", tags=["📚 Conteúdos Aluno"])

# ============================================
# Rotas principais
# ============================================

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🎓 AdaptAI API - Sistema de Educação Inclusiva com IA",
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "AdaptAI Backend", "version": settings.VERSION}

@app.get("/info", tags=["Info"])
def info():
    return {"name": settings.APP_NAME, "version": settings.VERSION, "production": bool(IS_PRODUCTION)}

@app.on_event("startup")
async def startup_event():
    print("="*60)
    print("[ADAPTAI] Backend Starting...")
    print(f"[VERSION] {settings.VERSION}")
    print(f"[AI MODEL] {settings.CLAUDE_MODEL}")
    print(f"[PRODUCTION] {bool(IS_PRODUCTION)}")
    print("="*60)

@app.on_event("shutdown")
async def shutdown_event():
    print("[ADAPTAI] Backend Shutting down...")
