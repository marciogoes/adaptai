# ============================================
# SCHEMAS - ESCOLA (TENANT)
# ============================================
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EscolaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=255)
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    tipo: Optional[str] = "ESCOLA"
    segmento: Optional[str] = None
    email: EmailStr
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    site: Optional[str] = None


class EscolaCreate(EscolaBase):
    # Endereço
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    
    # Branding
    cor_primaria: Optional[str] = "#8B5CF6"
    cor_secundaria: Optional[str] = "#EC4899"
    
    # Plano inicial (slug)
    plano_slug: Optional[str] = "profissional"


class EscolaUpdate(BaseModel):
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    tipo: Optional[str] = None
    segmento: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    site: Optional[str] = None
    
    # Endereço
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    
    # Branding
    logo: Optional[str] = None
    cor_primaria: Optional[str] = None
    cor_secundaria: Optional[str] = None


class EscolaResponse(EscolaBase):
    id: int
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    logo: Optional[str] = None
    cor_primaria: str
    cor_secundaria: str
    ativa: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EscolaComAssinatura(EscolaResponse):
    """Escola com dados da assinatura"""
    assinatura: Optional["AssinaturaResponse"] = None
    
    class Config:
        from_attributes = True


# ============================================
# SCHEMAS - CONFIGURAÇÃO ESCOLA
# ============================================

class ConfiguracaoEscolaBase(BaseModel):
    modelo_ia_preferido: Optional[str] = "claude-3-haiku-20240307"
    quantidade_questoes_padrao: Optional[int] = 5
    dificuldade_padrao: Optional[str] = "medio"
    notificacoes_email: Optional[bool] = True
    notificacoes_whatsapp: Optional[bool] = False
    pei_automatico_ativo: Optional[bool] = True
    materiais_adaptativos_ativo: Optional[bool] = True
    relatorios_avancados_ativo: Optional[bool] = True
    lgpd_ativo: Optional[bool] = True


class ConfiguracaoEscolaUpdate(ConfiguracaoEscolaBase):
    pass


class ConfiguracaoEscolaResponse(ConfiguracaoEscolaBase):
    id: int
    escola_id: int
    termo_aceito_em: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Import circular fix
from app.schemas.assinatura import AssinaturaResponse
EscolaComAssinatura.model_rebuild()
