"""
Rotas de Relatórios de Terapias e Acompanhamento
VERSÃO COM PROCESSAMENTO ASSÍNCRONO!
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import base64
import json
import os
from datetime import datetime
import hashlib
import asyncio

from app.database import get_db, SessionLocal
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

# Diretório para salvar relatórios
RELATORIOS_DIR = Path(__file__).parent.parent.parent.parent / "storage" / "relatorios"
RELATORIOS_DIR.mkdir(parents=True, exist_ok=True)

def get_anthropic_client():
    global _client
    if _client is None:
        try:
            from anthropic import Anthropic
            _client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except Exception as e:
            print(f"[AVISO] Erro ao inicializar Anthropic: {e}")
    return _client


# ============= PROCESSAMENTO EM BACKGROUND =============

def processar_relatorio_background(
    relatorio_id: int,
    pdf_path: Path,
    json_path: Path,
    content_type: str
):
    """
    Processa o relatório com IA em background
    NÃO bloqueia a resposta ao usuário!
    """
    print(f"🔄 [BACKGROUND] Iniciando análise do relatório {relatorio_id}...")
    
    try:
        client = get_anthropic_client()
        if not client:
            print(f"❌ [BACKGROUND] Cliente IA não disponível")
            return
        
        # Ler PDF
        with open(pdf_path, "rb") as f:
            file_content = f.read()
        
        # Converter para base64
        file_base64 = base64.standard_b64encode(file_content).decode("utf-8")
        
        # Prompt para análise
        prompt = """Analise este relatório e extraia as informações em formato JSON.

IMPORTANTE: Retorne APENAS o JSON, sem explicações.

Estrutura:
{
    "tipo_laudo": "string",
    "profissional": {"nome": "string", "registro": "string", "especialidade": "string"},
    "datas": {"emissao": "YYYY-MM-DD", "validade": "YYYY-MM-DD"},
    "diagnosticos": [{"cid": "string", "descricao": "string"}],
    "condicoes_identificadas": {"tea": false, "tdah": false, "dislexia": false, ...},
    "resumo_clinico": "string",
    "recomendacoes": ["string"],
    "adaptacoes_sugeridas": {"curriculares": "", "avaliacao": "", "ambiente": "", "recursos": ""},
    "observacoes": "string"
}"""

        # Determinar media type
        media_type = {
            "application/pdf": "application/pdf",
            "image/jpeg": "image/jpeg",
            "image/jpg": "image/jpeg",
            "image/png": "image/png",
            "image/webp": "image/webp"
        }.get(content_type, content_type)

        print(f"🤖 [BACKGROUND] Chamando Claude AI...")
        
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
        for marker in ["```json", "```"]:
            response_text = response_text.replace(marker, "")
        response_text = response_text.strip()
        
        try:
            dados_extraidos = json.loads(response_text)
        except json.JSONDecodeError:
            dados_extraidos = {
                "erro_parse": True,
                "texto_bruto": response_text,
                "mensagem": "Não foi possível estruturar os dados automaticamente"
            }
        
        # Salvar JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
        
        print(f"📄 [BACKGROUND] JSON salvo: {json_path}")
        
        # Atualizar banco de dados
        db = SessionLocal()
        try:
            relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
            if relatorio:
                relatorio.tipo = dados_extraidos.get("tipo_laudo", "Relatório")[:100]
                relatorio.profissional_nome = dados_extraidos.get("profissional", {}).get("nome", "")[:200]
                relatorio.profissional_registro = dados_extraidos.get("profissional", {}).get("registro", "")[:50]
                relatorio.profissional_especialidade = dados_extraidos.get("profissional", {}).get("especialidade", "")[:100]
                relatorio.data_emissao = parse_date(dados_extraidos.get("datas", {}).get("emissao"))
                relatorio.data_validade = parse_date(dados_extraidos.get("datas", {}).get("validade"))
                relatorio.resumo = dados_extraidos.get("resumo_clinico", "")[:200]
                
                db.commit()
                print(f"✅ [BACKGROUND] Relatório {relatorio_id} atualizado no banco!")
            else:
                print(f"⚠️ [BACKGROUND] Relatório {relatorio_id} não encontrado no banco")
        except Exception as e:
            print(f"❌ [BACKGROUND] Erro ao atualizar banco: {e}")
            db.rollback()
        finally:
            db.close()
        
        print(f"🎉 [BACKGROUND] Processamento completo para relatório {relatorio_id}!")
        
    except Exception as e:
        print(f"❌ [BACKGROUND] Erro no processamento: {e}")


def parse_date(date_str: str) -> Optional[datetime]:
    """Converte string de data para datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


# ============= CRUD =============

@router.get("/", response_model=RelatorioListResponse)
async def listar_relatorios(
    student_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os relatórios"""
    query = db.query(Relatorio)
    
    if student_id:
        query = query.filter(Relatorio.student_id == student_id)
    
    total = query.count()
    relatorios = query.order_by(Relatorio.created_at.desc()).offset(skip).limit(limit).all()
    
    # Adicionar dados do JSON
    result = []
    for r in relatorios:
        dados = r.dados_extraidos
        condicoes = r.condicoes
        
        # Carregar JSON se existir
        if isinstance(dados, dict) and dados.get("json_path"):
            json_file = RELATORIOS_DIR / dados["json_path"]
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    full_data = json.load(f)
                    dados = full_data
                    condicoes = full_data.get("condicoes_identificadas", {})
        
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
            "arquivo_path": getattr(r, 'arquivo_path', None),
            "dados_extraidos": dados,
            "condicoes": condicoes,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "student_name": r.student.name if r.student else None,
            "processando": dados == {"json_path": dados.get("json_path")} if isinstance(dados, dict) else False
        }
        result.append(rel_dict)
    
    return {"total": total, "relatorios": result}


@router.get("/{relatorio_id}/arquivo")
async def obter_arquivo_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Download do arquivo PDF"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    if hasattr(relatorio, 'arquivo_path') and relatorio.arquivo_path:
        file_path = RELATORIOS_DIR / relatorio.arquivo_path
        if file_path.exists():
            return FileResponse(
                path=file_path,
                filename=relatorio.arquivo_nome,
                media_type=relatorio.arquivo_tipo
            )
    
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")


@router.get("/{relatorio_id}")
async def obter_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém relatório com dados completos"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Carregar JSON se existir
    if relatorio.dados_extraidos and isinstance(relatorio.dados_extraidos, dict):
        if relatorio.dados_extraidos.get("json_path"):
            json_file = RELATORIOS_DIR / relatorio.dados_extraidos["json_path"]
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    return {
                        **relatorio.__dict__,
                        "dados_extraidos": dados,
                        "condicoes": dados.get("condicoes_identificadas"),
                        "processando": False
                    }
            else:
                # JSON ainda não existe - processando
                return {
                    **relatorio.__dict__,
                    "processando": True,
                    "message": "Relatório sendo processado pela IA..."
                }
    
    return relatorio


@router.delete("/{relatorio_id}")
async def excluir_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Exclui relatório e arquivos"""
    relatorio = db.query(Relatorio).filter(Relatorio.id == relatorio_id).first()
    
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    # Excluir PDF
    if hasattr(relatorio, 'arquivo_path') and relatorio.arquivo_path:
        file_path = RELATORIOS_DIR / relatorio.arquivo_path
        if file_path.exists():
            file_path.unlink()
    
    # Excluir JSON
    if relatorio.dados_extraidos and isinstance(relatorio.dados_extraidos, dict):
        if relatorio.dados_extraidos.get("json_path"):
            json_file = RELATORIOS_DIR / relatorio.dados_extraidos["json_path"]
            if json_file.exists():
                json_file.unlink()
    
    db.delete(relatorio)
    db.commit()
    
    return {"message": "Relatório excluído com sucesso"}


# ============= UPLOAD COM PROCESSAMENTO ASSÍNCRONO =============

@router.post("/upload-analisar")
async def upload_e_analisar_relatorio(
    background_tasks: BackgroundTasks,
    arquivo: UploadFile = File(...),
    student_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🚀 UPLOAD RÁPIDO com processamento em background!
    
    Retorna IMEDIATAMENTE após salvar o arquivo.
    A análise com IA acontece em background.
    """
    
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
            detail=f"Tipo não suportado: {content_type}"
        )
    
    # Ler arquivo
    file_content = await arquivo.read()
    
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo: 10MB")
    
    # Gerar nomes únicos
    file_hash = hashlib.md5(file_content).hexdigest()[:12]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = Path(arquivo.filename).suffix
    base_filename = f"relatorio_{student_id}_{timestamp}_{file_hash}"
    
    safe_pdf_filename = f"{base_filename}{file_extension}"
    safe_json_filename = f"{base_filename}.json"
    
    pdf_path = RELATORIOS_DIR / safe_pdf_filename
    json_path = RELATORIOS_DIR / safe_json_filename
    
    # Salvar PDF IMEDIATAMENTE
    with open(pdf_path, "wb") as f:
        f.write(file_content)
    
    print(f"⚡ PDF salvo: {pdf_path}")
    
    # Criar registro MÍNIMO no banco
    novo_relatorio = Relatorio(
        student_id=student_id,
        tipo="Processando...",  # Será atualizado
        profissional_nome="",
        profissional_registro="",
        profissional_especialidade="",
        data_emissao=None,
        data_validade=None,
        cid="",
        resumo="Relatório sendo analisado pela IA...",
        arquivo_nome=arquivo.filename[:255],
        arquivo_tipo=content_type[:50],
        arquivo_base64=None,
        dados_extraidos={"json_path": safe_json_filename},
        condicoes=None,
        created_by=current_user.id
    )
    
    if hasattr(Relatorio, 'arquivo_path'):
        setattr(novo_relatorio, 'arquivo_path', safe_pdf_filename)
    
    db.add(novo_relatorio)
    db.commit()
    db.refresh(novo_relatorio)
    
    print(f"✅ Relatório {novo_relatorio.id} salvo no banco!")
    
    # Adicionar processamento em BACKGROUND
    background_tasks.add_task(
        processar_relatorio_background,
        novo_relatorio.id,
        pdf_path,
        json_path,
        content_type
    )
    
    print(f"🚀 Processamento em background iniciado!")
    
    # RETORNAR IMEDIATAMENTE! ⚡
    return {
        "success": True,
        "relatorio_id": novo_relatorio.id,
        "arquivo_path": safe_pdf_filename,
        "json_path": safe_json_filename,
        "message": "Upload realizado com sucesso! A análise com IA está sendo processada em background.",
        "status": "processing",
        "tempo_estimado": "30-60 segundos"
    }
