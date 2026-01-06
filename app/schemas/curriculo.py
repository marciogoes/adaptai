# ============================================
# SCHEMAS - Currículo Nacional (BNCC)
# ============================================

from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class CurriculoNacionalBase(BaseModel):
    codigo_bncc: str
    ano_escolar: str
    componente: str
    campo_experiencia: Optional[str] = None
    eixo_tematico: Optional[str] = None
    habilidade_codigo: Optional[str] = None
    habilidade_descricao: Optional[str] = None
    objeto_conhecimento: Optional[str] = None
    exemplos_atividades: Optional[List[str]] = None
    prerequisitos: Optional[List[str]] = None
    dificuldade: Optional[str] = "intermediario"
    trimestre_sugerido: Optional[int] = None


class CurriculoNacionalCreate(CurriculoNacionalBase):
    pass


class CurriculoNacionalResponse(CurriculoNacionalBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CurriculoNacionalListResponse(BaseModel):
    total: int
    curriculos: List[CurriculoNacionalResponse]


class MapeamentoPrerequisitosBase(BaseModel):
    habilidade_codigo: str
    habilidade_titulo: str
    ano_escolar: str
    prerequisito_codigo: str
    prerequisito_titulo: str
    ano_prerequisito: str
    essencial: bool = True
    peso: float = 1.0


class MapeamentoPrerequisitosCreate(MapeamentoPrerequisitosBase):
    pass


class MapeamentoPrerequisitosResponse(MapeamentoPrerequisitosBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BuscarHabilidadesRequest(BaseModel):
    ano_escolar: str
    componente: Optional[str] = None
    trimestre: Optional[int] = None


class ImportarBNCCRequest(BaseModel):
    dados: List[CurriculoNacionalCreate]
