# 🛡️ Proteções Implementadas - Jobs de Planejamento BNCC

## Resumo das 3 Correções de Prioridade Alta

---

## 1️⃣ JSON Malformado - Validação Robusta

**Problema:** IA pode retornar JSON inválido, falhando todas as tentativas.

**Solução:** Sistema de 5 estratégias de recuperação:

```python
def _validar_e_extrair_json(response_text, habilidades):
    # Estratégia 1: Parse direto
    # Estratégia 2: Regex para encontrar {"objetivos": [...]}
    # Estratégia 3: Extrair array diretamente
    # Estratégia 4: Consertar JSON malformado (vírgulas, aspas)
    # Estratégia 5: Gerar objetivos fallback marcados com _fallback: True
```

**Métodos adicionados:**
- `_validar_e_extrair_json()` - Orquestrador das estratégias
- `_validar_estrutura_objetivos()` - Valida estrutura mínima
- `_consertar_json()` - Corrige problemas comuns
- `_gerar_objetivos_fallback()` - Fallback com dados mínimos

**Logs gerados:**
```
[⚠️ JSON] Parse falhou: Expecting ',' delimiter
[✅ JSON] Recuperado via regex (padrão 1)
[🔄 FALLBACK] Gerando objetivos mínimos para 12 habilidades
```

---

## 2️⃣ Race Condition - Lock Atômico no Banco

**Problema:** Duas requisições simultâneas podem criar jobs duplicados.

**Solução:** `SELECT FOR UPDATE NOWAIT` para lock exclusivo:

```python
def verificar_job_em_andamento(student_id, ano_letivo):
    result = db.execute(text("""
        SELECT id, task_id, status, updated_at, last_heartbeat
        FROM planejamento_jobs
        WHERE student_id = :student_id 
        AND ano_letivo = :ano_letivo
        AND status = 'processing'
        FOR UPDATE NOWAIT
    """))
    
    # Se outro processo já tem o lock, NOWAIT retorna erro imediato
    # Retornamos um "fake job" para bloquear criação
```

**Comportamento:**
- Requisição 1: Adquire lock, cria job
- Requisição 2: Recebe erro NOWAIT, retorna "job já em processamento"

**Logs gerados:**
```
[🔓 LOCK] Lock adquirido para student_id=123
[🔒 LOCK] Outro processo já está verificando este aluno
[🔓 LOCK] Job 456 travado, liberado para nova execução
```

---

## 3️⃣ Checkpoint por Lote - Recuperação Granular

**Problema:** Se crashar no lote 5/8, perde os 4 lotes já processados.

**Solução:** Checkpoint salvo após cada lote:

```python
# Estrutura salva em resultados_parciais:
{
    "Matemática": {
        "objetivos": [...],  # Todos acumulados até agora
        "lotes_processados": [1, 2, 3, 4],  # Quais lotes já foram
        "ultimo_lote": 4,
        "em_andamento": True
    }
}

# Na retomada:
lotes_ja_processados, objetivos_recuperados = _obter_lotes_ja_processados(job, componente)

for lote_numero in range(1, total_lotes + 1):
    if lote_numero in lotes_ja_processados:
        print(f"[⏭️ SKIP] Lote {lote_numero} já processado")
        continue
    
    # Processar lote...
    _salvar_checkpoint_lote(job, componente, lote_numero, objetivos_lote, todos_objetivos)
```

**Logs gerados:**
```
[💾 CHECKPOINT] Matemática lote 3: 36 objetivos salvos
[🔄 RECOVERY] Matemática: recuperados lotes [1, 2, 3] com 36 objetivos
[⏭️ SKIP] Matemática lote 1/8 já processado
[⏭️ SKIP] Matemática lote 2/8 já processado
[⏭️ SKIP] Matemática lote 3/8 já processado
```

---

## 📊 Tabela de Riscos Atualizada

| Risco | Nível | Proteção | Status |
|-------|-------|----------|--------|
| Railway crash/OOM | MÉDIO | Checkpoints por lote | ✅ |
| Jobs duplicados | MÉDIO | Lock atômico (FOR UPDATE NOWAIT) | ✅ |
| Job travado | MÉDIO | Heartbeat + Cleanup | ✅ |
| JSON malformado | MÉDIO | Validação robusta + fallback | ✅ |
| Rate limit 429 | BAIXO | Retry com backoff exponencial | ✅ |
| JSON muito grande | BAIXO | Compressão GZIP | ✅ |

---

## 🔄 Fluxo Completo com Todas as Proteções

```
1. [LOCK] Verificar job ativo com FOR UPDATE NOWAIT
   ├── Se lock bloqueado → Exception "job já existe"
   └── Se lock ok → Continuar

2. [JOB] Criar ou retomar job existente
   ├── Se existe job FAILED → Retomar do checkpoint
   └── Se novo → Criar job PENDING

3. [PROCESSING] Para cada componente:
   │
   ├── [RECOVERY] Verificar lotes já processados
   │   └── Carregar objetivos acumulados do checkpoint
   │
   └── Para cada lote:
       │
       ├── [SKIP] Se lote já processado → Pular
       │
       ├── [HEARTBEAT] Atualizar last_heartbeat
       │
       ├── [API CALL] Chamar Claude API
       │   ├── Se rate limit → Backoff exponencial (4s, 16s, 64s)
       │   └── Se erro → Retry até 3x
       │
       ├── [JSON] Validar resposta
       │   ├── Estratégia 1-4 → Tentar recuperar
       │   └── Estratégia 5 → Fallback com dados mínimos
       │
       └── [CHECKPOINT] Salvar após sucesso
           └── Registrar lote + objetivos acumulados

4. [COMPLETED] Finalizar job
   └── Comprimir se > 500KB

5. [CLEANUP] Startup marca jobs travados como FAILED
   └── Jobs sem heartbeat há 5+ min → FAILED
```

---

## 🚀 Deploy

Não são necessárias migrações adicionais. As alterações são apenas no código Python.

```bash
git add -A
git commit -m "feat: proteções de alta prioridade - JSON, Lock, Checkpoint"
git push origin main
```
