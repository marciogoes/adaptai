"""
📔 Rotas - Diário de Aprendizagem Inteligente
CRUD + Análise com IA + Estatísticas + Timeline
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import date, datetime, timedelta, timezone

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.diario_aprendizagem import (
    DiarioAprendizagem, 
    ConteudoExtraido, 
    ResumoSemanalAprendizagem,
    HumorEstudo,
    NivelCompreensao
)
from app.schemas.diario_aprendizagem import (
    DiarioCreate,
    DiarioUpdate,
    DiarioResponse,
    DiarioListItem,
    ConteudoExtraidoResponse,
    ConteudosParaMaterialResponse,
    ResumoSemanalResponse,
    AnaliseRegistroResponse,
    GerarResumoRequest,
    EstatisticasDiarioResponse,
    TimelineResponse,
    TimelineItem
)
from app.services.diario_ai_service import diario_ai_service


router = APIRouter(prefix="/diario-aprendizagem", tags=["📔 Diário de Aprendizagem"])


# ============================================
# CRUD - REGISTROS DO DIÁRIO
# ============================================

@router.post("/", response_model=DiarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_registro(
    dados: DiarioCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📝 Cria um novo registro no diário de aprendizagem
    
    O registro é criado e a análise com IA é executada em background.
    A IA irá extrair automaticamente:
    - Disciplinas estudadas
    - Tópicos e conceitos
    - Dificuldades identificadas
    - Sugestões de revisão
    - Conexões com BNCC
    """
    
    # Verificar se aluno existe e pertence ao usuário
    student = db.query(Student).filter(
        Student.id == dados.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado ou não pertence a você"
        )
    
    # Verificar se já existe registro para esta data
    existente = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.student_id == dados.student_id,
        DiarioAprendizagem.data_estudo == dados.data_estudo
    ).first()
    
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um registro para {dados.data_estudo}. Use PUT para atualizar."
        )
    
    # Criar registro
    diario = DiarioAprendizagem(
        student_id=dados.student_id,
        data_estudo=dados.data_estudo,
        registro_texto=dados.registro_texto,
        periodo=dados.periodo,
        humor=HumorEstudo(dados.humor) if dados.humor else None,
        nivel_compreensao=NivelCompreensao(dados.nivel_compreensao) if dados.nivel_compreensao else None,
        tempo_estudo_minutos=dados.tempo_estudo_minutos,
        created_by=current_user.id
    )
    
    db.add(diario)
    db.commit()
    db.refresh(diario)
    
    # Agendar análise com IA em background
    background_tasks.add_task(
        processar_diario_background,
        diario.id,
        student.id
    )
    
    return diario


async def processar_diario_background(diario_id: int, student_id: int):
    """Processa o diário com IA em background"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        diario = db.query(DiarioAprendizagem).filter(
            DiarioAprendizagem.id == diario_id
        ).first()
        
        student = db.query(Student).filter(
            Student.id == student_id
        ).first()
        
        if diario and student:
            await diario_ai_service.analisar_registro(db, diario, student)
            print(f"✅ Diário {diario_id} processado com IA!")
    except Exception as e:
        print(f"❌ Erro ao processar diário {diario_id}: {e}")
    finally:
        db.close()


@router.get("/student/{student_id}", response_model=List[DiarioListItem])
async def listar_registros_aluno(
    student_id: int,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📋 Lista registros do diário de um aluno
    
    Filtros opcionais por período de datas.
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    query = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.student_id == student_id
    )
    
    if data_inicio:
        query = query.filter(DiarioAprendizagem.data_estudo >= data_inicio)
    
    if data_fim:
        query = query.filter(DiarioAprendizagem.data_estudo <= data_fim)
    
    registros = query.order_by(
        desc(DiarioAprendizagem.data_estudo)
    ).limit(limit).offset(offset).all()
    
    return registros


@router.get("/{diario_id}", response_model=DiarioResponse)
async def obter_registro(
    diario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔍 Obtém um registro específico com toda a análise da IA
    """
    
    diario = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.id == diario_id
    ).first()
    
    if not diario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == diario.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este registro"
        )
    
    return diario


@router.put("/{diario_id}", response_model=DiarioResponse)
async def atualizar_registro(
    diario_id: int,
    dados: DiarioUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ✏️ Atualiza um registro existente
    
    Se o texto for alterado, a análise da IA será refeita.
    """
    
    diario = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.id == diario_id
    ).first()
    
    if not diario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == diario.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão"
        )
    
    texto_alterado = False
    
    if dados.registro_texto and dados.registro_texto != diario.registro_texto:
        diario.registro_texto = dados.registro_texto
        diario.ia_processado = False
        texto_alterado = True
    
    if dados.periodo:
        diario.periodo = dados.periodo
    
    if dados.humor:
        diario.humor = HumorEstudo(dados.humor)
    
    if dados.nivel_compreensao:
        diario.nivel_compreensao = NivelCompreensao(dados.nivel_compreensao)
    
    if dados.tempo_estudo_minutos is not None:
        diario.tempo_estudo_minutos = dados.tempo_estudo_minutos
    
    db.commit()
    db.refresh(diario)
    
    # Re-analisar se texto foi alterado
    if texto_alterado:
        background_tasks.add_task(
            processar_diario_background,
            diario.id,
            student.id
        )
    
    return diario


@router.delete("/{diario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_registro(
    diario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗑️ Deleta um registro do diário
    """
    
    diario = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.id == diario_id
    ).first()
    
    if not diario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == diario.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão"
        )
    
    db.delete(diario)
    db.commit()
    
    return None


# ============================================
# ANÁLISE COM IA
# ============================================

@router.post("/{diario_id}/analisar", response_model=AnaliseRegistroResponse)
async def analisar_registro(
    diario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🤖 Força re-análise de um registro com IA
    
    Útil quando a análise automática falhou ou precisa ser atualizada.
    """
    
    diario = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.id == diario_id
    ).first()
    
    if not diario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    student = db.query(Student).filter(
        Student.id == diario.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão"
        )
    
    resultado = await diario_ai_service.analisar_registro(db, diario, student)
    
    return AnaliseRegistroResponse(
        success=resultado["success"],
        diario_id=diario_id,
        analise=resultado.get("analise"),
        error=resultado.get("error")
    )


# ============================================
# RESUMO SEMANAL
# ============================================

@router.post("/resumo-semanal/gerar")
async def gerar_resumo_semanal(
    request: GerarResumoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📊 Gera resumo semanal consolidado com IA
    
    Analisa todos os registros da semana e gera:
    - Resumo geral
    - Principais conquistas
    - Áreas que precisam de atenção
    - Recomendações de estudo
    - Dados para gráficos
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == request.student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    resultado = await diario_ai_service.gerar_resumo_semanal(
        db,
        request.student_id,
        request.data_referencia
    )
    
    if not resultado["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resultado.get("error", "Erro ao gerar resumo")
        )
    
    return resultado


@router.get("/resumo-semanal/student/{student_id}", response_model=List[ResumoSemanalResponse])
async def listar_resumos_semanais(
    student_id: int,
    ano: Optional[int] = None,
    limit: int = Query(10, le=52),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📅 Lista resumos semanais de um aluno
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    query = db.query(ResumoSemanalAprendizagem).filter(
        ResumoSemanalAprendizagem.student_id == student_id
    )
    
    if ano:
        query = query.filter(ResumoSemanalAprendizagem.ano == ano)
    
    resumos = query.order_by(
        desc(ResumoSemanalAprendizagem.ano),
        desc(ResumoSemanalAprendizagem.numero_semana)
    ).limit(limit).all()
    
    return resumos


# ============================================
# CONTEÚDOS PARA MATERIAL
# ============================================

@router.get("/conteudos-material/student/{student_id}", response_model=ConteudosParaMaterialResponse)
async def obter_conteudos_para_material(
    student_id: int,
    disciplina: Optional[str] = None,
    limite: int = Query(10, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🎯 Obtém conteúdos prioritários para geração de material
    
    Retorna os tópicos mais relevantes extraídos dos diários,
    ordenados por prioridade de revisão.
    
    Usado como insumo para a geração de materiais adaptados!
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    conteudos = diario_ai_service.obter_conteudos_para_material(
        db, student_id, disciplina, limite
    )
    
    return ConteudosParaMaterialResponse(
        student_id=student_id,
        total=len(conteudos),
        conteudos=conteudos
    )


@router.post("/conteudos-material/{conteudo_id}/marcar-gerado")
async def marcar_conteudo_gerado(
    conteudo_id: int,
    material_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ✅ Marca um conteúdo como já tendo material gerado
    
    Usado após gerar material para evitar duplicação.
    """
    
    conteudo = db.query(ConteudoExtraido).filter(
        ConteudoExtraido.id == conteudo_id
    ).first()
    
    if not conteudo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado"
        )
    
    conteudo.material_gerado = True
    if material_id:
        conteudo.material_id = material_id
    
    db.commit()
    
    return {"success": True, "message": "Conteúdo marcado como gerado"}


# ============================================
# ESTATÍSTICAS
# ============================================

@router.get("/estatisticas/student/{student_id}", response_model=EstatisticasDiarioResponse)
async def obter_estatisticas(
    student_id: int,
    periodo_dias: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📈 Obtém estatísticas completas do diário
    
    Inclui distribuições, tendências e insights.
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    data_inicio = date.today() - timedelta(days=periodo_dias)
    
    # Buscar diários do período
    diarios = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.student_id == student_id,
        DiarioAprendizagem.data_estudo >= data_inicio
    ).all()
    
    # Calcular estatísticas
    total_registros = len(diarios)
    total_minutos = sum(d.tempo_estudo_minutos or 0 for d in diarios)
    media_minutos = total_minutos / total_registros if total_registros > 0 else 0
    
    # Por disciplina
    por_disciplina = {}
    for d in diarios:
        if d.ia_disciplinas_detectadas:
            for disc in d.ia_disciplinas_detectadas:
                por_disciplina[disc] = por_disciplina.get(disc, 0) + 1
    
    # Por humor
    por_humor = {}
    for d in diarios:
        if d.humor:
            por_humor[d.humor.value] = por_humor.get(d.humor.value, 0) + 1
    
    # Por nível de compreensão
    por_nivel = {}
    for d in diarios:
        if d.nivel_compreensao:
            por_nivel[d.nivel_compreensao.value] = por_nivel.get(d.nivel_compreensao.value, 0) + 1
    
    # Tópicos mais estudados
    conteudos = db.query(ConteudoExtraido).filter(
        ConteudoExtraido.student_id == student_id
    ).order_by(desc(ConteudoExtraido.vezes_mencionado)).limit(5).all()
    
    topicos_mais_estudados = [
        {
            "topico": c.topico,
            "disciplina": c.disciplina,
            "vezes": c.vezes_mencionado
        }
        for c in conteudos
    ]
    
    # Tópicos com dificuldade
    conteudos_dif = db.query(ConteudoExtraido).filter(
        ConteudoExtraido.student_id == student_id,
        ConteudoExtraido.nivel_dificuldade_percebido.in_(["dificil", "muito_dificil"])
    ).order_by(desc(ConteudoExtraido.prioridade_revisao)).limit(5).all()
    
    topicos_com_dificuldade = [
        {
            "topico": c.topico,
            "disciplina": c.disciplina,
            "prioridade": c.prioridade_revisao
        }
        for c in conteudos_dif
    ]
    
    # Por semana
    registros_por_semana = {}
    for d in diarios:
        semana = d.data_estudo.isocalendar()[1]
        chave = f"{d.data_estudo.year}-S{semana:02d}"
        registros_por_semana[chave] = registros_por_semana.get(chave, 0) + 1
    
    return EstatisticasDiarioResponse(
        student_id=student_id,
        student_name=student.name,
        periodo=f"Últimos {periodo_dias} dias",
        total_registros=total_registros,
        total_minutos_estudo=total_minutos,
        media_minutos_por_dia=round(media_minutos, 1),
        por_disciplina=por_disciplina,
        por_humor=por_humor,
        por_nivel_compreensao=por_nivel,
        topicos_mais_estudados=topicos_mais_estudados,
        topicos_com_dificuldade=topicos_com_dificuldade,
        registros_por_semana=registros_por_semana
    )


# ============================================
# TIMELINE
# ============================================

@router.get("/timeline/student/{student_id}", response_model=TimelineResponse)
async def obter_timeline(
    student_id: int,
    dias: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📅 Obtém timeline de aprendizagem do aluno
    
    Combina registros do diário com outros eventos educacionais.
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    data_inicio = date.today() - timedelta(days=dias)
    data_fim = date.today()
    
    # Buscar diários
    diarios = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.student_id == student_id,
        DiarioAprendizagem.data_estudo >= data_inicio
    ).order_by(desc(DiarioAprendizagem.data_estudo)).all()
    
    itens = []
    
    for d in diarios:
        itens.append(TimelineItem(
            data=d.data_estudo,
            tipo="diario",
            titulo=d.ia_resumo or f"Estudo - {d.data_estudo}",
            descricao=d.registro_texto[:200] + "..." if len(d.registro_texto) > 200 else d.registro_texto,
            disciplinas=d.ia_disciplinas_detectadas,
            humor=d.humor.value if d.humor else None,
            destaque=d.ia_sentimento_geral == "positivo"
        ))
    
    return TimelineResponse(
        student_id=student_id,
        periodo_inicio=data_inicio,
        periodo_fim=data_fim,
        total_itens=len(itens),
        itens=itens
    )


# ============================================
# BUSCA
# ============================================

@router.get("/buscar/student/{student_id}")
async def buscar_nos_diarios(
    student_id: int,
    q: str = Query(..., min_length=2),
    disciplina: Optional[str] = None,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔍 Busca nos diários do aluno
    
    Busca por texto, tags, conceitos ou tópicos.
    """
    
    # Verificar permissão
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    query = db.query(DiarioAprendizagem).filter(
        DiarioAprendizagem.student_id == student_id
    )
    
    # Buscar no texto
    query = query.filter(
        DiarioAprendizagem.registro_texto.ilike(f"%{q}%")
    )
    
    resultados = query.order_by(
        desc(DiarioAprendizagem.data_estudo)
    ).limit(limit).all()
    
    return {
        "query": q,
        "total": len(resultados),
        "resultados": [
            {
                "id": r.id,
                "data": r.data_estudo,
                "resumo": r.ia_resumo,
                "disciplinas": r.ia_disciplinas_detectadas,
                "trecho": r.registro_texto[:200]
            }
            for r in resultados
        ]
    }
