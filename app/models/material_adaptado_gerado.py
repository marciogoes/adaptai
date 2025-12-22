"""
Model para Materiais Adaptados Gerados
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class MaterialAdaptadoGerado(Base):
    """
    Tabela para armazenar materiais adaptados gerados pela IA
    Salva o resultado completo em JSON
    """
    __tablename__ = "materiais_adaptados_gerados"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Metadados da geração
    disciplina = Column(String(100), nullable=False)
    serie = Column(String(50), nullable=False)
    conteudo = Column(String(255), nullable=False)
    tipos_material = Column(JSON, nullable=False)  # Lista de tipos gerados
    
    # Resultado completo em JSON
    resultado_json = Column(JSON, nullable=False)
    
    # Informações de geração
    tempo_geracao = Column(Integer, nullable=True)  # Em segundos
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    student = relationship("Student", back_populates="materiais_adaptados_gerados")
    creator = relationship("User")
    
    def __repr__(self):
        return f"<MaterialAdaptadoGerado(id={self.id}, student_id={self.student_id}, disciplina={self.disciplina}, conteudo={self.conteudo})>"
