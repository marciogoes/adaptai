"""
Schemas para Materiais
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date, time
from enum import Enum


class TipoMaterialEnum(str, Enum):
    """Tipos de materiais"""
    visual = "visual"
    mapa_mental = "mapa_mental"


class StatusMaterialEnum(str, Enum):
    """Status do material"""
    gerando = "gerando"
    disponivel = "disponivel"
    erro = "erro"


class MaterialCreate(BaseModel):
    """Schema para criar material"""
    titulo: str = Field(..., max_length=200)
    descricao: Optional[str] = None
    conteudo_prompt: str
    tipo: TipoMaterialEnum
    materia: str = Field(..., max_length=100)
    serie_nivel: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = []
    aluno_ids: List[int] = Field(..., min_items=1)
    adaptacoes: Optional[List[str]] = None
    # NOVO: Campos para agendar aplicação
    data_aplicacao: Optional[date] = None
    hora_aplicacao: Optional[time] = Field(default=None, description="Hora da aplicação")
    criar_evento_agenda: bool = Field(default=False, description="Se True, cria evento na agenda automaticamente")


class MaterialResponse(BaseModel):
    """Schema de resposta do material"""
    id: int
    titulo: str
    descricao: Optional[str]
    conteudo_prompt: str
    tipo: TipoMaterialEnum
    materia: str
    serie_nivel: Optional[str]
    tags: Optional[List[str]]
    arquivo_path: Optional[str]  # NOVO: caminho do arquivo no storage
    metadados: Optional[dict]
    status: StatusMaterialEnum
    criado_em: datetime
    atualizado_em: Optional[datetime]
    criado_por_id: int
    
    class Config:
        from_attributes = True


class MaterialListResponse(BaseModel):
    """Schema resumido para listagem"""
    id: int
    titulo: str
    descricao: Optional[str]
    tipo: TipoMaterialEnum
    materia: str
    serie_nivel: Optional[str]
    status: StatusMaterialEnum
    criado_em: datetime
    total_alunos: int = 0
    
    class Config:
        from_attributes = True


class MaterialAlunoResponse(BaseModel):
    """Schema de material do aluno"""
    id: int
    material_id: int
    aluno_id: int
    data_disponibilizacao: datetime
    data_primeira_visualizacao: Optional[datetime]
    data_ultima_visualizacao: Optional[datetime]
    total_visualizacoes: int
    favorito: int
    anotacoes_aluno: Optional[str]
    
    # Material nested
    material: Optional[MaterialResponse]
    
    class Config:
        from_attributes = True


class VisualizarMaterialRequest(BaseModel):
    """Request para visualizar material"""
    pass


class AnotacaoRequest(BaseModel):
    """Request para salvar anotações"""
    anotacoes: str


class FavoritoRequest(BaseModel):
    """Request para marcar favorito"""
    favorito: bool
