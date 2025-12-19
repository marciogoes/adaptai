"""
Rotas para Professores - Analytics de Provas
Endpoints para professores visualizarem o rendimento dos alunos nas provas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.student import Student
from app.models.prova import Prova, ProvaAluno, QuestaoGerada, RespostaAluno, StatusProvaAluno
from app.api.dependencies import get_current_active_user

router = APIRouter(prefix="/professor/analytics", tags=["Professor - Analytics"])


@router.get("/dashboard")
def dashboard_professor(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Dashboard geral do professor com estatísticas de todas as provas
    """
    # Total de provas criadas
    total_provas = db.query(func.count(Prova.id)).filter(
        Prova.criado_por_id == current_user.id
    ).scalar()
    
    # Total de alunos
    total_alunos = db.query(func.count(Student.id)).filter(
        Student.created_by_user_id == current_user.id
    ).scalar()
    
    # Total de provas atribuídas
    total_provas_atribuidas = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id
    ).scalar()
    
    # Provas concluídas
    provas_concluidas = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.status.in_([StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA])
    ).scalar()
    
    # Provas em andamento
    provas_andamento = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.status == StatusProvaAluno.EM_ANDAMENTO
    ).scalar()
    
    # Provas pendentes
    provas_pendentes = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.status == StatusProvaAluno.PENDENTE
    ).scalar()
    
    # Média geral de notas
    media_geral = db.query(func.avg(ProvaAluno.nota_final)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.nota_final.isnot(None)
    ).scalar()
    
    # Taxa de aprovação
    total_com_nota = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.nota_final.isnot(None)
    ).scalar()
    
    aprovados = db.query(func.count(ProvaAluno.id)).join(
        Prova
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.aprovado == True
    ).scalar()
    
    taxa_aprovacao = (aprovados / total_com_nota * 100) if total_com_nota > 0 else 0
    
    # Provas recentes (últimas 10 conclusões)
    provas_recentes = db.query(ProvaAluno, Prova, Student).join(
        Prova, ProvaAluno.prova_id == Prova.id
    ).join(
        Student, ProvaAluno.aluno_id == Student.id
    ).filter(
        Prova.criado_por_id == current_user.id,
        ProvaAluno.status.in_([StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA])
    ).order_by(
        ProvaAluno.data_conclusao.desc()
    ).limit(10).all()
    
    provas_recentes_data = []
    for pa, prova, aluno in provas_recentes:
        provas_recentes_data.append({
            "prova_aluno_id": pa.id,
            "prova_titulo": prova.titulo,
            "aluno_nome": aluno.name,
            "nota_final": round(pa.nota_final, 2) if pa.nota_final else 0,
            "aprovado": pa.aprovado,
            "data_conclusao": pa.data_conclusao.isoformat() if pa.data_conclusao else None
        })
    
    return {
        "total_provas_criadas": total_provas,
        "total_alunos": total_alunos,
        "total_provas_atribuidas": total_provas_atribuidas,
        "provas_concluidas": provas_concluidas,
        "provas_em_andamento": provas_andamento,
        "provas_pendentes": provas_pendentes,
        "media_geral_notas": round(media_geral, 2) if media_geral else 0,
        "taxa_aprovacao": round(taxa_aprovacao, 2),
        "provas_recentes": provas_recentes_data
    }


@router.get("/alunos/lista")
def listar_alunos_com_rendimento(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os alunos do professor com estatísticas de rendimento
    """
    alunos = db.query(Student).filter(
        Student.created_by_user_id == current_user.id
    ).all()
    
    resultado = []
    
    for aluno in alunos:
        # Buscar todas as provas do aluno
        provas_aluno = db.query(ProvaAluno).join(
            Prova
        ).filter(
            ProvaAluno.aluno_id == aluno.id,
            Prova.criado_por_id == current_user.id
        ).all()
        
        total_provas = len(provas_aluno)
        provas_concluidas = len([p for p in provas_aluno if p.status in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]])
        provas_pendentes = len([p for p in provas_aluno if p.status == StatusProvaAluno.PENDENTE])
        provas_andamento = len([p for p in provas_aluno if p.status == StatusProvaAluno.EM_ANDAMENTO])
        
        # Calcular média de notas
        notas = [p.nota_final for p in provas_aluno if p.nota_final is not None]
        media_notas = sum(notas) / len(notas) if notas else 0
        
        # Última prova realizada
        ultima_prova = None
        if provas_concluidas > 0:
            ultima = max([p for p in provas_aluno if p.status in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]], 
                        key=lambda x: x.data_conclusao if x.data_conclusao else datetime.min)
            ultima_prova = {
                "id": ultima.id,
                "prova_titulo": ultima.prova.titulo,
                "nota": round(ultima.nota_final, 2) if ultima.nota_final else 0,
                "data": ultima.data_conclusao.isoformat() if ultima.data_conclusao else None
            }
        
        resultado.append({
            "aluno_id": aluno.id,
            "aluno_nome": aluno.name,
            "aluno_email": aluno.email,
            "serie_nivel": aluno.grade_level,
            "total_provas": total_provas,
            "provas_concluidas": provas_concluidas,
            "provas_pendentes": provas_pendentes,
            "provas_em_andamento": provas_andamento,
            "media_geral": round(media_notas, 2),
            "ultima_prova": ultima_prova
        })
    
    return resultado


@router.get("/aluno/{aluno_id}/provas")
def listar_provas_aluno(
    aluno_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Lista todas as provas de um aluno específico (resumo simples)
    """
    # Verificar se o aluno pertence ao professor
    aluno = db.query(Student).filter(
        Student.id == aluno_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    # Buscar todas as provas do aluno
    provas_aluno = db.query(ProvaAluno, Prova).join(
        Prova, ProvaAluno.prova_id == Prova.id
    ).filter(
        ProvaAluno.aluno_id == aluno_id,
        Prova.criado_por_id == current_user.id
    ).order_by(
        ProvaAluno.data_atribuicao.desc()
    ).all()
    
    resultado = []
    for pa, prova in provas_aluno:
        resultado.append({
            "prova_aluno_id": pa.id,
            "prova_id": prova.id,
            "titulo": prova.titulo,
            "materia": prova.materia,
            "status": pa.status.value,
            "nota": round(pa.nota_final, 2) if pa.nota_final else None,
            "aprovado": pa.aprovado,
            "data_conclusao": pa.data_conclusao.isoformat() if pa.data_conclusao else None
        })
    
    return resultado


@router.get("/aluno/{aluno_id}/detalhado")
def rendimento_detalhado_aluno(
    aluno_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Rendimento detalhado de um aluno específico com todas as provas
    """
    # Verificar se o aluno pertence ao professor
    aluno = db.query(Student).filter(
        Student.id == aluno_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    # Buscar todas as provas do aluno
    provas_aluno = db.query(ProvaAluno, Prova).join(
        Prova, ProvaAluno.prova_id == Prova.id
    ).filter(
        ProvaAluno.aluno_id == aluno_id,
        Prova.criado_por_id == current_user.id
    ).order_by(
        ProvaAluno.data_conclusao.desc()
    ).all()
    
    provas_detalhes = []
    for pa, prova in provas_aluno:
        # Buscar respostas
        respostas = db.query(RespostaAluno).filter(
            RespostaAluno.prova_aluno_id == pa.id
        ).all()
        
        total_questoes = len(respostas)
        acertos = len([r for r in respostas if r.esta_correta])
        erros = total_questoes - acertos
        
        provas_detalhes.append({
            "prova_aluno_id": pa.id,
            "prova_id": prova.id,
            "prova_titulo": prova.titulo,
            "prova_materia": prova.materia,
            "prova_serie": prova.serie_nivel,
            "status": pa.status.value,
            "data_atribuicao": pa.data_atribuicao.isoformat() if pa.data_atribuicao else None,
            "data_inicio": pa.data_inicio.isoformat() if pa.data_inicio else None,
            "data_conclusao": pa.data_conclusao.isoformat() if pa.data_conclusao else None,
            "nota_final": round(pa.nota_final, 2) if pa.nota_final else None,
            "aprovado": pa.aprovado,
            "tempo_gasto_minutos": pa.tempo_gasto_minutos,
            "total_questoes": total_questoes,
            "acertos": acertos,
            "erros": erros,
            "percentual_acerto": round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0,
            "pontuacao_obtida": pa.pontuacao_obtida,
            "pontuacao_maxima": pa.pontuacao_maxima,
            "analise_ia": pa.analise_ia,
            "feedback_ia": pa.feedback_ia
        })
    
    # Estatísticas gerais
    provas_concluidas = [p for p, _ in provas_aluno if p.status in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]]
    notas = [p.nota_final for p in provas_concluidas if p.nota_final is not None]
    
    estatisticas = {
        "total_provas": len(provas_aluno),
        "provas_concluidas": len(provas_concluidas),
        "provas_pendentes": len([p for p, _ in provas_aluno if p.status == StatusProvaAluno.PENDENTE]),
        "provas_em_andamento": len([p for p, _ in provas_aluno if p.status == StatusProvaAluno.EM_ANDAMENTO]),
        "media_notas": round(sum(notas) / len(notas), 2) if notas else 0,
        "nota_maxima": round(max(notas), 2) if notas else 0,
        "nota_minima": round(min(notas), 2) if notas else 0,
        "aprovacoes": len([p for p in provas_concluidas if p.aprovado]),
        "reprovacoes": len([p for p in provas_concluidas if not p.aprovado])
    }
    
    return {
        "aluno": {
            "id": aluno.id,
            "nome": aluno.name,
            "email": aluno.email,
            "serie": aluno.grade_level,
            "diagnostico": aluno.diagnosis
        },
        "estatisticas": estatisticas,
        "provas": provas_detalhes
    }


@router.get("/prova/{prova_aluno_id}/detalhes")
def detalhes_prova_realizada(
    prova_aluno_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Detalhes completos de uma prova realizada por um aluno
    Mostra todas as questões, respostas e análise
    """
    # Buscar prova do aluno
    prova_aluno = db.query(ProvaAluno, Prova, Student).join(
        Prova, ProvaAluno.prova_id == Prova.id
    ).join(
        Student, ProvaAluno.aluno_id == Student.id
    ).filter(
        ProvaAluno.id == prova_aluno_id,
        Prova.criado_por_id == current_user.id
    ).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    pa, prova, aluno = prova_aluno
    
    # Buscar todas as questões e respostas
    questoes_respostas = db.query(QuestaoGerada, RespostaAluno).outerjoin(
        RespostaAluno,
        and_(
            RespostaAluno.questao_id == QuestaoGerada.id,
            RespostaAluno.prova_aluno_id == prova_aluno_id
        )
    ).filter(
        QuestaoGerada.prova_id == prova.id
    ).order_by(
        QuestaoGerada.numero
    ).all()
    
    questoes_detalhes = []
    for questao, resposta in questoes_respostas:
        questoes_detalhes.append({
            "numero": questao.numero,
            "enunciado": questao.enunciado,
            "tipo": questao.tipo.value,
            "dificuldade": questao.dificuldade.value if questao.dificuldade else None,
            "opcoes": questao.opcoes,
            "resposta_correta": questao.resposta_correta,
            "resposta_aluno": resposta.resposta_aluno if resposta else None,
            "esta_correta": resposta.esta_correta if resposta else None,
            "pontuacao_obtida": resposta.pontuacao_obtida if resposta else 0,
            "pontuacao_maxima": questao.pontuacao,
            "explicacao": questao.explicacao,
            "feedback": resposta.feedback if resposta else None,
            "tempo_resposta_segundos": resposta.tempo_resposta_segundos if resposta else None
        })
    
    # Estatísticas da prova
    respostas = [r for _, r in questoes_respostas if r is not None]
    total_questoes = len(questoes_respostas)
    acertos = len([r for r in respostas if r.esta_correta])
    erros = len([r for r in respostas if not r.esta_correta])
    
    return {
        "prova_aluno_id": pa.id,
        "prova": {
            "id": prova.id,
            "titulo": prova.titulo,
            "descricao": prova.descricao,
            "materia": prova.materia,
            "serie_nivel": prova.serie_nivel,
            "tempo_limite_minutos": prova.tempo_limite_minutos,
            "pontuacao_total": prova.pontuacao_total,
            "nota_minima_aprovacao": prova.nota_minima_aprovacao
        },
        "aluno": {
            "id": aluno.id,
            "nome": aluno.name,
            "email": aluno.email,
            "serie": aluno.grade_level
        },
        "resultado": {
            "status": pa.status.value,
            "data_inicio": pa.data_inicio.isoformat() if pa.data_inicio else None,
            "data_conclusao": pa.data_conclusao.isoformat() if pa.data_conclusao else None,
            "tempo_gasto_minutos": pa.tempo_gasto_minutos,
            "nota_final": round(pa.nota_final, 2) if pa.nota_final else None,
            "aprovado": pa.aprovado,
            "pontuacao_obtida": pa.pontuacao_obtida,
            "pontuacao_maxima": pa.pontuacao_maxima,
            "total_questoes": total_questoes,
            "acertos": acertos,
            "erros": erros,
            "percentual_acerto": round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0
        },
        "questoes": questoes_detalhes,
        "analise_ia": pa.analise_ia,
        "feedback_ia": pa.feedback_ia
    }


@router.get("/prova/{prova_id}/estatisticas")
def estatisticas_prova(
    prova_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Estatísticas gerais de uma prova específica
    Mostra como todos os alunos se saíram nesta prova
    """
    # Verificar se a prova pertence ao professor
    prova = db.query(Prova).filter(
        Prova.id == prova_id,
        Prova.criado_por_id == current_user.id
    ).first()
    
    if not prova:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova não encontrada"
        )
    
    # Buscar todos os alunos que fizeram esta prova
    provas_alunos = db.query(ProvaAluno, Student).join(
        Student, ProvaAluno.aluno_id == Student.id
    ).filter(
        ProvaAluno.prova_id == prova_id
    ).all()
    
    total_atribuicoes = len(provas_alunos)
    concluidas = len([pa for pa, _ in provas_alunos if pa.status in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]])
    pendentes = len([pa for pa, _ in provas_alunos if pa.status == StatusProvaAluno.PENDENTE])
    em_andamento = len([pa for pa, _ in provas_alunos if pa.status == StatusProvaAluno.EM_ANDAMENTO])
    
    # Estatísticas de notas
    notas = [pa.nota_final for pa, _ in provas_alunos if pa.nota_final is not None]
    
    alunos_resultados = []
    for pa, aluno in provas_alunos:
        if pa.status in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]:
            alunos_resultados.append({
                "aluno_id": aluno.id,
                "aluno_nome": aluno.name,
                "nota": round(pa.nota_final, 2) if pa.nota_final else 0,
                "aprovado": pa.aprovado,
                "data_conclusao": pa.data_conclusao.isoformat() if pa.data_conclusao else None,
                "tempo_gasto": pa.tempo_gasto_minutos
            })
    
    # Ordenar por nota (decrescente)
    alunos_resultados.sort(key=lambda x: x['nota'], reverse=True)
    
    return {
        "prova": {
            "id": prova.id,
            "titulo": prova.titulo,
            "materia": prova.materia,
            "serie_nivel": prova.serie_nivel,
            "quantidade_questoes": prova.quantidade_questoes
        },
        "estatisticas": {
            "total_atribuicoes": total_atribuicoes,
            "concluidas": concluidas,
            "pendentes": pendentes,
            "em_andamento": em_andamento,
            "media_geral": round(sum(notas) / len(notas), 2) if notas else 0,
            "nota_maxima": round(max(notas), 2) if notas else 0,
            "nota_minima": round(min(notas), 2) if notas else 0,
            "taxa_aprovacao": round((len([n for n in notas if n >= prova.nota_minima_aprovacao]) / len(notas) * 100), 2) if notas else 0
        },
        "alunos": alunos_resultados
    }


@router.get("/comparar-alunos")
def comparar_alunos(
    aluno_ids: str,  # Ex: "1,2,3,4"
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Comparar desempenho de múltiplos alunos
    """
    # Parse IDs
    try:
        ids = [int(id.strip()) for id in aluno_ids.split(",")]
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de IDs inválido. Use IDs separados por vírgula."
        )
    
    comparacoes = []
    
    for aluno_id in ids:
        # Verificar se o aluno pertence ao professor
        aluno = db.query(Student).filter(
            Student.id == aluno_id,
            Student.created_by_user_id == current_user.id
        ).first()
        
        if not aluno:
            continue
        
        # Buscar provas concluídas
        provas_concluidas = db.query(ProvaAluno).join(
            Prova
        ).filter(
            ProvaAluno.aluno_id == aluno_id,
            Prova.criado_por_id == current_user.id,
            ProvaAluno.status.in_([StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA])
        ).all()
        
        if provas_concluidas:
            notas = [p.nota_final for p in provas_concluidas if p.nota_final is not None]
            media = sum(notas) / len(notas) if notas else 0
            
            comparacoes.append({
                "aluno_id": aluno.id,
                "aluno_nome": aluno.name,
                "total_provas": len(provas_concluidas),
                "media_geral": round(media, 2),
                "nota_maxima": round(max(notas), 2) if notas else 0,
                "nota_minima": round(min(notas), 2) if notas else 0,
                "aprovacoes": len([p for p in provas_concluidas if p.aprovado]),
                "reprovacoes": len([p for p in provas_concluidas if not p.aprovado])
            })
    
    return {
        "total_alunos": len(comparacoes),
        "comparacoes": comparacoes
    }
