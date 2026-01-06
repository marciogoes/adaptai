# ============================================
# SCHEMAS - PLANO
# ============================================
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PlanoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = None
    valor: float = Field(..., ge=0)
    valor_anual: Optional[float] = None


class PlanoCreate(PlanoBase):
    # Limites
    limite_alunos: int = Field(default=50, ge=1)
    limite_professores: int = Field(default=5, ge=1)
    limite_provas_mes: int = Field(default=100, ge=1)
    limite_materiais_mes: int = Field(default=100, ge=1)
    limite_peis_mes: int = Field(default=50, ge=1)
    limite_relatorios_mes: int = Field(default=50, ge=1)
    
    # Funcionalidades
    pei_automatico: bool = True
    materiais_adaptativos: bool = True
    mapas_mentais: bool = True
    relatorios_avancados: bool = False
    api_access: bool = False
    suporte_prioritario: bool = False
    treinamento_incluido: bool = False
    
    # Integrações
    integracao_whatsapp: bool = False
    integracao_google: bool = False
    exportacao_pdf: bool = True
    exportacao_excel: bool = True
    
    # Status
    ativo: bool = True
    destaque: bool = False
    ordem: int = 0


class PlanoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    valor_anual: Optional[float] = None
    
    # Limites
    limite_alunos: Optional[int] = None
    limite_professores: Optional[int] = None
    limite_provas_mes: Optional[int] = None
    limite_materiais_mes: Optional[int] = None
    limite_peis_mes: Optional[int] = None
    limite_relatorios_mes: Optional[int] = None
    
    # Funcionalidades
    pei_automatico: Optional[bool] = None
    materiais_adaptativos: Optional[bool] = None
    mapas_mentais: Optional[bool] = None
    relatorios_avancados: Optional[bool] = None
    api_access: Optional[bool] = None
    suporte_prioritario: Optional[bool] = None
    treinamento_incluido: Optional[bool] = None
    
    # Integrações
    integracao_whatsapp: Optional[bool] = None
    integracao_google: Optional[bool] = None
    exportacao_pdf: Optional[bool] = None
    exportacao_excel: Optional[bool] = None
    
    # Status
    ativo: Optional[bool] = None
    destaque: Optional[bool] = None
    ordem: Optional[int] = None


class PlanoResponse(BaseModel):
    id: int
    nome: str
    slug: str
    descricao: Optional[str] = None
    valor: float
    valor_anual: Optional[float] = None
    
    # Limites
    limite_alunos: int
    limite_professores: int
    limite_provas_mes: int
    limite_materiais_mes: int
    limite_peis_mes: int
    limite_relatorios_mes: int
    
    # Funcionalidades
    pei_automatico: bool
    materiais_adaptativos: bool
    mapas_mentais: bool
    relatorios_avancados: bool
    api_access: bool
    suporte_prioritario: bool
    treinamento_incluido: bool
    
    # Integrações
    integracao_whatsapp: bool
    integracao_google: bool
    exportacao_pdf: bool
    exportacao_excel: bool
    
    # Status
    ativo: bool
    destaque: bool
    ordem: int
    
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlanoPublico(BaseModel):
    """Versão pública do plano para landing page"""
    id: int
    nome: str
    slug: str
    descricao: Optional[str] = None
    valor: float
    valor_anual: Optional[float] = None
    
    # Limites principais
    limite_alunos: int
    limite_professores: int
    
    # Funcionalidades principais
    pei_automatico: bool
    materiais_adaptativos: bool
    mapas_mentais: bool
    relatorios_avancados: bool
    suporte_prioritario: bool
    
    destaque: bool
    ordem: int

    class Config:
        from_attributes = True
