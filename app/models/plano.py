# ============================================
# MODELO DE PLANO
# ============================================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Plano(Base):
    """
    Planos de assinatura disponíveis no sistema.
    """
    __tablename__ = "planos"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação
    nome = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)  # essencial, profissional, institucional
    descricao = Column(Text, nullable=True)
    
    # Preço
    valor = Column(Float, nullable=False)  # Valor mensal em R$
    valor_anual = Column(Float, nullable=True)  # Desconto para pagamento anual
    
    # Limites
    limite_alunos = Column(Integer, default=50)
    limite_professores = Column(Integer, default=5)
    limite_provas_mes = Column(Integer, default=100)
    limite_materiais_mes = Column(Integer, default=100)
    limite_peis_mes = Column(Integer, default=50)
    limite_relatorios_mes = Column(Integer, default=50)
    
    # Funcionalidades
    pei_automatico = Column(Boolean, default=True)
    materiais_adaptativos = Column(Boolean, default=True)
    mapas_mentais = Column(Boolean, default=True)
    relatorios_avancados = Column(Boolean, default=False)
    api_access = Column(Boolean, default=False)
    suporte_prioritario = Column(Boolean, default=False)
    treinamento_incluido = Column(Boolean, default=False)
    
    # Integrações
    integracao_whatsapp = Column(Boolean, default=False)
    integracao_google = Column(Boolean, default=False)
    exportacao_pdf = Column(Boolean, default=True)
    exportacao_excel = Column(Boolean, default=True)
    
    # Status
    ativo = Column(Boolean, default=True)
    destaque = Column(Boolean, default=False)  # Plano recomendado
    ordem = Column(Integer, default=0)  # Ordem de exibição
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assinaturas = relationship("Assinatura", back_populates="plano")
