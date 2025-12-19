from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
import base64
import json
from pathlib import Path

from app.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.relatorio import Relatorio
from app.models.student import Student

router = APIRouter(prefix="/pei", tags=["PEI - Plano Educacional Individualizado"])

# Diretório de relatórios
RELATORIOS_DIR = Path(__file__).parent.parent.parent.parent / "storage" / "relatorios"

# Cliente Anthropic (inicialização lazy)
_client = None

# Modelo que suporta PDFs e imagens
MODELO_VISAO = "claude-sonnet-4-20250514"

def get_anthropic_client():
    global _client
    if _client is None:
        try:
            from anthropic import Anthropic
            _client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except Exception as e:
            print(f"[AVISO] Erro ao inicializar Anthropic: {e}")
    return _client


@router.post("/analisar-laudo")
async def analisar_laudo(
    arquivo: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Analisa relatórios de terapias e acompanhamento usando IA e extrai informações automaticamente.
    Aceita relatórios de: psicopedagogos, terapeutas ocupacionais, fonoaudiólogos, psicólogos,
    neurologistas, psiquiatras e outros profissionais de saúde.
    Aceita PDF ou imagens (JPG, PNG).
    """
    client = get_anthropic_client()
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Serviço de IA não disponível"
        )
    
    # Verificar tipo de arquivo
    content_type = arquivo.content_type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg", "image/webp"]
    
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não suportado: {content_type}. Use PDF, JPG, PNG ou WebP."
        )
    
    # Ler conteúdo do arquivo
    file_content = await arquivo.read()
    
    # Verificar tamanho (máximo 10MB)
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Arquivo muito grande. Máximo permitido: 10MB"
        )
    
    # Converter para base64
    file_base64 = base64.standard_b64encode(file_content).decode("utf-8")
    
    # Preparar mensagem para o Claude
    prompt = """Analise este relatório de terapia, acompanhamento ou avaliação profissional e extraia as informações em formato JSON.

Este documento pode ser um relatório de:
- Psicopedagogo(a)
- Terapeuta Ocupacional
- Fonoaudiólogo(a)
- Psicólogo(a)
- Neuropsicólogo(a)
- Neurologista
- Psiquiatra
- Pediatra
- Neuropediatra
- Fisioterapeuta
- Assistente Social
- Ou outro profissional de saúde/educação

IMPORTANTE: Retorne APENAS o JSON, sem explicações ou texto adicional.

Estrutura esperada:
{
    "tipo_laudo": "string (ex: Relatório Psicopedagógico, Relatório de Terapia Ocupacional, Avaliação Fonoaudiológica, Laudo Médico Neurológico, Parecer Psicológico, etc)",
    "profissional": {
        "nome": "string (nome completo do profissional)",
        "registro": "string (CRM, CRP, CRFa, CREFITO, etc com número e estado)",
        "especialidade": "string (especialidade ou área de atuação)"
    },
    "paciente": {
        "nome": "string (se disponível)",
        "data_nascimento": "string formato YYYY-MM-DD (se disponível)",
        "idade": "string (se disponível)"
    },
    "datas": {
        "emissao": "string formato YYYY-MM-DD",
        "validade": "string formato YYYY-MM-DD (se mencionada)"
    },
    "diagnosticos": [
        {
            "cid": "string (código CID-10 ou CID-11, se disponível)",
            "descricao": "string (nome do diagnóstico ou hipótese diagnóstica)"
        }
    ],
    "condicoes_identificadas": {
        "tea": false,
        "tea_nivel": null,
        "tdah": false,
        "dislexia": false,
        "discalculia": false,
        "disgrafia": false,
        "deficiencia_visual": false,
        "deficiencia_auditiva": false,
        "deficiencia_intelectual": false,
        "deficiencia_fisica": false,
        "superdotacao": false,
        "atraso_desenvolvimento": false,
        "transtorno_linguagem": false,
        "transtorno_ansiedade": false,
        "outras": []
    },
    "resumo_clinico": "string (resumo das principais conclusões, observações e achados)",
    "recomendacoes": [
        "string (cada recomendação como item da lista)"
    ],
    "adaptacoes_sugeridas": {
        "curriculares": "string (adaptações curriculares sugeridas)",
        "avaliacao": "string (adaptações para avaliação)",
        "ambiente": "string (adaptações de ambiente)",
        "recursos": "string (recursos de apoio sugeridos)"
    },
    "acompanhamentos_indicados": [
        {
            "profissional": "string (tipo de profissional)",
            "frequencia": "string (frequência sugerida)"
        }
    ],
    "objetivos_terapeuticos": [
        "string (objetivos de tratamento/intervenção mencionados)"
    ],
    "evolucao": "string (se for relatório de acompanhamento, descrever a evolução observada)",
    "observacoes": "string (outras observações relevantes para o contexto escolar)"
}

Se algum campo não estiver disponível no documento, use null para valores únicos ou [] para listas.
Para as condições em condicoes_identificadas, marque true apenas se explicitamente mencionado no relatório.
Se o TEA for identificado, tente determinar o nível de suporte (1, 2 ou 3) se mencionado.

Analise o documento com atenção e extraia todas as informações relevantes para o Plano Educacional Individualizado (PEI)."""

    try:
        # Determinar media type
        if content_type == "application/pdf":
            media_type = "application/pdf"
        elif content_type in ["image/jpeg", "image/jpg"]:
            media_type = "image/jpeg"
        elif content_type == "image/png":
            media_type = "image/png"
        elif content_type == "image/webp":
            media_type = "image/webp"
        else:
            media_type = content_type

        # Chamar Claude com visão
        message = client.messages.create(
            model=MODELO_VISAO,  # Modelo que suporta PDF/imagens
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document" if content_type == "application/pdf" else "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": file_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        
        # Extrair resposta
        response_text = message.content[0].text
        
        # Tentar fazer parse do JSON
        # Remover possíveis marcadores de código
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            dados_extraidos = json.loads(response_text)
        except json.JSONDecodeError:
            # Se não conseguir fazer parse, retornar o texto bruto
            dados_extraidos = {
                "erro_parse": True,
                "texto_bruto": response_text,
                "mensagem": "Não foi possível estruturar os dados automaticamente"
            }
        
        return {
            "success": True,
            "dados": dados_extraidos,
            "arquivo_nome": arquivo.filename,
            "arquivo_tipo": content_type,
            "arquivo_base64": f"data:{content_type};base64,{file_base64}"
        }
        
    except Exception as e:
        print(f"[ERRO] Falha ao analisar relatório: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao analisar relatório com IA: {str(e)}"
        )


@router.post("/gerar-pei-completo")
async def gerar_pei_completo(
    dados_laudos: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Gera um PEI completo baseado nos dados extraídos dos relatórios de terapias e acompanhamento usando IA.
    """
    client = get_anthropic_client()
    if not client:
        raise HTTPException(
            status_code=500,
            detail="Serviço de IA não disponível"
        )
    
    prompt = f"""Com base nos dados dos relatórios de terapias e acompanhamento abaixo, gere um Plano Educacional Individualizado (PEI) completo.

DADOS DOS RELATÓRIOS:
{json.dumps(dados_laudos, ensure_ascii=False, indent=2)}

Gere o PEI em formato JSON com a seguinte estrutura:
{{
    "caracteristicas": "string (características gerais do aluno baseadas nos relatórios)",
    "pontos_fortes": "string (pontos fortes identificados ou potenciais)",
    "dificuldades": "string (principais dificuldades identificadas)",
    "adaptacoes_curriculares": "string (adaptações curriculares recomendadas)",
    "adaptacoes_avaliacao": "string (adaptações para avaliações)",
    "adaptacoes_ambiente": "string (adaptações de ambiente escolar)",
    "recursos_apoio": "string (recursos e materiais de apoio)",
    "metas_curto_prazo": "string (metas para 1-3 meses)",
    "metas_medio_prazo": "string (metas para 3-6 meses)",
    "metas_longo_prazo": "string (metas para o ano letivo)",
    "estrategias_ensino": "string (estratégias de ensino recomendadas)",
    "estrategias_comunicacao": "string (estratégias de comunicação)",
    "estrategias_comportamento": "string (estratégias de manejo comportamental)",
    "profissionais_apoio": "string (profissionais de apoio necessários)",
    "frequencia_acompanhamento": "string (frequência de acompanhamento sugerida)",
    "observacoes": "string (observações gerais)"
}}

Seja específico e prático nas recomendações. 
Considere o contexto escolar brasileiro.
Leve em consideração as orientações de todos os profissionais (psicopedagogos, terapeutas ocupacionais, fonoaudiólogos, psicólogos, médicos, etc).
Retorne APENAS o JSON, sem explicações adicionais."""

    try:
        message = client.messages.create(
            model=MODELO_VISAO,  # Modelo que suporta PDF/imagens
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )
        
        response_text = message.content[0].text.strip()
        
        # Limpar marcadores de código
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            pei_gerado = json.loads(response_text)
        except json.JSONDecodeError:
            pei_gerado = {
                "erro_parse": True,
                "texto_bruto": response_text
            }
        
        return {
            "success": True,
            "pei": pei_gerado
        }
        
    except Exception as e:
        print(f"[ERRO] Falha ao gerar PEI: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar PEI com IA: {str(e)}"
        )
