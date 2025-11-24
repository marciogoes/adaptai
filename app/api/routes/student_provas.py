"""
Rotas para Estudantes - Provas
Endpoints para estudantes verem e fazerem suas provas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.student import Student
from app.models.prova import ProvaAluno, Prova, QuestaoGerada, RespostaAluno, StatusProvaAluno
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

router = APIRouter(prefix="/student/provas", tags=["Student - Provas"])


def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Student:
    """Dependency para obter estudante atual do token"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    email: str = payload.get("sub")
    if not email or not email.startswith("student:"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não é de estudante")
    
    email = email.replace("student:", "")
    student = db.query(Student).filter(Student.email == email).first()
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudante não encontrado")
    if not student.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Estudante inativo")
    
    return student


@router.get("/")
def listar_minhas_provas(current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Listar todas as provas atribuídas ao estudante"""
    provas_aluno = db.query(ProvaAluno).filter(ProvaAluno.aluno_id == current_student.id).all()
    
    resultado = []
    for pa in provas_aluno:
        prova = db.query(Prova).filter(Prova.id == pa.prova_id).first()
        resultado.append({
            "prova_aluno_id": pa.id,
            "prova_id": prova.id,
            "titulo": prova.titulo,
            "descricao": prova.descricao,
            "materia": prova.materia,
            "serie_nivel": prova.serie_nivel,
            "quantidade_questoes": prova.quantidade_questoes,
            "tempo_limite_minutos": prova.tempo_limite_minutos,
            "pontuacao_total": prova.pontuacao_total,
            "status": pa.status.value,
            "data_atribuicao": pa.data_atribuicao,
            "nota_final": pa.nota_final,
            "aprovado": pa.aprovado
        })
    
    return resultado


@router.post("/{prova_aluno_id}/iniciar")
def iniciar_prova(prova_aluno_id: int, current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Iniciar prova"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id, ProvaAluno.aluno_id == current_student.id).first()
    
    if not prova_aluno:
        raise HTTPException(status_code=404, detail="Prova não encontrada")
    if prova_aluno.status != StatusProvaAluno.PENDENTE:
        raise HTTPException(status_code=400, detail=f"Prova já está: {prova_aluno.status.value}")
    
    prova_aluno.status = StatusProvaAluno.EM_ANDAMENTO
    prova_aluno.data_inicio = datetime.utcnow()
    db.commit()
    
    return {"message": "Prova iniciada!", "status": "em_andamento"}


@router.get("/{prova_aluno_id}/questoes")
def obter_questoes(prova_aluno_id: int, current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Obter questões da prova"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id, ProvaAluno.aluno_id == current_student.id).first()
    
    if not prova_aluno:
        raise HTTPException(status_code=404, detail="Prova não encontrada")
    if prova_aluno.status == StatusProvaAluno.PENDENTE:
        raise HTTPException(status_code=400, detail="Inicie a prova primeiro")
    
    questoes = db.query(QuestaoGerada).filter(QuestaoGerada.prova_id == prova_aluno.prova_id).order_by(QuestaoGerada.numero).all()
    
    respostas_dadas = db.query(RespostaAluno).filter(RespostaAluno.prova_aluno_id == prova_aluno_id).all()
    respostas_dict = {r.questao_id: r.resposta_aluno for r in respostas_dadas}
    
    return {
        "prova_aluno_id": prova_aluno_id,
        "status": prova_aluno.status.value,
        "questoes": [{"id": q.id, "numero": q.numero, "enunciado": q.enunciado, "opcoes": q.opcoes, "resposta_ja_dada": respostas_dict.get(q.id)} for q in questoes]
    }


@router.post("/{prova_aluno_id}/responder")
async def responder(prova_aluno_id: int, data: dict, current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Responder questão. Body: {"questao_id": 1, "resposta": "A"}"""
    questao_id = data.get("questao_id")
    resposta = data.get("resposta")
    
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id, ProvaAluno.aluno_id == current_student.id).first()
    if not prova_aluno or prova_aluno.status != StatusProvaAluno.EM_ANDAMENTO:
        raise HTTPException(status_code=400, detail="Prova indisponível")
    
    questao = db.query(QuestaoGerada).filter(QuestaoGerada.id == questao_id, QuestaoGerada.prova_id == prova_aluno.prova_id).first()
    if not questao:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    
    esta_correta = (resposta.strip().upper() == questao.resposta_correta.strip().upper())
    
    resposta_obj = db.query(RespostaAluno).filter(RespostaAluno.prova_aluno_id == prova_aluno_id, RespostaAluno.questao_id == questao_id).first()
    if resposta_obj:
        resposta_obj.resposta_aluno = resposta
        resposta_obj.esta_correta = esta_correta
        resposta_obj.pontuacao_obtida = questao.pontuacao if esta_correta else 0
        resposta_obj.respondido_em = datetime.utcnow()
    else:
        nova = RespostaAluno(
            prova_aluno_id=prova_aluno_id, 
            questao_id=questao_id, 
            resposta_aluno=resposta, 
            esta_correta=esta_correta, 
            pontuacao_obtida=questao.pontuacao if esta_correta else 0, 
            pontuacao_maxima=questao.pontuacao,
            respondido_em=datetime.utcnow()
        )
        db.add(nova)
    
    db.commit()
    return {"message": "Resposta salva!"}


@router.post("/{prova_aluno_id}/finalizar")
def finalizar(prova_aluno_id: int, current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Finalizar prova e calcular nota"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id, ProvaAluno.aluno_id == current_student.id).first()
    if not prova_aluno or prova_aluno.status != StatusProvaAluno.EM_ANDAMENTO:
        raise HTTPException(status_code=400, detail="Não pode finalizar")
    
    respostas = db.query(RespostaAluno).filter(RespostaAluno.prova_aluno_id == prova_aluno_id).all()
    pontuacao_obtida = sum(r.pontuacao_obtida for r in respostas)
    prova = db.query(Prova).filter(Prova.id == prova_aluno.prova_id).first()
    nota_final = (pontuacao_obtida / prova.pontuacao_total) * 10 if prova.pontuacao_total > 0 else 0
    aprovado = nota_final >= prova.nota_minima_aprovacao
    tempo_gasto = int((datetime.utcnow() - prova_aluno.data_inicio).total_seconds() / 60) if prova_aluno.data_inicio else None
    
    prova_aluno.status = StatusProvaAluno.CONCLUIDA
    prova_aluno.data_conclusao = datetime.utcnow()
    prova_aluno.pontuacao_obtida = pontuacao_obtida
    prova_aluno.pontuacao_maxima = prova.pontuacao_total
    prova_aluno.nota_final = nota_final
    prova_aluno.aprovado = aprovado
    prova_aluno.tempo_gasto_minutos = tempo_gasto
    db.commit()
    
    acertos = sum(1 for r in respostas if r.esta_correta)
    return {
        "message": "Prova finalizada!", 
        "nota_final": round(nota_final, 2), 
        "aprovado": aprovado, 
        "acertos": acertos, 
        "total_questoes": len(respostas),
        "percentual": round((acertos / len(respostas) * 100) if len(respostas) > 0 else 0, 1)
    }


@router.get("/{prova_aluno_id}/resultado")
def ver_resultado(prova_aluno_id: int, current_student: Student = Depends(get_current_student), db: Session = Depends(get_db)):
    """Ver resultado completo da prova"""
    prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id, ProvaAluno.aluno_id == current_student.id).first()
    
    if not prova_aluno:
        raise HTTPException(status_code=404, detail="Prova não encontrada")
    if prova_aluno.status not in [StatusProvaAluno.CONCLUIDA, StatusProvaAluno.CORRIGIDA]:
        raise HTTPException(status_code=400, detail="Prova ainda não foi finalizada")
    
    prova = db.query(Prova).filter(Prova.id == prova_aluno.prova_id).first()
    questoes = db.query(QuestaoGerada).filter(QuestaoGerada.prova_id == prova.id).order_by(QuestaoGerada.numero).all()
    respostas = db.query(RespostaAluno).filter(RespostaAluno.prova_aluno_id == prova_aluno_id).all()
    respostas_dict = {r.questao_id: r for r in respostas}
    
    questoes_com_respostas = []
    for q in questoes:
        resposta = respostas_dict.get(q.id)
        questoes_com_respostas.append({
            "numero": q.numero,
            "enunciado": q.enunciado,
            "opcoes": q.opcoes,
            "resposta_correta": q.resposta_correta,
            "resposta_aluno": resposta.resposta_aluno if resposta else None,
            "esta_correta": resposta.esta_correta if resposta else False,
            "explicacao": q.explicacao
        })
    
    acertos = sum(1 for r in respostas if r.esta_correta)
    
    return {
        "prova": {
            "titulo": prova.titulo,
            "materia": prova.materia,
            "serie_nivel": prova.serie_nivel
        },
        "resultado": {
            "nota_final": prova_aluno.nota_final,
            "aprovado": prova_aluno.aprovado,
            "acertos": acertos,
            "total_questoes": len(questoes),
            "percentual": round((acertos / len(questoes) * 100) if len(questoes) > 0 else 0, 1),
            "tempo_gasto_minutos": prova_aluno.tempo_gasto_minutos,
            "data_conclusao": prova_aluno.data_conclusao
        },
        "questoes": questoes_com_respostas,
        "feedback_ia": prova_aluno.feedback_ia,
        "analise_ia": prova_aluno.analise_ia
    }
