# ============================================
# MODEL - Registro Diário de Aulas
# ============================================
"""
Sistema para importar e armazenar registros diários
de aulas a partir de PDFs de relatórios escolares.
"""

from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from app.database import Base


class RegistroDiario(Base):
    """
    Registro diário de aulas importado de PDF.
    Armazena os dados extraídos do relatório da escola.
    """
    __tablename__ = "registros_diarios"
    __table_args__ = {'schema': None}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Quem importou
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Aluno relacionado (opcional - pode ser para turma inteira)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True, index=True)
    
    # Dados do relatório
    data_aula = Column(Date, nullable=False, index=True)
    serie_turma = Column(String(50), nullable=True)  # Ex: "9º ANO"
    escola_origem = Column(String(255), nullable=True)  # Nome da escola do PDF
    
    # Arquivo original
    arquivo_pdf = Column(String(500), nullable=True)  # Path do arquivo
    
    # Dados extraídos (JSON com todas as aulas)
    conteudo_extraido = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    professor = relationship("User", foreign_keys=[professor_id])
    student = relationship("Student", foreign_keys=[student_id])
    aulas = relationship("AulaRegistrada", back_populates="registro", cascade="all, delete-orphan")


class AulaRegistrada(Base):
    """
    Uma aula específica extraída do relatório diário.
    Cada linha do relatório vira um registro aqui.
    """
    __tablename__ = "aulas_registradas"
    __table_args__ = {'schema': None}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Registro pai
    registro_id = Column(Integer, ForeignKey("registros_diarios.id", ondelete="CASCADE"), nullable=False)
    
    # Dados da aula
    professor_nome = Column(String(255), nullable=True)  # Nome do professor da matéria
    disciplina = Column(String(100), nullable=False, index=True)
    conteudo = Column(Text, nullable=False)
    atividade_sala = Column(Text, nullable=True)
    
    # Referências do material
    livro = Column(String(100), nullable=True)
    capitulo = Column(String(100), nullable=True)
    paginas = Column(String(50), nullable=True)
    modulo = Column(String(50), nullable=True)
    
    # Indicadores
    tem_dever_casa = Column(Boolean, default=False)
    tem_atividade_avaliativa = Column(Boolean, default=False)
    dever_casa_descricao = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    registro = relationship("RegistroDiario", back_populates="aulas")
    
    def to_dict(self):
        return {
            "id": self.id,
            "professor_nome": self.professor_nome,
            "disciplina": self.disciplina,
            "conteudo": self.conteudo,
            "atividade_sala": self.atividade_sala,
            "livro": self.livro,
            "capitulo": self.capitulo,
            "paginas": self.paginas,
            "modulo": self.modulo,
            "tem_dever_casa": self.tem_dever_casa,
            "tem_atividade_avaliativa": self.tem_atividade_avaliativa,
            "dever_casa_descricao": self.dever_casa_descricao
        }
