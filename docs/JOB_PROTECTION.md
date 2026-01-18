# 🛡️ Sistema de Proteção de Jobs - AdaptAI

## Resumo das Proteções Implementadas

Este documento descreve as proteções implementadas para garantir robustez no processamento de jobs de planejamento BNCC.

---

## 1. 🔄 Checkpoints Incrementais (Railway crash/OOM)

**Problema:** Railway pode matar o processo (deploy, OOM, crash) deixando dados parciais.

**Solução:**
- Salvamento incremental após cada componente processado
- Compressão automática de dados grandes (>500KB)
- Recuperação automática de jobs incompletos

**Arquivos:**
- `app/services/job_protection_service.py` - `CheckpointManager`
- `app/services/planejamento_bncc_completo_service.py` - `_salvar_resultado_parcial()`

**Como funciona:**
```python
# A cada componente processado:
await salvar_checkpoint(job_id, "componente_X", dados_parciais)

# Na próxima execução, verifica se há checkpoint:
job = obter_job_para_retomar(student_id, ano_letivo)
if job:
    # Continua de onde parou
```

---

## 2. 🔒 Lock Anti-Duplicação (Jobs simultâneos)

**Problema:** 2 jobs podem iniciar para o mesmo aluno, duplicando dados.

**Solução:**
- Verificação de job ativo antes de criar novo
- Lock com timeout automático (10 minutos)
- Liberação automática de locks "travados"

**Arquivos:**
- `app/services/job_protection_service.py` - `JobLockManager`
- `app/services/planejamento_bncc_completo_service.py` - `verificar_job_em_andamento()`

**Como funciona:**
```python
# Antes de criar novo job:
job_ativo = verificar_job_em_andamento(student_id, ano_letivo)
if job_ativo:
    raise Exception("Já existe job em processamento")
```

---

## 3. 💓 Heartbeat + Cleanup (Jobs travados)

**Problema:** Job pode ficar "preso" em PROCESSING se cair sem atualizar status.

**Solução:**
- Heartbeat atualizado a cada lote processado
- Cleanup automático no startup da aplicação
- Jobs sem heartbeat há 5+ minutos são marcados como FAILED

**Arquivos:**
- `app/models/planejamento_job.py` - Colunas `last_heartbeat`, `heartbeat_count`
- `app/main.py` - Cleanup no `startup_event()`
- `app/services/job_protection_service.py` - `HeartbeatManager`, `cleanup_stuck_jobs()`

**Como funciona:**
```python
# Durante processamento de cada lote:
job.last_heartbeat = datetime.utcnow()
job.heartbeat_count += 1

# No startup da aplicação:
UPDATE planejamento_jobs 
SET status = 'failed'
WHERE status = 'processing'
AND last_heartbeat < NOW() - INTERVAL 5 MINUTE
```

---

## 4. ⏳ Retry Inteligente para Rate Limits (429)

**Problema:** Anthropic pode retornar rate limit (429) sem retry adequado.

**Solução:**
- Detecção específica de erro 429
- Backoff exponencial (4s, 16s, 64s)
- Logging detalhado de rate limits

**Arquivos:**
- `app/services/planejamento_bncc_completo_service.py` - `_processar_lote_com_retry()`
- `app/services/job_protection_service.py` - `retry_com_backoff()`

**Como funciona:**
```python
# Detecção de rate limit:
if "rate" in erro or "429" in erro:
    wait_time = 4 ** tentativa  # 4s, 16s, 64s
    await asyncio.sleep(wait_time)
    continue  # Tenta novamente
```

---

## 5. 📦 Compressão de Dados Grandes (JSON >500KB)

**Problema:** JSON muito grande pode causar problemas no banco com 500+ objetivos.

**Solução:**
- Compressão GZIP automática para dados >500KB
- Checksum MD5 para verificar integridade
- Descompressão transparente ao ler

**Arquivos:**
- `app/services/planejamento_bncc_completo_service.py` - `_comprimir_se_necessario()`, `_descomprimir_se_necessario()`
- `app/services/job_protection_service.py` - `DataCompressor`

**Como funciona:**
```python
# Ao salvar:
if len(json_str) > 500_000:
    comprimido = gzip.compress(json_str)
    dados = {"__compressed__": True, "__data__": comprimido.hex()}

# Ao ler:
if dados.get("__compressed__"):
    json_str = gzip.decompress(bytes.fromhex(dados["__data__"]))
```

---

## Colunas Adicionadas ao Banco

Execute a migration para adicionar as novas colunas:

```bash
python -m app.scripts.migrate_job_protection
```

**Colunas:**
- `last_heartbeat` - Última vez que o job sinalizou que está vivo
- `heartbeat_count` - Contador de heartbeats
- `lock_token` - Token único para controle de concorrência
- `lock_expires_at` - Expiração do lock

---

## Fluxo Completo de Proteção

```
1. Usuário inicia planejamento
   ↓
2. Verifica se já existe job ativo (LOCK)
   ↓
3. Cria job com status PENDING
   ↓
4. Inicia processamento (status = PROCESSING)
   ↓
5. Para cada componente:
   - Atualiza heartbeat
   - Processa lotes com retry
   - Salva checkpoint parcial (comprimido se grande)
   ↓
6. Finaliza job (status = COMPLETED)
   ↓
7. Se crash durante 5: 
   - Startup detecta job travado
   - Marca como FAILED
   - Próxima execução retoma do checkpoint
```

---

## Logs de Proteção

O sistema gera logs detalhados para cada proteção:

```
[💓 HEARTBEAT] Job 123
[⏳ RATE LIMIT] Lote 2 de Matemática - Aguardando 16s...
[📦 COMPRESS] 750,000 bytes → 125,000 bytes (83.3% redução)
[🔄 RECOVERY] Encontrado job recuperável: 123
[🧹 CLEANUP] 3 jobs travados marcados como FAILED
```

---

## Tabela de Riscos vs Proteções

| Risco | Nível | Proteção | Status |
|-------|-------|----------|--------|
| Railway crash/OOM | MÉDIO | Checkpoints | ✅ |
| Jobs duplicados | MÉDIO | Lock | ✅ |
| Job travado | MÉDIO | Heartbeat + Cleanup | ✅ |
| Rate limit 429 | BAIXO | Retry inteligente | ✅ |
| JSON muito grande | BAIXO | Compressão GZIP | ✅ |

---

## Arquivos Modificados

1. `app/models/planejamento_job.py` - Novas colunas
2. `app/services/job_protection_service.py` - **NOVO** - Serviço completo de proteção
3. `app/services/planejamento_bncc_completo_service.py` - Integração das proteções
4. `app/main.py` - Cleanup no startup
5. `app/scripts/migrate_job_protection.py` - **NOVO** - Migration para novas colunas
