# ============================================
# SERVICE - Proteção de Jobs
# ============================================
# Sistema robusto de proteção contra:
# - Crash/OOM do Railway
# - Jobs duplicados para mesmo aluno
# - Jobs travados (sem resposta)
# - Rate limits da Anthropic
# - JSON muito grande no banco

import asyncio
import uuid
import gzip
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable, TypeVar
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_
from sqlalchemy.exc import IntegrityError

from app.database import get_db_async
from app.models.planejamento_job import PlanejamentoJob, PlanejamentoJobLog, JobStatus

# ============================================
# 1. CONSTANTES DE CONFIGURAÇÃO
# ============================================

HEARTBEAT_INTERVAL_SECONDS = 30  # Intervalo entre heartbeats
JOB_TIMEOUT_MINUTES = 5  # Timeout para considerar job travado
MAX_RETRY_ATTEMPTS = 3  # Máximo de tentativas
LOCK_DURATION_MINUTES = 10  # Duração do lock por aluno
MAX_JSON_SIZE_BYTES = 500_000  # 500KB - acima disso comprime
RATE_LIMIT_BASE_WAIT = 2  # Base para backoff exponencial (segundos)


# ============================================
# 2. SISTEMA DE CHECKPOINTS
# ============================================

class CheckpointManager:
    """
    Gerencia checkpoints para permitir recovery após crash.
    Salva estado parcial no banco de dados.
    """
    
    @staticmethod
    async def salvar_checkpoint(
        db: AsyncSession,
        job_id: int,
        etapa: str,
        dados_parciais: Dict[str, Any],
        progress: int = None,
        message: str = None
    ):
        """
        Salva checkpoint com dados parciais processados.
        Permite retomar de onde parou em caso de crash.
        """
        # Comprimir se muito grande
        dados_para_salvar = CheckpointManager._comprimir_se_necessario(dados_parciais)
        
        await db.execute(
            update(PlanejamentoJob)
            .where(PlanejamentoJob.id == job_id)
            .values(
                resultados_parciais=dados_para_salvar,
                componente_atual=etapa,
                updated_at=datetime.utcnow(),
                last_heartbeat=datetime.utcnow(),
                heartbeat_count=PlanejamentoJob.heartbeat_count + 1,
                progress=progress if progress is not None else PlanejamentoJob.progress,
                message=message if message else PlanejamentoJob.message
            )
        )
        await db.commit()
        
        # Log do checkpoint
        log_entry = PlanejamentoJobLog(
            job_id=job_id,
            evento="checkpoint",
            componente=etapa,
            mensagem=f"Checkpoint salvo: {etapa}",
            dados={"progress": progress, "dados_size": len(json.dumps(dados_parciais))}
        )
        db.add(log_entry)
        await db.commit()
        
        print(f"✅ [CHECKPOINT] Job {job_id} - Etapa: {etapa} - Progress: {progress}%")
    
    @staticmethod
    async def recuperar_checkpoint(
        db: AsyncSession,
        student_id: int,
        ano_letivo: str
    ) -> Optional[PlanejamentoJob]:
        """
        Recupera job incompleto para retomar processamento.
        Retorna None se não houver job recuperável.
        """
        result = await db.execute(
            select(PlanejamentoJob)
            .where(
                and_(
                    PlanejamentoJob.student_id == student_id,
                    PlanejamentoJob.ano_letivo == ano_letivo,
                    PlanejamentoJob.status.in_([
                        JobStatus.PROCESSING.value,
                        JobStatus.PAUSED.value
                    ])
                )
            )
            .order_by(PlanejamentoJob.created_at.desc())
        )
        job = result.scalars().first()
        
        if job:
            # Verificar se tem dados parciais
            if job.resultados_parciais:
                print(f"🔄 [RECOVERY] Encontrado job recuperável: {job.id}")
                return job
        
        return None
    
    @staticmethod
    def _comprimir_se_necessario(dados: Dict[str, Any]) -> Dict[str, Any]:
        """Comprime dados se ultrapassar limite de tamanho."""
        json_str = json.dumps(dados, ensure_ascii=False)
        
        if len(json_str.encode('utf-8')) > MAX_JSON_SIZE_BYTES:
            # Comprimir
            comprimido = gzip.compress(json_str.encode('utf-8'))
            return {
                "_compressed": True,
                "_data": comprimido.hex(),  # Hex para armazenar como string
                "_original_size": len(json_str)
            }
        
        return dados
    
    @staticmethod
    def descomprimir_se_necessario(dados: Dict[str, Any]) -> Dict[str, Any]:
        """Descomprime dados se estiverem comprimidos."""
        if dados and dados.get("_compressed"):
            comprimido = bytes.fromhex(dados["_data"])
            json_str = gzip.decompress(comprimido).decode('utf-8')
            return json.loads(json_str)
        return dados


# ============================================
# 3. SISTEMA DE LOCK (Anti-duplicação)
# ============================================

class JobLockManager:
    """
    Gerencia locks para evitar jobs duplicados para mesmo aluno.
    Usa lock otimista com token único.
    """
    
    @staticmethod
    async def adquirir_lock(
        db: AsyncSession,
        student_id: int,
        ano_letivo: str,
        user_id: int
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Tenta adquirir lock para processar job de um aluno.
        
        Returns:
            (sucesso, lock_token, mensagem_erro)
        """
        # Verificar se já existe job em andamento
        result = await db.execute(
            select(PlanejamentoJob)
            .where(
                and_(
                    PlanejamentoJob.student_id == student_id,
                    PlanejamentoJob.ano_letivo == ano_letivo,
                    PlanejamentoJob.status == JobStatus.PROCESSING.value,
                    # Lock ainda válido
                    or_(
                        PlanejamentoJob.lock_expires_at == None,
                        PlanejamentoJob.lock_expires_at > datetime.utcnow()
                    )
                )
            )
        )
        job_existente = result.scalars().first()
        
        if job_existente:
            # Verificar se está travado (sem heartbeat recente)
            if job_existente.last_heartbeat:
                tempo_sem_heartbeat = datetime.utcnow() - job_existente.last_heartbeat
                if tempo_sem_heartbeat > timedelta(minutes=JOB_TIMEOUT_MINUTES):
                    # Job travado - pode roubar o lock
                    print(f"⚠️ [LOCK] Job {job_existente.id} travado há {tempo_sem_heartbeat}. Liberando lock.")
                    await JobLockManager.liberar_lock(db, job_existente.id, forcar=True)
                else:
                    return (
                        False, 
                        None, 
                        f"Já existe job em processamento (ID: {job_existente.id}). Aguarde conclusão."
                    )
        
        # Criar novo lock
        lock_token = str(uuid.uuid4())
        return (True, lock_token, None)
    
    @staticmethod
    async def liberar_lock(
        db: AsyncSession,
        job_id: int,
        forcar: bool = False
    ):
        """Libera o lock de um job."""
        valores = {
            "lock_token": None,
            "lock_expires_at": None
        }
        
        if forcar:
            valores["status"] = JobStatus.FAILED.value
            valores["ultimo_erro"] = "Job travado - timeout de heartbeat"
            valores["completed_at"] = datetime.utcnow()
        
        await db.execute(
            update(PlanejamentoJob)
            .where(PlanejamentoJob.id == job_id)
            .values(**valores)
        )
        await db.commit()
    
    @staticmethod
    async def renovar_lock(db: AsyncSession, job_id: int, lock_token: str) -> bool:
        """Renova o lock durante processamento longo."""
        result = await db.execute(
            update(PlanejamentoJob)
            .where(
                and_(
                    PlanejamentoJob.id == job_id,
                    PlanejamentoJob.lock_token == lock_token
                )
            )
            .values(
                lock_expires_at=datetime.utcnow() + timedelta(minutes=LOCK_DURATION_MINUTES),
                last_heartbeat=datetime.utcnow()
            )
        )
        await db.commit()
        return result.rowcount > 0


# ============================================
# 4. SISTEMA DE HEARTBEAT
# ============================================

class HeartbeatManager:
    """
    Gerencia heartbeats para detectar jobs travados.
    """
    
    @staticmethod
    async def enviar_heartbeat(db: AsyncSession, job_id: int, lock_token: str = None):
        """Atualiza heartbeat para indicar que job está vivo."""
        await db.execute(
            update(PlanejamentoJob)
            .where(PlanejamentoJob.id == job_id)
            .values(
                last_heartbeat=datetime.utcnow(),
                heartbeat_count=PlanejamentoJob.heartbeat_count + 1
            )
        )
        await db.commit()
    
    @staticmethod
    async def criar_task_heartbeat(
        db_factory: Callable,
        job_id: int,
        lock_token: str,
        intervalo: int = HEARTBEAT_INTERVAL_SECONDS
    ) -> asyncio.Task:
        """
        Cria task assíncrona que envia heartbeats periodicamente.
        Deve ser cancelada quando o job terminar.
        """
        async def _heartbeat_loop():
            while True:
                try:
                    await asyncio.sleep(intervalo)
                    async with db_factory() as db:
                        await HeartbeatManager.enviar_heartbeat(db, job_id, lock_token)
                        print(f"💓 [HEARTBEAT] Job {job_id}")
                except asyncio.CancelledError:
                    print(f"🛑 [HEARTBEAT] Task cancelada para job {job_id}")
                    break
                except Exception as e:
                    print(f"⚠️ [HEARTBEAT] Erro no job {job_id}: {e}")
        
        return asyncio.create_task(_heartbeat_loop())


# ============================================
# 5. CLEANUP DE JOBS TRAVADOS
# ============================================

async def cleanup_stuck_jobs(db: AsyncSession):
    """
    Limpa jobs que ficaram travados (sem heartbeat por muito tempo).
    Deve ser executado periodicamente (ex: cron job ou startup).
    """
    timeout = datetime.utcnow() - timedelta(minutes=JOB_TIMEOUT_MINUTES)
    
    result = await db.execute(
        select(PlanejamentoJob)
        .where(
            and_(
                PlanejamentoJob.status == JobStatus.PROCESSING.value,
                or_(
                    PlanejamentoJob.last_heartbeat < timeout,
                    PlanejamentoJob.last_heartbeat == None
                )
            )
        )
    )
    stuck_jobs = result.scalars().all()
    
    for job in stuck_jobs:
        print(f"🧹 [CLEANUP] Marcando job {job.id} como FAILED (travado)")
        
        job.status = JobStatus.FAILED.value
        job.ultimo_erro = f"Job travado - sem heartbeat desde {job.last_heartbeat}"
        job.completed_at = datetime.utcnow()
        
        # Log
        log_entry = PlanejamentoJobLog(
            job_id=job.id,
            evento="timeout",
            mensagem="Job marcado como FAILED por timeout de heartbeat",
            dados={
                "last_heartbeat": job.last_heartbeat.isoformat() if job.last_heartbeat else None,
                "timeout_minutes": JOB_TIMEOUT_MINUTES
            }
        )
        db.add(log_entry)
    
    await db.commit()
    
    return len(stuck_jobs)


# ============================================
# 6. RETRY INTELIGENTE PARA RATE LIMITS
# ============================================

T = TypeVar('T')

async def retry_com_backoff(
    func: Callable[..., T],
    max_tentativas: int = MAX_RETRY_ATTEMPTS,
    erros_para_retry: tuple = (Exception,),
    *args,
    **kwargs
) -> T:
    """
    Executa função com retry e backoff exponencial.
    Trata especialmente rate limits (429).
    """
    ultima_excecao = None
    
    for tentativa in range(max_tentativas):
        try:
            return await func(*args, **kwargs)
            
        except Exception as e:
            ultima_excecao = e
            erro_str = str(e).lower()
            
            # Rate limit específico (429)
            if "rate" in erro_str or "429" in erro_str or "too many" in erro_str:
                wait_time = RATE_LIMIT_BASE_WAIT ** (tentativa + 2)  # 4s, 8s, 16s
                print(f"⏳ [RATE LIMIT] Tentativa {tentativa + 1}/{max_tentativas}. "
                      f"Aguardando {wait_time}s...")
                await asyncio.sleep(wait_time)
                continue
            
            # Outros erros recuperáveis
            if isinstance(e, erros_para_retry):
                wait_time = RATE_LIMIT_BASE_WAIT ** tentativa  # 1s, 2s, 4s
                print(f"⚠️ [RETRY] Tentativa {tentativa + 1}/{max_tentativas}. "
                      f"Erro: {e}. Aguardando {wait_time}s...")
                await asyncio.sleep(wait_time)
                continue
            
            # Erro não recuperável
            raise
    
    # Esgotou tentativas
    raise ultima_excecao


def com_retry(max_tentativas: int = MAX_RETRY_ATTEMPTS):
    """Decorator para adicionar retry automático a funções async."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await retry_com_backoff(
                func, 
                max_tentativas=max_tentativas,
                *args, 
                **kwargs
            )
        return wrapper
    return decorator


# ============================================
# 7. COMPRESSÃO DE DADOS GRANDES
# ============================================

class DataCompressor:
    """
    Gerencia compressão/descompressão de dados grandes.
    """
    
    @staticmethod
    def comprimir(dados: Any, limite_bytes: int = MAX_JSON_SIZE_BYTES) -> tuple[Any, bool]:
        """
        Comprime dados se ultrapassar limite.
        Returns: (dados_processados, foi_comprimido)
        """
        json_str = json.dumps(dados, ensure_ascii=False)
        tamanho = len(json_str.encode('utf-8'))
        
        if tamanho > limite_bytes:
            comprimido = gzip.compress(json_str.encode('utf-8'))
            resultado = {
                "__compressed__": True,
                "__algorithm__": "gzip",
                "__original_size__": tamanho,
                "__compressed_size__": len(comprimido),
                "__data__": comprimido.hex(),
                "__checksum__": hashlib.md5(json_str.encode()).hexdigest()
            }
            print(f"📦 [COMPRESS] {tamanho:,} bytes → {len(comprimido):,} bytes "
                  f"({100 - (len(comprimido)/tamanho*100):.1f}% redução)")
            return resultado, True
        
        return dados, False
    
    @staticmethod
    def descomprimir(dados: Any) -> Any:
        """Descomprime dados se estiverem comprimidos."""
        if isinstance(dados, dict) and dados.get("__compressed__"):
            try:
                comprimido = bytes.fromhex(dados["__data__"])
                json_str = gzip.decompress(comprimido).decode('utf-8')
                
                # Verificar checksum
                if dados.get("__checksum__"):
                    checksum_atual = hashlib.md5(json_str.encode()).hexdigest()
                    if checksum_atual != dados["__checksum__"]:
                        raise ValueError("Checksum inválido - dados corrompidos")
                
                return json.loads(json_str)
            except Exception as e:
                print(f"❌ [DECOMPRESS] Erro: {e}")
                raise
        
        return dados
    
    @staticmethod
    def estimar_tamanho(dados: Any) -> int:
        """Estima tamanho dos dados em bytes."""
        return len(json.dumps(dados, ensure_ascii=False).encode('utf-8'))


# ============================================
# 8. EXECUTOR DE JOB PROTEGIDO
# ============================================

class ProtectedJobExecutor:
    """
    Executor que combina todas as proteções:
    - Lock anti-duplicação
    - Heartbeat automático
    - Checkpoints incrementais
    - Retry com backoff
    - Compressão automática
    """
    
    def __init__(
        self,
        db_factory: Callable,
        job_id: int,
        student_id: int,
        ano_letivo: str,
        user_id: int
    ):
        self.db_factory = db_factory
        self.job_id = job_id
        self.student_id = student_id
        self.ano_letivo = ano_letivo
        self.user_id = user_id
        self.lock_token = None
        self.heartbeat_task = None
        self.checkpoint_data = {}
    
    async def __aenter__(self):
        """Adquire lock e inicia heartbeat."""
        async with self.db_factory() as db:
            # Adquirir lock
            sucesso, self.lock_token, erro = await JobLockManager.adquirir_lock(
                db, self.student_id, self.ano_letivo, self.user_id
            )
            
            if not sucesso:
                raise Exception(erro)
            
            # Atualizar job com lock
            await db.execute(
                update(PlanejamentoJob)
                .where(PlanejamentoJob.id == self.job_id)
                .values(
                    lock_token=self.lock_token,
                    lock_expires_at=datetime.utcnow() + timedelta(minutes=LOCK_DURATION_MINUTES),
                    status=JobStatus.PROCESSING.value,
                    started_at=datetime.utcnow(),
                    last_heartbeat=datetime.utcnow()
                )
            )
            await db.commit()
        
        # Iniciar heartbeat
        self.heartbeat_task = await HeartbeatManager.criar_task_heartbeat(
            self.db_factory, self.job_id, self.lock_token
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Libera recursos e lock."""
        # Parar heartbeat
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
        
        # Liberar lock
        async with self.db_factory() as db:
            await JobLockManager.liberar_lock(db, self.job_id)
    
    async def salvar_checkpoint(
        self,
        etapa: str,
        dados: Dict[str, Any],
        progress: int = None,
        message: str = None
    ):
        """Salva checkpoint com dados parciais."""
        # Mesclar com dados anteriores
        self.checkpoint_data.update(dados)
        
        async with self.db_factory() as db:
            await CheckpointManager.salvar_checkpoint(
                db,
                self.job_id,
                etapa,
                self.checkpoint_data,
                progress,
                message
            )
    
    async def executar_com_retry(
        self,
        func: Callable,
        *args,
        max_tentativas: int = MAX_RETRY_ATTEMPTS,
        **kwargs
    ):
        """Executa função com retry e backoff."""
        return await retry_com_backoff(
            func,
            max_tentativas=max_tentativas,
            *args,
            **kwargs
        )


# ============================================
# 9. FUNÇÕES UTILITÁRIAS
# ============================================

async def criar_job_protegido(
    db: AsyncSession,
    task_id: str,
    student_id: int,
    user_id: int,
    ano_letivo: str,
    componentes: list
) -> PlanejamentoJob:
    """Cria um novo job com todas as proteções habilitadas."""
    
    job = PlanejamentoJob(
        task_id=task_id,
        student_id=student_id,
        user_id=user_id,
        ano_letivo=ano_letivo,
        componentes_solicitados=componentes,
        status=JobStatus.PENDING.value,
        progress=0,
        message="Job criado, aguardando início",
        componentes_processados=[],
        resultados_parciais={},
        tentativas=0,
        last_heartbeat=datetime.utcnow(),
        heartbeat_count=0
    )
    
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Log de criação
    log_entry = PlanejamentoJobLog(
        job_id=job.id,
        evento="created",
        mensagem="Job criado",
        dados={
            "student_id": student_id,
            "componentes": componentes,
            "ano_letivo": ano_letivo
        }
    )
    db.add(log_entry)
    await db.commit()
    
    return job


async def finalizar_job(
    db: AsyncSession,
    job_id: int,
    sucesso: bool,
    resultado: Any = None,
    erro: str = None,
    pei_id: int = None
):
    """Finaliza um job (sucesso ou falha)."""
    
    # Comprimir resultado se necessário
    resultado_para_salvar = None
    if resultado:
        resultado_para_salvar, _ = DataCompressor.comprimir(resultado)
    
    valores = {
        "status": JobStatus.COMPLETED.value if sucesso else JobStatus.FAILED.value,
        "progress": 100 if sucesso else None,
        "message": "Concluído com sucesso!" if sucesso else "Falhou",
        "completed_at": datetime.utcnow(),
        "lock_token": None,
        "lock_expires_at": None
    }
    
    if resultado_para_salvar:
        valores["resultado_final"] = resultado_para_salvar
    if erro:
        valores["ultimo_erro"] = erro
    if pei_id:
        valores["pei_id"] = pei_id
    
    await db.execute(
        update(PlanejamentoJob)
        .where(PlanejamentoJob.id == job_id)
        .values(**valores)
    )
    
    # Log de finalização
    log_entry = PlanejamentoJobLog(
        job_id=job_id,
        evento="completed" if sucesso else "failed",
        mensagem="Job finalizado" if sucesso else f"Job falhou: {erro}",
        dados={"pei_id": pei_id} if pei_id else None
    )
    db.add(log_entry)
    await db.commit()


# ============================================
# 10. EXEMPLO DE USO
# ============================================
"""
# Exemplo de como usar o executor protegido:

async def processar_planejamento(db_factory, job_id, student_id, ano_letivo, user_id, componentes):
    async with ProtectedJobExecutor(
        db_factory=db_factory,
        job_id=job_id,
        student_id=student_id,
        ano_letivo=ano_letivo,
        user_id=user_id
    ) as executor:
        
        resultados = {}
        
        for i, componente in enumerate(componentes):
            progress = int((i / len(componentes)) * 100)
            
            # Salvar checkpoint antes de processar
            await executor.salvar_checkpoint(
                etapa=f"processando_{componente}",
                dados=resultados,
                progress=progress,
                message=f"Processando {componente}..."
            )
            
            # Executar com retry automático
            resultado = await executor.executar_com_retry(
                gerar_objetivos_ia,
                componente=componente,
                student_id=student_id
            )
            
            resultados[componente] = resultado
        
        return resultados
"""
