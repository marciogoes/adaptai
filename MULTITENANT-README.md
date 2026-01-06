# 🏢 AdaptAI Multi-tenant

Sistema multi-tenant completo replicado do Seu Cartório, adaptado para o contexto educacional do AdaptAI.

## 📦 Arquitetura

```
AdaptAI Multi-tenant
│
├── 🏫 Escolas (Tenants)
│   ├── Dados isolados por escola
│   ├── Branding customizado (logo, cores)
│   └── Configurações específicas
│
├── 💳 Planos
│   ├── Gratuito (R$ 0)
│   ├── Essencial (R$ 79,90)
│   ├── Profissional (R$ 159,00) ⭐ MAIS POPULAR
│   ├── Institucional (R$ 399,00)
│   └── Enterprise (R$ 999,00)
│
├── 📋 Assinaturas
│   ├── Status: trial, ativa, pendente, atrasada, cancelada
│   ├── Controle de limites
│   └── Integração Asaas (pagamentos)
│
└── 👥 Usuários
    ├── SUPER_ADMIN (acessa todas as escolas)
    ├── ADMIN (admin da escola)
    ├── COORDINATOR (coordenador)
    └── TEACHER (professor)
```

## 💰 Plano Profissional (R$ 159,00)

O plano principal inclui:

| Recurso | Limite |
|---------|--------|
| 👥 Alunos | até 100 |
| 👨‍🏫 Professores | até 10 |
| 📝 Provas/mês | 200 |
| 📚 Materiais/mês | 200 |
| ❤️ PEIs/mês | 100 |
| 📊 Relatórios avançados | ✅ |
| 💬 WhatsApp | ✅ |
| 🎓 Treinamento | ✅ |
| ⚡ Suporte prioritário | ✅ |

## 🚀 Como Ativar

### 1. Executar Migration

```bash
# Via MySQL
mysql -u usuario -p banco < migrations/multitenant_migration.sql

# Ou via Python
python -m scripts.seed_planos
```

### 2. Criar Planos (se não existirem)

```bash
cd backend
CRIAR_PLANOS.bat
```

### 3. Endpoints Disponíveis

```
# Públicos
GET  /api/v1/planos/publicos          - Lista planos
GET  /api/v1/planos/publicos/{slug}   - Detalhes do plano

# Autenticados
GET  /api/v1/planos/meu-plano         - Plano atual
GET  /api/v1/planos/minha-assinatura  - Assinatura atual
GET  /api/v1/planos/uso-atual         - Uso vs limites

# Admin (Super Admin)
GET  /api/v1/planos/admin/todos
POST /api/v1/planos/admin/escola
PUT  /api/v1/planos/admin/assinatura/{escola_id}
POST /api/v1/planos/admin/ativar-plano-159/{escola_id}
GET  /api/v1/planos/admin/escolas-assinaturas

# Escolas
GET  /api/v1/escolas/minha
GET  /api/v1/escolas/minha/dashboard
PUT  /api/v1/escolas/minha
GET  /api/v1/escolas/admin/todas
GET  /api/v1/escolas/admin/{escola_id}
```

## 🔐 Middleware de Tenant

O sistema filtra automaticamente os dados por escola:

```python
from app.core.tenant import get_tenant_context, TenantContext

@router.get("/alunos")
def listar_alunos(tenant: TenantContext = Depends(get_tenant_context)):
    # Só retorna alunos da escola do usuário logado
    alunos = db.query(Student).filter(
        Student.escola_id == tenant.escola_id
    ).all()
    return alunos
```

## 📊 Verificação de Limites

```python
from app.core.tenant import check_limite_alunos, check_limite_provas

@router.post("/alunos")
def criar_aluno(
    dados: AlunoCreate,
    tenant: TenantContext = Depends(check_limite_alunos)
):
    # Só executa se ainda tem cota de alunos
    ...

@router.post("/provas")
def criar_prova(
    dados: ProvaCreate,
    tenant: TenantContext = Depends(check_limite_provas)
):
    # Só executa se ainda tem cota de provas no mês
    ...
```

## 🎯 Ativar Plano 159 para uma Escola

```python
# Via API (como Super Admin)
POST /api/v1/planos/admin/ativar-plano-159/{escola_id}

# Resposta:
{
    "message": "Plano Profissional (R$ 159,00) ativado para Escola XYZ",
    "escola_id": 1,
    "plano": "Profissional",
    "valor": 159.00,
    "status": "ativa",
    "funcionalidades": {
        "alunos": "até 100",
        "professores": "até 10",
        "provas_mes": "200",
        "materiais_mes": "200",
        "pei_mes": "100",
        "relatorios_avancados": true,
        "whatsapp": true,
        "suporte_prioritario": true,
        "treinamento": true
    }
}
```

## 📁 Arquivos Criados

```
backend/
├── app/
│   ├── core/
│   │   └── tenant.py          # Middleware multi-tenant
│   ├── models/
│   │   ├── escola.py          # Model Escola
│   │   ├── plano.py           # Model Plano
│   │   └── assinatura.py      # Model Assinatura/Fatura
│   ├── api/routes/
│   │   ├── planos.py          # Rotas de planos
│   │   └── escolas.py         # Rotas de escolas
│   └── schemas/
│       └── multitenant.py     # Schemas Pydantic
├── scripts/
│   └── seed_planos.py         # Seed dos planos
├── migrations/
│   └── multitenant_migration.sql
├── CRIAR_PLANOS.bat
└── MULTITENANT-README.md
```

## ✅ Comparativo: Seu Cartório vs AdaptAI

| Feature | Seu Cartório | AdaptAI |
|---------|-------------|---------|
| Multi-tenant | ✅ Empresas | ✅ Escolas |
| Planos | 3 planos | 5 planos |
| Preço principal | Variável | R$ 159,00 |
| Auth | JWT | JWT |
| Roles | 3 níveis | 4 níveis |
| Integração pagamento | Asaas | Asaas |
| Limites por plano | ✅ | ✅ |
| Isolamento de dados | ✅ | ✅ |
| Branding por tenant | ✅ | ✅ |

---

*Gerado por Claude AI - Replicação Multi-tenant Seu Cartório → AdaptAI*
*29 de Dezembro de 2025*
