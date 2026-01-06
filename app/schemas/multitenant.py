# ============================================
# SCHEMAS MULTI-TENANT (Escolas, Planos, Assinaturas)
# ============================================
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ==========================================
# ENUMS
# ==========================================

class TipoEscola(str, Enum):
    ESCOLA = "ESCOLA"
    CLINICA = "CLINICA"
    CENTRO_TERAPEUTICO = "CENTRO_TERAPEUTICO"
    AEE = "AEE"
    PARTICULAR = "PARTICULAR"


class StatusAssinatura(str, Enum):
    TRIAL = "trial"
    ATIVA = "ativa"
    PENDENTE = "pendente"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"
    SUSPENSA = "suspensa"


class StatusFatura(str, Enum):
    PENDENTE = "pendente"
    PAGA = "paga"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"


# ==========================================
# PLANO
# ==========================================

class PlanoBase(BaseModel):
    nome: str
    slug: str
    descricao: Optional[str] = None
    valor: float
    valor_anual: Optional[float] = None
    limite_alunos: int = 50
    limite_professores: int = 5
    limite_provas_mes: int = 100
    limite_materiais_mes: int = 100
    limite_peis_mes: int = 50
    limite_relatorios_mes: int = 50
    pei_automatico: bool = True
    materiais_adaptativos: bool = True
    mapas_mentais: bool = True
    relatorios_avancados: bool = False
    api_access: bool = False
    suporte_prioritario: bool = False
    treinamento_incluido: bool = False
    integracao_whatsapp: bool = False
    integracao_google: bool = False
    exportacao_pdf: bool = True
    exportacao_excel: bool = True


class PlanoCreate(PlanoBase):
    pass


class PlanoResponse(PlanoBase):
    id: int
    ativo: bool
    destaque: bool
    ordem: int
    created_at: datetime

    class Config:
        from_attributes = True


class PlanoPublico(BaseModel):
    """Plano para exibição pública (checkout)"""
    id: int
    nome: str
    slug: str
    descricao: Optional[str]
    valor: float
    valor_anual: Optional[float]
    limite_alunos: int
    limite_professores: int
    limite_provas_mes: int
    limite_materiais_mes: int
    limite_peis_mes: int
    pei_automatico: bool
    materiais_adaptativos: bool
    mapas_mentais: bool
    relatorios_avancados: bool
    suporte_prioritario: bool
    destaque: bool
    ordem: int

    class Config:
        from_attributes = True


# ==========================================
# ESCOLA
# ==========================================

class EscolaBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=255)
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    tipo: TipoEscola = TipoEscola.ESCOLA
    segmento: Optional[str] = None
    email: EmailStr
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    site: Optional[str] = None


class EscolaCreate(EscolaBase):
    """Dados para criar uma nova escola"""
    plano_id: int = Field(..., description="ID do plano escolhido")
    
    # Endereço opcional
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class EscolaUpdate(BaseModel):
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    tipo: Optional[TipoEscola] = None
    segmento: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    site: Optional[str] = None
    logo: Optional[str] = None
    cor_primaria: Optional[str] = None
    cor_secundaria: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class EscolaResponse(EscolaBase):
    id: int
    logo: Optional[str]
    cor_primaria: str
    cor_secundaria: str
    ativa: bool
    cep: Optional[str]
    logradouro: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    asaas_customer_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class EscolaComAssinatura(EscolaResponse):
    """Escola com dados da assinatura"""
    assinatura: Optional["AssinaturaResponse"] = None
    total_alunos: int = 0
    total_professores: int = 0


# ==========================================
# ASSINATURA
# ==========================================

class AssinaturaBase(BaseModel):
    status: StatusAssinatura = StatusAssinatura.TRIAL
    valor_mensal: float
    desconto_percentual: float = 0
    dia_vencimento: int = 10
    forma_pagamento: Optional[str] = None


class AssinaturaCreate(BaseModel):
    escola_id: int
    plano_id: int


class AssinaturaUpdate(BaseModel):
    plano_id: Optional[int] = None
    status: Optional[StatusAssinatura] = None
    dia_vencimento: Optional[int] = None
    forma_pagamento: Optional[str] = None
    desconto_percentual: Optional[float] = None


class AssinaturaResponse(BaseModel):
    id: int
    escola_id: int
    plano_id: int
    status: str
    data_inicio: datetime
    data_fim: Optional[datetime]
    data_proxima_cobranca: Optional[datetime]
    valor_mensal: float
    desconto_percentual: float
    dia_vencimento: int
    forma_pagamento: Optional[str]
    
    # Uso atual
    alunos_ativos: int
    professores_ativos: int
    provas_mes_atual: int
    materiais_mes_atual: int
    peis_mes_atual: int
    relatorios_mes_atual: int
    
    # Integração
    asaas_subscription_id: Optional[str]
    
    # Plano
    plano: Optional[PlanoResponse] = None
    
    created_at: datetime

    class Config:
        from_attributes = True


class AssinaturaComLimites(AssinaturaResponse):
    """Assinatura com informações de limites"""
    limite_alunos: int = 0
    limite_professores: int = 0
    limite_provas_mes: int = 0
    limite_materiais_mes: int = 0
    limite_peis_mes: int = 0
    
    # Percentuais de uso
    uso_alunos_percentual: float = 0
    uso_professores_percentual: float = 0
    uso_provas_percentual: float = 0
    uso_materiais_percentual: float = 0
    uso_peis_percentual: float = 0


# ==========================================
# FATURA
# ==========================================

class FaturaBase(BaseModel):
    valor: float
    data_vencimento: datetime
    observacoes: Optional[str] = None


class FaturaCreate(FaturaBase):
    assinatura_id: int


class FaturaResponse(BaseModel):
    id: int
    assinatura_id: int
    numero: str
    valor: float
    valor_pago: Optional[float]
    status: str
    data_emissao: datetime
    data_vencimento: datetime
    data_pagamento: Optional[datetime]
    metodo_pagamento: Optional[str]
    link_pagamento: Optional[str]
    codigo_pix: Optional[str]
    linha_digitavel: Optional[str]
    nota_fiscal: Optional[str]
    asaas_payment_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# CHECKOUT / ONBOARDING
# ==========================================

class CheckoutRequest(BaseModel):
    """Dados para iniciar processo de checkout"""
    plano_id: int = Field(..., description="ID do plano escolhido")
    
    # Dados da escola
    escola_nome: str = Field(..., min_length=3, max_length=255)
    escola_cnpj: Optional[str] = None
    escola_tipo: TipoEscola = TipoEscola.ESCOLA
    
    # Dados do administrador
    admin_nome: str = Field(..., min_length=3, max_length=255)
    admin_email: EmailStr
    admin_senha: str = Field(..., min_length=6)
    admin_telefone: Optional[str] = None
    
    # Endereço (opcional para trial)
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None


class CheckoutResponse(BaseModel):
    """Resposta do checkout"""
    success: bool
    message: str
    escola_id: Optional[int] = None
    usuario_id: Optional[int] = None
    assinatura_id: Optional[int] = None
    status: StatusAssinatura = StatusAssinatura.TRIAL
    trial_dias: int = 14
    link_pagamento: Optional[str] = None
    token: Optional[str] = None  # JWT para login automático


# ==========================================
# DASHBOARD ADMIN
# ==========================================

class DashboardEscola(BaseModel):
    """Dados do dashboard da escola"""
    escola: EscolaResponse
    assinatura: AssinaturaComLimites
    
    # Estatísticas
    total_alunos: int
    total_professores: int
    provas_criadas_mes: int
    materiais_criados_mes: int
    peis_gerados_mes: int
    
    # Alertas
    dias_restantes_trial: Optional[int] = None
    proxima_fatura: Optional[FaturaResponse] = None
    alertas: List[str] = []


# Update forward refs
EscolaComAssinatura.model_rebuild()
