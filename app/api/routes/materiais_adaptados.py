"""
Rotas para Geração de Materiais Adaptados
ATUALIZADO: Novos tipos (história social, sequenciamento, linha do tempo, jogo da memória)
ATUALIZADO: Série obtida automaticamente do aluno
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import time

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.material_adaptado_gerado import MaterialAdaptadoGerado
from app.services.ai_materiais_service import MaterialAdaptadoService


router = APIRouter(prefix="/materiais-adaptados", tags=["Materiais Adaptados"])


# Schema simplificado (sem serie obrigatória)
class MaterialRequest(BaseModel):
    student_id: int
    disciplina: str
    serie: Optional[str] = None  # Opcional - pega do aluno se não informada
    conteudo: str
    tipos_material: List[str]


@router.post("/gerar")
async def gerar_materiais_adaptados(
    request: MaterialRequest,
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
    - bingo: Bingo educativo
    - avaliacao: Avaliação em 3 formatos
    - mapa_mental: Mapa mental/conceitual
    - historia_social: História social (TEA/TDAH) [NOVO]
    - sequenciamento: Sequenciamento visual [NOVO]
    - linha_tempo: Linha do tempo [NOVO]
    - jogo_memoria: Jogo da memória [NOVO]
    
    A série é obtida automaticamente do cadastro do aluno se não informada.
    """
    
    inicio = time.time()
    
    # Buscar aluno
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # SÉRIE: Usar do aluno se não informada
    serie = request.serie or student.grade_level or "Não especificada"
    
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
        "student_serie": serie,  # Informar série usada
        "disciplina": request.disciplina,
        "conteudo": request.conteudo
    }
    
    # Gerar cada tipo de material solicitado
    try:
        # === MATERIAIS ORIGINAIS ===
        if "texto_niveis" in request.tipos_material:
            print("🔄 Gerando texto em 3 níveis...")
            response["texto_niveis"] = service.gerar_texto_3_niveis(
                request.disciplina, serie, request.conteudo, diagnosticos
            )
            print("✅ Texto gerado!")
        
        if "infografico" in request.tipos_material:
            print("🔄 Gerando infográfico...")
            response["infografico"] = service.gerar_infografico(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Infográfico gerado!")
        
        if "flashcards" in request.tipos_material:
            print("🔄 Gerando flashcards...")
            response["flashcards"] = service.gerar_flashcards(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Flashcards gerados!")
        
        if "caca_palavras" in request.tipos_material:
            print("🔄 Gerando caça-palavras...")
            response["caca_palavras"] = service.gerar_caca_palavras(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Caça-palavras gerado!")
        
        if "bingo" in request.tipos_material:
            print("🔄 Gerando bingo educativo...")
            response["bingo"] = service.gerar_bingo_educativo(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Bingo gerado!")
        
        if "avaliacao" in request.tipos_material:
            print("🔄 Gerando avaliação multiformato...")
            response["avaliacao"] = service.gerar_avaliacao_multiformato(
                request.disciplina, serie, request.conteudo, diagnosticos
            )
            print("✅ Avaliação gerada!")
        
        if "mapa_mental" in request.tipos_material:
            print("🔄 Gerando mapa mental...")
            response["mapa_mental"] = service.gerar_mapa_mental(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Mapa mental gerado!")
        
        # === NOVOS MATERIAIS ===
        if "historia_social" in request.tipos_material:
            print("🔄 Gerando história social...")
            response["historia_social"] = service.gerar_historia_social(
                request.disciplina, serie, request.conteudo, diagnosticos
            )
            print("✅ História social gerada!")
        
        if "sequenciamento" in request.tipos_material:
            print("🔄 Gerando sequenciamento visual...")
            response["sequenciamento"] = service.gerar_sequenciamento(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Sequenciamento gerado!")
        
        if "linha_tempo" in request.tipos_material:
            print("🔄 Gerando linha do tempo...")
            response["linha_tempo"] = service.gerar_linha_tempo(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Linha do tempo gerada!")
        
        if "jogo_memoria" in request.tipos_material:
            print("🔄 Gerando jogo da memória...")
            response["jogo_memoria"] = service.gerar_jogo_memoria(
                request.disciplina, serie, request.conteudo
            )
            print("✅ Jogo da memória gerado!")
        
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
        material_salvo = MaterialAdaptadoGerado(
            student_id=request.student_id,
            disciplina=request.disciplina,
            serie=serie,
            conteudo=request.conteudo,
            tipos_material=request.tipos_material,
            resultado_json=response,
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
    
    return response


@router.get("/tipos-disponiveis")
async def listar_tipos_materiais(
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os tipos de materiais disponíveis"""
    return {
        "tipos": [
            # Originais
            {
                "id": "texto_niveis",
                "nome": "Texto em 3 Níveis",
                "descricao": "Texto adaptado para diferentes níveis",
                "icon": "📄",
                "categoria": "Leitura",
                "tempo_estimado": "30-60s"
            },
            {
                "id": "infografico",
                "nome": "Infográfico",
                "descricao": "Representação visual do conteúdo",
                "icon": "📊",
                "categoria": "Visual",
                "tempo_estimado": "20-40s"
            },
            {
                "id": "flashcards",
                "nome": "Flashcards",
                "descricao": "Cards de estudo",
                "icon": "💳",
                "categoria": "Memorização",
                "tempo_estimado": "20-40s"
            },
            {
                "id": "mapa_mental",
                "nome": "Mapa Mental",
                "descricao": "Diagrama conceitual",
                "icon": "🧠",
                "categoria": "Visual",
                "tempo_estimado": "20-40s"
            },
            {
                "id": "caca_palavras",
                "nome": "Busca de Termos",
                "descricao": "Caça-palavras técnico",
                "icon": "🎯",
                "categoria": "Jogos",
                "tempo_estimado": "30-50s"
            },
            {
                "id": "bingo",
                "nome": "Bingo Educativo",
                "descricao": "Jogo de bingo temático",
                "icon": "🎮",
                "categoria": "Jogos",
                "tempo_estimado": "30-50s"
            },
            {
                "id": "jogo_memoria",
                "nome": "Jogo da Memória",
                "descricao": "Pares de cartas com conceitos",
                "icon": "🃏",
                "categoria": "Jogos",
                "tempo_estimado": "20-40s",
                "novo": True
            },
            {
                "id": "avaliacao",
                "nome": "Avaliação Adaptada",
                "descricao": "Prova em 3 formatos",
                "icon": "📝",
                "categoria": "Avaliação",
                "tempo_estimado": "40-70s"
            },
            # Novos
            {
                "id": "historia_social",
                "nome": "História Social",
                "descricao": "Narrativa para comportamentos (TEA/TDAH)",
                "icon": "📖",
                "categoria": "TEA/TDAH",
                "tempo_estimado": "20-40s",
                "novo": True
            },
            {
                "id": "sequenciamento",
                "nome": "Sequenciamento Visual",
                "descricao": "Passo a passo de tarefas",
                "icon": "📋",
                "categoria": "TEA/TDAH",
                "tempo_estimado": "20-40s",
                "novo": True
            },
            {
                "id": "linha_tempo",
                "nome": "Linha do Tempo",
                "descricao": "Eventos em ordem cronológica",
                "icon": "📅",
                "categoria": "Visual",
                "tempo_estimado": "20-40s",
                "novo": True
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
    """📚 Lista histórico de materiais gerados para um aluno"""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    materiais = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .order_by(MaterialAdaptadoGerado.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    
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
                "created_at": m.created_at.isoformat() if m.created_at else None,
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
    """🔍 Busca material específico por ID"""
    
    material = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.id == material_id)\
        .first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    return {
        "id": material.id,
        "student_id": material.student_id,
        "student_name": material.student.name if material.student else "Aluno",
        "disciplina": material.disciplina,
        "serie": material.serie,
        "conteudo": material.conteudo,
        "tipos_material": material.tipos_material,
        "resultado": material.resultado_json,
        "tempo_geracao": material.tempo_geracao,
        "created_at": material.created_at.isoformat() if material.created_at else None,
        "created_by": material.created_by
    }


@router.delete("/historico/{material_id}")
async def deletar_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """🗑️ Deleta material do histórico"""
    
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
    """📊 Estatísticas de materiais gerados para um aluno"""
    from sqlalchemy import func
    
    total = db.query(func.count(MaterialAdaptadoGerado.id))\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .scalar()
    
    por_disciplina = db.query(
        MaterialAdaptadoGerado.disciplina,
        func.count(MaterialAdaptadoGerado.id).label('total')
    ).filter(MaterialAdaptadoGerado.student_id == student_id)\
     .group_by(MaterialAdaptadoGerado.disciplina)\
     .all()
    
    materiais = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .all()
    
    tipos_count = {}
    for m in materiais:
        for tipo in (m.tipos_material or []):
            tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    return {
        "total_materiais": total,
        "por_disciplina": {d: t for d, t in por_disciplina},
        "tipos_mais_gerados": tipos_count,
        "tempo_medio_geracao": db.query(func.avg(MaterialAdaptadoGerado.tempo_geracao))\
            .filter(MaterialAdaptadoGerado.student_id == student_id)\
            .scalar() or 0
    }
