# ============================================
# ROUTER - Planejamento BNCC e PEI
# ============================================
# Versão com suporte a processamento em background

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import asyncio
from datetime import datetime

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.curriculo import CurriculoNacional, MapeamentoPrerequisitos
from app.models.pei import PEI, PEIObjetivo, PEIProgressLog, PEIAjuste
from app.services.planejamento_bncc_service import PlanejamentoBNNCService
from app.services.planejamento_bncc_completo_service import PlanejamentoBNNCCompletoService
from app.services.background_tasks import get_task_manager, TaskStatus
from app.schemas.curriculo import (
    CurriculoNacionalCreate,
    CurriculoNacionalResponse,
    CurriculoNacionalListResponse,
    MapeamentoPrerequisitosCreate,
    MapeamentoPrerequisitosResponse
)
from app.schemas.pei import (
    PEICreate,
    PEIUpdate,
    PEIResponse,
    PEIListResponse,
    PEIObjetivoCreate,
    PEIObjetivoUpdate,
    PEIObjetivoResponse,
    ProgressLogCreate,
    ProgressLogResponse,
    GerarPlanejamentoRequest,
    GerarPlanejamentoTrimestreRequest,
    SalvarPlanejamentoRequest,
    PlanejamentoResponse
)

router = APIRouter(prefix="/planejamento", tags=["Planejamento BNCC e PEI"])


# ============================================
# ENDPOINTS - Background Tasks (Processamento Assíncrono)
# ============================================

@router.post("/gerar-planejamento-anual/async")
async def iniciar_geracao_planejamento(
    request: GerarPlanejamentoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Inicia a geração de planejamento em background.
    Retorna imediatamente com um task_id para acompanhar o progresso.
    """
    # Verificar se o aluno existe
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Criar tarefa
    task_manager = get_task_manager()
    task_id = task_manager.create_task()
    
    # Função que será executada em background
    async def executar_geracao():
        # Criar nova sessão para a tarefa em background
        from app.database import SessionLocal
        db_bg = SessionLocal()
        try:
            service = PlanejamentoBNNCService(db_bg)
            resultado = await service.gerar_planejamento_anual(
                student_id=request.student_id,
                ano_letivo=request.ano_letivo,
                componentes=request.componentes,
                user_id=current_user.id,
                task_id=task_id,
                task_manager=task_manager
            )
            return resultado
        finally:
            db_bg.close()
    
    # Executar em background
    asyncio.create_task(
        task_manager.run_task(task_id, executar_geracao)
    )
    
    return {
        "task_id": task_id,
        "message": "Geração de planejamento iniciada. Use o endpoint /planejamento/task/{task_id} para acompanhar.",
        "status": "pending"
    }


@router.get("/task/{task_id}")
async def verificar_status_tarefa(
    task_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Verifica o status de uma tarefa em background.
    Retorna progresso, mensagem e resultado quando completo.
    """
    task_manager = get_task_manager()
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return task.to_dict()


# ============================================
# ENDPOINTS - Listar PEIs do Aluno
# ============================================

@router.get("/peis/aluno/{student_id}")
async def listar_peis_aluno_v2(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os PEIs de um aluno específico"""
    # Verificar se o aluno existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Buscar PEIs do aluno
    peis = db.query(PEI).filter(PEI.student_id == student_id).order_by(PEI.created_at.desc()).all()
    
    resultado = []
    for pei in peis:
        # Contar objetivos
        total_objetivos = len(pei.objetivos) if pei.objetivos else 0
        atingidos = sum(1 for o in pei.objetivos if o.status == "atingido") if pei.objetivos else 0
        em_progresso = sum(1 for o in pei.objetivos if o.status == "em_progresso") if pei.objetivos else 0
        
        resultado.append({
            "id": pei.id,
            "student_id": pei.student_id,
            "ano_letivo": pei.ano_letivo,
            "tipo_periodo": pei.tipo_periodo,
            "status": pei.status,
            "data_inicio": pei.data_inicio.isoformat() if pei.data_inicio else None,
            "data_fim": pei.data_fim.isoformat() if pei.data_fim else None,
            "created_at": pei.created_at.isoformat() if pei.created_at else None,
            "estatisticas": {
                "total_objetivos": total_objetivos,
                "atingidos": atingidos,
                "em_progresso": em_progresso,
                "nao_iniciados": total_objetivos - atingidos - em_progresso
            }
        })
    
    return {
        "aluno": {
            "id": student.id,
            "nome": student.name,
            "serie": student.grade_level
        },
        "total_peis": len(resultado),
        "peis": resultado
    }


@router.get("/pei/{pei_id}/completo")
async def obter_pei_completo(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém o PEI completo com todos os objetivos"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Buscar aluno
    student = db.query(Student).filter(Student.id == pei.student_id).first()
    
    # Organizar objetivos por trimestre
    objetivos_por_trimestre = {1: [], 2: [], 3: [], 4: []}
    
    for obj in pei.objetivos:
        trimestre = obj.trimestre or 1
        objetivos_por_trimestre[trimestre].append({
            "id": obj.id,
            "area": obj.area,
            "codigo_bncc": obj.codigo_bncc,
            "titulo": obj.titulo,
            "descricao": obj.descricao,
            "meta_especifica": obj.meta_especifica,
            "valor_alvo": obj.valor_alvo,
            "valor_atual": obj.valor_atual,
            "status": obj.status,
            "adaptacoes": json.loads(obj.adaptacoes) if obj.adaptacoes else [],
            "estrategias": json.loads(obj.estrategias) if obj.estrategias else [],
            "materiais_recursos": json.loads(obj.materiais_recursos) if obj.materiais_recursos else [],
            "criterios_avaliacao": json.loads(obj.criterios_avaliacao) if obj.criterios_avaliacao else [],
            "prazo": obj.prazo.isoformat() if obj.prazo else None
        })
    
    return {
        "pei": {
            "id": pei.id,
            "ano_letivo": pei.ano_letivo,
            "tipo_periodo": pei.tipo_periodo,
            "status": pei.status,
            "data_inicio": pei.data_inicio.isoformat() if pei.data_inicio else None,
            "data_fim": pei.data_fim.isoformat() if pei.data_fim else None,
            "created_at": pei.created_at.isoformat() if pei.created_at else None
        },
        "aluno": {
            "id": student.id if student else None,
            "nome": student.name if student else None,
            "serie": student.grade_level if student else None
        },
        "objetivos_por_trimestre": objetivos_por_trimestre,
        "total_objetivos": len(pei.objetivos)
    }


# ============================================
# ENDPOINTS - Currículo BNCC
# ============================================

@router.get("/bncc/componentes", response_model=List[str])
async def listar_componentes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os componentes curriculares disponíveis"""
    result = db.query(CurriculoNacional.componente).distinct().all()
    componentes = [r[0] for r in result if r[0]]
    
    # Se não houver componentes no banco, retornar padrão
    if not componentes:
        return ["Matemática", "Língua Portuguesa", "Ciências", "História", "Geografia"]
    
    return componentes


@router.get("/bncc/anos", response_model=List[str])
async def listar_anos_escolares(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os anos escolares disponíveis"""
    result = db.query(CurriculoNacional.ano_escolar).distinct().all()
    return [r[0] for r in result if r[0]]


@router.get("/bncc/habilidades", response_model=CurriculoNacionalListResponse)
async def listar_habilidades_bncc(
    ano_escolar: str = Query(..., description="Ano escolar (ex: 5º ano)"),
    componente: Optional[str] = Query(None, description="Componente curricular"),
    trimestre: Optional[int] = Query(None, ge=1, le=4, description="Trimestre"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista habilidades da BNCC com filtros"""
    query = db.query(CurriculoNacional).filter(
        CurriculoNacional.ano_escolar == ano_escolar
    )
    
    if componente:
        query = query.filter(CurriculoNacional.componente == componente)
    
    if trimestre:
        query = query.filter(CurriculoNacional.trimestre_sugerido == trimestre)
    
    habilidades = query.all()
    
    return CurriculoNacionalListResponse(
        total=len(habilidades),
        curriculos=[CurriculoNacionalResponse.model_validate(h) for h in habilidades]
    )


@router.get("/bncc/habilidade/{codigo_bncc}", response_model=CurriculoNacionalResponse)
async def obter_habilidade_bncc(
    codigo_bncc: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém detalhes de uma habilidade específica"""
    habilidade = db.query(CurriculoNacional).filter(
        CurriculoNacional.codigo_bncc == codigo_bncc
    ).first()
    
    if not habilidade:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    
    return habilidade


@router.get("/bncc/prerequisitos/{codigo_bncc}", response_model=List[MapeamentoPrerequisitosResponse])
async def obter_prerequisitos(
    codigo_bncc: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista os pré-requisitos de uma habilidade"""
    prerequisitos = db.query(MapeamentoPrerequisitos).filter(
        MapeamentoPrerequisitos.habilidade_codigo == codigo_bncc
    ).all()
    
    return prerequisitos


@router.post("/bncc/importar")
async def importar_habilidades_bncc(
    dados: List[CurriculoNacionalCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Importa habilidades da BNCC em lote"""
    importados = 0
    atualizados = 0
    erros = []
    
    for item in dados:
        try:
            existente = db.query(CurriculoNacional).filter(
                CurriculoNacional.codigo_bncc == item.codigo_bncc
            ).first()
            
            if existente:
                for key, value in item.model_dump().items():
                    if value is not None:
                        setattr(existente, key, value)
                atualizados += 1
            else:
                novo = CurriculoNacional(**item.model_dump())
                db.add(novo)
                importados += 1
                
        except Exception as e:
            erros.append({"codigo": item.codigo_bncc, "erro": str(e)})
    
    db.commit()
    
    return {
        "importados": importados,
        "atualizados": atualizados,
        "erros": erros
    }


# ============================================
# ENDPOINTS - Geração de Planejamento IA (Síncrono)
# ============================================

@router.post("/gerar-planejamento-anual", response_model=PlanejamentoResponse)
async def gerar_planejamento_anual(
    request: GerarPlanejamentoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera um planejamento anual completo baseado na BNCC adaptado ao perfil do aluno.
    Usa IA para criar objetivos personalizados considerando laudos e diagnósticos.
    
    ATENÇÃO: Esta operação pode demorar até 2 minutos.
    Para acompanhar o progresso, use o endpoint /gerar-planejamento-anual/async
    """
    # Verificar se o aluno existe
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    service = PlanejamentoBNNCService(db)
    
    try:
        resultado = await service.gerar_planejamento_anual(
            student_id=request.student_id,
            ano_letivo=request.ano_letivo,
            componentes=request.componentes,
            user_id=current_user.id
        )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gerar-objetivos-trimestre")
async def gerar_objetivos_trimestre(
    request: GerarPlanejamentoTrimestreRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera objetivos específicos para um trimestre e componente.
    Útil para planejamento parcial ou ajustes durante o ano.
    """
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    service = PlanejamentoBNNCService(db)
    
    try:
        resultado = await service.gerar_objetivos_pei_por_trimestre(
            student_id=request.student_id,
            componente=request.componente,
            trimestre=request.trimestre,
            ano_letivo=request.ano_letivo
        )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/salvar-planejamento", response_model=PEIResponse)
async def salvar_planejamento_como_pei(
    request: SalvarPlanejamentoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Salva o planejamento gerado como um PEI no banco de dados.
    Cria o PEI e todos os objetivos associados.
    """
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    service = PlanejamentoBNNCService(db)
    
    try:
        pei = service.salvar_planejamento_como_pei(
            student_id=request.student_id,
            planejamento=request.planejamento,
            user_id=current_user.id,
            ano_letivo=request.ano_letivo
        )
        
        return pei
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/planejamento-completo/jobs/{student_id}")
async def listar_jobs_aluno(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos os jobs de planejamento de um aluno.
    Útil para verificar histórico e encontrar jobs para retomar.
    """
    from app.models.planejamento_job import PlanejamentoJob
    
    jobs = db.query(PlanejamentoJob).filter(
        PlanejamentoJob.student_id == student_id
    ).order_by(PlanejamentoJob.created_at.desc()).all()
    
    return {
        "total": len(jobs),
        "jobs": [job.to_dict() for job in jobs]
    }


@router.get("/planejamento-completo/job/{task_id}")
async def obter_job_detalhado(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtém detalhes completos de um job, incluindo logs.
    """
    from app.models.planejamento_job import PlanejamentoJob, PlanejamentoJobLog
    
    job = db.query(PlanejamentoJob).filter(
        PlanejamentoJob.task_id == task_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    # Buscar logs
    logs = db.query(PlanejamentoJobLog).filter(
        PlanejamentoJobLog.job_id == job.id
    ).order_by(PlanejamentoJobLog.created_at.desc()).limit(50).all()
    
    # Parsear resultados parciais
    resultados = job.resultados_parciais
    if isinstance(resultados, str):
        try:
            resultados = json.loads(resultados)
        except:
            resultados = {}
    
    return {
        "job": job.to_dict(),
        "resultados_parciais": {
            comp: {
                "total_objetivos": len(dados.get("objetivos", [])),
                "processado_em": dados.get("processado_em")
            }
            for comp, dados in (resultados or {}).items()
        },
        "logs": [
            {
                "evento": log.evento,
                "componente": log.componente,
                "lote": log.lote,
                "mensagem": log.mensagem,
                "created_at": log.created_at.isoformat() if log.created_at else None
            }
            for log in logs
        ]
    }


@router.post("/planejamento-completo/retomar/{task_id}")
async def retomar_job(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retoma um job interrompido de onde parou.
    Usa os resultados parciais já salvos.
    """
    from app.models.planejamento_job import PlanejamentoJob, JobStatus
    
    job = db.query(PlanejamentoJob).filter(
        PlanejamentoJob.task_id == task_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.status == JobStatus.COMPLETED.value:
        raise HTTPException(status_code=400, detail="Job já foi concluído")
    
    if job.status == JobStatus.PROCESSING.value:
        raise HTTPException(status_code=400, detail="Job já está em processamento")
    
    # Criar nova tarefa
    task_manager = get_task_manager()
    new_task_id = task_manager.create_task()
    
    async def executar_retomada():
        from app.database import SessionLocal
        db_bg = SessionLocal()
        try:
            service = PlanejamentoBNNCCompletoService(db_bg)
            
            # Recarregar job na nova sessão
            job_bg = db_bg.query(PlanejamentoJob).filter(
                PlanejamentoJob.id == job.id
            ).first()
            
            resultado = await service.gerar_planejamento_completo(
                student_id=job_bg.student_id,
                ano_letivo=job_bg.ano_letivo,
                componentes=job_bg.componentes_solicitados,
                user_id=job_bg.user_id,
                task_id=new_task_id,
                task_manager=task_manager,
                retomar_job=True
            )
            return resultado
        finally:
            db_bg.close()
    
    asyncio.create_task(
        task_manager.run_task(new_task_id, executar_retomada)
    )
    
    return {
        "task_id": new_task_id,
        "job_original": task_id,
        "message": "Retomada iniciada. Use /planejamento/task/{task_id} para acompanhar.",
        "status": "pending",
        "componentes_ja_processados": job.componentes_processados or []
    }


@router.delete("/planejamento-completo/job/{task_id}")
async def cancelar_job(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Cancela/pausa um job em andamento.
    Os resultados parciais são preservados para retomada futura.
    """
    from app.models.planejamento_job import PlanejamentoJob, JobStatus
    
    job = db.query(PlanejamentoJob).filter(
        PlanejamentoJob.task_id == task_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job não encontrado")
    
    if job.status == JobStatus.COMPLETED.value:
        raise HTTPException(status_code=400, detail="Job já foi concluído")
    
    job.status = JobStatus.PAUSED.value
    job.message = "Job pausado pelo usuário"
    db.commit()
    
    return {
        "message": "Job pausado com sucesso",
        "task_id": task_id,
        "componentes_processados": job.componentes_processados,
        "pode_retomar": True
    }


# ============================================
# ENDPOINTS - PEI CRUD
# ============================================

@router.get("/pei/aluno/{student_id}", response_model=PEIListResponse)
async def listar_peis_aluno(
    student_id: int,
    ano_letivo: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os PEIs de um aluno"""
    query = db.query(PEI).filter(PEI.student_id == student_id)
    
    if ano_letivo:
        query = query.filter(PEI.ano_letivo == ano_letivo)
    
    if status:
        query = query.filter(PEI.status == status)
    
    peis = query.order_by(PEI.created_at.desc()).all()
    
    return PEIListResponse(
        total=len(peis),
        peis=[PEIResponse.model_validate(p) for p in peis]
    )


@router.get("/pei/{pei_id}", response_model=PEIResponse)
async def obter_pei(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém um PEI específico com todos os objetivos"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    return pei


@router.put("/pei/{pei_id}", response_model=PEIResponse)
async def atualizar_pei(
    pei_id: int,
    dados: PEIUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza dados gerais de um PEI"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Registrar ajuste se mudou status
    if dados.status and dados.status != pei.status:
        ajuste = PEIAjuste(
            pei_id=pei_id,
            adjustment_type="status_changed",
            description=f"Status alterado de {pei.status} para {dados.status}",
            old_value={"status": pei.status},
            new_value={"status": dados.status},
            adjusted_by=current_user.id
        )
        db.add(ajuste)
    
    # Atualizar campos
    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(pei, key, value)
    
    db.commit()
    db.refresh(pei)
    
    return pei


@router.delete("/pei/{pei_id}")
async def excluir_pei(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Exclui um PEI"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    db.delete(pei)
    db.commit()
    
    return {"message": "PEI excluído com sucesso"}


@router.post("/pei/{pei_id}/ativar", response_model=PEIResponse)
async def ativar_pei(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Ativa um PEI (muda status de rascunho para ativo)"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Verificar se tem objetivos
    if not pei.objetivos:
        raise HTTPException(
            status_code=400,
            detail="O PEI precisa ter pelo menos um objetivo para ser ativado"
        )
    
    pei.status = "ativo"
    
    ajuste = PEIAjuste(
        pei_id=pei_id,
        adjustment_type="status_changed",
        description="PEI ativado",
        old_value={"status": "rascunho"},
        new_value={"status": "ativo"},
        adjusted_by=current_user.id
    )
    db.add(ajuste)
    
    db.commit()
    db.refresh(pei)
    
    return pei


# ============================================
# ENDPOINTS - Objetivos do PEI
# ============================================

@router.post("/pei/{pei_id}/objetivo", response_model=PEIObjetivoResponse)
async def adicionar_objetivo(
    pei_id: int,
    objetivo: PEIObjetivoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Adiciona um novo objetivo ao PEI"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Buscar currículo se tiver código BNCC
    curriculo_id = None
    if objetivo.codigo_bncc:
        curriculo = db.query(CurriculoNacional).filter(
            CurriculoNacional.codigo_bncc == objetivo.codigo_bncc
        ).first()
        if curriculo:
            curriculo_id = curriculo.id
    
    novo_objetivo = PEIObjetivo(
        pei_id=pei_id,
        curriculo_nacional_id=curriculo_id,
        origem="professor_manual",
        **objetivo.model_dump()
    )
    
    db.add(novo_objetivo)
    
    # Registrar ajuste
    ajuste = PEIAjuste(
        pei_id=pei_id,
        adjustment_type="goal_added",
        description=f"Objetivo adicionado: {objetivo.titulo}",
        new_value=objetivo.model_dump(),
        adjusted_by=current_user.id
    )
    db.add(ajuste)
    
    db.commit()
    db.refresh(novo_objetivo)
    
    return novo_objetivo


@router.put("/pei/objetivo/{objetivo_id}", response_model=PEIObjetivoResponse)
async def atualizar_objetivo(
    objetivo_id: int,
    dados: PEIObjetivoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza um objetivo do PEI"""
    objetivo = db.query(PEIObjetivo).filter(PEIObjetivo.id == objetivo_id).first()
    
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    
    # Guardar valor antigo
    old_value = {
        "titulo": objetivo.titulo,
        "status": objetivo.status,
        "valor_atual": float(objetivo.valor_atual) if objetivo.valor_atual else 0
    }
    
    # Atualizar campos
    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(objetivo, key, value)
    
    objetivo.ultima_atualizacao = datetime.utcnow()
    
    # Se mudou de ia_sugestao para editado pelo professor
    if objetivo.origem == "ia_sugestao":
        objetivo.origem = "ia_ajustado"
    
    # Registrar ajuste
    ajuste = PEIAjuste(
        pei_id=objetivo.pei_id,
        adjustment_type="goal_modified",
        description=f"Objetivo modificado: {objetivo.titulo}",
        old_value=old_value,
        new_value=dados.model_dump(exclude_unset=True),
        adjusted_by=current_user.id
    )
    db.add(ajuste)
    
    db.commit()
    db.refresh(objetivo)
    
    return objetivo


@router.delete("/pei/objetivo/{objetivo_id}")
async def excluir_objetivo(
    objetivo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove um objetivo do PEI"""
    objetivo = db.query(PEIObjetivo).filter(PEIObjetivo.id == objetivo_id).first()
    
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    
    # Registrar ajuste
    ajuste = PEIAjuste(
        pei_id=objetivo.pei_id,
        adjustment_type="goal_removed",
        description=f"Objetivo removido: {objetivo.titulo}",
        old_value={"titulo": objetivo.titulo, "area": objetivo.area},
        adjusted_by=current_user.id
    )
    db.add(ajuste)
    
    db.delete(objetivo)
    db.commit()
    
    return {"message": "Objetivo excluído com sucesso"}


# ============================================
# ENDPOINTS - Progresso
# ============================================

@router.post("/pei/objetivo/{objetivo_id}/progresso", response_model=ProgressLogResponse)
async def registrar_progresso(
    objetivo_id: int,
    dados: ProgressLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Registra progresso em um objetivo"""
    objetivo = db.query(PEIObjetivo).filter(PEIObjetivo.id == objetivo_id).first()
    
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo não encontrado")
    
    # Criar registro de progresso
    log = PEIProgressLog(
        goal_id=objetivo_id,
        observation=dados.observation,
        progress_value=dados.progress_value,
        recorded_by=current_user.id
    )
    
    db.add(log)
    
    # Atualizar valor atual do objetivo
    objetivo.valor_atual = dados.progress_value
    objetivo.ultima_atualizacao = datetime.utcnow()
    
    # Atualizar status baseado no progresso
    if dados.progress_value >= objetivo.valor_alvo:
        objetivo.status = "atingido"
    elif dados.progress_value > 0:
        objetivo.status = "em_progresso"
    
    db.commit()
    db.refresh(log)
    
    return log


@router.get("/pei/objetivo/{objetivo_id}/progresso", response_model=List[ProgressLogResponse])
async def listar_progresso(
    objetivo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista histórico de progresso de um objetivo"""
    logs = db.query(PEIProgressLog).filter(
        PEIProgressLog.goal_id == objetivo_id
    ).order_by(PEIProgressLog.recorded_at.desc()).all()
    
    return logs


# ============================================
# ENDPOINTS - Resumo e Dashboard
# ============================================

@router.get("/pei/{pei_id}/resumo")
async def obter_resumo_pei(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém resumo do progresso do PEI"""
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    
    # Calcular estatísticas
    total_objetivos = len(pei.objetivos)
    atingidos = sum(1 for o in pei.objetivos if o.status == "atingido")
    em_progresso = sum(1 for o in pei.objetivos if o.status == "em_progresso")
    nao_iniciados = sum(1 for o in pei.objetivos if o.status == "nao_iniciado")
    
    # Progresso médio
    progresso_medio = 0
    if total_objetivos > 0:
        progresso_medio = sum(
            float(o.valor_atual or 0) for o in pei.objetivos
        ) / total_objetivos
    
    # Por área
    por_area = {}
    for obj in pei.objetivos:
        area = obj.area or "outro"
        if area not in por_area:
            por_area[area] = {"total": 0, "atingidos": 0, "progresso_medio": 0}
        por_area[area]["total"] += 1
        if obj.status == "atingido":
            por_area[area]["atingidos"] += 1
        por_area[area]["progresso_medio"] += float(obj.valor_atual or 0)
    
    # Calcular média por área
    for area in por_area:
        if por_area[area]["total"] > 0:
            por_area[area]["progresso_medio"] /= por_area[area]["total"]
    
    # Por trimestre
    por_trimestre = {}
    for obj in pei.objetivos:
        tri = obj.trimestre or 1
        if tri not in por_trimestre:
            por_trimestre[tri] = {"total": 0, "atingidos": 0}
        por_trimestre[tri]["total"] += 1
        if obj.status == "atingido":
            por_trimestre[tri]["atingidos"] += 1
    
    return {
        "pei_id": pei_id,
        "status": pei.status,
        "ano_letivo": pei.ano_letivo,
        "estatisticas": {
            "total_objetivos": total_objetivos,
            "atingidos": atingidos,
            "em_progresso": em_progresso,
            "nao_iniciados": nao_iniciados,
            "progresso_medio": round(progresso_medio, 1),
            "percentual_conclusao": round((atingidos / total_objetivos * 100) if total_objetivos > 0 else 0, 1)
        },
        "por_area": por_area,
        "por_trimestre": por_trimestre
    }


@router.get("/pei/{pei_id}/historico")
async def obter_historico_ajustes(
    pei_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista histórico de ajustes do PEI"""
    ajustes = db.query(PEIAjuste).filter(
        PEIAjuste.pei_id == pei_id
    ).order_by(PEIAjuste.adjusted_at.desc()).all()
    
    return [
        {
            "id": a.id,
            "tipo": a.adjustment_type,
            "descricao": a.description,
            "razao": a.reason,
            "valor_antigo": a.old_value,
            "valor_novo": a.new_value,
            "ajustado_por": a.adjusted_by,
            "data": a.adjusted_at.isoformat() if a.adjusted_at else None
        }
        for a in ajustes
    ]


# ============================================
# ENDPOINTS - Planejamento COMPLETO (TODAS as habilidades)
# ============================================

@router.get("/planejamento-completo/componentes/{ano_escolar}")
async def listar_componentes_ano(
    ano_escolar: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Lista todos os componentes curriculares disponíveis para um ano escolar
    com a contagem de habilidades de cada um.
    """
    service = PlanejamentoBNNCCompletoService(db)
    return service.listar_componentes_disponiveis(ano_escolar)


@router.post("/gerar-planejamento-completo/async")
async def iniciar_geracao_planejamento_completo(
    request: GerarPlanejamentoRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Inicia a geração de planejamento COMPLETO em background.
    Gera adaptações para TODAS as habilidades da BNCC do ano escolar.
    
    Retorna imediatamente com um task_id para acompanhar o progresso.
    
    ATENÇÃO: Este processo pode demorar vários minutos dependendo da
    quantidade de habilidades e componentes selecionados.
    """
    # Verificar se o aluno existe
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Criar tarefa
    task_manager = get_task_manager()
    task_id = task_manager.create_task()
    
    # Função que será executada em background
    async def executar_geracao_completa():
        from app.database import SessionLocal
        db_bg = SessionLocal()
        try:
            service = PlanejamentoBNNCCompletoService(db_bg)
            resultado = await service.gerar_planejamento_completo(
                student_id=request.student_id,
                ano_letivo=request.ano_letivo,
                componentes=request.componentes,
                task_id=task_id,
                task_manager=task_manager
            )
            return resultado
        finally:
            db_bg.close()
    
    # Executar em background
    asyncio.create_task(
        task_manager.run_task(task_id, executar_geracao_completa)
    )
    
    return {
        "task_id": task_id,
        "message": "Geração de planejamento COMPLETO iniciada. Use /planejamento/task/{task_id} para acompanhar.",
        "status": "pending",
        "tipo": "planejamento_completo"
    }


@router.post("/gerar-planejamento-completo")
async def gerar_planejamento_completo_sincrono(
    request: GerarPlanejamentoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Gera planejamento COMPLETO de forma síncrona.
    Gera adaptações para TODAS as habilidades da BNCC.
    
    ATENÇÃO: Esta operação pode demorar MUITO tempo (vários minutos).
    Para melhor experiência, use o endpoint /async.
    """
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    service = PlanejamentoBNNCCompletoService(db)
    
    try:
        resultado = await service.gerar_planejamento_completo(
            student_id=request.student_id,
            ano_letivo=request.ano_letivo,
            componentes=request.componentes
        )
        
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/salvar-planejamento-completo")
async def salvar_planejamento_completo(
    request: SalvarPlanejamentoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Salva o planejamento COMPLETO como PEI no banco de dados.
    Cria o PEI e TODOS os objetivos (um para cada habilidade da BNCC).
    """
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    service = PlanejamentoBNNCCompletoService(db)
    
    try:
        pei = service.salvar_planejamento_completo(
            student_id=request.student_id,
            planejamento=request.planejamento,
            user_id=current_user.id,
            ano_letivo=request.ano_letivo
        )
        
        return {
            "success": True,
            "pei_id": pei.id,
            "message": "Planejamento completo salvo com sucesso",
            "total_objetivos": len(pei.objetivos)
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
