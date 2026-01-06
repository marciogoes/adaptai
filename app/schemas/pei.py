# ============================================
# SCHEMAS - PEI (Plano Educacional Individualizado)
# ============================================

from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime, date


# ============================================
# Schemas de Objetivo
# ============================================

class PEIObjetivoBase(BaseModel):
    area: str
    codigo_bncc: Optional[str] = None
    titulo: str
    descricao: Optional[str] = None
    trimestre: int = 1
    meta_especifica: Optional[str] = None
    criterio_medicao: Optional[str] = None
    valor_alvo: float = 80.0
    prazo: Optional[date] = None
    adaptacoes: Optional[List[str]] = None
    estrategias: Optional[List[str]] = None
    materiais_recursos: Optional[List[str]] = None
    criterios_avaliacao: Optional[List[str]] = None
    justificativa: Optional[Dict[str, Any]] = None


class PEIObjetivoCreate(PEIObjetivoBase):
    pass


class PEIObjetivoUpdate(BaseModel):
    area: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    trimestre: Optional[int] = None
    meta_especifica: Optional[str] = None
    criterio_medicao: Optional[str] = None
    valor_alvo: Optional[float] = None
    valor_atual: Optional[float] = None
    prazo: Optional[date] = None
    status: Optional[str] = None
    adaptacoes: Optional[List[str]] = None
    estrategias: Optional[List[str]] = None
    materiais_recursos: Optional[List[str]] = None
    criterios_avaliacao: Optional[List[str]] = None
    observacoes: Optional[str] = None


class PEIObjetivoResponse(PEIObjetivoBase):
    id: int
    pei_id: int
    curriculo_nacional_id: Optional[int] = None
    valor_atual: float = 0.0
    status: str = "nao_iniciado"
    origem: str = "ia_sugestao"
    ia_sugestao_original: Optional[Dict[str, Any]] = None
    ultima_atualizacao: Optional[datetime] = None
    observacoes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============================================
# Schemas de Progresso
# ============================================

class ProgressLogCreate(BaseModel):
    observation: str
    progress_value: float


class ProgressLogResponse(BaseModel):
    id: int
    goal_id: int
    observation: str
    progress_value: float
    ai_analysis: Optional[str] = None
    ai_suggestions: Optional[List[str]] = None
    recorded_by: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# Schemas de PEI
# ============================================

class PEIBase(BaseModel):
    ano_letivo: str
    tipo_periodo: str = "anual"
    semestre: Optional[int] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    data_proxima_revisao: Optional[date] = None
    diagnosticos: Optional[Dict[str, Any]] = None
    pontos_fortes: Optional[List[str]] = None
    desafios: Optional[List[str]] = None
    estilo_aprendizagem: Optional[Dict[str, Any]] = None
    adaptacoes_atuais: Optional[List[str]] = None
    contexto_familiar: Optional[str] = None


class PEICreate(PEIBase):
    student_id: int
    objetivos: Optional[List[PEIObjetivoCreate]] = None


class PEIUpdate(BaseModel):
    ano_letivo: Optional[str] = None
    tipo_periodo: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    data_proxima_revisao: Optional[date] = None
    diagnosticos: Optional[Dict[str, Any]] = None
    pontos_fortes: Optional[List[str]] = None
    desafios: Optional[List[str]] = None
    estilo_aprendizagem: Optional[Dict[str, Any]] = None
    adaptacoes_atuais: Optional[List[str]] = None
    contexto_familiar: Optional[str] = None
    status: Optional[str] = None


class PEIResponse(PEIBase):
    id: int
    student_id: int
    created_by: int
    status: str = "rascunho"
    ia_sugestoes_originais: Optional[Dict[str, Any]] = None
    baseline_estabelecido: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    objetivos: List[PEIObjetivoResponse] = []
    
    class Config:
        from_attributes = True


class PEIListResponse(BaseModel):
    total: int
    peis: List[PEIResponse]


# ============================================
# Schemas para Planejamento
# ============================================

class GerarPlanejamentoRequest(BaseModel):
    student_id: int
    ano_letivo: str
    componentes: List[str]


class GerarPlanejamentoTrimestreRequest(BaseModel):
    student_id: int
    componente: str
    trimestre: int
    ano_letivo: str


class SalvarPlanejamentoRequest(BaseModel):
    student_id: int
    ano_letivo: str
    planejamento: Dict[str, Any]


class PlanejamentoResponse(BaseModel):
    success: bool
    perfil_aluno: Optional[Dict[str, Any]] = None
    planejamento: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ============================================
# Schemas de Ajuste
# ============================================

class PEIAjusteResponse(BaseModel):
    id: int
    pei_id: int
    adjustment_type: str
    description: str
    reason: Optional[str] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    adjusted_by: int
    adjusted_at: datetime
    
    class Config:
        from_attributes = True
