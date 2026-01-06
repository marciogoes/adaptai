# ============================================
# ROTAS DE ESCOLAS - AdaptAI Multi-tenant
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.escola import Escola, ConfiguracaoEscola
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.assinatura import Assinatura
from app.models.plano import Plano
from app.api.dependencies import get_current_user
from app.core.tenant import get_tenant_context, TenantContext
from app.schemas.multitenant import (
    EscolaCreate, EscolaUpdate, EscolaResponse, 
    EscolaComAssinatura, DashboardEscola, AssinaturaComLimites
)

router = APIRouter(prefix="/escolas", tags=["🏫 Escolas"])


# ==========================================
# ROTAS DA ESCOLA ATUAL (TENANT)
# ==========================================

@router.get("/minha", response_model=EscolaComAssinatura)
async def obter_minha_escola(
    tenant: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db)
):
    """
    🏫 Obtém dados da escola do usuário logado
    """
    if not tenant.escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não está vinculado a nenhuma escola"
        )
    
    # Conta alunos e professores
    total_alunos = db.query(Student).filter(
        Student.escola_id == tenant.escola_id
    ).count() if hasattr(Student, 'escola_id') else 0
    
    total_professores = db.query(User).filter(
        User.escola_id == tenant.escola_id,
        User.role.in_([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
    ).count()
    
    escola_dict = {
        **tenant.escola.__dict__,
        "assinatura": tenant.assinatura,
        "total_alunos": total_alunos,
        "total_professores": total_professores
    }
    
    return escola_dict


@router.get("/minha/dashboard", response_model=DashboardEscola)
async def obter_dashboard_escola(
    tenant: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db)
):
    """
    📊 Obtém dashboard completo da escola
    """
    if not tenant.escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não está vinculado a nenhuma escola"
        )
    
    # Estatísticas
    total_alunos = db.query(Student).filter(
        Student.escola_id == tenant.escola_id
    ).count() if hasattr(Student, 'escola_id') else 0
    
    total_professores = db.query(User).filter(
        User.escola_id == tenant.escola_id,
        User.role.in_([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
    ).count()
    
    # Alertas
    alertas = []
    dias_trial = None
    
    if tenant.assinatura:
        if tenant.em_trial and tenant.assinatura.data_fim:
            dias_trial = (tenant.assinatura.data_fim - datetime.now()).days
            if dias_trial <= 3:
                alertas.append(f"⚠️ Seu período de teste expira em {dias_trial} dias!")
        
        if tenant.assinatura.status == "atrasada":
            alertas.append("🔴 Pagamento em atraso! Regularize para continuar usando.")
        
        # Verifica limites
        if tenant.assinatura.plano:
            if tenant.assinatura.alunos_ativos >= tenant.assinatura.plano.limite_alunos * 0.9:
                alertas.append("⚠️ Você está próximo do limite de alunos do plano.")
            
            if tenant.assinatura.provas_mes_atual >= tenant.assinatura.plano.limite_provas_mes * 0.9:
                alertas.append("⚠️ Você está próximo do limite de provas do mês.")
    
    # Monta assinatura com limites
    assinatura_limites = None
    if tenant.assinatura and tenant.assinatura.plano:
        plano = tenant.assinatura.plano
        assinatura_limites = {
            **tenant.assinatura.__dict__,
            "plano": plano,
            "limite_alunos": plano.limite_alunos,
            "limite_professores": plano.limite_professores,
            "limite_provas_mes": plano.limite_provas_mes,
            "limite_materiais_mes": plano.limite_materiais_mes,
            "limite_peis_mes": plano.limite_peis_mes,
            "uso_alunos_percentual": (tenant.assinatura.alunos_ativos / plano.limite_alunos * 100) if plano.limite_alunos > 0 else 0,
            "uso_professores_percentual": (tenant.assinatura.professores_ativos / plano.limite_professores * 100) if plano.limite_professores > 0 else 0,
            "uso_provas_percentual": (tenant.assinatura.provas_mes_atual / plano.limite_provas_mes * 100) if plano.limite_provas_mes > 0 else 0,
            "uso_materiais_percentual": (tenant.assinatura.materiais_mes_atual / plano.limite_materiais_mes * 100) if plano.limite_materiais_mes > 0 else 0,
            "uso_peis_percentual": (tenant.assinatura.peis_mes_atual / plano.limite_peis_mes * 100) if plano.limite_peis_mes > 0 else 0,
        }
    
    return {
        "escola": tenant.escola,
        "assinatura": assinatura_limites,
        "total_alunos": total_alunos,
        "total_professores": total_professores,
        "provas_criadas_mes": tenant.assinatura.provas_mes_atual if tenant.assinatura else 0,
        "materiais_criados_mes": tenant.assinatura.materiais_mes_atual if tenant.assinatura else 0,
        "peis_gerados_mes": tenant.assinatura.peis_mes_atual if tenant.assinatura else 0,
        "dias_restantes_trial": dias_trial,
        "proxima_fatura": None,  # TODO: Implementar
        "alertas": alertas
    }


@router.put("/minha", response_model=EscolaResponse)
async def atualizar_minha_escola(
    escola_data: EscolaUpdate,
    tenant: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db)
):
    """
    ✏️ Atualiza dados da escola (Admin da escola)
    """
    if not tenant.escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não está vinculado a nenhuma escola"
        )
    
    # Verifica permissão
    if tenant.user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem editar dados da escola"
        )
    
    # Atualiza campos
    for key, value in escola_data.model_dump(exclude_unset=True).items():
        setattr(tenant.escola, key, value)
    
    db.commit()
    db.refresh(tenant.escola)
    
    return tenant.escola


# ==========================================
# ROTAS ADMIN (Super Admin)
# ==========================================

@router.get("/admin/todas", response_model=List[EscolaComAssinatura])
async def listar_todas_escolas(
    ativa: Optional[bool] = None,
    tipo: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    📋 Lista todas as escolas (Super Admin)
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Super Admin pode listar todas as escolas"
        )
    
    query = db.query(Escola)
    
    if ativa is not None:
        query = query.filter(Escola.ativa == ativa)
    
    if tipo:
        query = query.filter(Escola.tipo == tipo)
    
    escolas = query.order_by(Escola.created_at.desc()).all()
    
    resultado = []
    for escola in escolas:
        total_alunos = db.query(Student).filter(
            Student.escola_id == escola.id
        ).count() if hasattr(Student, 'escola_id') else 0
        
        total_professores = db.query(User).filter(
            User.escola_id == escola.id
        ).count()
        
        assinatura = db.query(Assinatura).filter(
            Assinatura.escola_id == escola.id
        ).first()
        
        resultado.append({
            **escola.__dict__,
            "assinatura": assinatura,
            "total_alunos": total_alunos,
            "total_professores": total_professores
        })
    
    return resultado


@router.get("/admin/{escola_id}", response_model=EscolaComAssinatura)
async def obter_escola_por_id(
    escola_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🔍 Obtém escola por ID (Super Admin)
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Super Admin pode acessar qualquer escola"
        )
    
    escola = db.query(Escola).filter(Escola.id == escola_id).first()
    
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escola não encontrada"
        )
    
    total_alunos = db.query(Student).filter(
        Student.escola_id == escola.id
    ).count() if hasattr(Student, 'escola_id') else 0
    
    total_professores = db.query(User).filter(
        User.escola_id == escola.id
    ).count()
    
    assinatura = db.query(Assinatura).filter(
        Assinatura.escola_id == escola.id
    ).first()
    
    return {
        **escola.__dict__,
        "assinatura": assinatura,
        "total_alunos": total_alunos,
        "total_professores": total_professores
    }


@router.put("/admin/{escola_id}/ativar")
async def ativar_escola(
    escola_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ✅ Ativa uma escola (Super Admin)
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Super Admin"
        )
    
    escola = db.query(Escola).filter(Escola.id == escola_id).first()
    if not escola:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    
    escola.ativa = True
    db.commit()
    
    return {"message": f"Escola '{escola.nome}' ativada com sucesso"}


@router.put("/admin/{escola_id}/desativar")
async def desativar_escola(
    escola_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🚫 Desativa uma escola (Super Admin)
    """
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas Super Admin"
        )
    
    escola = db.query(Escola).filter(Escola.id == escola_id).first()
    if not escola:
        raise HTTPException(status_code=404, detail="Escola não encontrada")
    
    escola.ativa = False
    db.commit()
    
    return {"message": f"Escola '{escola.nome}' desativada"}
