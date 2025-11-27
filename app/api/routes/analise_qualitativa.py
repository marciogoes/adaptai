"""
Rotas de Análise Qualitativa
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.prova import ProvaAluno, StatusProvaAluno
from app.models.analise_qualitativa import AnaliseQualitativa
from app.schemas.analise_qualitativa import (
    AnaliseQualitativaResponse,
    GerarAnaliseRequest,
    AnaliseQualitativaCompleta
)
from app.services.analise_qualitativa_service import analise_service
from app.api.dependencies import get_current_active_user
from app.models.user import User


router = APIRouter(prefix="/analise-qualitativa", tags=["Análise Qualitativa"])


@router.post("/prova-aluno/{prova_aluno_id}/gerar")
async def gerar_analise_qualitativa(
    prova_aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🤖 Gera análise qualitativa usando IA
    
    Analisa as respostas do aluno e gera insights sobre:
    - Pontos fortes
    - Pontos fracos  
    - Conteúdos a revisar
    - Recomendações específicas
    """
    
    # Buscar prova do aluno
    prova_aluno = db.query(ProvaAluno).filter(
        ProvaAluno.id == prova_aluno_id
    ).first()
    
    if not prova_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prova do aluno não encontrada"
        )
    
    # Verificar se prova está corrigida
    if prova_aluno.status != StatusProvaAluno.CORRIGIDA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prova precisa estar corrigida para gerar análise"
        )
    
    # Verificar se já existe análise
    analise_existente = db.query(AnaliseQualitativa).filter(
        AnaliseQualitativa.prova_aluno_id == prova_aluno_id
    ).first()
    
    if analise_existente:
        # Deletar análise antiga para gerar nova
        db.delete(analise_existente)
        db.commit()
    
    try:
        # Gerar análise com IA
        analise_ia = analise_service.gerar_analise(prova_aluno)
        
        # Salvar no banco
        nova_analise = AnaliseQualitativa(
            prova_aluno_id=prova_aluno_id,
            pontos_fortes=analise_ia.get('pontos_fortes', ''),
            pontos_fracos=analise_ia.get('pontos_fracos', ''),
            conteudos_revisar=analise_ia.get('conteudos_revisar', []),
            recomendacoes=analise_ia.get('recomendacoes', ''),
            analise_por_conteudo=analise_ia.get('analise_por_conteudo', {}),
            nivel_dominio=analise_ia.get('nivel_dominio', 'regular'),
            areas_prioridade=analise_ia.get('areas_prioridade', [])
        )
        
        db.add(nova_analise)
        db.commit()
        db.refresh(nova_analise)
        
        return {
            "success": True,
            "message": "Análise qualitativa gerada com sucesso!",
            "analise_id": nova_analise.id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar análise: {str(e)}"
        )


@router.get("/prova-aluno/{prova_aluno_id}", response_model=AnaliseQualitativaCompleta)
async def obter_analise_qualitativa(
    prova_aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📊 Obtém análise qualitativa de uma prova
    """
    
    # Buscar análise
    analise = db.query(AnaliseQualitativa).filter(
        AnaliseQualitativa.prova_aluno_id == prova_aluno_id
    ).first()
    
    if not analise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Análise não encontrada. Gere a análise primeiro."
        )
    
    # Buscar prova do aluno
    prova_aluno = db.query(ProvaAluno).filter(
        ProvaAluno.id == prova_aluno_id
    ).first()
    
    # Montar resposta completa
    return {
        "analise": analise,
        "prova_info": {
            "titulo": prova_aluno.prova.titulo,
            "materia": prova_aluno.prova.materia,
            "serie_nivel": prova_aluno.prova.serie_nivel,
            "nota_final": prova_aluno.nota_final,
            "aprovado": prova_aluno.aprovado
        },
        "aluno_info": {
            "nome": prova_aluno.aluno.name,
            "email": prova_aluno.aluno.email,
            "serie": prova_aluno.aluno.grade_level
        },
        "metricas": {
            "total_questoes": len(prova_aluno.respostas),
            "acertos": sum(1 for r in prova_aluno.respostas if r.esta_correta),
            "erros": sum(1 for r in prova_aluno.respostas if not r.esta_correta),
            "percentual_acerto": (sum(1 for r in prova_aluno.respostas if r.esta_correta) / len(prova_aluno.respostas) * 100) if prova_aluno.respostas else 0
        }
    }


@router.delete("/prova-aluno/{prova_aluno_id}")
async def deletar_analise(
    prova_aluno_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗑️ Deleta análise qualitativa
    """
    
    analise = db.query(AnaliseQualitativa).filter(
        AnaliseQualitativa.prova_aluno_id == prova_aluno_id
    ).first()
    
    if not analise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Análise não encontrada"
        )
    
    db.delete(analise)
    db.commit()
    
    return {"success": True, "message": "Análise deletada com sucesso"}
