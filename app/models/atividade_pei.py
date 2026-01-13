# ============================================
# MODEL - Atividades do PEI (Calendário)
# ============================================

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.database import Base


class TipoAtividade(str, enum.Enum):
    """Tipos de atividade no calendário"""
    MATERIAL = "material"           # Estudar um material
    EXERCICIO = "exercicio"         # Fazer exercícios
    PROVA = "prova"                 # Realizar prova
    REVISAO = "revisao"             # Revisão de conteúdo
    ATIVIDADE_PRATICA = "pratica"   # Atividade prática


class StatusAtividade(str, enum.Enum):
    """Status da atividade"""
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    ATRASADA = "atrasada"
    CANCELADA = "cancelada"


class AtividadePEI(Base):
    """
    Atividades do calendário vinculadas ao PEI.
    Cada objetivo do PEI pode ter múltiplas atividades (materiais, exercícios, provas).
    """
    __tablename__ = "atividades_pei"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Vínculos
    pei_id = Column(Integer, ForeignKey("peis.id", ondelete="CASCADE"), nullable=False)
    objetivo_id = Column(Integer, ForeignKey("pei_objetivos.id", ondelete="CASCADE"), nullable=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Vínculos opcionais com materiais/provas existentes
    material_id = Column(Integer, ForeignKey("materiais.id", ondelete="SET NULL"), nullable=True)
    material_aluno_id = Column(Integer, ForeignKey("materiais_alunos.id", ondelete="SET NULL"), nullable=True)
    prova_id = Column(Integer, ForeignKey("provas.id", ondelete="SET NULL"), nullable=True)
    prova_aluno_id = Column(Integer, ForeignKey("provas_alunos.id", ondelete="SET NULL"), nullable=True)
    
    # Dados da atividade
    tipo = Column(Enum(TipoAtividade), nullable=False, default=TipoAtividade.MATERIAL)
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    
    # Datas
    data_programada = Column(Date, nullable=False)
    data_inicio = Column(DateTime, nullable=True)  # Quando o aluno começou
    data_conclusao = Column(DateTime, nullable=True)  # Quando concluiu
    
    # Status e progresso
    status = Column(Enum(StatusAtividade), nullable=False, default=StatusAtividade.PENDENTE)
    duracao_estimada_min = Column(Integer, nullable=True)  # Duração estimada em minutos
    ordem_sequencial = Column(Integer, nullable=True)  # Ordem dentro do objetivo
    
    # Dados adicionais
    instrucoes = Column(Text, nullable=True)  # Instruções específicas
    adaptacoes = Column(JSON, nullable=True)  # Adaptações para o aluno
    resultado = Column(JSON, nullable=True)  # Resultado/nota se for prova
    observacoes_professor = Column(Text, nullable=True)
    
    # Metadados
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    pei = relationship("PEI", back_populates="atividades")
    objetivo = relationship("PEIObjetivo", back_populates="atividades")
    student = relationship("Student")
    
    def __repr__(self):
        return f"<AtividadePEI {self.id}: {self.titulo} ({self.tipo.value})>"


class SequenciaObjetivo(Base):
    """
    Define a sequência de atividades para cada objetivo do PEI.
    Gerado automaticamente pela IA ao criar o planejamento.
    """
    __tablename__ = "sequencias_objetivo"
    
    id = Column(Integer, primary_key=True, index=True)
    
    objetivo_id = Column(Integer, ForeignKey("pei_objetivos.id", ondelete="CASCADE"), nullable=False)
    
    # Configuração da sequência
    total_semanas = Column(Integer, default=4)  # Semanas para concluir o objetivo
    total_materiais = Column(Integer, default=2)  # Quantidade de materiais
    total_exercicios = Column(Integer, default=2)  # Quantidade de exercícios
    incluir_prova = Column(Boolean, default=True)  # Incluir prova final
    
    # Dados gerados pela IA
    plano_sequencial = Column(JSON, nullable=True)  # Plano detalhado semana a semana
    
    # Status
    gerado = Column(Boolean, default=False)
    data_geracao = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relacionamento
    objetivo = relationship("PEIObjetivo", back_populates="sequencia")
