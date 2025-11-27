"""
Schemas para Análise Qualitativa
"""
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class AnaliseQualitativaResponse(BaseModel):
    """Response de análise qualitativa"""
    id: int
    prova_aluno_id: int
    
    # Análise
    pontos_fortes: str
    pontos_fracos: str
    conteudos_revisar: List[str]
    recomendacoes: str
    
    # Análise detalhada
    analise_por_conteudo: Dict
    
    # Métricas
    nivel_dominio: str
    areas_prioridade: List[str]
    
    # Timestamps
    criado_em: datetime
    atualizado_em: Optional[datetime]
    
    class Config:
        from_attributes = True


class GerarAnaliseRequest(BaseModel):
    """Request para gerar análise"""
    pass


class AnaliseQualitativaCompleta(BaseModel):
    """Análise completa com informações da prova"""
    analise: AnaliseQualitativaResponse
    prova_info: Dict
    aluno_info: Dict
    metricas: Dict
