"""
📝 AdaptAI - Schemas de Redação
Validação de dados para redações estilo ENEM
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class StatusRedacaoEnum(str, Enum):
    RASCUNHO = "rascunho"
    SUBMETIDA = "submetida"
    CORRIGINDO = "corrigindo"
    CORRIGIDA = "corrigida"
    ERRO = "erro"


# ========================================
# SCHEMAS DE CRIAÇÃO
# ========================================

class GerarTemaRequest(BaseModel):
    """Solicitar geração de tema pela IA"""
    area_tematica: Optional[str] = Field(None, description="Área: tecnologia, meio_ambiente, saude, educacao, etc.")
    nivel_dificuldade: str = Field("medio", description="facil, medio, dificil")
    aluno_ids: Optional[List[int]] = Field(None, description="IDs dos alunos para atribuir")


class TemaRedacaoCreate(BaseModel):
    """Criar tema manualmente"""
    titulo: str = Field(..., min_length=10, max_length=500)
    tema_completo: str = Field(..., min_length=100)
    textos_motivadores: Optional[List[str]] = None
    area_tematica: Optional[str] = None
    nivel_dificuldade: str = Field("medio")
    aluno_ids: Optional[List[int]] = None


class IniciarRedacaoRequest(BaseModel):
    """Aluno inicia uma redação"""
    tema_id: int
    aluno_id: int


class SalvarRascunhoRequest(BaseModel):
    """Salvar rascunho da redação"""
    redacao_id: int
    titulo_redacao: Optional[str] = Field(None, max_length=255)
    texto: str


class SubmeterRedacaoRequest(BaseModel):
    """Submeter redação para correção"""
    redacao_id: int
    titulo_redacao: Optional[str] = Field(None, max_length=255)
    texto: str = Field(..., min_length=100, description="Mínimo 100 caracteres")


# ========================================
# SCHEMAS DE RESPOSTA
# ========================================

class CompetenciaENEM(BaseModel):
    """Uma competência do ENEM"""
    numero: int
    nome: str
    descricao: str
    nota: int  # 0-200
    nivel: int  # 0-5
    nivel_texto: str  # "Nível 5", "Nível 4", etc.
    comentario: str
    detalhes: Optional[Dict[str, Any]] = None


class TemaRedacaoResponse(BaseModel):
    """Resposta do tema"""
    id: int
    titulo: str
    tema_completo: str
    textos_motivadores: Optional[List[str]]
    area_tematica: Optional[str]
    nivel_dificuldade: str
    ativo: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class CorrecaoRedacaoResponse(BaseModel):
    """Resposta da correção"""
    id: int
    redacao_id: int
    
    # Competências
    comp1_nota: int
    comp1_nivel: int
    comp1_comentario: Optional[str]
    
    comp2_nota: int
    comp2_nivel: int
    comp2_comentario: Optional[str]
    
    comp3_nota: int
    comp3_nivel: int
    comp3_comentario: Optional[str]
    
    comp4_nota: int
    comp4_nivel: int
    comp4_comentario: Optional[str]
    
    comp5_nota: int
    comp5_nivel: int
    comp5_comentario: Optional[str]
    
    nota_total: int
    
    feedback_geral: Optional[str]
    pontos_fortes: Optional[List[str]]
    pontos_melhorar: Optional[List[str]]
    sugestoes_estudo: Optional[List[str]]
    
    corrigida_em: datetime

    model_config = ConfigDict(from_attributes=True)


class RedacaoResponse(BaseModel):
    """Resposta da redação"""
    id: int
    tema_id: int
    aluno_id: int
    titulo_redacao: Optional[str]
    texto: Optional[str]
    quantidade_palavras: int
    quantidade_linhas: int
    status: StatusRedacaoEnum
    iniciada_em: datetime
    submetida_em: Optional[datetime]
    corrigida_em: Optional[datetime]
    tempo_escrita_minutos: Optional[int]
    
    # Nested
    tema: Optional[TemaRedacaoResponse] = None
    correcao: Optional[CorrecaoRedacaoResponse] = None
    aluno_nome: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CorrecaoCompletaResponse(BaseModel):
    """Correção completa formatada"""
    redacao_id: int
    nota_final: int  # 0-1000
    percentual: float  # 0-100%
    classificacao: str  # "Excelente", "Bom", "Regular", etc.
    
    competencias: List[CompetenciaENEM]
    
    feedback_geral: str
    pontos_fortes: List[str]
    pontos_melhorar: List[str]
    sugestoes_estudo: List[str]
    
    estatisticas: Dict[str, Any]  # palavras, linhas, parágrafos

    model_config = ConfigDict(from_attributes=True)


class HistoricoRedacoesResponse(BaseModel):
    """Histórico de redações do aluno"""
    total_redacoes: int
    total_corrigidas: int
    media_geral: Optional[float]
    melhor_nota: Optional[int]
    evolucao: List[Dict[str, Any]]  # Evolução das notas
    media_por_competencia: Dict[str, float]
    redacoes: List[RedacaoResponse]

    model_config = ConfigDict(from_attributes=True)


class TemaListResponse(BaseModel):
    """Lista resumida de temas"""
    id: int
    titulo: str
    area_tematica: Optional[str]
    nivel_dificuldade: str
    criado_em: datetime
    total_redacoes: int
    total_corrigidas: int
    media_notas: Optional[float]

    model_config = ConfigDict(from_attributes=True)
