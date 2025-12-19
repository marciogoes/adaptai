"""
Rotas de Relatórios de Terapias e Acompanhamento
Módulo independente que serve como insumo para o PEI
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import base64
import json
from datetime import datetime

from app.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.relatorio import Relatorio
from app.schemas.relatorio import (
    RelatorioCreate,
    RelatorioUpdate,
    RelatorioResponse,
    RelatorioComArquivo,
    RelatorioListResponse,
    RelatorioResumo
)

router = APIRouter(prefix="/relatorios", tags=["Relatórios de Terapias"])

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


# ============= CRUD =============

@router.get("/", response_model=RelatorioListResponse)
async def listar_relatorios(
    student_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os relatórios, opcionalmente filtrado por aluno"""
    query = db.query(Relatorio)
    
    if student_id:
        query = query.filter(Relatorio.student_id == student_id)
    
    total = query.count()
    relatorios = query.order_by(Relatorio.created_at.desc()).offset(skip).limit(limit).all()
    
    # Adicionar nome do aluno
    result = []
    for r in relatorios:
        rel_dict = {
            "id": r.id,
            "student_id": r.student_id,
            "tipo": r.tipo,
            "profissional_nome": r.profissional_nome,
            "profissional_registro": r.profissional_registro,
            "profissional_especialidade": r.profissional_especialidade,
            "data_emissao": r.data_emissao,
            "data_validade": r.data_validade,
            "cid": r.cid,
            "resumo": r.resumo,
            "arquivo_nome": r.arquivo_nome,
            "arquivo_tipo": r.arquivo_tipo,
            "dados_extraidos": r.dados_extraidos,
            "condicoes": r.condicoes,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "student_name": r.student.name if r.student else None
        }
        result.append(rel_dict)
    
    return {"total": total, "relatorios": result}


@router.get("/aluno/{student_id}", response_model=List[RelatorioResumo])
async def listar_relatorios_aluno(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista relatórios de um aluno específico (para uso no PEI)"""
    relatorios = db.query(Relatorio).filter(
        Relatorio.student_id == student_id
    ).order_by(Relatorio.data_emissao.desc()).all()
    
    return relatorios


@router.get("/{relatorio_id}", response_model=RelatorioComArquivo)
async def obter_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém um relatório específico com arquivo"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    return relatorio


@router.delete("/{relatorio_id}")
async def excluir_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Exclui um relatório"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    db.delete(relatorio)
    db.commit()
    
    return {"message": "Relatório excluído com sucesso"}


@router.put("/{relatorio_id}", response_model=RelatorioResponse)
async def atualizar_relatorio(
    relatorio_id: int,
    dados: RelatorioUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza dados de um relatório"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Atualizar campos
    for field, value in dados.dict(exclude_unset=True).items():
        setattr(relatorio, field, value)
    
    db.commit()
    db.refresh(relatorio)
    
    return relatorio


# ============= UPLOAD E ANÁLISE COM IA =============

@router.post("/upload-analisar")
async def upload_e_analisar_relatorio(
    arquivo: UploadFile = File(...),
    student_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Faz upload de um relatório e analisa com IA.
    Aceita PDF ou imagens (JPG, PNG).
    Retorna os dados extraídos e salva no banco.
    """
    client = get_anthropic_client()
    if not client:
        raise HTTPException(status_code=500, detail="Serviço de IA não disponível")
    
    # Verificar se aluno existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
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
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo: 10MB")
    
    # Converter para base64
    file_base64 = base64.standard_b64encode(file_content).decode("utf-8")
    
    # Prompt para análise
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
    "tipo_laudo": "string (ex: Relatório Psicopedagógico, Relatório de Terapia Ocupacional, etc)",
    "profissional": {
        "nome": "string (nome completo do profissional)",
        "registro": "string (CRM, CRP, CRFa, CREFITO, etc)",
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
            "descricao": "string (nome do diagnóstico)"
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
        "outras": []
    },
    "resumo_clinico": "string (resumo das principais conclusões)",
    "recomendacoes": ["string"],
    "adaptacoes_sugeridas": {
        "curriculares": "string",
        "avaliacao": "string",
        "ambiente": "string",
        "recursos": "string"
    },
    "acompanhamentos_indicados": [
        {"profissional": "string", "frequencia": "string"}
    ],
    "observacoes": "string"
}

Se algum campo não estiver disponível, use null ou [].
Analise o documento e extraia todas as informações relevantes."""

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
            model=MODELO_VISAO,
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
        response_text = message.content[0].text.strip()
        
        # Limpar markdown
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
            dados_extraidos = {
                "erro_parse": True,
                "texto_bruto": response_text,
                "mensagem": "Não foi possível estruturar os dados automaticamente"
            }
        
        # Criar relatório no banco
        novo_relatorio = Relatorio(
            student_id=student_id,
            tipo=dados_extraidos.get("tipo_laudo", "Relatório de Acompanhamento"),
            profissional_nome=dados_extraidos.get("profissional", {}).get("nome"),
            profissional_registro=dados_extraidos.get("profissional", {}).get("registro"),
            profissional_especialidade=dados_extraidos.get("profissional", {}).get("especialidade"),
            data_emissao=parse_date(dados_extraidos.get("datas", {}).get("emissao")),
            data_validade=parse_date(dados_extraidos.get("datas", {}).get("validade")),
            cid=", ".join([d.get("cid", "") for d in dados_extraidos.get("diagnosticos", []) if d.get("cid")]),
            resumo=dados_extraidos.get("resumo_clinico"),
            arquivo_nome=arquivo.filename,
            arquivo_tipo=content_type,
            arquivo_base64=f"data:{content_type};base64,{file_base64}",
            dados_extraidos=dados_extraidos,
            condicoes=dados_extraidos.get("condicoes_identificadas"),
            created_by=current_user.id
        )
        
        db.add(novo_relatorio)
        db.commit()
        db.refresh(novo_relatorio)
        
        return {
            "success": True,
            "relatorio_id": novo_relatorio.id,
            "dados": dados_extraidos,
            "message": "Relatório analisado e salvo com sucesso"
        }
        
    except Exception as e:
        print(f"[ERRO] Falha ao analisar relatório: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao analisar relatório: {str(e)}"
        )


def parse_date(date_str: str) -> Optional[datetime]:
    """Converte string de data para datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None
