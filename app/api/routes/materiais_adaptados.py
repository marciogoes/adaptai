"""
Rotas para Geração de Materiais Adaptados
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import time

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.material_adaptado_gerado import MaterialAdaptadoGerado
from app.schemas.material_adaptado import (
    MaterialAdaptadoRequest,
    MaterialAdaptadoResponse,
    TextoNiveisResponse,
    InfograficoResponse,
    FlashcardResponse,
    CacaPalavrasResponse,
    BingoEducativoResponse,
    AvaliacaoMultiformatoResponse,
    MapaMentalResponse
)
from app.services.ai_materiais_service import MaterialAdaptadoService


router = APIRouter(prefix="/materiais-adaptados", tags=["Materiais Adaptados"])


@router.post("/gerar", response_model=MaterialAdaptadoResponse)
async def gerar_materiais_adaptados(
    request: MaterialAdaptadoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🎨 GERA MATERIAIS EDUCACIONAIS ADAPTADOS
    
    Tipos disponíveis:
    - texto_niveis: Texto em 3 níveis de complexidade
    - infografico: Infográfico visual
    - flashcards: Cards de estudo
    - caca_palavras: Busca de termos técnicos
    - cruzadinha: Palavras cruzadas técnicas
    - bingo: Bingo educativo
    - avaliacao: Avaliação em 3 formatos
    - mapa_mental: Mapa mental/conceitual
    """
    
    inicio = time.time()
    
    # Buscar aluno
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Extrair diagnósticos do aluno
    diagnosticos = {}
    if student.diagnosis:
        diag = student.diagnosis
        diagnosticos = {
            "tea": diag.get("tea", False),
            "tea_nivel": diag.get("tea_nivel", ""),
            "tdah": diag.get("tdah", False),
            "dislexia": diag.get("dislexia", False),
            "discalculia": diag.get("discalculia", False),
            "disgrafia": diag.get("disgrafia", False),
            "deficiencia_intelectual": diag.get("deficiencia_intelectual", False),
            "superdotacao": diag.get("superdotacao", False),
            "outro": diag.get("outro", False),
            "caracteristicas": diag.get("caracteristicas", ""),
            "pontos_fortes": diag.get("pontos_fortes", ""),
            "dificuldades": diag.get("dificuldades", "")
        }
    
    # Inicializar service
    service = MaterialAdaptadoService()
    
    # Resposta base
    response = {
        "success": True,
        "student_name": student.name,
        "disciplina": request.disciplina,
        "conteudo": request.conteudo
    }
    
    # Gerar cada tipo de material solicitado
    try:
        if "texto_niveis" in request.tipos_material:
            print("🔄 Gerando texto em 3 níveis...")
            texto_data = service.gerar_texto_3_niveis(
                request.disciplina,
                request.serie,
                request.conteudo,
                diagnosticos
            )
            response["texto_niveis"] = TextoNiveisResponse(**texto_data)
            print("✅ Texto gerado!")
        
        if "infografico" in request.tipos_material:
            print("🔄 Gerando infográfico...")
            info_data = service.gerar_infografico(
                request.disciplina,
                request.serie,
                request.conteudo
            )
            response["infografico"] = InfograficoResponse(**info_data)
            print("✅ Infográfico gerado!")
        
        if "flashcards" in request.tipos_material:
            print("🔄 Gerando flashcards...")
            flash_data = service.gerar_flashcards(
                request.disciplina,
                request.serie,
                request.conteudo
            )
            response["flashcards"] = FlashcardResponse(**flash_data)
            print("✅ Flashcards gerados!")
        
        if "caca_palavras" in request.tipos_material:
            print("🔄 Gerando caça-palavras...")
            caca_data = service.gerar_caca_palavras(
                request.disciplina,
                request.serie,
                request.conteudo
            )
            response["caca_palavras"] = CacaPalavrasResponse(**caca_data)
            print("✅ Caça-palavras gerado!")
        
        if "bingo" in request.tipos_material:
            print("🔄 Gerando bingo educativo...")
            bingo_data = service.gerar_bingo_educativo(
                request.disciplina,
                request.serie,
                request.conteudo
            )
            response["bingo"] = BingoEducativoResponse(**bingo_data)
            print("✅ Bingo gerado!")
        
        if "avaliacao" in request.tipos_material:
            print("🔄 Gerando avaliação multiformato...")
            aval_data = service.gerar_avaliacao_multiformato(
                request.disciplina,
                request.serie,
                request.conteudo,
                diagnosticos
            )
            response["avaliacao"] = AvaliacaoMultiformatoResponse(**aval_data)
            print("✅ Avaliação gerada!")
        
        if "mapa_mental" in request.tipos_material:
            print("🔄 Gerando mapa mental...")
            mapa_data = service.gerar_mapa_mental(
                request.disciplina,
                request.serie,
                request.conteudo
            )
            response["mapa_mental"] = MapaMentalResponse(**mapa_data)
            print("✅ Mapa mental gerado!")
        
    except Exception as e:
        print(f"❌ Erro ao gerar materiais: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar materiais: {str(e)}"
        )
    
    tempo_total = time.time() - inicio
    response["tempo_geracao"] = round(tempo_total, 2)
    
    # SALVAR NO BANCO DE DADOS
    try:
        # Converter Pydantic models para dict para salvar em JSON
        resultado_json = {}
        for key, value in response.items():
            if hasattr(value, 'model_dump'):
                resultado_json[key] = value.model_dump()
            else:
                resultado_json[key] = value
        
        material_salvo = MaterialAdaptadoGerado(
            student_id=request.student_id,
            disciplina=request.disciplina,
            serie=request.serie,
            conteudo=request.conteudo,
            tipos_material=request.tipos_material,
            resultado_json=resultado_json,
            tempo_geracao=int(tempo_total),
            created_by=current_user.id
        )
        db.add(material_salvo)
        db.commit()
        db.refresh(material_salvo)
        
        print(f"✅ Material salvo no banco! ID: {material_salvo.id}")
        response["material_id"] = material_salvo.id
    except Exception as e:
        print(f"⚠️ Erro ao salvar material no banco: {e}")
        db.rollback()
        # Continua mesmo se falhar o salvamento
    
    return MaterialAdaptadoResponse(**response)


@router.get("/tipos-disponiveis")
async def listar_tipos_materiais(
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os tipos de materiais disponíveis"""
    return {
        "tipos": [
            {
                "id": "texto_niveis",
                "nome": "Texto em 3 Níveis",
                "descricao": "Texto adaptado para diferentes níveis de complexidade",
                "icon": "📄",
                "tempo_estimado": "30-60s"
            },
            {
                "id": "infografico",
                "nome": "Infográfico",
                "descricao": "Representação visual do conteúdo",
                "icon": "📊",
                "tempo_estimado": "20-40s"
            },
            {
                "id": "flashcards",
                "nome": "Flashcards",
                "descricao": "Cards de estudo com perguntas e respostas",
                "icon": "💳",
                "tempo_estimado": "20-40s"
            },
            {
                "id": "caca_palavras",
                "nome": "Busca de Termos",
                "descricao": "Caça-palavras com termos técnicos",
                "icon": "🎯",
                "tempo_estimado": "30-50s"
            },
            {
                "id": "bingo",
                "nome": "Bingo Educativo",
                "descricao": "Jogo de bingo temático",
                "icon": "🎮",
                "tempo_estimado": "30-50s"
            },
            {
                "id": "avaliacao",
                "nome": "Avaliação Adaptada",
                "descricao": "Prova em 3 formatos (padrão, adaptado, oral)",
                "icon": "📝",
                "tempo_estimado": "40-70s"
            },
            {
                "id": "mapa_mental",
                "nome": "Mapa Mental",
                "descricao": "Diagrama conceitual hierárquico",
                "icon": "🧠",
                "tempo_estimado": "20-40s"
            }
        ]
    }


@router.get("/historico/student/{student_id}")
async def listar_historico_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    limit: int = 50,
    offset: int = 0
):
    """
    📚 Lista histórico de materiais gerados para um aluno
    """
    # Verificar se aluno existe
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Buscar materiais
    materiais = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .order_by(MaterialAdaptadoGerado.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    
    # Contar total
    total = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .count()
    
    return {
        "total": total,
        "materiais": [
            {
                "id": m.id,
                "disciplina": m.disciplina,
                "serie": m.serie,
                "conteudo": m.conteudo,
                "tipos_material": m.tipos_material,
                "tempo_geracao": m.tempo_geracao,
                "created_at": m.created_at.isoformat(),
                "created_by": m.created_by
            }
            for m in materiais
        ]
    }


@router.get("/historico/{material_id}")
async def buscar_material_por_id(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔍 Busca material específico por ID
    """
    material = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.id == material_id)\
        .first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    return {
        "id": material.id,
        "student_id": material.student_id,
        "student_name": material.student.name,
        "disciplina": material.disciplina,
        "serie": material.serie,
        "conteudo": material.conteudo,
        "tipos_material": material.tipos_material,
        "resultado": material.resultado_json,
        "tempo_geracao": material.tempo_geracao,
        "created_at": material.created_at.isoformat(),
        "created_by": material.created_by
    }


@router.delete("/historico/{material_id}")
async def deletar_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗑️ Deleta material do histórico
    """
    material = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.id == material_id)\
        .first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    db.delete(material)
    db.commit()
    
    return {"message": "Material deletado com sucesso"}


@router.get("/stats/student/{student_id}")
async def estatisticas_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📊 Estatísticas de materiais gerados para um aluno
    """
    from sqlalchemy import func
    
    # Total de materiais
    total = db.query(func.count(MaterialAdaptadoGerado.id))\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .scalar()
    
    # Por disciplina
    por_disciplina = db.query(
        MaterialAdaptadoGerado.disciplina,
        func.count(MaterialAdaptadoGerado.id).label('total')
    ).filter(MaterialAdaptadoGerado.student_id == student_id)\
     .group_by(MaterialAdaptadoGerado.disciplina)\
     .all()
    
    # Tipos mais gerados
    materiais = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .all()
    
    tipos_count = {}
    for m in materiais:
        for tipo in m.tipos_material:
            tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    return {
        "total_materiais": total,
        "por_disciplina": {d: t for d, t in por_disciplina},
        "tipos_mais_gerados": tipos_count,
        "tempo_medio_geracao": db.query(func.avg(MaterialAdaptadoGerado.tempo_geracao))\
            .filter(MaterialAdaptadoGerado.student_id == student_id)\
            .scalar() or 0
    }
