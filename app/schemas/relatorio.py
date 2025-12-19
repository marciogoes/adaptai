"""
Schemas para Relatórios de Terapias e Acompanhamento
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class RelatorioBase(BaseModel):
    """Base para Relatório"""
    tipo: str
    profissional_nome: Optional[str] = None
    profissional_registro: Optional[str] = None
    profissional_especialidade: Optional[str] = None
    data_emissao: Optional[datetime] = None
    data_validade: Optional[datetime] = None
    cid: Optional[str] = None
    resumo: Optional[str] = None


class RelatorioCreate(RelatorioBase):
    """Criar relatório"""
    student_id: int
    arquivo_nome: Optional[str] = None
    arquivo_tipo: Optional[str] = None
    arquivo_base64: Optional[str] = None
    dados_extraidos: Optional[Dict[str, Any]] = None
    condicoes: Optional[Dict[str, Any]] = None


class RelatorioUpdate(BaseModel):
    """Atualizar relatório"""
    tipo: Optional[str] = None
    profissional_nome: Optional[str] = None
    profissional_registro: Optional[str] = None
    profissional_especialidade: Optional[str] = None
    data_emissao: Optional[datetime] = None
    data_validade: Optional[datetime] = None
    cid: Optional[str] = None
    resumo: Optional[str] = None


class RelatorioResponse(RelatorioBase):
    """Resposta de relatório"""
    id: int
    student_id: int
    arquivo_nome: Optional[str] = None
    arquivo_tipo: Optional[str] = None
    dados_extraidos: Optional[Dict[str, Any]] = None
    condicoes: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Dados do aluno (para listagem)
    student_name: Optional[str] = None

    class Config:
        from_attributes = True


class RelatorioComArquivo(RelatorioResponse):
    """Relatório com arquivo base64 (para download)"""
    arquivo_base64: Optional[str] = None

    class Config:
        from_attributes = True


class RelatorioListResponse(BaseModel):
    """Lista de relatórios"""
    total: int
    relatorios: List[RelatorioResponse]


class AnalisarRelatorioRequest(BaseModel):
    """Request para analisar relatório com IA"""
    student_id: int


class RelatorioResumo(BaseModel):
    """Resumo de relatório para uso no PEI"""
    id: int
    tipo: str
    profissional_nome: Optional[str] = None
    profissional_especialidade: Optional[str] = None
    data_emissao: Optional[datetime] = None
    resumo: Optional[str] = None
    condicoes: Optional[Dict[str, Any]] = None
    dados_extraidos: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
