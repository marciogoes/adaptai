"""
📔 Model - Diário de Aprendizagem Inteligente
Registra o que o aluno estudou diariamente e a IA extrai insights
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, JSON, Boolean, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
import enum


class HumorEstudo(str, enum.Enum):
    """Como o aluno se sentiu durante o estudo"""
    MUITO_BEM = "muito_bem"
    BEM = "bem"
    NEUTRO = "neutro"
    DIFICIL = "dificil"
    MUITO_DIFICIL = "muito_dificil"


class NivelCompreensao(str, enum.Enum):
    """Nível de compreensão auto-avaliado"""
    DOMINEI = "dominei"
    ENTENDI_BEM = "entendi_bem"
    ENTENDI_PARCIAL = "entendi_parcial"
    TENHO_DUVIDAS = "tenho_duvidas"
    NAO_ENTENDI = "nao_entendi"


class DiarioAprendizagem(Base):
    """
    📔 Registro diário do que o aluno estudou
    Professor ou responsável pode registrar, IA analisa e extrai conteúdos
    """
    __tablename__ = "diario_aprendizagem"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    
    # Data e período
    data_estudo = Column(Date, nullable=False, index=True)
    periodo = Column(String(20), default="integral")  # manha, tarde, noite, integral
    
    # Registro livre do que foi estudado
    registro_texto = Column(Text, nullable=False)  # Texto livre: "Hoje estudamos frações..."
    
    # Auto-avaliação (opcional)
    humor = Column(SQLEnum(HumorEstudo), nullable=True)
    nivel_compreensao = Column(SQLEnum(NivelCompreensao), nullable=True)
    tempo_estudo_minutos = Column(Integer, nullable=True)
    
    # Campos preenchidos pela IA
    ia_processado = Column(Boolean, default=False)
    ia_disciplinas_detectadas = Column(JSON, nullable=True)  # ["Matemática", "Português"]
    ia_topicos_extraidos = Column(JSON, nullable=True)  # [{"disciplina": "Mat", "topicos": [...]}]
    ia_conceitos_chave = Column(JSON, nullable=True)  # ["frações", "numerador", "denominador"]
    ia_dificuldades_identificadas = Column(JSON, nullable=True)  # Dificuldades mencionadas
    ia_pontos_positivos = Column(JSON, nullable=True)  # O que foi bem
    ia_sugestoes_revisao = Column(JSON, nullable=True)  # Sugestões de revisão
    ia_conexoes_bncc = Column(JSON, nullable=True)  # Códigos BNCC relacionados
    ia_sentimento_geral = Column(String(50), nullable=True)  # positivo, neutro, negativo
    ia_resumo = Column(Text, nullable=True)  # Resumo gerado pela IA
    ia_tags = Column(JSON, nullable=True)  # Tags para busca
    
    # Metadados
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    
    # Relacionamentos
    student = relationship("Student", back_populates="diarios_aprendizagem")
    creator = relationship("User")
    conteudos = relationship("ConteudoExtraido", back_populates="diario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DiarioAprendizagem(id={self.id}, student_id={self.student_id}, data={self.data_estudo})>"


class ConteudoExtraido(Base):
    """
    📚 Conteúdos específicos extraídos do diário pela IA
    Cada registro representa um tópico/conceito identificado
    Serve como insumo para geração de materiais
    """
    __tablename__ = "conteudos_extraidos"
    
    id = Column(Integer, primary_key=True, index=True)
    diario_id = Column(Integer, ForeignKey("diario_aprendizagem.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    
    # Categorização
    disciplina = Column(String(100), nullable=False, index=True)
    area_conhecimento = Column(String(100), nullable=True)  # Exatas, Humanas, Linguagens, etc
    
    # Conteúdo
    topico = Column(String(255), nullable=False)
    subtopicos = Column(JSON, nullable=True)  # Lista de subtópicos
    conceitos = Column(JSON, nullable=True)  # Conceitos relacionados
    
    # Contexto
    contexto_original = Column(Text, nullable=True)  # Trecho do diário
    nivel_dificuldade_percebido = Column(String(50), nullable=True)
    
    # BNCC
    codigo_bncc = Column(String(20), nullable=True)
    habilidade_bncc = Column(Text, nullable=True)
    
    # Para geração de materiais
    prioridade_revisao = Column(Integer, default=0)  # 0-10, quanto maior mais prioritário
    vezes_mencionado = Column(Integer, default=1)  # Quantas vezes apareceu nos diários
    ultima_mencao = Column(Date, nullable=True)
    
    # Status
    material_gerado = Column(Boolean, default=False)
    material_id = Column(Integer, nullable=True)  # ID do material gerado
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relacionamentos
    diario = relationship("DiarioAprendizagem", back_populates="conteudos")
    student = relationship("Student")
    
    def __repr__(self):
        return f"<ConteudoExtraido(id={self.id}, disciplina={self.disciplina}, topico={self.topico})>"


class ResumoSemanalAprendizagem(Base):
    """
    📊 Resumo semanal gerado pela IA
    Consolida todos os diários da semana
    """
    __tablename__ = "resumos_semanais_aprendizagem"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    
    # Período
    semana_inicio = Column(Date, nullable=False)
    semana_fim = Column(Date, nullable=False)
    ano = Column(Integer, nullable=False)
    numero_semana = Column(Integer, nullable=False)
    
    # Estatísticas
    total_registros = Column(Integer, default=0)
    total_minutos_estudo = Column(Integer, default=0)
    disciplinas_estudadas = Column(JSON, nullable=True)  # {"Matemática": 5, "Português": 3}
    
    # Análise da IA
    resumo_geral = Column(Text, nullable=True)
    principais_conquistas = Column(JSON, nullable=True)
    areas_atencao = Column(JSON, nullable=True)
    recomendacoes = Column(JSON, nullable=True)
    progresso_observado = Column(Text, nullable=True)
    
    # Gráficos (dados para frontend)
    dados_grafico_disciplinas = Column(JSON, nullable=True)
    dados_grafico_humor = Column(JSON, nullable=True)
    dados_grafico_tempo = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relacionamentos
    student = relationship("Student")
    
    def __repr__(self):
        return f"<ResumoSemanal(student_id={self.student_id}, semana={self.numero_semana}/{self.ano})>"
