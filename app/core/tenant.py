# ============================================
# MIDDLEWARE E DEPENDÊNCIAS MULTI-TENANT
# ============================================
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User, UserRole
from app.models.escola import Escola
from app.models.assinatura import Assinatura, StatusAssinatura
from app.api.dependencies import get_current_user


class TenantContext:
    """
    Contexto do tenant atual na requisição.
    Contém informações sobre a escola e limites de uso.
    """
    def __init__(
        self,
        escola: Optional[Escola] = None,
        assinatura: Optional[Assinatura] = None,
        user: Optional[User] = None
    ):
        self.escola = escola
        self.assinatura = assinatura
        self.user = user
    
    @property
    def escola_id(self) -> Optional[int]:
        return self.escola.id if self.escola else None
    
    @property
    def escola_nome(self) -> str:
        return self.escola.nome if self.escola else "Sem escola"
    
    @property
    def plano_ativo(self) -> bool:
        if not self.assinatura:
            return False
        return self.assinatura.status in [
            StatusAssinatura.TRIAL.value,
            StatusAssinatura.ATIVA.value
        ]
    
    @property
    def em_trial(self) -> bool:
        if not self.assinatura:
            return False
        return self.assinatura.status == StatusAssinatura.TRIAL.value
    
    def verificar_limite_alunos(self) -> bool:
        """Verifica se pode adicionar mais alunos"""
        if not self.assinatura or not self.assinatura.plano:
            return False
        return self.assinatura.alunos_ativos < self.assinatura.plano.limite_alunos
    
    def verificar_limite_professores(self) -> bool:
        """Verifica se pode adicionar mais professores"""
        if not self.assinatura or not self.assinatura.plano:
            return False
        return self.assinatura.professores_ativos < self.assinatura.plano.limite_professores
    
    def verificar_limite_provas(self) -> bool:
        """Verifica se pode criar mais provas este mês"""
        if not self.assinatura or not self.assinatura.plano:
            return False
        return self.assinatura.provas_mes_atual < self.assinatura.plano.limite_provas_mes
    
    def verificar_limite_materiais(self) -> bool:
        """Verifica se pode criar mais materiais este mês"""
        if not self.assinatura or not self.assinatura.plano:
            return False
        return self.assinatura.materiais_mes_atual < self.assinatura.plano.limite_materiais_mes
    
    def verificar_limite_peis(self) -> bool:
        """Verifica se pode gerar mais PEIs este mês"""
        if not self.assinatura or not self.assinatura.plano:
            return False
        return self.assinatura.peis_mes_atual < self.assinatura.plano.limite_peis_mes


async def get_tenant_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TenantContext:
    """
    Obtém o contexto do tenant (escola) atual.
    Usado para filtrar dados e verificar limites.
    """
    # Super admin não tem escola vinculada obrigatoriamente
    if current_user.role == UserRole.SUPER_ADMIN:
        return TenantContext(user=current_user)
    
    # Busca a escola do usuário
    if not current_user.escola_id:
        # Usuário sem escola - pode ser usuário legado ou erro
        return TenantContext(user=current_user)
    
    escola = db.query(Escola).filter(
        Escola.id == current_user.escola_id,
        Escola.ativa == True
    ).first()
    
    if not escola:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Escola não encontrada ou inativa"
        )
    
    # Busca assinatura da escola
    assinatura = db.query(Assinatura).filter(
        Assinatura.escola_id == escola.id
    ).first()
    
    return TenantContext(
        escola=escola,
        assinatura=assinatura,
        user=current_user
    )


async def require_active_subscription(
    tenant: TenantContext = Depends(get_tenant_context)
) -> TenantContext:
    """
    Requer que a escola tenha uma assinatura ativa.
    Bloqueia acesso se a assinatura estiver cancelada/suspensa.
    """
    # Super admin sempre tem acesso
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.plano_ativo:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Assinatura inativa ou expirada. Por favor, renove seu plano."
        )
    
    return tenant


async def require_escola(
    tenant: TenantContext = Depends(get_tenant_context)
) -> TenantContext:
    """
    Requer que o usuário esteja vinculado a uma escola.
    """
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.escola:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não está vinculado a nenhuma escola"
        )
    
    return tenant


def check_limite_alunos(tenant: TenantContext = Depends(require_active_subscription)):
    """Verifica limite de alunos antes de criar novo"""
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.verificar_limite_alunos():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Limite de alunos atingido. Faça upgrade do plano."
        )
    return tenant


def check_limite_provas(tenant: TenantContext = Depends(require_active_subscription)):
    """Verifica limite de provas antes de criar nova"""
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.verificar_limite_provas():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Limite de provas mensais atingido. Aguarde o próximo mês ou faça upgrade."
        )
    return tenant


def check_limite_materiais(tenant: TenantContext = Depends(require_active_subscription)):
    """Verifica limite de materiais antes de criar novo"""
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.verificar_limite_materiais():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Limite de materiais mensais atingido. Aguarde o próximo mês ou faça upgrade."
        )
    return tenant


def check_limite_peis(tenant: TenantContext = Depends(require_active_subscription)):
    """Verifica limite de PEIs antes de gerar novo"""
    if tenant.user and tenant.user.role == UserRole.SUPER_ADMIN:
        return tenant
    
    if not tenant.verificar_limite_peis():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Limite de PEIs mensais atingido. Aguarde o próximo mês ou faça upgrade."
        )
    return tenant
