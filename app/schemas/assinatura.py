# ============================================
# SCHEMAS - ASSINATURA E FATURA
# ============================================
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.assinatura import StatusAssinatura, StatusFatura


class AssinaturaBase(BaseModel):
    plano_id: int
    forma_pagamento: Optional[str] = None
    dia_vencimento: int = Field(default=10, ge=1, le=28)


class AssinaturaCreate(AssinaturaBase):
    escola_id: int


class AssinaturaUpdate(BaseModel):
    plano_id: Optional[int] = None
    forma_pagamento: Optional[str] = None
    dia_vencimento: Optional[int] = None
    desconto_percentual: Optional[float] = None


class AssinaturaResponse(BaseModel):
    id: int
    escola_id: int
    plano_id: int
    status: str
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    data_proxima_cobranca: Optional[datetime] = None
    valor_mensal: float
    desconto_percentual: float
    dia_vencimento: int
    forma_pagamento: Optional[str] = None
    
    # Uso atual
    alunos_ativos: int
    professores_ativos: int
    provas_mes_atual: int
    materiais_mes_atual: int
    peis_mes_atual: int
    relatorios_mes_atual: int
    
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssinaturaComPlano(AssinaturaResponse):
    """Assinatura com dados do plano"""
    plano: Optional["PlanoResponse"] = None

    class Config:
        from_attributes = True


class AssinaturaDetalhada(AssinaturaComPlano):
    """Assinatura com limites calculados"""
    limite_alunos: int = 0
    limite_professores: int = 0
    limite_provas_mes: int = 0
    limite_materiais_mes: int = 0
    limite_peis_mes: int = 0
    limite_relatorios_mes: int = 0
    
    # Percentuais de uso
    percentual_alunos: float = 0.0
    percentual_professores: float = 0.0
    percentual_provas: float = 0.0
    percentual_materiais: float = 0.0
    percentual_peis: float = 0.0
    percentual_relatorios: float = 0.0

    class Config:
        from_attributes = True


# ============================================
# SCHEMAS - FATURA
# ============================================

class FaturaBase(BaseModel):
    valor: float = Field(..., gt=0)
    data_vencimento: datetime
    observacoes: Optional[str] = None


class FaturaCreate(FaturaBase):
    assinatura_id: int


class FaturaUpdate(BaseModel):
    status: Optional[str] = None
    valor_pago: Optional[float] = None
    data_pagamento: Optional[datetime] = None
    metodo_pagamento: Optional[str] = None
    observacoes: Optional[str] = None


class FaturaResponse(BaseModel):
    id: int
    assinatura_id: int
    numero: str
    valor: float
    valor_pago: Optional[float] = None
    status: str
    data_emissao: datetime
    data_vencimento: datetime
    data_pagamento: Optional[datetime] = None
    metodo_pagamento: Optional[str] = None
    link_pagamento: Optional[str] = None
    nota_fiscal: Optional[str] = None
    observacoes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FaturaComEscola(FaturaResponse):
    """Fatura com dados da escola"""
    escola_nome: Optional[str] = None
    escola_cnpj: Optional[str] = None

    class Config:
        from_attributes = True


# Import circular fix
from app.schemas.plano import PlanoResponse
AssinaturaComPlano.model_rebuild()
AssinaturaDetalhada.model_rebuild()
