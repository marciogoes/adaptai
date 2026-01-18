"""
🎓 AdaptAI - Schemas de Prova
Schemas Pydantic para validação de dados
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.models.prova import (
    StatusProva, 
    StatusProvaAluno, 
    DificuldadeQuestao, 
    TipoQuestao
)


# ============= SCHEMAS DE CRIAÇÃO =============

class ProvaCreate(BaseModel):
    """Schema para criar uma nova prova"""
    titulo: str = Field(..., min_length=3, max_length=200, description="Título da prova")
    descricao: Optional[str] = Field(None, description="Descrição da prova")
    conteudo_prompt: str = Field(..., min_length=10, description="Prompt/conteúdo para IA gerar questões")
    materia: str = Field(..., min_length=2, max_length=100, description="Matéria da prova")
    serie_nivel: Optional[str] = Field(None, max_length=50, description="Série/nível escolar")
    quantidade_questoes: int = Field(20, ge=1, le=100, description="Quantidade de questões")
    tipo_questao: TipoQuestao = Field(TipoQuestao.MULTIPLA_ESCOLHA, description="Tipo das questões")
    dificuldade: DificuldadeQuestao = Field(DificuldadeQuestao.MEDIO, description="Dificuldade das questões")
    tempo_limite_minutos: Optional[int] = Field(None, ge=1, description="Tempo limite em minutos")
    pontuacao_total: float = Field(10.0, ge=0, description="Pontuação total da prova")
    nota_minima_aprovacao: float = Field(6.0, ge=0, le=10, description="Nota mínima para aprovação")


class QuestaoGeradaCreate(BaseModel):
    """Schema para criar uma questão gerada"""
    numero: int = Field(..., ge=1, description="Número da questão")
    enunciado: str = Field(..., min_length=10, description="Enunciado da questão")
    tipo: TipoQuestao = Field(..., description="Tipo da questão")
    dificuldade: Optional[DificuldadeQuestao] = Field(None, description="Dificuldade")
    opcoes: Optional[List[str]] = Field(None, description="Opções de resposta")
    resposta_correta: str = Field(..., description="Resposta correta")
    criterios_avaliacao: Optional[List[str]] = Field(None, description="Critérios de avaliação")
    pontuacao: float = Field(0.5, ge=0, description="Pontos da questão")
    explicacao: Optional[str] = Field(None, description="Explicação da resposta")
    tags: Optional[List[str]] = Field(None, description="Tags/tópicos")


class ProvaAlunoCreate(BaseModel):
    """Schema para associar prova a um aluno"""
    prova_id: int = Field(..., description="ID da prova")
    aluno_id: int = Field(..., description="ID do aluno")


class RespostaAlunoCreate(BaseModel):
    """Schema para registrar resposta do aluno"""
    questao_id: int = Field(..., description="ID da questão")
    resposta_aluno: str = Field(..., description="Resposta do aluno")
    tempo_resposta_segundos: Optional[int] = Field(None, ge=0, description="Tempo de resposta")


# ============= SCHEMAS DE RESPOSTA =============

class QuestaoGeradaResponse(BaseModel):
    """Schema de resposta de questão gerada"""
    id: int
    prova_id: int
    numero: int
    enunciado: str
    tipo: TipoQuestao
    dificuldade: Optional[DificuldadeQuestao]
    opcoes: Optional[List[str]]
    resposta_correta: str
    criterios_avaliacao: Optional[List[str]]
    pontuacao: float
    explicacao: Optional[str]
    tags: Optional[List[str]]
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestaoParaAluno(BaseModel):
    """Schema de questão para o aluno (SEM resposta correta)"""
    id: int
    numero: int
    enunciado: str
    tipo: TipoQuestao
    opcoes: Optional[List[str]]
    pontuacao: float

    model_config = ConfigDict(from_attributes=True)


class ProvaResponse(BaseModel):
    """Schema de resposta de prova"""
    id: int
    titulo: str
    descricao: Optional[str]
    conteudo_prompt: str
    materia: str
    serie_nivel: Optional[str]
    quantidade_questoes: int
    tipo_questao: TipoQuestao
    dificuldade: DificuldadeQuestao
    tempo_limite_minutos: Optional[int]
    pontuacao_total: float
    nota_minima_aprovacao: float
    status: StatusProva
    criado_em: datetime
    atualizado_em: datetime
    criado_por_id: int
    questoes: List[QuestaoGeradaResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProvaParaAluno(BaseModel):
    """Schema de prova para o aluno fazer"""
    id: int
    titulo: str
    descricao: Optional[str]
    materia: str
    serie_nivel: Optional[str]
    tempo_limite_minutos: Optional[int]
    pontuacao_total: float
    questoes: List[QuestaoParaAluno] = []

    model_config = ConfigDict(from_attributes=True)


class RespostaAlunoResponse(BaseModel):
    """Schema de resposta do aluno"""
    id: int
    prova_aluno_id: int
    questao_id: int
    resposta_aluno: str
    esta_correta: Optional[bool]
    pontuacao_obtida: Optional[float]
    pontuacao_maxima: Optional[float]
    feedback: Optional[str]
    tempo_resposta_segundos: Optional[int]
    respondido_em: datetime

    model_config = ConfigDict(from_attributes=True)


class ProvaAlunoResponse(BaseModel):
    """Schema de resposta de prova do aluno"""
    id: int
    prova_id: int
    aluno_id: int
    status: StatusProvaAluno
    data_atribuicao: datetime
    data_inicio: Optional[datetime]
    data_conclusao: Optional[datetime]
    data_correcao: Optional[datetime]
    pontuacao_obtida: Optional[float]
    pontuacao_maxima: Optional[float]
    nota_final: Optional[float]
    aprovado: Optional[bool]
    tempo_gasto_minutos: Optional[int]
    analise_ia: Optional[Dict[str, Any]]
    feedback_ia: Optional[str]
    respostas: List[RespostaAlunoResponse] = []
    prova: Optional[ProvaResponse] = None

    model_config = ConfigDict(from_attributes=True)


# ============= SCHEMAS DE ATUALIZAÇÃO =============

class ProvaUpdate(BaseModel):
    """Schema para atualizar prova"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    descricao: Optional[str] = None
    status: Optional[StatusProva] = None
    tempo_limite_minutos: Optional[int] = Field(None, ge=1)
    pontuacao_total: Optional[float] = Field(None, ge=0)
    nota_minima_aprovacao: Optional[float] = Field(None, ge=0, le=10)


class ProvaAlunoUpdate(BaseModel):
    """Schema para atualizar prova do aluno"""
    status: Optional[StatusProvaAluno] = None
    data_inicio: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None


# ============= SCHEMAS ESPECIAIS =============

class GerarProvaRequest(BaseModel):
    """
    Schema para solicitar geração de prova pela IA
    
    NOVO: Aceita aluno_ids e adaptacoes para criar prova contextualizada
    """
    titulo: str = Field(..., min_length=3, description="Título da prova")
    descricao: Optional[str] = None
    conteudo_prompt: str = Field(..., min_length=20, description="Descrição do conteúdo para gerar questões")
    materia: str = Field(..., description="Matéria")
    serie_nivel: Optional[str] = None
    quantidade_questoes: int = Field(20, ge=1, le=50, description="Quantidade de questões")
    tipo_questao: TipoQuestao = Field(TipoQuestao.MULTIPLA_ESCOLHA)
    dificuldade: DificuldadeQuestao = Field(DificuldadeQuestao.MEDIO)
    tempo_limite_minutos: Optional[int] = None
    pontuacao_total: float = Field(10.0, ge=0)
    nota_minima_aprovacao: float = Field(6.0, ge=0, le=10)
    # NOVO: IDs dos alunos para associar automaticamente
    aluno_ids: Optional[List[int]] = Field(default=None, description="IDs dos alunos para associar à prova")
    # NOVO: Adaptações necessárias (TEA, TDAH, etc.)
    adaptacoes: Optional[List[str]] = Field(default=None, description="Diagnósticos/adaptações dos alunos")


class IniciarProvaRequest(BaseModel):
    """Schema para aluno iniciar prova"""
    prova_aluno_id: int = Field(..., description="ID da associação prova-aluno")


class FinalizarProvaRequest(BaseModel):
    """Schema para aluno finalizar prova"""
    prova_aluno_id: int = Field(..., description="ID da associação prova-aluno")
    respostas: List[RespostaAlunoCreate] = Field(..., description="Lista de respostas")


class CorrigirProvaResponse(BaseModel):
    """Schema de resposta da correção"""
    prova_aluno_id: int
    pontuacao_obtida: float
    pontuacao_maxima: float
    nota_final: float
    aprovado: bool
    acertos: int
    erros: int
    percentual_acerto: float
    analise_ia: Dict[str, Any]
    feedback_ia: str
    respostas_detalhadas: List[RespostaAlunoResponse]

    model_config = ConfigDict(from_attributes=True)


class ProvaListResponse(BaseModel):
    """Schema para listagem de provas"""
    id: int
    titulo: str
    materia: str
    quantidade_questoes: int
    status: StatusProva
    criado_em: datetime
    criado_por_id: int

    model_config = ConfigDict(from_attributes=True)


class ProvaAlunoListResponse(BaseModel):
    """Schema para listagem de provas do aluno"""
    id: int
    prova_id: int
    status: StatusProvaAluno
    data_atribuicao: datetime
    nota_final: Optional[float]
    aprovado: Optional[bool]
    prova: Optional[ProvaListResponse] = None

    model_config = ConfigDict(from_attributes=True)
