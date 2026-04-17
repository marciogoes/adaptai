"""
Rotas para Materiais de Estudo - COM STORAGE E AGENDA
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import List
from datetime import time as dt_time
import time

from app.database import get_db, SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.material import Material, MaterialAluno, TipoMaterial, StatusMaterial
from app.models.agenda import AgendaProfessor, TipoEvento, StatusEvento, Recorrencia
from app.schemas.material import (
    MaterialCreate, MaterialResponse, MaterialListResponse,
    MaterialAlunoResponse, AnotacaoRequest, FavoritoRequest
)
from app.api.dependencies import get_current_active_user
from app.core.pagination import PaginationParams, build_page
from app.services.material_service import material_service
from app.services.storage_service import storage_service

router = APIRouter(prefix="/materiais", tags=["Materiais de Estudo"])


def gerar_material_background(material_id: int):
    """
    Gera o conteúdo do material em background e salva no STORAGE
    ESTRATÉGIA: Gera conteúdo, salva em arquivo, UPDATE rápido no banco
    """
    db_session = SessionLocal()
    
    try:
        # ETAPA 1: BUSCAR DADOS (transação rápida)
        material = db_session.query(Material).filter(Material.id == material_id).first()
        if not material:
            db_session.close()
            return
        
        # Guardar dados necessários
        material_titulo = material.titulo
        material_prompt = material.conteudo_prompt
        material_tipo = material.tipo
        material_materia = material.materia
        material_serie = material.serie_nivel or "Geral"
        
        # Buscar adaptações
        alunos_ids = [ma.aluno_id for ma in material.materiais_alunos]
        alunos = db_session.query(Student).filter(Student.id.in_(alunos_ids)).all()
        adaptacoes = list(set([a.diagnosis for a in alunos if a.diagnosis]))
        
        # FECHAR SESSÃO - vamos gerar conteúdo SEM banco aberto
        db_session.close()
        
        print(f"📝 Gerando conteúdo para material {material_id}...")
        
        # ETAPA 2: GERAR CONTEÚDO (SEM BANCO)
        arquivo_path = None
        conteudo_erro = None
        
        if material_tipo == TipoMaterial.VISUAL:
            resultado = material_service.gerar_material_visual(
                titulo=material_titulo,
                conteudo=material_prompt,
                materia=material_materia,
                serie=material_serie,
                adaptacoes=adaptacoes
            )
            
            if resultado["success"]:
                # Salvar HTML em arquivo
                arquivo_path = storage_service.salvar_html(material_id, resultado["html"])
                print(f"💾 HTML salvo em: storage/{arquivo_path}")
            else:
                conteudo_erro = resultado.get("error")
        
        elif material_tipo == TipoMaterial.MAPA_MENTAL:
            resultado = material_service.gerar_mapa_mental(
                titulo=material_titulo,
                conteudo=material_prompt,
                materia=material_materia,
                serie=material_serie,
                adaptacoes=adaptacoes
            )
            
            if resultado["success"]:
                # Salvar JSON em arquivo
                arquivo_path = storage_service.salvar_json(material_id, resultado["json"])
                print(f"💾 JSON salvo em: storage/{arquivo_path}")
            else:
                conteudo_erro = resultado.get("error")
        
        print(f"✨ Conteúdo gerado! Atualizando banco...")
        
        # ETAPA 3: ATUALIZAR BANCO (transação SUPER RÁPIDA - só UPDATE status)
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Criar nova sessão apenas para UPDATE
                db_session = SessionLocal()
                
                # Buscar material novamente
                material = db_session.query(Material).filter(Material.id == material_id).first()
                
                if not material:
                    db_session.close()
                    return
                
                # UPDATE RÁPIDO - só campos pequenos!
                if arquivo_path:
                    material.arquivo_path = arquivo_path
                    material.status = StatusMaterial.DISPONIVEL
                else:
                    material.status = StatusMaterial.ERRO
                    material.metadados = {"erro": conteudo_erro or "Erro desconhecido"}
                
                # COMMIT IMEDIATO
                db_session.commit()
                db_session.close()
                
                print(f"✅ Material {material_id} salvo com sucesso!")
                return
            
            except OperationalError as e:
                retry_count += 1
                db_session.rollback()
                db_session.close()
                
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    print(f"⚠️ Erro MySQL. Retry {retry_count}/{max_retries} em {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Material {material_id} falhou após {max_retries} tentativas: {str(e)}")
                    
                    # Deletar arquivo se criou
                    if arquivo_path:
                        storage_service.deletar(material_id)
                    
                    # Marcar como erro
                    try:
                        db_session = SessionLocal()
                        material = db_session.query(Material).filter(Material.id == material_id).first()
                        if material:
                            material.status = StatusMaterial.ERRO
                            material.metadados = {"erro": f"Timeout MySQL após {max_retries} tentativas"}
                            db_session.commit()
                        db_session.close()
                    except:
                        pass
                    return
    
    except Exception as e:
        print(f"❌ Erro ao gerar material {material_id}: {str(e)}")
        try:
            db_session = SessionLocal()
            material = db_session.query(Material).filter(Material.id == material_id).first()
            if material:
                material.status = StatusMaterial.ERRO
                material.metadados = {"erro": str(e)}
                db_session.commit()
            db_session.close()
        except:
            pass


@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
async def criar_material(
    material_data: MaterialCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo material de estudo e inicia geração em background.
    
    Se data_aplicacao for fornecida e criar_evento_agenda=True,
    um evento será criado automaticamente na agenda do professor.
    """
    
    # Verificar se alunos pertencem ao usuário
    alunos = db.query(Student).filter(
        Student.id.in_(material_data.aluno_ids),
        Student.created_by_user_id == current_user.id
    ).all()
    
    if len(alunos) != len(material_data.aluno_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Um ou mais alunos não encontrados ou não pertencem a você"
        )
    
    # Criar material
    novo_material = Material(
        titulo=material_data.titulo,
        descricao=material_data.descricao,
        conteudo_prompt=material_data.conteudo_prompt,
        tipo=material_data.tipo,
        materia=material_data.materia,
        serie_nivel=material_data.serie_nivel,
        tags=material_data.tags or [],
        status=StatusMaterial.GERANDO,
        criado_por_id=current_user.id
    )
    
    db.add(novo_material)
    db.commit()
    db.refresh(novo_material)
    
    # Associar aos alunos
    for aluno in alunos:
        material_aluno = MaterialAluno(
            material_id=novo_material.id,
            aluno_id=aluno.id
        )
        db.add(material_aluno)
    
    db.commit()
    db.refresh(novo_material)
    
    # ============================================
    # NOVO: Criar evento na agenda se solicitado
    # ============================================
    if material_data.criar_evento_agenda and material_data.data_aplicacao:
        try:
            # Para cada aluno, criar evento na agenda
            hora_inicio = material_data.hora_aplicacao or dt_time(8, 0)  # Default 08:00
            
            for aluno in alunos:
                evento = AgendaProfessor(
                    professor_id=current_user.id,
                    titulo=f"📚 {material_data.titulo}",
                    descricao=f"Aplicação de material: {material_data.titulo}\nMatéria: {material_data.materia}",
                    tipo=TipoEvento.AULA,
                    student_id=aluno.id,
                    data=material_data.data_aplicacao,
                    hora_inicio=hora_inicio,
                    duracao_minutos=50,
                    cor="#10B981",  # Verde para materiais
                    recorrencia=Recorrencia.UNICO,
                    status=StatusEvento.AGENDADO,
                    notas_privadas=f"Material ID: {novo_material.id}"
                )
                db.add(evento)
            
            db.commit()
            print(f"📅 Evento(s) criado(s) na agenda para {len(alunos)} aluno(s)")
        except Exception as e:
            print(f"⚠️ Erro ao criar evento na agenda: {e}")
            # Não falha a criação do material se erro na agenda
    
    # Agendar geração em background
    background_tasks.add_task(gerar_material_background, novo_material.id)
    
    return novo_material


@router.get("/")
async def listar_materiais(
    tipo: str = None,
    materia: str = None,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Lista materiais criados pelo professor com paginacao.
    
    Query params:
    - page: pagina (default 1)
    - size: itens por pagina (default 20, max 100)
    - tipo: 'visual' ou 'mapa_mental' (opcional)
    - materia: nome da materia (opcional)
    
    Retorna:
    {
        "items": [...materiais...],
        "meta": {"page": 1, "size": 20, "total": 150, "total_pages": 8, ...}
    }
    
    IMPORTANTE: Endpoint mudou para formato paginado. Frontend antigo que espera
    array puro precisa acessar response.items ao inves de response direto.
    """
    query = db.query(Material).filter(Material.criado_por_id == current_user.id)
    
    if tipo:
        query = query.filter(Material.tipo == tipo.upper())
    
    if materia:
        query = query.filter(Material.materia == materia)
    
    query = query.order_by(Material.criado_em.desc())
    
    total = query.count()
    materiais = query.offset(pagination.offset).limit(pagination.limit).all()
    
    # Serializar com total de alunos (eager-load relationship evita N+1)
    items = []
    for material in materiais:
        items.append({
            "id": material.id,
            "titulo": material.titulo,
            "descricao": material.descricao,
            "tipo": material.tipo,
            "materia": material.materia,
            "serie_nivel": material.serie_nivel,
            "status": material.status,
            "criado_em": material.criado_em,
            "total_alunos": len(material.materiais_alunos),
        })
    
    return build_page(items=items, total=total, pagination=pagination)


@router.get("/{material_id}", response_model=MaterialResponse)
async def obter_material(
    material_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de um material específico"""
    material = db.query(Material).filter(
        Material.id == material_id,
        Material.criado_por_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    return material


@router.get("/{material_id}/conteudo")
async def obter_conteudo_material(
    material_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obter o conteúdo do material do storage
    Retorna HTML ou JSON dependendo do tipo
    """
    material = db.query(Material).filter(
        Material.id == material_id,
        Material.criado_por_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    if material.status != StatusMaterial.DISPONIVEL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Material não está disponível. Status: {material.status}"
        )
    
    # Ler do storage
    if material.tipo == TipoMaterial.VISUAL:
        conteudo = storage_service.ler_html(material_id)
        if not conteudo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteúdo do material não encontrado no storage"
            )
        return {"tipo": "html", "conteudo": conteudo}
    
    elif material.tipo == TipoMaterial.MAPA_MENTAL:
        conteudo = storage_service.ler_json(material_id)
        if not conteudo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteúdo do material não encontrado no storage"
            )
        return {"tipo": "json", "conteudo": conteudo}


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_material(
    material_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deletar um material e seu arquivo"""
    material = db.query(Material).filter(
        Material.id == material_id,
        Material.criado_por_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    # Deletar arquivo do storage
    storage_service.deletar(material_id)
    
    # Deletar do banco
    db.delete(material)
    db.commit()
    
    return None


@router.get("/{material_id}/alunos", response_model=List[MaterialAlunoResponse])
async def listar_alunos_material(
    material_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Listar todos os alunos que têm acesso a este material"""
    material = db.query(Material).filter(
        Material.id == material_id,
        Material.criado_por_id == current_user.id
    ).first()
    
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    return material.materiais_alunos
