"""
Rotas para Geração de Materiais Adaptados
VERSÃO MEGA COMPLETA: 25+ tipos de materiais
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import time

from app.database import get_db
from app.api.dependencies import get_current_active_user, verificar_acesso_aluno
from app.core.rate_limit import check_rate_limit
from app.core.pagination import PaginationParams, build_page
from app.models.user import User
from app.models.student import Student
from app.models.material_adaptado_gerado import MaterialAdaptadoGerado
from app.services.ai_materiais_service import MaterialAdaptadoService


router = APIRouter(prefix="/materiais-adaptados", tags=["Materiais Adaptados"])


class MaterialRequest(BaseModel):
    student_id: int
    disciplina: str
    serie: Optional[str] = None
    conteudo: str
    tipos_material: List[str]


# Mapeamento de tipos para métodos do service
TIPOS_MATERIAIS = {
    # Leitura
    "texto_niveis": {"metodo": "gerar_texto_3_niveis", "nome": "Texto em 3 Níveis", "categoria": "📚 Leitura", "usa_diagnostico": True},
    "resumo_estruturado": {"metodo": "gerar_resumo_estruturado", "nome": "Resumo Estruturado", "categoria": "📚 Leitura"},
    "ficha_leitura": {"metodo": "gerar_ficha_leitura", "nome": "Ficha de Leitura", "categoria": "📚 Leitura"},
    
    # Visual
    "infografico": {"metodo": "gerar_infografico", "nome": "Infográfico", "categoria": "🎨 Visual"},
    "mapa_mental": {"metodo": "gerar_mapa_mental", "nome": "Mapa Mental", "categoria": "🎨 Visual"},
    "linha_tempo": {"metodo": "gerar_linha_tempo", "nome": "Linha do Tempo", "categoria": "🎨 Visual"},
    "hq_tirinha": {"metodo": "gerar_hq_tirinha", "nome": "HQ/Tirinha", "categoria": "🎨 Visual"},
    "diagrama_venn": {"metodo": "gerar_diagrama_venn", "nome": "Diagrama de Venn", "categoria": "🎨 Visual"},
    "tabela_comparativa": {"metodo": "gerar_tabela_comparativa", "nome": "Tabela Comparativa", "categoria": "🎨 Visual"},
    "arvore_decisao": {"metodo": "gerar_arvore_decisao", "nome": "Árvore de Decisão", "categoria": "🎨 Visual"},
    
    # Memorização
    "flashcards": {"metodo": "gerar_flashcards", "nome": "Flashcards", "categoria": "🧠 Memorização"},
    "jogo_memoria": {"metodo": "gerar_jogo_memoria", "nome": "Jogo da Memória", "categoria": "🧠 Memorização"},
    "album_figurinhas": {"metodo": "gerar_album_figurinhas", "nome": "Álbum de Figurinhas", "categoria": "🧠 Memorização"},
    
    # Jogos
    "caca_palavras": {"metodo": "gerar_caca_palavras", "nome": "Caça-Palavras", "categoria": "🎮 Jogos"},
    "cruzadinha": {"metodo": "gerar_cruzadinha", "nome": "Cruzadinha", "categoria": "🎮 Jogos"},
    "bingo": {"metodo": "gerar_bingo_educativo", "nome": "Bingo Educativo", "categoria": "🎮 Jogos"},
    "domino": {"metodo": "gerar_domino", "nome": "Dominó Educativo", "categoria": "🎮 Jogos"},
    "quiz_interativo": {"metodo": "gerar_quiz_interativo", "nome": "Quiz Interativo", "categoria": "🎮 Jogos"},
    "trilha_aprendizagem": {"metodo": "gerar_trilha_aprendizagem", "nome": "Trilha/Tabuleiro", "categoria": "🎮 Jogos"},
    "roleta_perguntas": {"metodo": "gerar_roleta_perguntas", "nome": "Roleta de Perguntas", "categoria": "🎮 Jogos"},
    
    # TEA/TDAH
    "historia_social": {"metodo": "gerar_historia_social", "nome": "História Social", "categoria": "💙 TEA/TDAH", "usa_diagnostico": True},
    "sequenciamento": {"metodo": "gerar_sequenciamento", "nome": "Sequenciamento Visual", "categoria": "💙 TEA/TDAH"},
    "quadro_rotina": {"metodo": "gerar_quadro_rotina", "nome": "Quadro de Rotina", "categoria": "💙 TEA/TDAH"},
    "cartoes_comunicacao": {"metodo": "gerar_cartoes_comunicacao", "nome": "Cartões de Comunicação", "categoria": "💙 TEA/TDAH"},
    "termometro_emocoes": {"metodo": "gerar_termometro_emocoes", "nome": "Termômetro de Emoções", "categoria": "💙 TEA/TDAH"},
    "contrato_comportamento": {"metodo": "gerar_contrato_comportamento", "nome": "Contrato de Comportamento", "categoria": "💙 TEA/TDAH"},
    "checklist_tarefas": {"metodo": "gerar_checklist_tarefas", "nome": "Checklist de Tarefas", "categoria": "💙 TEA/TDAH"},
    "painel_primeiro_depois": {"metodo": "gerar_painel_primeiro_depois", "nome": "Primeiro-Depois", "categoria": "💙 TEA/TDAH"},
    
    # Completar
    "complete_lacunas": {"metodo": "gerar_complete_lacunas", "nome": "Complete as Lacunas", "categoria": "✍️ Completar"},
    "ligue_colunas": {"metodo": "gerar_ligue_colunas", "nome": "Ligue as Colunas", "categoria": "✍️ Completar"},
    "verdadeiro_falso": {"metodo": "gerar_verdadeiro_falso", "nome": "Verdadeiro ou Falso", "categoria": "✍️ Completar"},
    "ordenar_sequencia": {"metodo": "gerar_ordenar_sequencia", "nome": "Ordenar Sequência", "categoria": "✍️ Completar"},
    
    # Avaliação
    "avaliacao": {"metodo": "gerar_avaliacao_multiformato", "nome": "Avaliação 3 Formatos", "categoria": "📝 Avaliação", "usa_diagnostico": True},
    
    # Práticos
    "experimento": {"metodo": "gerar_experimento", "nome": "Experimento", "categoria": "🔬 Práticos"},
    "receita_procedimento": {"metodo": "gerar_receita_procedimento", "nome": "Receita/Procedimento", "categoria": "🔬 Práticos"},
    "estudo_caso": {"metodo": "gerar_estudo_caso", "nome": "Estudo de Caso", "categoria": "🔬 Práticos"},
    "diario_bordo": {"metodo": "gerar_diario_bordo", "nome": "Diário de Bordo", "categoria": "🔬 Práticos"},
}


@router.post("/gerar")
async def gerar_materiais_adaptados(
    request_body: MaterialRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🎨 GERA MATERIAIS EDUCACIONAIS ADAPTADOS
    
    25+ tipos disponiveis! A serie e obtida automaticamente do aluno.
    
    SEGURANCA: rate limited a 20 geracoes por hora por IP 
    (cada geracao pode fazer ate 25 chamadas caras a API Claude).
    """
    # SEGURANCA: limitar gastos com IA por IP
    check_rate_limit(
        request, key="gerar_material_adaptado", max_requests=20, window_seconds=3600,
        error_message="Limite de geracoes de IA atingido. Aguarde 1 hora."
    )
    
    inicio = time.time()
    
    # SEGURANCA: verificar acesso ao aluno (evita IDOR entre escolas)
    student = verificar_acesso_aluno(db, request_body.student_id, current_user)
    
    # Serie: usar do aluno se nao informada
    serie = request_body.serie or student.grade_level or "Nao especificada"
    
    # Extrair diagnosticos do aluno
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
        "student_serie": serie,
        "disciplina": request_body.disciplina,
        "conteudo": request_body.conteudo,
        "materiais_gerados": []
    }
    
    # Gerar cada tipo de material solicitado
    erros = []
    for tipo in request_body.tipos_material:
        if tipo not in TIPOS_MATERIAIS:
            erros.append(f"Tipo '{tipo}' nao encontrado")
            continue
        
        config = TIPOS_MATERIAIS[tipo]
        metodo_nome = config["metodo"]
        
        try:
            print(f"[IA] Gerando {config['nome']}...")
            metodo = getattr(service, metodo_nome)
            
            # Chamar metodo com ou sem diagnosticos
            if config.get("usa_diagnostico"):
                resultado = metodo(request_body.disciplina, serie, request_body.conteudo, diagnosticos)
            else:
                resultado = metodo(request_body.disciplina, serie, request_body.conteudo)
            
            response[tipo] = resultado
            response["materiais_gerados"].append(tipo)
            print(f"[OK] {config['nome']} gerado!")
            
        except Exception as e:
            print(f"[ERRO] Gerar {config['nome']}: {type(e).__name__}")
            # SEGURANCA: nao vazar detalhes de erro interno ao cliente
            erros.append(f"{config['nome']}: erro na geracao")
    
    if erros:
        response["erros"] = erros
    
    tempo_total = time.time() - inicio
    response["tempo_geracao"] = round(tempo_total, 2)
    
    # Salvar no banco
    try:
        material_salvo = MaterialAdaptadoGerado(
            student_id=request_body.student_id,
            disciplina=request_body.disciplina,
            serie=serie,
            conteudo=request_body.conteudo,
            tipos_material=request_body.tipos_material,
            resultado_json=response,
            tempo_geracao=int(tempo_total),
            created_by=current_user.id
        )
        db.add(material_salvo)
        db.commit()
        db.refresh(material_salvo)
        response["material_id"] = material_salvo.id
        print(f"[OK] Material salvo! ID: {material_salvo.id}")
    except Exception as e:
        print(f"[ERRO] Salvar material: {type(e).__name__}")
        db.rollback()
    
    return response


@router.get("/tipos-disponiveis")
async def listar_tipos_materiais(
    current_user: User = Depends(get_current_active_user)
):
    """Lista todos os 25+ tipos de materiais disponíveis por categoria"""
    
    # Agrupar por categoria
    por_categoria = {}
    for tipo_id, config in TIPOS_MATERIAIS.items():
        categoria = config["categoria"]
        if categoria not in por_categoria:
            por_categoria[categoria] = []
        
        por_categoria[categoria].append({
            "id": tipo_id,
            "nome": config["nome"],
            "usa_diagnostico": config.get("usa_diagnostico", False)
        })
    
    return {
        "total_tipos": len(TIPOS_MATERIAIS),
        "por_categoria": por_categoria,
        "lista_completa": [
            {"id": k, "nome": v["nome"], "categoria": v["categoria"]}
            for k, v in TIPOS_MATERIAIS.items()
        ]
    }


@router.get("/historico/student/{student_id}")
async def listar_historico_student(
    student_id: int,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Lista historico de materiais gerados para um aluno (paginado).
    
    Query params:
    - page: pagina (default 1)
    - size: itens por pagina (default 20, max 100)
    
    Resposta no formato {items, meta} + chaves legadas 'total'/'materiais'
    para compatibilidade com frontend existente.
    """
    
    # SEGURANCA: verificar acesso ao aluno (evita IDOR entre escolas)
    student = verificar_acesso_aluno(db, student_id, current_user)
    
    query = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.student_id == student_id)\
        .order_by(MaterialAdaptadoGerado.created_at.desc())
    
    total = query.count()
    materiais = query.offset(pagination.offset).limit(pagination.limit).all()
    
    items = [
        {
            "id": m.id,
            "disciplina": m.disciplina,
            "serie": m.serie,
            "conteudo": m.conteudo,
            "tipos_material": m.tipos_material,
            "tempo_geracao": m.tempo_geracao,
            "created_at": m.created_at.isoformat() if m.created_at else None
        }
        for m in materiais
    ]
    
    page = build_page(items=items, total=total, pagination=pagination)
    # Compat retroativa: manter 'total' e 'materiais' no nivel raiz
    page["total"] = total
    page["materiais"] = items
    return page


@router.get("/historico/{material_id}")
async def buscar_material_por_id(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """🔍 Busca material específico por ID"""
    
    material = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    # SEGURANCA: verificar acesso ao aluno dono do material (evita IDOR)
    verificar_acesso_aluno(db, material.student_id, current_user)
    
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
        "created_at": material.created_at.isoformat() if material.created_at else None
    }


@router.delete("/historico/{material_id}")
async def deletar_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """🗑️ Deleta material do histórico"""
    
    material = db.query(MaterialAdaptadoGerado)\
        .filter(MaterialAdaptadoGerado.id == material_id).first()
    
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    # SEGURANCA: verificar acesso ao aluno dono do material (evita IDOR)
    verificar_acesso_aluno(db, material.student_id, current_user)
    
    db.delete(material)
    db.commit()
    
    return {"message": "Material deletado com sucesso"}
