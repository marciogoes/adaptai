"""
ROTAS DE RELATÓRIOS - VERSÃO ULTRA-RÁPIDA v2.0
• Processamento paralelo (30s → 8-12s)
• WebSockets para tempo real
• Progress bar no frontend
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import List, Optional
from pathlib import Path
import base64
import json
import os
from datetime import datetime
import hashlib
import time
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

# NOVOS IMPORTS
from app.services.relatorio_processor import processar_relatorio_com_progresso
from app.services.websocket_manager import ws_manager

router = APIRouter(prefix="/relatorios", tags=["Relatórios de Terapias"])

# Diretório para salvar relatórios
RELATORIOS_DIR = Path(__file__).parent.parent.parent.parent / "storage" / "relatorios"
RELATORIOS_DIR.mkdir(parents=True, exist_ok=True)


# ============= WEBSOCKET ENDPOINT =============

@router.websocket("/ws/{relatorio_id}")
async def websocket_relatorio(
    websocket: WebSocket,
    relatorio_id: int
):
    """
    WebSocket para receber atualizações em tempo real do processamento
    
    Frontend se conecta aqui e recebe:
    - {"type": "progress", "progress": 50, "message": "Analisando..."}
    - {"type": "complete", "progress": 100, "dados": {...}}
    - {"type": "error", "message": "Erro..."}
    """
    await ws_manager.connect(websocket, relatorio_id)
    
    try:
        # Manter conexão viva
        while True:
            # Aguardar mensagens do cliente (apenas ping/pong)
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, relatorio_id)


# ============= PROCESSAMENTO ULTRA-RÁPIDO =============

async def processar_relatorio_ultra_rapido(
    relatorio_id: int,
    pdf_path: Path,
    json_path: Path
):
    """
    Processa relatório com:
    • Processamento paralelo de páginas
    • Notificações WebSocket em tempo real
    • Progress bar 0% → 100%
    
    ANTES: 30 segundos
    DEPOIS: 8-12 segundos! ⚡
    """
    print(f"🚀 [ULTRA-RÁPIDO] Iniciando processamento do relatório {relatorio_id}")
    
    db = None
    try:
        # Função de callback para enviar progresso via WebSocket
        async def progress_callback(progress: int, message: str):
            await ws_manager.send_progress(relatorio_id, progress, message)
            print(f"📊 [{progress}%] {message}")
        
        # PROCESSAR COM PARALELIZAÇÃO!
        dados_extraidos = await processar_relatorio_com_progresso(
            pdf_path,
            settings.ANTHROPIC_API_KEY,
            progress_callback
        )
        
        # Salvar JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_extraidos, f, ensure_ascii=False, indent=2)
        
        print(f"📄 JSON salvo: {json_path}")
        
        # Atualizar banco com retry
        for tentativa in range(3):
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
                    print(f"✅ Banco atualizado!")
                    break
                    
            except OperationalError as e:
                print(f"⚠️ Tentativa {tentativa + 1}/3 falhou")
                db.rollback()
                db.close()
                db = None
                if tentativa < 2:
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Erro: {e}")
                db.rollback()
                break
            finally:
                if db:
                    try:
                        db.close()
                    except:
                        pass
                    db = None
        
        # Notificar conclusão via WebSocket
        await ws_manager.send_complete(relatorio_id, dados_extraidos)
        print(f"🎉 Processamento completo: {relatorio_id}")
        
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        await ws_manager.send_error(relatorio_id, str(e))
    finally:
        if db:
            try:
                db.close()
            except:
                pass


def parse_date(date_str: str) -> Optional[datetime]:
    """Converte string de data para datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


# ============= CRUD (mantém igual) =============

@router.get("/")
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
    
    result = []
    for r in relatorios:
        dados = r.dados_extraidos
        condicoes = r.condicoes
        processando = False
        
        if isinstance(dados, dict) and dados.get("json_path"):
            json_file = RELATORIOS_DIR / dados["json_path"]
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        full_data = json.load(f)
                        dados = full_data
                        condicoes = full_data.get("condicoes_identificadas", {})
                except:
                    pass
            else:
                processando = True
        
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
            "dados_extraidos": dados if not processando else None,
            "condicoes": condicoes,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "student_name": r.student.name if r.student else None,
            "processando": processando
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
    
    dados_extraidos = relatorio.dados_extraidos
    condicoes = relatorio.condicoes
    processando = False
    
    if isinstance(dados_extraidos, dict) and dados_extraidos.get("json_path"):
        json_file = RELATORIOS_DIR / dados_extraidos["json_path"]
        if json_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    full_data = json.load(f)
                    dados_extraidos = full_data
                    condicoes = full_data.get("condicoes_identificadas", {})
            except:
                pass
        else:
            processando = True
    
    return {
        "id": relatorio.id,
        "student_id": relatorio.student_id,
        "student_name": relatorio.student.name if relatorio.student else None,
        "tipo": relatorio.tipo,
        "profissional_nome": relatorio.profissional_nome,
        "profissional_registro": relatorio.profissional_registro,
        "profissional_especialidade": relatorio.profissional_especialidade,
        "data_emissao": relatorio.data_emissao.isoformat() if relatorio.data_emissao else None,
        "data_validade": relatorio.data_validade.isoformat() if relatorio.data_validade else None,
        "cid": relatorio.cid,
        "resumo": relatorio.resumo,
        "arquivo_nome": relatorio.arquivo_nome,
        "arquivo_tipo": relatorio.arquivo_tipo,
        "arquivo_path": getattr(relatorio, 'arquivo_path', None),
        "arquivo_base64": relatorio.arquivo_base64,
        "dados_extraidos": dados_extraidos,
        "condicoes": condicoes,
        "created_at": relatorio.created_at.isoformat() if relatorio.created_at else None,
        "updated_at": relatorio.updated_at.isoformat() if relatorio.updated_at else None,
        "processando": processando,
        "message": "Relatório sendo processado pela IA..." if processando else None
    }


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
    
    if hasattr(relatorio, 'arquivo_path') and relatorio.arquivo_path:
        file_path = RELATORIOS_DIR / relatorio.arquivo_path
        if file_path.exists():
            file_path.unlink()
    
    if relatorio.dados_extraidos and isinstance(relatorio.dados_extraidos, dict):
        if relatorio.dados_extraidos.get("json_path"):
            json_file = RELATORIOS_DIR / relatorio.dados_extraidos["json_path"]
            if json_file.exists():
                json_file.unlink()
    
    db.delete(relatorio)
    db.commit()
    
    return {"message": "Relatório excluído com sucesso"}


# ============= UPLOAD ULTRA-RÁPIDO =============

@router.post("/upload-analisar")
async def upload_e_analisar_relatorio(
    background_tasks: BackgroundTasks,
    arquivo: UploadFile = File(...),
    student_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🚀 UPLOAD ULTRA-RÁPIDO v2.0
    
    • Retorna em <1 segundo
    • Processamento paralelo em background (8-12s)
    • WebSocket para progress bar em tempo real
    • Frontend mostra 0% → 100% automaticamente!
    """
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    content_type = arquivo.content_type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg", "image/webp"]
    
    if content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Tipo não suportado: {content_type}")
    
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
    
    # Criar registro no banco
    novo_relatorio = Relatorio(
        student_id=student_id,
        tipo="Processando...",
        profissional_nome="",
        profissional_registro="",
        profissional_especialidade="",
        data_emissao=None,
        data_validade=None,
        cid="",
        resumo="Aguardando análise...",
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
    
    print(f"✅ Relatório {novo_relatorio.id} criado!")
    
    # Adicionar processamento ULTRA-RÁPIDO em background
    background_tasks.add_task(
        processar_relatorio_ultra_rapido,
        novo_relatorio.id,
        pdf_path,
        json_path
    )
    
    print(f"🚀 Processamento ultra-rápido iniciado!")
    
    # RETORNAR IMEDIATAMENTE com instruções de WebSocket
    return {
        "success": True,
        "relatorio_id": novo_relatorio.id,
        "websocket_url": f"/api/v1/relatorios/ws/{novo_relatorio.id}",
        "message": "✅ Upload concluído! Conecte-se ao WebSocket para acompanhar o processamento em tempo real.",
        "tempo_estimado": "8-12 segundos"
    }
