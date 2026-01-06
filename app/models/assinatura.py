# ============================================
# MODELO DE ASSINATURA E FATURA
# ============================================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class StatusAssinatura(str, enum.Enum):
    TRIAL = "trial"           # Período de teste (7-14 dias)
    ATIVA = "ativa"           # Assinatura ativa e paga
    PENDENTE = "pendente"     # Aguardando pagamento
    ATRASADA = "atrasada"     # Pagamento em atraso
    CANCELADA = "cancelada"   # Assinatura cancelada
    SUSPENSA = "suspensa"     # Suspensa por inadimplência


class Assinatura(Base):
    """
    Assinatura de uma escola a um plano.
    """
    __tablename__ = "assinaturas"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamentos
    escola_id = Column(Integer, ForeignKey("escolas.id"), unique=True, nullable=False)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)
    
    # Status e período
    status = Column(String(20), default=StatusAssinatura.TRIAL.value)
    data_inicio = Column(DateTime(timezone=True), server_default=func.now())
    data_fim = Column(DateTime(timezone=True), nullable=True)
    data_proxima_cobranca = Column(DateTime(timezone=True), nullable=True)
    
    # Valores
    valor_mensal = Column(Float, nullable=False)
    desconto_percentual = Column(Float, default=0)
    dia_vencimento = Column(Integer, default=10)
    forma_pagamento = Column(String(50), nullable=True)  # PIX, BOLETO, CARTAO
    
    # Uso atual (resetado mensalmente)
    alunos_ativos = Column(Integer, default=0)
    professores_ativos = Column(Integer, default=0)
    provas_mes_atual = Column(Integer, default=0)
    materiais_mes_atual = Column(Integer, default=0)
    peis_mes_atual = Column(Integer, default=0)
    relatorios_mes_atual = Column(Integer, default=0)
    
    # Cancelamento
    cancelada_em = Column(DateTime(timezone=True), nullable=True)
    motivo_cancelamento = Column(Text, nullable=True)
    
    # Integração Asaas
    asaas_subscription_id = Column(String(100), nullable=True)
    asaas_customer_id = Column(String(100), nullable=True)
    asaas_payment_link_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    escola = relationship("Escola", back_populates="assinatura")
    plano = relationship("Plano", back_populates="assinaturas")
    faturas = relationship("Fatura", back_populates="assinatura", cascade="all, delete-orphan")


class StatusFatura(str, enum.Enum):
    PENDENTE = "pendente"
    PAGA = "paga"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"


class Fatura(Base):
    """
    Faturas geradas para cobrança.
    """
    __tablename__ = "faturas"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamento
    assinatura_id = Column(Integer, ForeignKey("assinaturas.id"), nullable=False)
    
    # Identificação
    numero = Column(String(50), unique=True, nullable=False)
    
    # Valores
    valor = Column(Float, nullable=False)
    valor_pago = Column(Float, nullable=True)
    
    # Status e datas
    status = Column(String(20), default=StatusFatura.PENDENTE.value)
    data_emissao = Column(DateTime(timezone=True), server_default=func.now())
    data_vencimento = Column(DateTime(timezone=True), nullable=False)
    data_pagamento = Column(DateTime(timezone=True), nullable=True)
    
    # Pagamento
    metodo_pagamento = Column(String(50), nullable=True)
    link_pagamento = Column(String(500), nullable=True)
    codigo_pix = Column(Text, nullable=True)
    linha_digitavel = Column(String(100), nullable=True)
    
    # Nota fiscal
    nota_fiscal = Column(String(255), nullable=True)
    
    # Observações
    observacoes = Column(Text, nullable=True)
    
    # Integração Asaas
    asaas_payment_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assinatura = relationship("Assinatura", back_populates="faturas")
