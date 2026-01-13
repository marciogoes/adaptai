"""
📔 Schemas - Diário de Aprendizagem
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum


class HumorEstudoEnum(str, Enum):
    MUITO_BEM = "muito_bem"
    BEM = "bem"
    NEUTRO = "neutro"
    DIFICIL = "dificil"
    MUITO_DIFICIL = "muito_dificil"


class NivelCompreensaoEnum(str, Enum):
    DOMINEI = "dominei"
    ENTENDI_BEM = "entendi_bem"
    ENTENDI_PARCIAL = "entendi_parcial"
    TENHO_DUVIDAS = "tenho_duvidas"
    NAO_ENTENDI = "nao_entendi"


# ============================================
# CREATE
# ============================================

class DiarioCreate(BaseModel):
    """Criar novo registro no diário"""
    student_id: int
    data_estudo: date
    registro_texto: str = Field(..., min_length=10, description="O que foi estudado hoje")
    periodo: Optional[str] = Field("integral", description="manha, tarde, noite, integral")
    humor: Optional[HumorEstudoEnum] = None
    nivel_compreensao: Optional[NivelCompreensaoEnum] = None
    tempo_estudo_minutos: Optional[int] = Field(None, ge=0, le=720)
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1,
                "data_estudo": "2026-01-13",
                "registro_texto": "Hoje estudamos frações. Aprendemos sobre numerador e denominador. O aluno teve um pouco de dificuldade com frações equivalentes, mas conseguiu entender após usar material concreto (pizza de papel). Também fizemos exercícios de português sobre interpretação de texto.",
                "periodo": "manha",
                "humor": "bem",
                "nivel_compreensao": "entendi_parcial",
                "tempo_estudo_minutos": 90
            }
        }


class DiarioUpdate(BaseModel):
    """Atualizar registro existente"""
    registro_texto: Optional[str] = None
    periodo: Optional[str] = None
    humor: Optional[HumorEstudoEnum] = None
    nivel_compreensao: Optional[NivelCompreensaoEnum] = None
    tempo_estudo_minutos: Optional[int] = None


# ============================================
# RESPONSE
# ============================================

class TopicoExtraido(BaseModel):
    """Tópico extraído pela IA"""
    disciplina: str
    topico_principal: str
    subtopicos: Optional[List[str]] = []
    conceitos_chave: Optional[List[str]] = []
    nivel_dificuldade: Optional[str] = None


class DificuldadeIdentificada(BaseModel):
    """Dificuldade identificada pela IA"""
    descricao: str
    disciplina: Optional[str] = None
    gravidade: Optional[str] = None


class SugestaoRevisao(BaseModel):
    """Sugestão de revisão da IA"""
    topico: str
    motivo: Optional[str] = None
    prioridade: Optional[str] = None


class ConexaoBNCC(BaseModel):
    """Conexão com código BNCC"""
    codigo: str
    descricao_resumida: Optional[str] = None


class DiarioResponse(BaseModel):
    """Resposta completa do diário"""
    id: int
    student_id: int
    data_estudo: date
    registro_texto: str
    periodo: Optional[str]
    humor: Optional[str]
    nivel_compreensao: Optional[str]
    tempo_estudo_minutos: Optional[int]
    
    # Análise da IA
    ia_processado: bool
    ia_disciplinas_detectadas: Optional[List[str]]
    ia_topicos_extraidos: Optional[List[Dict]]
    ia_conceitos_chave: Optional[List[str]]
    ia_dificuldades_identificadas: Optional[List[Dict]]
    ia_pontos_positivos: Optional[List[str]]
    ia_sugestoes_revisao: Optional[List[Dict]]
    ia_conexoes_bncc: Optional[List[Dict]]
    ia_sentimento_geral: Optional[str]
    ia_resumo: Optional[str]
    ia_tags: Optional[List[str]]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class DiarioListItem(BaseModel):
    """Item da lista de diários"""
    id: int
    student_id: int
    data_estudo: date
    periodo: Optional[str]
    humor: Optional[str]
    tempo_estudo_minutos: Optional[int]
    ia_processado: bool
    ia_disciplinas_detectadas: Optional[List[str]]
    ia_resumo: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# CONTEÚDOS EXTRAÍDOS
# ============================================

class ConteudoExtraidoResponse(BaseModel):
    """Conteúdo extraído para geração de material"""
    id: int
    disciplina: str
    area_conhecimento: Optional[str]
    topico: str
    subtopicos: Optional[List[str]]
    conceitos: Optional[List[str]]
    codigo_bncc: Optional[str]
    prioridade_revisao: int
    vezes_mencionado: int
    ultima_mencao: Optional[date]
    material_gerado: bool
    
    class Config:
        from_attributes = True


class ConteudosParaMaterialResponse(BaseModel):
    """Lista de conteúdos prioritários para material"""
    student_id: int
    total: int
    conteudos: List[ConteudoExtraidoResponse]


# ============================================
# RESUMO SEMANAL
# ============================================

class AreaAtencao(BaseModel):
    """Área que precisa de atenção"""
    area: str
    descricao: str
    sugestao: Optional[str] = None


class Recomendacao(BaseModel):
    """Recomendação de estudo"""
    tipo: str
    disciplina: str
    topico: str
    descricao: str


class ResumoSemanalResponse(BaseModel):
    """Resposta do resumo semanal"""
    id: int
    student_id: int
    semana_inicio: date
    semana_fim: date
    ano: int
    numero_semana: int
    
    # Estatísticas
    total_registros: int
    total_minutos_estudo: int
    disciplinas_estudadas: Optional[Dict[str, int]]
    
    # Análise
    resumo_geral: Optional[str]
    principais_conquistas: Optional[List[str]]
    areas_atencao: Optional[List[Dict]]
    recomendacoes: Optional[List[Dict]]
    progresso_observado: Optional[str]
    
    # Dados para gráficos
    dados_grafico_disciplinas: Optional[Dict]
    dados_grafico_humor: Optional[Dict]
    dados_grafico_tempo: Optional[Dict]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================
# ANÁLISE
# ============================================

class AnaliseRegistroResponse(BaseModel):
    """Resposta da análise de um registro"""
    success: bool
    diario_id: int
    analise: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class GerarResumoRequest(BaseModel):
    """Request para gerar resumo semanal"""
    student_id: int
    data_referencia: Optional[date] = None


# ============================================
# ESTATÍSTICAS
# ============================================

class EstatisticasDiarioResponse(BaseModel):
    """Estatísticas do diário de um aluno"""
    student_id: int
    student_name: str
    periodo: str
    
    # Contadores
    total_registros: int
    total_minutos_estudo: int
    media_minutos_por_dia: float
    
    # Distribuições
    por_disciplina: Dict[str, int]
    por_humor: Dict[str, int]
    por_nivel_compreensao: Dict[str, int]
    
    # Top conteúdos
    topicos_mais_estudados: List[Dict[str, Any]]
    topicos_com_dificuldade: List[Dict[str, Any]]
    
    # Evolução
    registros_por_semana: Dict[str, int]


# ============================================
# TIMELINE
# ============================================

class TimelineItem(BaseModel):
    """Item da timeline de aprendizagem"""
    data: date
    tipo: str  # diario, material, prova, marco
    titulo: str
    descricao: Optional[str]
    disciplinas: Optional[List[str]]
    humor: Optional[str]
    destaque: bool = False


class TimelineResponse(BaseModel):
    """Timeline completa de aprendizagem"""
    student_id: int
    periodo_inicio: date
    periodo_fim: date
    total_itens: int
    itens: List[TimelineItem]
