# 📅 CALENDÁRIO DE ATIVIDADES PEI - DOCUMENTAÇÃO

## 🎯 VISÃO GERAL

O sistema de Calendário de Atividades integra automaticamente o planejamento BNCC/PEI com a geração de materiais, exercícios e provas, distribuindo tudo em um calendário organizado por datas.

## 🔄 FLUXO COMPLETO

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  1. GERAR PLANEJAMENTO BNCC                                                 │
│     └── IA analisa perfil do aluno + BNCC                                   │
│         └── Gera 8-12 objetivos adaptados                                   │
│                                                                             │
│  2. SALVAR COMO PEI                                                         │
│     └── Objetivos são salvos no banco de dados                              │
│                                                                             │
│  3. GERAR CALENDÁRIO (NOVO!)                                                │
│     └── Para CADA objetivo do PEI:                                          │
│         ├── Gera 2 materiais de estudo (introdução + aprofundamento)        │
│         ├── Gera 2 sessões de exercícios                                    │
│         ├── Gera 1 revisão                                                  │
│         └── Gera 1 prova de avaliação                                       │
│         └── Distribui tudo no calendário com datas                          │
│                                                                             │
│  4. ACOMPANHAMENTO                                                          │
│     └── Aluno e professor veem o calendário                                 │
│     └── Marcam atividades como concluídas                                   │
│     └── Sistema identifica atrasadas                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📁 ARQUIVOS CRIADOS

### Backend
- `app/models/atividade_pei.py` - Modelos AtividadePEI e SequenciaObjetivo
- `app/services/calendario_atividades_service.py` - Serviço de geração
- `app/api/routes/calendario_atividades.py` - Endpoints da API
- `criar_tabelas_calendario.py` - Script de criação das tabelas
- `CONFIGURAR_CALENDARIO.bat` - Script de configuração

### Frontend
- `src/pages/CalendarioAtividades.jsx` - Página do calendário
- Atualização em `src/pages/PlanejamentoBNCC.jsx` - Botão de gerar calendário
- Atualização em `src/App.jsx` - Novas rotas

## 🗄️ TABELAS DO BANCO DE DADOS

### atividades_pei
```sql
- id (PK)
- pei_id (FK -> peis)
- objetivo_id (FK -> pei_objetivos)
- student_id (FK -> students)
- material_id (FK -> materiais) - opcional
- prova_id (FK -> provas) - opcional
- tipo: material | exercicio | prova | revisao | pratica
- titulo
- descricao
- data_programada
- status: pendente | em_andamento | concluida | atrasada | cancelada
- duracao_estimada_min
- instrucoes
- adaptacoes (JSON)
```

### sequencias_objetivo
```sql
- id (PK)
- objetivo_id (FK -> pei_objetivos)
- total_semanas
- total_materiais
- total_exercicios
- incluir_prova
- plano_sequencial (JSON)
- gerado (boolean)
- data_geracao
```

## 🔌 ENDPOINTS DA API

### Geração
- `POST /api/v1/calendario/gerar` - Gera calendário completo para um PEI
- `POST /api/v1/calendario/regenerar/{pei_id}` - Regenera calendário

### Consultas
- `GET /api/v1/calendario/aluno/{student_id}` - Lista todas atividades
- `GET /api/v1/calendario/aluno/{student_id}/semana` - Atividades da semana
- `GET /api/v1/calendario/aluno/{student_id}/hoje` - Atividades de hoje
- `GET /api/v1/calendario/aluno/{student_id}/proximas` - Próximas atividades
- `GET /api/v1/calendario/aluno/{student_id}/atrasadas` - Atrasadas
- `GET /api/v1/calendario/aluno/{student_id}/mensal/{ano}/{mes}` - Calendário mensal
- `GET /api/v1/calendario/pei/{pei_id}` - Atividades por PEI

### Gerenciamento
- `GET /api/v1/calendario/atividade/{id}` - Detalhes da atividade
- `PUT /api/v1/calendario/atividade/{id}/status` - Atualizar status
- `PUT /api/v1/calendario/atividade/{id}/reagendar` - Reagendar
- `DELETE /api/v1/calendario/atividade/{id}` - Excluir

## 🚀 COMO USAR

### 1. Configurar o sistema
```bash
cd backend
CONFIGURAR_CALENDARIO.bat
```

### 2. Reiniciar o backend
```bash
python -m uvicorn app.main:app --reload
```

### 3. Acessar no navegador
1. Vá para a página de um aluno
2. Clique em "Planejamento BNCC"
3. Selecione as matérias e gere o planejamento
4. Salve como PEI
5. Clique em "Gerar Calendário Completo"
6. Acesse o calendário em `/calendario/{studentId}`

## 📊 O QUE É GERADO AUTOMATICAMENTE

Para cada objetivo do PEI (exemplo: objetivo de 4 semanas):

| Semana | Atividade | Tipo |
|--------|-----------|------|
| 1 | Material de Introdução | 📚 material |
| 1 | Exercícios Iniciais | 📝 exercicio |
| 2 | Material de Aprofundamento | 📚 material |
| 2 | Exercícios Avançados | 📝 exercicio |
| 3-4 | Revisão | 🔄 revisao |
| 4 | Prova de Avaliação | ✅ prova |

## 🎨 INTERFACE DO USUÁRIO

### Calendário Mensal
- Visualização por mês
- Cores diferentes por tipo de atividade
- Estatísticas (total, concluídas, pendentes, atrasadas)

### Painel Lateral
- Atividades de hoje
- Próximas atividades
- Atividades atrasadas (destaque em vermelho)

### Modal de Atividade
- Detalhes completos
- Botões: Iniciar, Concluir, Ver Material, Fazer Prova
- Instruções adaptadas

## 🔄 STATUS DAS ATIVIDADES

```
pendente → em_andamento → concluida
    │
    └──────────────────→ atrasada (se passou da data)
```

## 📱 ROTAS DO FRONTEND

- `/calendario/{studentId}` - Calendário do aluno
- `/students/{studentId}/calendario` - Mesma página

## ⚙️ CONFIGURAÇÃO

### Variáveis de ambiente necessárias
- `ANTHROPIC_API_KEY` - Para geração de materiais e provas com IA

### Dependências
- Todas as dependências existentes do AdaptAI
- Nenhuma nova dependência necessária

## 📝 NOTAS IMPORTANTES

1. **Geração com IA**: Cada material e prova é gerado individualmente pela IA Claude, adaptado ao perfil do aluno.

2. **Tempo de geração**: A geração do calendário completo pode levar alguns minutos, pois cada material e prova são criados separadamente.

3. **Materiais e Provas**: São criados como registros normais nas tabelas `materiais` e `provas`, podendo ser acessados pelas rotas existentes.

4. **Flexibilidade**: O professor pode reagendar atividades, excluir ou adicionar novas manualmente.

5. **Integração**: O calendário está totalmente integrado com o sistema de materiais e provas existente.
