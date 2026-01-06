# ============================================
# ROTAS DE CHECKOUT / ONBOARDING - AdaptAI
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from app.database import get_db
from app.models.escola import Escola, ConfiguracaoEscola
from app.models.user import User, UserRole
from app.models.plano import Plano
from app.models.assinatura import Assinatura
from app.core.config import settings
from app.schemas.multitenant import CheckoutRequest, CheckoutResponse, StatusAssinatura

router = APIRouter(prefix="/checkout", tags=["🛒 Checkout"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_token_acesso(user_id: int, email: str) -> str:
    """Cria token JWT para login automático após cadastro"""
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


@router.post("/iniciar", response_model=CheckoutResponse)
async def iniciar_checkout(
    dados: CheckoutRequest,
    db: Session = Depends(get_db)
):
    """
    🚀 Inicia o processo de checkout (cria escola + admin + trial)
    
    Este endpoint cria:
    1. A escola (tenant)
    2. O usuário administrador
    3. A assinatura em modo TRIAL (14 dias)
    4. As configurações padrão da escola
    
    Retorna um token JWT para login automático.
    """
    
    # 1. Verifica se o plano existe
    plano = db.query(Plano).filter(
        Plano.id == dados.plano_id,
        Plano.ativo == True
    ).first()
    
    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano não encontrado ou inativo"
        )
    
    # 2. Verifica se email do admin já existe
    usuario_existente = db.query(User).filter(
        User.email == dados.admin_email
    ).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está cadastrado. Faça login ou use outro email."
        )
    
    # 3. Verifica se CNPJ já existe (se fornecido)
    if dados.escola_cnpj:
        escola_existente = db.query(Escola).filter(
            Escola.cnpj == dados.escola_cnpj
        ).first()
        
        if escola_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma escola cadastrada com este CNPJ"
            )
    
    try:
        # 4. Cria a escola
        escola = Escola(
            nome=dados.escola_nome,
            cnpj=dados.escola_cnpj,
            tipo=dados.escola_tipo.value,
            email=dados.admin_email,  # Email principal = email do admin
            cep=dados.cep,
            cidade=dados.cidade,
            estado=dados.estado,
            ativa=True,
            cor_primaria="#8B5CF6",  # Roxo AdaptAI
            cor_secundaria="#EC4899"  # Rosa
        )
        db.add(escola)
        db.flush()  # Para obter o ID
        
        # 5. Cria o usuário administrador
        hashed_password = pwd_context.hash(dados.admin_senha)
        
        usuario = User(
            name=dados.admin_nome,
            email=dados.admin_email,
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            escola_id=escola.id,
            is_active=True
        )
        db.add(usuario)
        db.flush()
        
        # 6. Cria a assinatura em modo TRIAL
        data_fim_trial = datetime.now() + timedelta(days=14)
        
        assinatura = Assinatura(
            escola_id=escola.id,
            plano_id=plano.id,
            status=StatusAssinatura.TRIAL.value,
            data_inicio=datetime.now(),
            data_fim=data_fim_trial,
            valor_mensal=plano.valor,
            dia_vencimento=10,
            alunos_ativos=0,
            professores_ativos=1,  # O admin conta como professor
            provas_mes_atual=0,
            materiais_mes_atual=0,
            peis_mes_atual=0,
            relatorios_mes_atual=0
        )
        db.add(assinatura)
        
        # 7. Cria configurações padrão da escola
        configuracao = ConfiguracaoEscola(
            escola_id=escola.id,
            modelo_ia_preferido="claude-3-haiku-20240307",
            quantidade_questoes_padrao=5,
            dificuldade_padrao="medio",
            notificacoes_email=True,
            pei_automatico_ativo=True,
            materiais_adaptativos_ativo=True,
            relatorios_avancados_ativo=plano.relatorios_avancados,
            lgpd_ativo=True
        )
        db.add(configuracao)
        
        # 8. Commit de tudo
        db.commit()
        
        # 9. Gera token para login automático
        token = criar_token_acesso(usuario.id, usuario.email)
        
        return CheckoutResponse(
            success=True,
            message=f"🎉 Bem-vindo ao AdaptAI! Sua escola '{escola.nome}' foi criada com sucesso.",
            escola_id=escola.id,
            usuario_id=usuario.id,
            assinatura_id=assinatura.id,
            status=StatusAssinatura.TRIAL,
            trial_dias=14,
            link_pagamento=None,  # TODO: Integrar com Asaas
            token=token
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar conta: {str(e)}"
        )


@router.get("/verificar-email/{email}")
async def verificar_email_disponivel(
    email: str,
    db: Session = Depends(get_db)
):
    """
    ✉️ Verifica se um email está disponível para cadastro
    """
    usuario = db.query(User).filter(User.email == email).first()
    
    return {
        "email": email,
        "disponivel": usuario is None,
        "mensagem": "Email disponível" if not usuario else "Email já cadastrado"
    }


@router.get("/verificar-cnpj/{cnpj}")
async def verificar_cnpj_disponivel(
    cnpj: str,
    db: Session = Depends(get_db)
):
    """
    🏢 Verifica se um CNPJ está disponível para cadastro
    """
    escola = db.query(Escola).filter(Escola.cnpj == cnpj).first()
    
    return {
        "cnpj": cnpj,
        "disponivel": escola is None,
        "mensagem": "CNPJ disponível" if not escola else "CNPJ já cadastrado"
    }


@router.get("/resumo-plano/{plano_id}")
async def obter_resumo_plano(
    plano_id: int,
    db: Session = Depends(get_db)
):
    """
    📋 Obtém resumo do plano para exibir no checkout
    """
    plano = db.query(Plano).filter(
        Plano.id == plano_id,
        Plano.ativo == True
    ).first()
    
    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano não encontrado"
        )
    
    return {
        "id": plano.id,
        "nome": plano.nome,
        "valor_mensal": plano.valor,
        "valor_anual": plano.valor_anual,
        "economia_anual": (plano.valor * 12 - plano.valor_anual) if plano.valor_anual else 0,
        "trial_dias": 14,
        "funcionalidades": {
            "limite_alunos": plano.limite_alunos,
            "limite_professores": plano.limite_professores,
            "limite_provas_mes": plano.limite_provas_mes,
            "limite_materiais_mes": plano.limite_materiais_mes,
            "limite_peis_mes": plano.limite_peis_mes,
            "pei_automatico": plano.pei_automatico,
            "materiais_adaptativos": plano.materiais_adaptativos,
            "mapas_mentais": plano.mapas_mentais,
            "relatorios_avancados": plano.relatorios_avancados,
            "suporte_prioritario": plano.suporte_prioritario,
            "exportacao_pdf": plano.exportacao_pdf,
            "exportacao_excel": plano.exportacao_excel
        }
    }
