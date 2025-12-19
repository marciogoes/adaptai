"""
Rotas de Materiais para Estudantes - COM STORAGE
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from jose import JWTError

from app.database import get_db
from app.models.student import Student
from app.models.material import Material, MaterialAluno, StatusMaterial, TipoMaterial
from app.schemas.material import (
    MaterialAlunoResponse, VisualizarMaterialRequest,
    AnotacaoRequest, FavoritoRequest
)
from app.services.storage_service import storage_service
from app.core.security import decode_access_token

# OAuth2 scheme para alunos
oauth2_scheme_student = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/student/login")

router = APIRouter(prefix="/student/materiais", tags=["Student - Materiais"])


async def get_current_student(
    token: str = Depends(oauth2_scheme_student),
    db: Session = Depends(get_db)
) -> Student:
    """Dependency para obter estudante atual do token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate student credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Verificar se é token de estudante (tem prefixo "student:")
        if not email.startswith("student:"):
            raise credentials_exception
        
        # Remover prefixo "student:"
        student_email = email.replace("student:", "")
        
    except JWTError:
        raise credentials_exception
    
    # Buscar estudante no banco
    student = db.query(Student).filter(Student.email == student_email).first()
    
    if student is None or not student.is_active:
        raise credentials_exception
    
    return student


@router.get("/", response_model=List[MaterialAlunoResponse])
async def listar_meus_materiais(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Lista todos os materiais disponíveis para o aluno
    """
    # Buscar materiais do aluno com status DISPONIVEL
    materiais_aluno = db.query(MaterialAluno).join(Material).filter(
        MaterialAluno.aluno_id == current_student.id,
        Material.status == StatusMaterial.DISPONIVEL
    ).all()
    
    return materiais_aluno


@router.get("/{material_aluno_id}/visualizar")
async def visualizar_material(
    material_aluno_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """
    Visualiza um material e registra a visualização
    Retorna o conteúdo do storage
    """
    # Buscar MaterialAluno
    material_aluno = db.query(MaterialAluno).filter(
        MaterialAluno.id == material_aluno_id,
        MaterialAluno.aluno_id == current_student.id
    ).first()
    
    if not material_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    # Verificar se material está disponível
    if material_aluno.material.status != StatusMaterial.DISPONIVEL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Material não está disponível. Status: {material_aluno.material.status}"
        )
    
    # Registrar visualização
    if material_aluno.data_primeira_visualizacao is None:
        material_aluno.data_primeira_visualizacao = func.now()
    
    material_aluno.data_ultima_visualizacao = func.now()
    material_aluno.total_visualizacoes += 1
    
    db.commit()
    db.refresh(material_aluno)
    
    # Buscar conteúdo do storage
    material = material_aluno.material
    
    if material.tipo == TipoMaterial.VISUAL:
        conteudo = storage_service.ler_html(material.id)
        if not conteudo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteúdo do material não encontrado"
            )
        
        return {
            "material_aluno": material_aluno,
            "material": {
                "id": material.id,
                "titulo": material.titulo,
                "descricao": material.descricao,
                "tipo": material.tipo,
                "materia": material.materia,
                "serie_nivel": material.serie_nivel
            },
            "conteudo_tipo": "html",
            "conteudo": conteudo
        }
    
    elif material.tipo == TipoMaterial.MAPA_MENTAL:
        conteudo = storage_service.ler_json(material.id)
        if not conteudo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteúdo do material não encontrado"
            )
        
        return {
            "material_aluno": material_aluno,
            "material": {
                "id": material.id,
                "titulo": material.titulo,
                "descricao": material.descricao,
                "tipo": material.tipo,
                "materia": material.materia,
                "serie_nivel": material.serie_nivel
            },
            "conteudo_tipo": "json",
            "conteudo": conteudo
        }


@router.post("/{material_aluno_id}/favorito")
async def marcar_favorito(
    material_aluno_id: int,
    favorito_data: FavoritoRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Marcar ou desmarcar material como favorito"""
    material_aluno = db.query(MaterialAluno).filter(
        MaterialAluno.id == material_aluno_id,
        MaterialAluno.aluno_id == current_student.id
    ).first()
    
    if not material_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    material_aluno.favorito = 1 if favorito_data.favorito else 0
    db.commit()
    
    return {"success": True, "favorito": bool(material_aluno.favorito)}


@router.post("/{material_aluno_id}/anotacoes")
async def salvar_anotacoes(
    material_aluno_id: int,
    anotacoes_data: AnotacaoRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    """Salvar anotações do aluno sobre o material"""
    material_aluno = db.query(MaterialAluno).filter(
        MaterialAluno.id == material_aluno_id,
        MaterialAluno.aluno_id == current_student.id
    ).first()
    
    if not material_aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material não encontrado"
        )
    
    material_aluno.anotacoes_aluno = anotacoes_data.anotacoes
    db.commit()
    
    return {"success": True, "anotacoes": material_aluno.anotacoes_aluno}
