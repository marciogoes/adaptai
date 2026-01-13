"""
🎓 AdaptAI - Rotas de Prova
Endpoints para gerenciamento de provas com IA
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timezone

from app.database import get_db, SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.prova import (
    Prova, 
    QuestaoGerada, 
    ProvaAluno, 
    RespostaAluno,
    StatusProva,
    StatusProvaAluno
)
from app.schemas.prova import (
    ProvaCreate,
    ProvaResponse,
    ProvaListResponse,
    ProvaUpdate,
    GerarProvaRequest,
    ProvaAlunoCreate,
    ProvaAlunoResponse,
    ProvaAlunoListResponse,
    IniciarProvaRequest,
    FinalizarProvaRequest,
    RespostaAlunoCreate,
    RespostaAlunoResponse,
    CorrigirProvaResponse,
    ProvaParaAluno,
    QuestaoParaAluno
)
from app.services.prova_ai_service import prova_ai_service
from app.api.dependencies import get_current_user, oauth2_scheme, get_user_from_token

router = APIRouter(prefix="/provas")


# ============= ENDPOINTS ADMIN =============

@router.post("/gerar", response_model=ProvaResponse, status_code=status.HTTP_201_CREATED)
async def gerar_prova_com_ia(
    request: GerarProvaRequest,
    token: str = Depends(oauth2_scheme)
):
    """
    Gerar prova automaticamente com IA
    
    **Fluxo:**
    1. Admin define o tema/conteudo e configuracoes
    2. IA (Claude) gera automaticamente as questoes
    3. Prova e salva no banco de dados
    
    **Requer:** Autenticacao de admin/professor
    """
    
    # Valida usuario e fecha conexao ANTES de chamar IA
    current_user = get_user_from_token(token)
    user_id = current_user.id
    
    try:
        # PASSO 1: Gera questoes com IA (SEM conexao com banco)
        print(f"[GERANDO] {request.quantidade_questoes} questoes com IA...")
        questoes_geradas = await prova_ai_service.gerar_questoes(
            conteudo_prompt=request.conteudo_prompt,
            materia=request.materia,
            serie_nivel=request.serie_nivel or "Nao especificado",
            quantidade=request.quantidade_questoes,
            tipo_questao=request.tipo_questao,
            dificuldade=request.dificuldade
        )
        print(f"[OK] IA gerou {len(questoes_geradas)} questoes")
        
        # PASSO 2: Abre NOVA conexao e salva tudo (conexao fresca)
        db = SessionLocal()
        try:
            # Cria a prova
            nova_prova = Prova(
                titulo=request.titulo,
                descricao=request.descricao,
                conteudo_prompt=request.conteudo_prompt,
                materia=request.materia,
                serie_nivel=request.serie_nivel,
                quantidade_questoes=request.quantidade_questoes,
                tipo_questao=request.tipo_questao,
                dificuldade=request.dificuldade,
                tempo_limite_minutos=request.tempo_limite_minutos,
                pontuacao_total=request.pontuacao_total,
                nota_minima_aprovacao=request.nota_minima_aprovacao,
                status=StatusProva.ATIVA,
                criado_por_id=user_id
            )
            
            db.add(nova_prova)
            db.flush()  # Get prova.id
            
            # Adiciona as questoes geradas
            pontos_por_questao = request.pontuacao_total / request.quantidade_questoes
            
            for questao_data in questoes_geradas:
                questao = QuestaoGerada(
                    prova_id=nova_prova.id,
                    numero=questao_data.get("numero"),
                    enunciado=questao_data.get("enunciado"),
                    tipo=request.tipo_questao,
                    dificuldade=questao_data.get("dificuldade", request.dificuldade),
                    opcoes=questao_data.get("opcoes"),
                    resposta_correta=questao_data.get("resposta_correta"),
                    criterios_avaliacao=questao_data.get("criterios_avaliacao"),
                    pontuacao=pontos_por_questao,
                    explicacao=questao_data.get("explicacao"),
                    tags=questao_data.get("tags", [])
                )
                db.add(questao)
            
            db.commit()
            
            # Busca a prova com questoes carregadas (eager loading)
            prova_completa = db.query(Prova).options(
                joinedload(Prova.questoes)
            ).filter(Prova.id == nova_prova.id).first()
            
            print(f"[OK] Prova '{prova_completa.titulo}' criada com sucesso! (ID: {prova_completa.id})")
            
            return prova_completa
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
        
    except Exception as e:
        print(f"[ERRO] Erro ao gerar prova: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar prova: {str(e)}"
        )


@router.get("/", response_model=List[ProvaListResponse])
def listar_provas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """📋 Listar todas as provas criadas"""
    provas = db.query(Prova).offset(skip).limit(limit).all()
    return provas


@router.get("/{prova_id}", response_model=ProvaResponse)
def obter_prova(
    prova_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """📄 Obter detalhes de uma prova específica (com questões e respostas)"""
    prova = db.query(Prova).filter(Prova.id == prova_id).first()
    
    if not prova:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    return prova


@router.patch("/{prova_id}", response_model=ProvaResponse)
def atualizar_prova(
    prova_id: int,
    prova_update: ProvaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """✏️ Atualizar informações da prova"""
    prova = db.query(Prova).filter(Prova.id == prova_id).first()
    
    if not prova:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    # Atualiza campos
    for field, value in prova_update.dict(exclude_unset=True).items():
        setattr(prova, field, value)
    
    prova.atualizado_em = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(prova)
    
    return prova


@router.delete("/{prova_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_prova(
    prova_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """🗑️ Deletar uma prova"""
    prova = db.query(Prova).filter(Prova.id == prova_id).first()
    
    if not prova:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    db.delete(prova)
    db.commit()
    
    return None


# ============= ENDPOINTS ASSOCIAÇÃO PROVA-ALUNO =============

@router.post("/associar", response_model=ProvaAlunoResponse, status_code=status.HTTP_201_CREATED)
def associar_prova_ao_aluno(
    associacao: ProvaAlunoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    👨‍🎓 Associar prova a um aluno
    
    O admin seleciona uma prova e um aluno, e o sistema libera a prova para o aluno fazer.
    """
    
    # Verifica se prova existe
    prova = db.query(Prova).filter(Prova.id == associacao.prova_id).first()
    if not prova:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    # Verifica se aluno existe
    aluno = db.query(Student).filter(Student.id == associacao.aluno_id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    # Verifica se já está associado
    ja_associado = db.query(ProvaAluno).filter(
        ProvaAluno.prova_id == associacao.prova_id,
        ProvaAluno.aluno_id == associacao.aluno_id
    ).first()
    
    if ja_associado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta prova já está associada a este aluno"
        )
    
    # Cria associação
    prova_aluno = ProvaAluno(
        prova_id=associacao.prova_id,
        aluno_id=associacao.aluno_id,
        status=StatusProvaAluno.PENDENTE,
        pontuacao_maxima=prova.pontuacao_total
    )
    
    db.add(prova_aluno)
    db.commit()
    db.refresh(prova_aluno)
    
    print(f"[OK] Prova '{prova.titulo}' associada ao aluno '{aluno.name}'")
    
    return prova_aluno


@router.get("/aluno/{aluno_id}/provas", response_model=List[ProvaAlunoListResponse])
def listar_provas_do_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """📚 Listar todas as provas de um aluno"""
    provas_aluno = db.query(ProvaAluno).filter(
        ProvaAluno.aluno_id == aluno_id
    ).all()
    
    return provas_aluno


# ============= ENDPOINTS DO ALUNO =============

@router.get("/aluno/{prova_aluno_id}/fazer", response_model=ProvaParaAluno)
def obter_prova_para_fazer(
    prova_aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    📝 Obter prova para o aluno fazer
    
    Retorna as questões SEM as respostas corretas.
    """
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    prova = prova_aluno.prova
    
    # Monta questões sem respostas
    questoes_para_aluno = [
        QuestaoParaAluno(
            id=q.id,
            numero=q.numero,
            enunciado=q.enunciado,
            tipo=q.tipo,
            opcoes=q.opcoes,
            pontuacao=q.pontuacao
        )
        for q in prova.questoes
    ]
    
    return ProvaParaAluno(
        id=prova.id,
        titulo=prova.titulo,
        descricao=prova.descricao,
        materia=prova.materia,
        serie_nivel=prova.serie_nivel,
        tempo_limite_minutos=prova.tempo_limite_minutos,
        pontuacao_total=prova.pontuacao_total,
        questoes=questoes_para_aluno
    )


@router.post("/aluno/iniciar")
def iniciar_prova(
    request: IniciarProvaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """▶️ Aluno inicia a prova"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == request.prova_aluno_id).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    if prova_aluno.status != StatusProvaAluno.PENDENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prova já foi iniciada"
        )
    
    prova_aluno.status = StatusProvaAluno.EM_ANDAMENTO
    prova_aluno.data_inicio = datetime.now(timezone.utc)
    
    db.commit()
    
    return {"message": "Prova iniciada com sucesso", "data_inicio": prova_aluno.data_inicio}


@router.post("/aluno/finalizar", response_model=CorrigirProvaResponse)
async def finalizar_prova(
    request: FinalizarProvaRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ✅ Aluno finaliza a prova e sistema corrige automaticamente
    
    **Processo:**
    1. Recebe todas as respostas do aluno
    2. Salva as respostas no banco
    3. Corrige automaticamente
    4. Gera análise com IA
    5. Retorna resultado
    """
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == request.prova_aluno_id).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    if prova_aluno.status == StatusProvaAluno.CONCLUIDA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prova já foi finalizada"
        )
    
    prova = prova_aluno.prova
    questoes = {q.id: q for q in prova.questoes}
    
    # Salva respostas e corrige
    respostas_salvas = []
    acertos = 0
    erros = 0
    pontuacao_obtida = 0.0
    
    for resposta_data in request.respostas:
        questao = questoes.get(resposta_data.questao_id)
        
        if not questao:
            continue
        
        # Verifica se está correta
        esta_correta = questao.resposta_correta.strip().lower() == resposta_data.resposta_aluno.strip().lower()
        pontos = questao.pontuacao if esta_correta else 0.0
        
        if esta_correta:
            acertos += 1
        else:
            erros += 1
        
        pontuacao_obtida += pontos
        
        # Salva resposta
        resposta = RespostaAluno(
            prova_aluno_id=prova_aluno.id,
            questao_id=questao.id,
            resposta_aluno=resposta_data.resposta_aluno,
            esta_correta=esta_correta,
            pontuacao_obtida=pontos,
            pontuacao_maxima=questao.pontuacao,
            tempo_resposta_segundos=resposta_data.tempo_resposta_segundos
        )
        
        db.add(resposta)
        respostas_salvas.append(resposta)
    
    # Calcula nota final
    nota_final = (pontuacao_obtida / prova.pontuacao_total) * 10
    aprovado = nota_final >= prova.nota_minima_aprovacao
    
    # Calcula tempo gasto
    tempo_gasto = int((datetime.now(timezone.utc) - prova_aluno.data_inicio).total_seconds() / 60) if prova_aluno.data_inicio else 0
    
    # Atualiza prova_aluno
    prova_aluno.status = StatusProvaAluno.CONCLUIDA
    prova_aluno.data_conclusao = datetime.now(timezone.utc)
    prova_aluno.pontuacao_obtida = pontuacao_obtida
    prova_aluno.nota_final = nota_final
    prova_aluno.aprovado = aprovado
    prova_aluno.tempo_gasto_minutos = tempo_gasto
    
    db.commit()
    
    # Gera análise com IA
    try:
        aluno = prova_aluno.aluno
        questoes_lista = [
            {
                "numero": q.numero,
                "enunciado": q.enunciado,
                "resposta_correta": q.resposta_correta
            }
            for q in prova.questoes
        ]
        
        respostas_lista = [
            {
                "questao_numero": questoes[r.questao_id].numero,
                "resposta_aluno": r.resposta_aluno,
                "esta_correta": r.esta_correta
            }
            for r in respostas_salvas
        ]
        
        aluno_info = {
            "nome": aluno.name,
            "serie": aluno.grade_level,
            "diagnosticos": aluno.diagnosis or {}
        }
        
        analise = await prova_ai_service.analisar_desempenho(
            questoes=questoes_lista,
            respostas=respostas_lista,
            aluno_info=aluno_info
        )
        
        feedback = await prova_ai_service.gerar_feedback_personalizado(
            questoes=questoes_lista,
            respostas=respostas_lista,
            analise=analise,
            aluno_info=aluno_info
        )
        
        prova_aluno.analise_ia = analise
        prova_aluno.feedback_ia = feedback
        prova_aluno.status = StatusProvaAluno.CORRIGIDA
        prova_aluno.data_correcao = datetime.now(timezone.utc)
        
        db.commit()
        
    except Exception as e:
        print(f"[AVISO] Erro ao gerar analise IA: {e}")
        analise = {}
        feedback = "Prova corrigida com sucesso!"
    
    # Monta resposta
    percentual = (acertos / len(request.respostas) * 100) if request.respostas else 0
    
    db.refresh(prova_aluno)
    
    return CorrigirProvaResponse(
        prova_aluno_id=prova_aluno.id,
        pontuacao_obtida=pontuacao_obtida,
        pontuacao_maxima=prova.pontuacao_total,
        nota_final=nota_final,
        aprovado=aprovado,
        acertos=acertos,
        erros=erros,
        percentual_acerto=percentual,
        analise_ia=analise,
        feedback_ia=feedback,
        respostas_detalhadas=[RespostaAlunoResponse.from_orm(r) for r in respostas_salvas]
    )


@router.get("/aluno/{prova_aluno_id}/resultado", response_model=ProvaAlunoResponse)
def obter_resultado(
    prova_aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """📊 Obter resultado da prova do aluno"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    if prova_aluno.status not in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prova ainda não foi finalizada"
        )
    
    return prova_aluno
