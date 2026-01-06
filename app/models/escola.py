# ============================================
# MODELO DE ESCOLA/INSTITUIÇÃO (TENANT)
# ============================================
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Escola(Base):
    """
    Modelo principal para multi-tenancy.
    Cada escola é um tenant isolado no sistema.
    """
    __tablename__ = "escolas"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    
    # Dados básicos
    nome = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=True)
    cnpj = Column(String(18), unique=True, nullable=True, index=True)
    razao_social = Column(String(255), nullable=True)
    
    # Tipo de instituição
    tipo = Column(String(50), default="ESCOLA")  # ESCOLA, CLINICA, CENTRO_TERAPEUTICO
    segmento = Column(String(100), nullable=True)  # Educação Especial, AEE, etc.
    
    # Contato
    email = Column(String(255), nullable=False, unique=True)
    telefone = Column(String(20), nullable=True)
    whatsapp = Column(String(20), nullable=True)
    site = Column(String(255), nullable=True)
    
    # Endereço
    cep = Column(String(10), nullable=True)
    logradouro = Column(String(255), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    
    # Branding
    logo = Column(String(500), nullable=True)
    cor_primaria = Column(String(7), default="#8B5CF6")  # Roxo AdaptAI
    cor_secundaria = Column(String(7), default="#EC4899")  # Rosa
    
    # Status
    ativa = Column(Boolean, default=True)
    data_fundacao = Column(DateTime(timezone=True), nullable=True)
    
    # Integração Asaas (pagamentos)
    asaas_customer_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    usuarios = relationship("User", back_populates="escola")
    alunos = relationship("Student", back_populates="escola")
    assinatura = relationship("Assinatura", back_populates="escola", uselist=False)
    configuracao = relationship("ConfiguracaoEscola", back_populates="escola", uselist=False)


class ConfiguracaoEscola(Base):
    """
    Configurações específicas de cada escola
    """
    __tablename__ = "configuracoes_escola"
    __table_args__ = {'schema': None}

    id = Column(Integer, primary_key=True, index=True)
    escola_id = Column(Integer, ForeignKey("escolas.id"), nullable=False, unique=True)
    
    # Preferências pedagógicas
    modelo_ia_preferido = Column(String(100), default="claude-3-haiku-20240307")
    quantidade_questoes_padrao = Column(Integer, default=5)
    dificuldade_padrao = Column(String(20), default="medio")
    
    # Notificações
    notificacoes_email = Column(Boolean, default=True)
    notificacoes_whatsapp = Column(Boolean, default=False)
    
    # Funcionalidades
    pei_automatico_ativo = Column(Boolean, default=True)
    materiais_adaptativos_ativo = Column(Boolean, default=True)
    relatorios_avancados_ativo = Column(Boolean, default=True)
    
    # LGPD
    lgpd_ativo = Column(Boolean, default=True)
    termo_aceito_em = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    escola = relationship("Escola", back_populates="configuracao")
