# ============================================
# SEED DE PLANOS - AdaptAI Multi-tenant
# ============================================
# Execute: python -m scripts.seed_planos
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.plano import Plano
from app.database import Base

def criar_planos():
    """Cria os planos padrão do sistema"""
    
    # Conectar ao banco
    engine = create_engine(settings.db_url, echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    # Definição dos planos
    planos = [
        {
            "nome": "Gratuito",
            "slug": "gratuito",
            "descricao": "Plano gratuito para experimentar a plataforma. Ideal para professores que querem conhecer o sistema.",
            "valor": 0.0,
            "valor_anual": 0.0,
            "limite_alunos": 5,
            "limite_professores": 1,
            "limite_provas_mes": 10,
            "limite_materiais_mes": 10,
            "limite_peis_mes": 5,
            "limite_relatorios_mes": 5,
            "pei_automatico": True,
            "materiais_adaptativos": True,
            "mapas_mentais": True,
            "relatorios_avancados": False,
            "api_access": False,
            "suporte_prioritario": False,
            "treinamento_incluido": False,
            "integracao_whatsapp": False,
            "integracao_google": False,
            "exportacao_pdf": True,
            "exportacao_excel": False,
            "ativo": True,
            "destaque": False,
            "ordem": 0
        },
        {
            "nome": "Essencial",
            "slug": "essencial",
            "descricao": "Plano ideal para professores e pequenas escolas. Todas as funcionalidades essenciais da IA.",
            "valor": 79.90,
            "valor_anual": 766.80,  # 20% desconto (12x R$63,90)
            "limite_alunos": 30,
            "limite_professores": 3,
            "limite_provas_mes": 50,
            "limite_materiais_mes": 50,
            "limite_peis_mes": 30,
            "limite_relatorios_mes": 30,
            "pei_automatico": True,
            "materiais_adaptativos": True,
            "mapas_mentais": True,
            "relatorios_avancados": False,
            "api_access": False,
            "suporte_prioritario": False,
            "treinamento_incluido": False,
            "integracao_whatsapp": False,
            "integracao_google": False,
            "exportacao_pdf": True,
            "exportacao_excel": True,
            "ativo": True,
            "destaque": False,
            "ordem": 1
        },
        {
            "nome": "Profissional",
            "slug": "profissional",
            "descricao": "Para escolas e clínicas. Relatórios avançados, mais alunos e suporte prioritário. MAIS POPULAR!",
            "valor": 159.00,  # <<<< PLANO DE R$ 159 >>>>
            "valor_anual": 1526.40,  # 20% desconto (12x R$127,20)
            "limite_alunos": 100,
            "limite_professores": 10,
            "limite_provas_mes": 200,
            "limite_materiais_mes": 200,
            "limite_peis_mes": 100,
            "limite_relatorios_mes": 100,
            "pei_automatico": True,
            "materiais_adaptativos": True,
            "mapas_mentais": True,
            "relatorios_avancados": True,
            "api_access": False,
            "suporte_prioritario": True,
            "treinamento_incluido": True,
            "integracao_whatsapp": True,
            "integracao_google": True,
            "exportacao_pdf": True,
            "exportacao_excel": True,
            "ativo": True,
            "destaque": True,  # Plano recomendado
            "ordem": 2
        },
        {
            "nome": "Institucional",
            "slug": "institucional",
            "descricao": "Para grandes instituições. Ilimitado, API, treinamento completo e gerente de conta dedicado.",
            "valor": 399.00,
            "valor_anual": 3830.40,  # 20% desconto (12x R$319,20)
            "limite_alunos": 500,
            "limite_professores": 50,
            "limite_provas_mes": 1000,
            "limite_materiais_mes": 1000,
            "limite_peis_mes": 500,
            "limite_relatorios_mes": 500,
            "pei_automatico": True,
            "materiais_adaptativos": True,
            "mapas_mentais": True,
            "relatorios_avancados": True,
            "api_access": True,
            "suporte_prioritario": True,
            "treinamento_incluido": True,
            "integracao_whatsapp": True,
            "integracao_google": True,
            "exportacao_pdf": True,
            "exportacao_excel": True,
            "ativo": True,
            "destaque": False,
            "ordem": 3
        },
        {
            "nome": "Enterprise",
            "slug": "enterprise",
            "descricao": "Personalizado para redes de ensino e secretarias. Ilimitado + SLA + Customização completa.",
            "valor": 999.00,
            "valor_anual": 9590.40,  # 20% desconto
            "limite_alunos": 9999,
            "limite_professores": 999,
            "limite_provas_mes": 9999,
            "limite_materiais_mes": 9999,
            "limite_peis_mes": 9999,
            "limite_relatorios_mes": 9999,
            "pei_automatico": True,
            "materiais_adaptativos": True,
            "mapas_mentais": True,
            "relatorios_avancados": True,
            "api_access": True,
            "suporte_prioritario": True,
            "treinamento_incluido": True,
            "integracao_whatsapp": True,
            "integracao_google": True,
            "exportacao_pdf": True,
            "exportacao_excel": True,
            "ativo": True,
            "destaque": False,
            "ordem": 4
        }
    ]
    
    print("="*60)
    print("🎓 AdaptAI - Criando/Atualizando Planos")
    print("="*60)
    
    for plano_data in planos:
        # Verificar se já existe
        existing = db.query(Plano).filter(Plano.slug == plano_data["slug"]).first()
        
        if existing:
            # Atualizar valores
            for key, value in plano_data.items():
                setattr(existing, key, value)
            print(f"✅ Plano '{plano_data['nome']}' atualizado - R$ {plano_data['valor']:.2f}/mês")
        else:
            # Criar novo
            novo_plano = Plano(**plano_data)
            db.add(novo_plano)
            print(f"✨ Plano '{plano_data['nome']}' criado - R$ {plano_data['valor']:.2f}/mês")
    
    db.commit()
    
    # Listar todos os planos
    print("\n" + "="*60)
    print("📋 PLANOS CADASTRADOS:")
    print("="*60)
    
    todos_planos = db.query(Plano).filter(Plano.ativo == True).order_by(Plano.ordem).all()
    
    for p in todos_planos:
        destaque = "⭐ MAIS POPULAR" if p.destaque else ""
        print(f"""
{'='*50}
📦 {p.nome.upper()} {destaque}
{'='*50}
   💰 Valor: R$ {p.valor:.2f}/mês (anual: R$ {p.valor_anual:.2f})
   👥 Alunos: até {p.limite_alunos}
   👨‍🏫 Professores: até {p.limite_professores}
   📝 Provas/mês: {p.limite_provas_mes}
   📚 Materiais/mês: {p.limite_materiais_mes}
   ❤️ PEIs/mês: {p.limite_peis_mes}
   📊 Relatórios avançados: {'✅' if p.relatorios_avancados else '❌'}
   💬 WhatsApp: {'✅' if p.integracao_whatsapp else '❌'}
   🎓 Treinamento: {'✅' if p.treinamento_incluido else '❌'}
   ⚡ Suporte prioritário: {'✅' if p.suporte_prioritario else '❌'}
   🔌 Acesso API: {'✅' if p.api_access else '❌'}
""")
    
    db.close()
    print("\n✅ Planos configurados com sucesso!")
    print("   O plano PROFISSIONAL de R$ 159,00 está ativo!")


if __name__ == "__main__":
    criar_planos()
