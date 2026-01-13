# ============================================
# MODELOS - AdaptAI Multi-tenant
# ============================================

# Multi-tenant (Escolas e Assinaturas)
from app.models.escola import Escola, ConfiguracaoEscola
from app.models.plano import Plano
from app.models.assinatura import Assinatura, Fatura, StatusAssinatura, StatusFatura

# Usuários e Alunos
from app.models.user import User, UserRole
from app.models.student import Student

# Questões e Provas
from app.models.question import QuestionSet, Question, DifficultyLevel
from app.models.application import Application, StudentAnswer, ApplicationStatus
from app.models.prova import (
    Prova, 
    QuestaoGerada, 
    ProvaAluno, 
    RespostaAluno,
    StatusProva,
    StatusProvaAluno,
    DificuldadeQuestao,
    TipoQuestao
)

# Análises e Relatórios
from app.models.performance import PerformanceAnalysis
from app.models.relatorio import Relatorio
from app.models.analise_qualitativa import AnaliseQualitativa

# Materiais
from app.models.material import Material, MaterialAluno, StatusMaterial
from app.models.material_adaptado_gerado import MaterialAdaptadoGerado

# Currículo e BNCC
from app.models.curriculo import (
    CurriculoNacional,
    MapeamentoPrerequisitos,
    CurriculoEscola,
    DificuldadeCurriculo
)

# PEI - Plano Educacional Individualizado
from app.models.pei import (
    PEI,
    PEIObjetivo,
    PEIProgressLog,
    PEIAjuste,
    StatusPEI,
    TipoPeriodo,
    AreaPEI,
    StatusObjetivo,
    OrigemObjetivo
)

# Atividades do PEI (Calendário)
from app.models.atividade_pei import (
    AtividadePEI,
    SequenciaObjetivo,
    TipoAtividade,
    StatusAtividade
)

# Diário de Aprendizagem
from app.models.diario_aprendizagem import (
    DiarioAprendizagem,
    ConteudoExtraido,
    ResumoSemanalAprendizagem,
    HumorEstudo,
    NivelCompreensao
)


__all__ = [
    # Multi-tenant
    "Escola",
    "ConfiguracaoEscola",
    "Plano",
    "Assinatura",
    "Fatura",
    "StatusAssinatura",
    "StatusFatura",
    
    # Usuários
    "User",
    "UserRole",
    "Student",
    
    # Questões e Provas
    "QuestionSet",
    "Question",
    "DifficultyLevel",
    "Application",
    "StudentAnswer",
    "ApplicationStatus",
    "Prova",
    "QuestaoGerada",
    "ProvaAluno",
    "RespostaAluno",
    "StatusProva",
    "StatusProvaAluno",
    "DificuldadeQuestao",
    "TipoQuestao",
    
    # Análises
    "PerformanceAnalysis",
    "Relatorio",
    "AnaliseQualitativa",
    
    # Materiais
    "Material",
    "MaterialAluno",
    "StatusMaterial",
    "MaterialAdaptadoGerado",
    
    # Currículo e BNCC
    "CurriculoNacional",
    "MapeamentoPrerequisitos",
    "CurriculoEscola",
    "DificuldadeCurriculo",
    
    # PEI
    "PEI",
    "PEIObjetivo",
    "PEIProgressLog",
    "PEIAjuste",
    "StatusPEI",
    "TipoPeriodo",
    "AreaPEI",
    "StatusObjetivo",
    "OrigemObjetivo",
    
    # Atividades PEI (Calendário)
    "AtividadePEI",
    "SequenciaObjetivo",
    "TipoAtividade",
    "StatusAtividade",
    
    # Diário de Aprendizagem
    "DiarioAprendizagem",
    "ConteudoExtraido",
    "ResumoSemanalAprendizagem",
    "HumorEstudo",
    "NivelCompreensao",
]
