# ============================================
# MODEL - Agenda do Professor
# ============================================
"""
Sistema de agenda para professores gerenciarem
compromissos, aulas e atividades com alunos.
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Time, ForeignKey, Boolean, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone
import enum

from app.database import Base


class TipoEvento(str, enum.Enum):
    """Tipos de evento na agenda"""
    AULA = "aula"                      # Aula regular
    ATENDIMENTO = "atendimento"        # Atendimento individual
    AVALIACAO = "avaliacao"            # Prova/avaliação
    REUNIAO = "reuniao"                # Reunião (pais, equipe, etc)
    PLANEJAMENTO = "planejamento"      # Tempo de planejamento
    TERAPIA = "terapia"                # Acompanhamento terapêutico
    OUTRO = "outro"


class StatusEvento(str, enum.Enum):
    """Status do evento"""
    AGENDADO = "agendado"
    CONFIRMADO = "confirmado"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    REAGENDADO = "reagendado"


class Recorrencia(str, enum.Enum):
    """Tipos de recorrência"""
    UNICO = "unico"           # Evento único
    DIARIO = "diario"         # Todo dia
    SEMANAL = "semanal"       # Toda semana
    QUINZENAL = "quinzenal"   # A cada 2 semanas
    MENSAL = "mensal"         # Todo mês


class AgendaProfessor(Base):
    """
    Evento na agenda do professor.
    Pode ser aula, atendimento, reunião, etc.
    """
    __tablename__ = "agenda_professor"
    __table_args__ = {'schema': None}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Quem criou o evento
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Aluno relacionado (opcional - alguns eventos não têm aluno específico)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True, index=True)
    
    # Dados do evento
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)
    tipo = Column(Enum(TipoEvento), nullable=False, default=TipoEvento.AULA)
    
    # Data e hora
    data = Column(Date, nullable=False, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=True)
    duracao_minutos = Column(Integer, default=50)  # Duração em minutos
    
    # Local
    local = Column(String(255), nullable=True)  # Sala, online, etc.
    link_online = Column(String(500), nullable=True)  # Link Zoom, Meet, etc.
    
    # Status
    status = Column(Enum(StatusEvento), default=StatusEvento.AGENDADO)
    
    # Recorrência
    recorrencia = Column(Enum(Recorrencia), default=Recorrencia.UNICO)
    recorrencia_fim = Column(Date, nullable=True)  # Até quando repetir
    evento_pai_id = Column(Integer, ForeignKey("agenda_professor.id"), nullable=True)  # Se for evento recorrente
    
    # Cor para visualização (hex)
    cor = Column(String(7), default="#8B5CF6")
    
    # Notificações
    notificar_aluno = Column(Boolean, default=True)
    notificar_responsavel = Column(Boolean, default=True)
    lembrete_minutos = Column(Integer, default=30)  # Lembrete X minutos antes
    
    # Notas e observações
    notas_privadas = Column(Text, nullable=True)  # Notas só do professor
    notas_compartilhadas = Column(Text, nullable=True)  # Notas visíveis para o aluno
    
    # Metadados
    dados_extras = Column(JSON, nullable=True)  # Dados adicionais flexíveis
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    professor = relationship("User", foreign_keys=[professor_id])
    student = relationship("Student", foreign_keys=[student_id])
    evento_pai = relationship("AgendaProfessor", remote_side=[id], backref="eventos_filhos")
    
    def __repr__(self):
        return f"<AgendaProfessor {self.id}: {self.titulo} ({self.data})>"
    
    @property
    def is_recorrente(self) -> bool:
        """Verifica se é evento recorrente"""
        return self.recorrencia != Recorrencia.UNICO


class LembreteAgenda(Base):
    """
    Lembretes enviados para eventos da agenda
    """
    __tablename__ = "lembretes_agenda"
    __table_args__ = {'schema': None}
    
    id = Column(Integer, primary_key=True, index=True)
    
    evento_id = Column(Integer, ForeignKey("agenda_professor.id", ondelete="CASCADE"), nullable=False)
    
    # Tipo de lembrete
    tipo = Column(String(50), nullable=False)  # email, whatsapp, push
    destinatario = Column(String(255), nullable=False)  # email ou telefone
    
    # Status
    enviado = Column(Boolean, default=False)
    enviado_em = Column(DateTime(timezone=True), nullable=True)
    erro = Column(Text, nullable=True)
    
    # Quando enviar (minutos antes do evento)
    minutos_antes = Column(Integer, default=30)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    evento = relationship("AgendaProfessor", backref="lembretes")
