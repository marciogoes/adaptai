# ============================================
# ROTAS - Registro Diário de Aulas
# ============================================
"""
Endpoints para importar e gerenciar registros diários
de aulas a partir de PDFs escolares.

INTEGRAÇÃO:
- Cria eventos na Agenda do Professor automaticamente
- Fornece sugestões para Materiais e Provas
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date, datetime, time, timedelta
from pathlib import Path
import shutil
import uuid

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.student import Student
from app.models.registro_diario import RegistroDiario, AulaRegistrada
from app.models.agenda import AgendaProfessor, TipoEvento, StatusEvento
from app.services.relatorio_extrator_service import relatorio_extrator_service


router = APIRouter(prefix="/registro-diario", tags=["📋 Registro Diário de Aulas"])

# Diretório para salvar os PDFs
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "storage" / "registros_diarios"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def criar_eventos_agenda(
    db: Session,
    professor_id: int,
    student_id: int,
    data_aula: date,
    aulas: List[AulaRegistrada],
    serie_turma: str = None
):
    """
    Cria eventos na agenda do professor baseado nas aulas registradas.
    Cada disciplina vira um evento.
    """
    eventos_criados = []
    
    # Horários base para as aulas (simulados)
    horarios = [
        (time(7, 30), time(8, 20)),
        (time(8, 20), time(9, 10)),
        (time(9, 30), time(10, 20)),
        (time(10, 20), time(11, 10)),
        (time(11, 10), time(12, 0)),
    ]
    
    for i, aula in enumerate(aulas):
        # Usar horário base ou gerar sequencialmente
        hora_inicio = horarios[i % len(horarios)][0] if i < len(horarios) else time(8 + i, 0)
        hora_fim = horarios[i % len(horarios)][1] if i < len(horarios) else time(8 + i, 50)
        
        # Descrição do evento
        descricao = f"📚 {aula.conteudo}"
        if aula.atividade_sala:
            descricao += f"\n\n📝 Atividade: {aula.atividade_sala}"
        if aula.paginas:
            descricao += f"\n📄 Páginas: {aula.paginas}"
        if aula.modulo:
            descricao += f"\n📖 Módulo: {aula.modulo}"
        if aula.tem_dever_casa:
            descricao += f"\n\n🏠 TEM DEVER DE CASA"
        if aula.tem_atividade_avaliativa:
            descricao += f"\n\n⚠️ TEM ATIVIDADE AVALIATIVA"
        
        # Título do evento
        titulo = f"{aula.disciplina}"
        if serie_turma:
            titulo += f" - {serie_turma}"
        
        # Criar evento na agenda
        evento = AgendaProfessor(
            professor_id=professor_id,
            student_id=student_id,
            titulo=titulo,
            descricao=descricao,
            tipo=TipoEvento.AULA,
            data=data_aula,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            status=StatusEvento.CONCLUIDO,  # Já aconteceu
            cor="#3B82F6" if not aula.tem_atividade_avaliativa else "#EF4444",  # Azul ou Vermelho
            notas_privadas=f"Importado do registro diário - Prof. {aula.professor_nome}" if aula.professor_nome else "Importado do registro diário"
        )
        
        db.add(evento)
        eventos_criados.append(evento)
    
    db.commit()
    return eventos_criados


@router.post("/importar")
async def importar_relatorio(
    arquivo: UploadFile = File(..., description="PDF do relatório diário"),
    student_id: Optional[int] = Query(None, description="ID do aluno (opcional)"),
    usar_visao: bool = Query(False, description="Usar análise de imagem (para PDFs escaneados)"),
    criar_agenda: bool = Query(True, description="Criar eventos na agenda automaticamente"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📤 Importar relatório diário de aulas (PDF)
    
    Faz upload de um PDF de relatório diário escolar e extrai
    automaticamente todas as informações usando IA.
    
    **INTEGRAÇÃO AUTOMÁTICA:**
    - ✅ Cria eventos na Agenda do Professor (se `criar_agenda=true`)
    - ✅ Dados disponíveis para sugestões de Materiais e Provas
    
    **Parâmetros:**
    - `arquivo`: PDF do relatório diário
    - `student_id`: ID do aluno (opcional, para associar)
    - `usar_visao`: Se True, usa análise de imagem (melhor para PDFs escaneados)
    - `criar_agenda`: Se True, cria eventos na agenda automaticamente
    """
    
    # Verificar tipo de arquivo
    if not arquivo.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas arquivos PDF são aceitos"
        )
    
    # Verificar aluno se fornecido
    student = None
    if student_id:
        student = db.query(Student).filter(
            Student.id == student_id,
            Student.created_by_user_id == current_user.id
        ).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado ou não pertence a você"
            )
    
    # Salvar arquivo
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}.pdf"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar arquivo: {str(e)}"
        )
    
    # Extrair dados usando IA
    if usar_visao:
        resultado = await relatorio_extrator_service.extrair_com_imagem(str(file_path))
    else:
        resultado = await relatorio_extrator_service.extrair_dados_relatorio(str(file_path))
    
    if not resultado.get("success"):
        # Deletar arquivo se falhou
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro ao extrair dados do PDF: {resultado.get('error', 'Erro desconhecido')}"
        )
    
    dados = resultado["dados"]
    
    # Converter data
    try:
        data_aula = datetime.strptime(dados.get("data", ""), "%Y-%m-%d").date()
    except:
        data_aula = date.today()
    
    # Criar registro no banco
    registro = RegistroDiario(
        professor_id=current_user.id,
        student_id=student_id,
        data_aula=data_aula,
        serie_turma=dados.get("serie_turma"),
        escola_origem=dados.get("escola"),
        arquivo_pdf=str(file_path),
        conteudo_extraido=dados
    )
    
    db.add(registro)
    db.commit()
    db.refresh(registro)
    
    # Criar registros de aulas individuais
    aulas_criadas = []
    for aula_data in dados.get("aulas", []):
        aula = AulaRegistrada(
            registro_id=registro.id,
            professor_nome=aula_data.get("professor"),
            disciplina=aula_data.get("disciplina", "Não identificado"),
            conteudo=aula_data.get("conteudo", "Não identificado"),
            atividade_sala=aula_data.get("atividade_sala"),
            livro=aula_data.get("livro"),
            capitulo=aula_data.get("capitulo"),
            paginas=aula_data.get("paginas"),
            modulo=aula_data.get("modulo"),
            tem_dever_casa=aula_data.get("tem_dever_casa", False),
            tem_atividade_avaliativa=aula_data.get("tem_atividade_avaliativa", False),
            dever_casa_descricao=aula_data.get("dever_casa_descricao")
        )
        db.add(aula)
        aulas_criadas.append(aula)
    
    db.commit()
    
    # Criar eventos na agenda (se aluno foi especificado e criar_agenda=True)
    eventos_agenda = []
    if student_id and criar_agenda:
        eventos_agenda = criar_eventos_agenda(
            db=db,
            professor_id=current_user.id,
            student_id=student_id,
            data_aula=data_aula,
            aulas=aulas_criadas,
            serie_turma=dados.get("serie_turma")
        )
    
    return {
        "success": True,
        "message": f"Relatório importado com sucesso! {len(aulas_criadas)} aulas identificadas.",
        "registro_id": registro.id,
        "data_aula": data_aula.isoformat(),
        "serie_turma": dados.get("serie_turma"),
        "escola": dados.get("escola"),
        "total_aulas": len(aulas_criadas),
        "eventos_agenda_criados": len(eventos_agenda),
        "aulas": [
            {
                "disciplina": a.disciplina,
                "conteudo": a.conteudo,
                "professor": a.professor_nome,
                "tem_dever": a.tem_dever_casa,
                "tem_avaliacao": a.tem_atividade_avaliativa
            }
            for a in aulas_criadas
        ],
        "integracao": {
            "agenda": f"{len(eventos_agenda)} eventos criados" if eventos_agenda else "Nenhum (aluno não selecionado ou criar_agenda=false)",
            "materiais": "Disponível em /conteudos-aluno/{student_id}/sugestoes-material" if student_id else "Selecione um aluno",
            "provas": "Disponível em /conteudos-aluno/{student_id}/sugestoes-prova" if student_id else "Selecione um aluno"
        }
    }


@router.post("/{registro_id}/criar-agenda")
async def criar_agenda_de_registro(
    registro_id: int,
    student_id: int = Query(..., description="ID do aluno para criar agenda"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📅 Criar eventos na agenda a partir de um registro existente
    
    Use quando importou sem selecionar aluno e agora quer criar a agenda.
    """
    # Verificar registro
    registro = db.query(RegistroDiario).filter(
        RegistroDiario.id == registro_id,
        RegistroDiario.professor_id == current_user.id
    ).first()
    
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    # Verificar aluno
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.created_by_user_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Buscar aulas do registro
    aulas = db.query(AulaRegistrada).filter(AulaRegistrada.registro_id == registro_id).all()
    
    # Atualizar student_id do registro se não tinha
    if not registro.student_id:
        registro.student_id = student_id
        db.commit()
    
    # Criar eventos
    eventos = criar_eventos_agenda(
        db=db,
        professor_id=current_user.id,
        student_id=student_id,
        data_aula=registro.data_aula,
        aulas=aulas,
        serie_turma=registro.serie_turma
    )
    
    return {
        "success": True,
        "message": f"{len(eventos)} eventos criados na agenda",
        "eventos": [
            {
                "id": e.id,
                "titulo": e.titulo,
                "data": e.data.isoformat(),
                "hora": e.hora_inicio.isoformat() if e.hora_inicio else None
            }
            for e in eventos
        ]
    }


@router.get("/")
async def listar_registros(
    data_inicio: Optional[date] = Query(None, description="Data inicial"),
    data_fim: Optional[date] = Query(None, description="Data final"),
    student_id: Optional[int] = Query(None, description="Filtrar por aluno"),
    disciplina: Optional[str] = Query(None, description="Filtrar por disciplina"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📋 Listar registros diários importados
    """
    query = db.query(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id
    )
    
    if data_inicio:
        query = query.filter(RegistroDiario.data_aula >= data_inicio)
    if data_fim:
        query = query.filter(RegistroDiario.data_aula <= data_fim)
    if student_id:
        query = query.filter(RegistroDiario.student_id == student_id)
    
    total = query.count()
    registros = query.order_by(RegistroDiario.data_aula.desc()).offset(offset).limit(limit).all()
    
    resultado = []
    for reg in registros:
        aulas = db.query(AulaRegistrada).filter(AulaRegistrada.registro_id == reg.id).all()
        
        # Filtrar por disciplina se especificado
        if disciplina:
            aulas = [a for a in aulas if disciplina.lower() in a.disciplina.lower()]
        
        resultado.append({
            "id": reg.id,
            "data_aula": reg.data_aula.isoformat(),
            "serie_turma": reg.serie_turma,
            "escola": reg.escola_origem,
            "student_id": reg.student_id,
            "total_aulas": len(aulas),
            "disciplinas": list(set(a.disciplina for a in aulas)),
            "created_at": reg.created_at.isoformat() if reg.created_at else None
        })
    
    return {
        "total": total,
        "registros": resultado
    }


@router.get("/{registro_id}")
async def obter_registro(
    registro_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🔍 Obter detalhes de um registro diário
    """
    registro = db.query(RegistroDiario).filter(
        RegistroDiario.id == registro_id,
        RegistroDiario.professor_id == current_user.id
    ).first()
    
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    aulas = db.query(AulaRegistrada).filter(AulaRegistrada.registro_id == registro_id).all()
    
    return {
        "id": registro.id,
        "data_aula": registro.data_aula.isoformat(),
        "serie_turma": registro.serie_turma,
        "escola": registro.escola_origem,
        "student_id": registro.student_id,
        "created_at": registro.created_at.isoformat() if registro.created_at else None,
        "aulas": [a.to_dict() for a in aulas]
    }


@router.get("/aulas/por-disciplina")
async def aulas_por_disciplina(
    disciplina: str = Query(..., description="Nome da disciplina"),
    data_inicio: Optional[date] = Query(None, description="Data inicial"),
    data_fim: Optional[date] = Query(None, description="Data final"),
    student_id: Optional[int] = Query(None, description="Filtrar por aluno"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📚 Listar todas as aulas de uma disciplina específica
    """
    query = db.query(AulaRegistrada).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id,
        AulaRegistrada.disciplina.ilike(f"%{disciplina}%")
    )
    
    if data_inicio:
        query = query.filter(RegistroDiario.data_aula >= data_inicio)
    if data_fim:
        query = query.filter(RegistroDiario.data_aula <= data_fim)
    if student_id:
        query = query.filter(RegistroDiario.student_id == student_id)
    
    aulas = query.order_by(RegistroDiario.data_aula.desc()).all()
    
    return {
        "disciplina": disciplina,
        "total_aulas": len(aulas),
        "aulas": [
            {
                "id": a.id,
                "data": a.registro.data_aula.isoformat(),
                "conteudo": a.conteudo,
                "atividade_sala": a.atividade_sala,
                "professor": a.professor_nome,
                "paginas": a.paginas,
                "modulo": a.modulo,
                "tem_dever": a.tem_dever_casa,
                "tem_avaliacao": a.tem_atividade_avaliativa
            }
            for a in aulas
        ]
    }


@router.get("/aulas/conteudos-estudados")
async def conteudos_estudados(
    student_id: Optional[int] = Query(None, description="Filtrar por aluno"),
    dias: int = Query(30, description="Últimos X dias"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📖 Resumo de conteúdos estudados por disciplina
    """
    data_inicio = date.today() - timedelta(days=dias)
    
    query = db.query(AulaRegistrada).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id,
        RegistroDiario.data_aula >= data_inicio
    )
    
    if student_id:
        query = query.filter(RegistroDiario.student_id == student_id)
    
    aulas = query.order_by(RegistroDiario.data_aula.desc()).all()
    
    # Agrupar por disciplina
    por_disciplina = {}
    for aula in aulas:
        disc = aula.disciplina
        if disc not in por_disciplina:
            por_disciplina[disc] = {
                "disciplina": disc,
                "total_aulas": 0,
                "conteudos": [],
                "tem_deveres_pendentes": False,
                "tem_avaliacoes": False
            }
        
        por_disciplina[disc]["total_aulas"] += 1
        por_disciplina[disc]["conteudos"].append({
            "data": aula.registro.data_aula.isoformat(),
            "conteudo": aula.conteudo,
            "paginas": aula.paginas
        })
        
        if aula.tem_dever_casa:
            por_disciplina[disc]["tem_deveres_pendentes"] = True
        if aula.tem_atividade_avaliativa:
            por_disciplina[disc]["tem_avaliacoes"] = True
    
    return {
        "periodo": f"Últimos {dias} dias",
        "data_inicio": data_inicio.isoformat(),
        "total_disciplinas": len(por_disciplina),
        "total_aulas": len(aulas),
        "por_disciplina": list(por_disciplina.values())
    }


@router.delete("/{registro_id}")
async def deletar_registro(
    registro_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    🗑️ Deletar um registro diário
    """
    registro = db.query(RegistroDiario).filter(
        RegistroDiario.id == registro_id,
        RegistroDiario.professor_id == current_user.id
    ).first()
    
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    # Deletar arquivo PDF
    if registro.arquivo_pdf:
        Path(registro.arquivo_pdf).unlink(missing_ok=True)
    
    db.delete(registro)
    db.commit()
    
    return {"success": True, "message": "Registro deletado com sucesso"}


@router.get("/stats/resumo")
async def estatisticas_registros(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    📊 Estatísticas dos registros diários
    """
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    
    total_registros = db.query(func.count(RegistroDiario.id)).filter(
        RegistroDiario.professor_id == current_user.id
    ).scalar()
    
    registros_mes = db.query(func.count(RegistroDiario.id)).filter(
        RegistroDiario.professor_id == current_user.id,
        RegistroDiario.data_aula >= inicio_mes
    ).scalar()
    
    total_aulas = db.query(func.count(AulaRegistrada.id)).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id
    ).scalar()
    
    disciplinas = db.query(AulaRegistrada.disciplina).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id
    ).distinct().all()
    
    com_dever = db.query(func.count(AulaRegistrada.id)).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id,
        AulaRegistrada.tem_dever_casa == True
    ).scalar()
    
    com_avaliacao = db.query(func.count(AulaRegistrada.id)).join(RegistroDiario).filter(
        RegistroDiario.professor_id == current_user.id,
        AulaRegistrada.tem_atividade_avaliativa == True
    ).scalar()
    
    return {
        "total_registros": total_registros,
        "registros_mes": registros_mes,
        "total_aulas": total_aulas,
        "total_disciplinas": len(disciplinas),
        "disciplinas": [d[0] for d in disciplinas],
        "aulas_com_dever": com_dever,
        "aulas_com_avaliacao": com_avaliacao
    }
