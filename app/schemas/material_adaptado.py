"""
Schemas para Materiais Adaptados
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MaterialAdaptadoRequest(BaseModel):
    """Request para gerar material adaptado"""
    student_id: int
    disciplina: str = Field(..., description="Disciplina (Matemática, Português, etc)")
    serie: str = Field(..., description="Série do aluno (1º ano EF, 9º ano EF, 1ª série EM, etc)")
    conteudo: str = Field(..., description="Conteúdo/tema específico")
    tipos_material: List[str] = Field(..., description="Tipos de material: texto_niveis, infografico, flashcards, caca_palavras, cruzadinha, bingo, avaliacao, mapa_mental")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1,
                "disciplina": "Matemática",
                "serie": "9º ano EF",
                "conteudo": "Equações do 2º Grau",
                "tipos_material": ["texto_niveis", "infografico", "flashcards"]
            }
        }


class TextoNiveisResponse(BaseModel):
    """Texto adaptado em 3 níveis"""
    nivel_1: str = Field(..., description="Nível básico - DI, TEA severo")
    nivel_2: str = Field(..., description="Nível intermediário - TDAH, Dislexia")
    nivel_3: str = Field(..., description="Nível avançado - Superdotação")
    vocabulario_tecnico: Dict[str, str] = Field(default_factory=dict, description="Glossário de termos")


class InfograficoResponse(BaseModel):
    """Infográfico em texto/markdown"""
    titulo: str
    conteudo_markdown: str = Field(..., description="Conteúdo formatado em markdown")
    elementos_visuais: List[str] = Field(default_factory=list, description="Sugestões de elementos visuais")


class FlashcardResponse(BaseModel):
    """Lista de flashcards"""
    cards: List[Dict[str, str]] = Field(..., description="Lista de {frente, verso, dica}")


class CacaPalavrasResponse(BaseModel):
    """Caça-palavras adaptado"""
    titulo: str
    palavras: List[str]
    matriz: List[List[str]] = Field(..., description="Grid do caça-palavras")
    tamanho: str = Field(..., description="Dimensões da matriz")
    nivel_dificuldade: str


class CruzadinhaResponse(BaseModel):
    """Cruzadinha técnica"""
    titulo: str
    dicas_horizontal: Dict[str, str]
    dicas_vertical: Dict[str, str]
    palavras: List[Dict[str, Any]]


class BingoEducativoResponse(BaseModel):
    """Bingo educativo"""
    titulo: str
    tipo: str = Field(..., description="Tipo do bingo: termos, formulas, conceitos")
    cartelas: List[List[str]] = Field(..., description="Lista de cartelas")
    chamadas: List[Dict[str, str]] = Field(..., description="Lista de chamadas com dica e resposta")


class AvaliacaoMultiformatoResponse(BaseModel):
    """Avaliação em 3 formatos"""
    formato_a: Dict[str, Any] = Field(..., description="Formato padrão escrito")
    formato_b: Dict[str, Any] = Field(..., description="Formato adaptado")
    formato_c: Dict[str, Any] = Field(..., description="Formato oral/roteiro")


class MapaMentalResponse(BaseModel):
    """Mapa mental estruturado"""
    conceito_central: str
    ramos_principais: List[Dict[str, Any]]
    markdown_mermaid: str = Field(..., description="Código Mermaid para visualização")


class MaterialAdaptadoResponse(BaseModel):
    """Resposta com todos os materiais gerados"""
    success: bool = True
    student_name: str
    disciplina: str
    conteudo: str
    
    # Materiais opcionais gerados
    texto_niveis: Optional[TextoNiveisResponse] = None
    infografico: Optional[InfograficoResponse] = None
    flashcards: Optional[FlashcardResponse] = None
    caca_palavras: Optional[CacaPalavrasResponse] = None
    cruzadinha: Optional[CruzadinhaResponse] = None
    bingo: Optional[BingoEducativoResponse] = None
    avaliacao: Optional[AvaliacaoMultiformatoResponse] = None
    mapa_mental: Optional[MapaMentalResponse] = None
    
    tempo_geracao: float
    material_id: Optional[int] = None  # ID do material salvo no banco
    created_at: datetime = Field(default_factory=datetime.now)
