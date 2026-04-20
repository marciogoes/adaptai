# ============================================
# SERVICE - Planejamento Curricular BNCC COMPLETO
# ============================================
# Versão ROBUSTA com:
# - Persistência de progresso no banco
# - Keep-alive no MySQL
# - Retry automático em caso de falha

import json
import asyncio
import uuid
import gzip
import hashlib
import re
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.core.config import settings
from app.core.anthropic_client import (
    get_anthropic_client as _get_core_anthropic_client,
    get_default_model,
)
from app.models.student import Student
from app.models.curriculo import CurriculoNacional, MapeamentoPrerequisitos
from app.models.pei import PEI, PEIObjetivo
from app.models.relatorio import Relatorio
from app.models.planejamento_job import PlanejamentoJob, PlanejamentoJobLog, JobStatus

from app.core.logging_config import get_logger

logger = get_logger(__name__)


# Cliente Anthropic: centralizado em app.core.anthropic_client (singleton lazy).
# Antes este arquivo mantinha _client/MODELO_IA proprios, duplicando instancia
# e abrindo TLS handshake extra a cada novo servico. Agora reusa o singleton.

# Configurações de retry e processamento
MAX_RETRIES = 3  # Tentativas por lote
RETRY_DELAY = 2  # Segundos entre tentativas
LOTE_SIZE = 12   # Habilidades por lote (reduzido para maior segurança)
KEEPALIVE_INTERVAL = 30  # Segundos entre pings no MySQL
MAX_JSON_SIZE_BYTES = 500_000  # 500KB - acima disso comprime


def _utcnow() -> datetime:
    """
    Retorna datetime timezone-aware (UTC).

    FIX: substitui datetime.utcnow() (deprecated no Python 3.12+, produz
    naive datetime e causa TypeError ao comparar/subtrair de datetimes
    aware como os setados em main.py::lifespan e em planejamento_job
    model defaults).
    """
    return datetime.now(timezone.utc)


class PlanejamentoBNNCCompletoService:
    """
    Serviço para gerar planejamento curricular COMPLETO
    com proteções contra interrupção.
    """
    
    def __init__(self, db: Session):
        self.db = db
        # Usa cliente Anthropic centralizado. Se nao houver API key configurada,
        # get_anthropic_client() levanta RuntimeError - capturamos para preservar
        # o comportamento anterior (construir a instancia, falhar so no uso).
        try:
            self.client = _get_core_anthropic_client()
        except Exception as e:
            logger.exception(f"[AVISO] Cliente Anthropic indisponivel: {e}")
            self.client = None
    
    # ============================================
    # MÉTODOS DE KEEP-ALIVE E PERSISTÊNCIA
    # ============================================
    
    def _keep_alive(self):
        """Faz ping no MySQL para manter conexão ativa"""
        try:
            self.db.execute(text("SELECT 1"))
            self.db.commit()
        except Exception as e:
            logger.exception(f"[KEEPALIVE] Erro no ping: {e}")
    
    def _comprimir_se_necessario(self, dados: Dict) -> Dict:
        """
        Comprime dados JSON se ultrapassar limite de tamanho.
        Retorna dados originais ou comprimidos com metadados.
        """
        json_str = json.dumps(dados, ensure_ascii=False)
        tamanho = len(json_str.encode('utf-8'))
        
        if tamanho > MAX_JSON_SIZE_BYTES:
            comprimido = gzip.compress(json_str.encode('utf-8'))
            resultado = {
                "__compressed__": True,
                "__algorithm__": "gzip",
                "__original_size__": tamanho,
                "__compressed_size__": len(comprimido),
                "__data__": comprimido.hex(),
                "__checksum__": hashlib.md5(json_str.encode()).hexdigest()
            }
            reducao = 100 - (len(comprimido)/tamanho*100)
            logger.info(f"[📦 COMPRESS] {tamanho:,} bytes → {len(comprimido):,} bytes ({reducao:.1f}% redução)")
            return resultado
        
        return dados
    
    def _descomprimir_se_necessario(self, dados: Dict) -> Dict:
        """
        Descomprime dados se estiverem comprimidos.
        """
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
                logger.exception(f"[❌ DECOMPRESS] Erro: {e}")
                raise
        
        return dados
    
    def _criar_job(
        self,
        task_id: str,
        student_id: int,
        user_id: int,
        ano_letivo: str,
        componentes: List[str]
    ) -> PlanejamentoJob:
        """Cria um novo job de planejamento no banco"""
        job = PlanejamentoJob(
            task_id=task_id,
            student_id=student_id,
            user_id=user_id,
            ano_letivo=ano_letivo,
            status=JobStatus.PENDING.value,
            progress=0,
            message="Job criado, aguardando início",
            componentes_solicitados=componentes,
            componentes_processados=[],
            resultados_parciais={}
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def _atualizar_job(
        self,
        job: PlanejamentoJob,
        status: str = None,
        progress: int = None,
        message: str = None,
        componente_atual: str = None,
        lote_atual: int = None,
        ultimo_erro: str = None
    ):
        """Atualiza o estado do job no banco"""
        if status:
            job.status = status
        if progress is not None:
            job.progress = progress
        if message:
            job.message = message
        if componente_atual is not None:
            job.componente_atual = componente_atual
        if lote_atual is not None:
            job.lote_atual = lote_atual
        if ultimo_erro:
            job.ultimo_erro = ultimo_erro
        
        job.updated_at = _utcnow()
        self.db.commit()
        self._keep_alive()  # Mantém conexão ativa
    
    def _salvar_resultado_parcial(
        self,
        job: PlanejamentoJob,
        componente: str,
        objetivos: List[Dict]
    ):
        """Salva resultado parcial de um componente (com compressão se necessário)"""
        resultados = job.resultados_parciais or {}
        if isinstance(resultados, str):
            resultados = json.loads(resultados)
        
        # Descomprimir se estava comprimido
        resultados = self._descomprimir_se_necessario(resultados)
        
        resultados[componente] = {
            "total_habilidades": len(objetivos),
            "objetivos": objetivos,
            "processado_em": _utcnow().isoformat()
        }
        
        # Comprimir se muito grande
        resultados_para_salvar = self._comprimir_se_necessario(resultados)
        # FIX: dict direto, nao json.dumps (ver comentario em _salvar_checkpoint_lote).
        job.resultados_parciais = resultados_para_salvar
        
        # Atualizar lista de componentes processados
        processados = job.componentes_processados or []
        if componente not in processados:
            processados.append(componente)
        job.componentes_processados = processados
        
        self.db.commit()
        self._keep_alive()
    
    def _salvar_checkpoint_lote(
        self,
        job: PlanejamentoJob,
        componente: str,
        lote_numero: int,
        objetivos_lote: List[Dict],
        objetivos_acumulados: List[Dict]
    ):
        """
        Salva checkpoint GRANULAR após cada lote processado.
        Permite retomar do lote específico em caso de crash.
        """
        try:
            resultados = job.resultados_parciais or {}
            if isinstance(resultados, str):
                resultados = json.loads(resultados)
            
            # Descomprimir se estava comprimido
            resultados = self._descomprimir_se_necessario(resultados)
            
            # Salvar progresso do componente atual (parcial)
            if componente not in resultados:
                resultados[componente] = {
                    "total_habilidades": 0,
                    "objetivos": [],
                    "lotes_processados": [],
                    "em_andamento": True
                }
            
            # Atualizar objetivos acumulados
            resultados[componente]["objetivos"] = objetivos_acumulados
            resultados[componente]["ultimo_lote"] = lote_numero
            
            # Registrar lotes já processados
            lotes_processados = resultados[componente].get("lotes_processados", [])
            if lote_numero not in lotes_processados:
                lotes_processados.append(lote_numero)
            resultados[componente]["lotes_processados"] = lotes_processados
            
            # Comprimir se muito grande
            resultados_para_salvar = self._comprimir_se_necessario(resultados)
            # FIX: passar dict direto. Antes fazia json.dumps() armazenando
            # uma string em uma coluna JSON (dupla serializacao - o MySQL
            # guardava uma string JSON dentro de um campo JSON). A leitura
            # ja trata ambos os formatos defensivamente.
            job.resultados_parciais = resultados_para_salvar
            
            # Atualizar heartbeat e lote atual
            job.lote_atual = lote_numero
            if hasattr(job, 'last_heartbeat'):
                job.last_heartbeat = _utcnow()
            
            self.db.commit()
            self._keep_alive()
            
            logger.info(f"[💾 CHECKPOINT] {componente} lote {lote_numero}: {len(objetivos_acumulados)} objetivos salvos")
            
        except Exception as e:
            logger.exception(f"[⚠️ CHECKPOINT] Erro ao salvar lote {lote_numero}: {e}")
            # Não propagar erro - o lote foi processado, só o checkpoint falhou
    
    def _obter_lotes_ja_processados(self, job: PlanejamentoJob, componente: str) -> tuple[List[int], List[Dict]]:
        """
        Recupera lotes já processados para um componente.
        Retorna (lista_de_lotes_processados, objetivos_acumulados)
        """
        try:
            resultados = job.resultados_parciais or {}
            if isinstance(resultados, str):
                resultados = json.loads(resultados)
            
            # Descomprimir se estava comprimido
            resultados = self._descomprimir_se_necessario(resultados)
            
            if componente in resultados:
                dados_componente = resultados[componente]
                lotes = dados_componente.get("lotes_processados", [])
                objetivos = dados_componente.get("objetivos", [])
                
                if lotes:
                    logger.info(f"[🔄 RECOVERY] {componente}: recuperados lotes {lotes} com {len(objetivos)} objetivos")
                    return lotes, objetivos
            
            return [], []
            
        except Exception as e:
            logger.exception(f"[⚠️ RECOVERY] Erro ao recuperar lotes de {componente}: {e}")
            return [], []
    
    def _registrar_log(
        self,
        job: PlanejamentoJob,
        evento: str,
        componente: str = None,
        lote: int = None,
        mensagem: str = None,
        dados: Dict = None
    ):
        """Registra evento no log do job"""
        log = PlanejamentoJobLog(
            job_id=job.id,
            evento=evento,
            componente=componente,
            lote=lote,
            mensagem=mensagem,
            dados=dados
        )
        self.db.add(log)
        self.db.commit()
    
    def obter_job(self, task_id: str) -> Optional[PlanejamentoJob]:
        """Busca um job pelo task_id"""
        return self.db.query(PlanejamentoJob).filter(
            PlanejamentoJob.task_id == task_id
        ).first()
    
    def obter_job_para_retomar(self, student_id: int, ano_letivo: str) -> Optional[PlanejamentoJob]:
        """Busca um job incompleto que pode ser retomado"""
        return self.db.query(PlanejamentoJob).filter(
            PlanejamentoJob.student_id == student_id,
            PlanejamentoJob.ano_letivo == ano_letivo,
            PlanejamentoJob.status.in_([
                JobStatus.PROCESSING.value,
                JobStatus.PAUSED.value,
                JobStatus.FAILED.value
            ])
        ).order_by(PlanejamentoJob.created_at.desc()).first()
    
    def verificar_job_em_andamento(self, student_id: int, ano_letivo: str) -> Optional[PlanejamentoJob]:
        """
        Verifica se já existe um job em andamento para o aluno.
        Usa SELECT FOR UPDATE para evitar race condition.
        """
        from datetime import timedelta
        limite_travado = _utcnow() - timedelta(minutes=10)
        
        try:
            # LOCK ATÔMICO: SELECT FOR UPDATE impede que outra transação
            # leia/modifique estes registros até o commit
            result = self.db.execute(text("""
                SELECT id, task_id, status, updated_at, last_heartbeat
                FROM planejamento_jobs
                WHERE student_id = :student_id 
                AND ano_letivo = :ano_letivo
                AND status = 'processing'
                FOR UPDATE NOWAIT
            """), {"student_id": student_id, "ano_letivo": ano_letivo})
            
            job_row = result.fetchone()
            
            if job_row:
                job_id, task_id, status, updated_at, last_heartbeat = job_row
                
                # Verificar se está travado (sem atualização por 10+ minutos)
                check_time = last_heartbeat or updated_at
                if check_time and check_time < limite_travado:
                    # Job travado - marcar como failed
                    self.db.execute(text("""
                        UPDATE planejamento_jobs 
                        SET status = 'failed',
                            ultimo_erro = 'Job travado (sem atualização por 10+ minutos)',
                            completed_at = NOW()
                        WHERE id = :job_id
                    """), {"job_id": job_id})
                    self.db.commit()
                    logger.info(f"[🔓 LOCK] Job {job_id} travado, liberado para nova execução")
                    return None  # Permite criar novo
                
                # Job ativo encontrado
                job = self.db.query(PlanejamentoJob).filter(
                    PlanejamentoJob.id == job_id
                ).first()
                return job
            
            # Nenhum job ativo
            return None
            
        except Exception as e:
            erro_str = str(e).lower()
            # Se outro processo já tem o lock (NOWAIT retorna erro)
            if "lock" in erro_str or "timeout" in erro_str or "nowait" in erro_str:
                logger.info(f"[🔒 LOCK] Outro processo já está verificando este aluno")
                # Retornar um job "fake" para bloquear criação
                fake_job = PlanejamentoJob()
                fake_job.id = -1
                fake_job.status = "processing"
                fake_job.message = "Outro processo está iniciando job para este aluno"
                return fake_job
            
            # Outro erro - logar e permitir continuar
            logger.exception(f"[⚠️ LOCK] Erro na verificação: {e}")
            self.db.rollback()
            return None
    
    def adquirir_lock_job(self, student_id: int, ano_letivo: str, task_id: str) -> bool:
        """
        Tenta adquirir lock exclusivo para criar job.
        Retorna True se conseguiu, False se já existe job ativo.
        """
        try:
            # Tentar inserir registro de lock (usar task_id como chave única)
            # Se já existir job ativo, a verificação anterior já bloqueou
            
            # Verificar novamente com lock (double-check locking)
            result = self.db.execute(text("""
                SELECT COUNT(*) FROM planejamento_jobs
                WHERE student_id = :student_id 
                AND ano_letivo = :ano_letivo
                AND status = 'processing'
                FOR UPDATE
            """), {"student_id": student_id, "ano_letivo": ano_letivo})
            
            count = result.scalar()
            
            if count > 0:
                self.db.rollback()
                logger.info(f"[🔒 LOCK] Job já existe após double-check")
                return False
            
            # Lock adquirido com sucesso
            self.db.commit()
            logger.info(f"[🔓 LOCK] Lock adquirido para student_id={student_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.exception(f"[⚠️ LOCK] Erro ao adquirir lock: {e}")
            return False
    
    def limpar_jobs_antigos(self, student_id: int, manter_ultimos: int = 5):
        """
        Remove jobs antigos para não acumular lixo no banco.
        Mantém apenas os últimos N jobs.
        """
        jobs = self.db.query(PlanejamentoJob).filter(
            PlanejamentoJob.student_id == student_id
        ).order_by(PlanejamentoJob.created_at.desc()).all()
        
        if len(jobs) > manter_ultimos:
            for job in jobs[manter_ultimos:]:
                # Só remove se não for PROCESSING
                if job.status != JobStatus.PROCESSING.value:
                    self.db.delete(job)
            self.db.commit()
    
    # ============================================
    # MÉTODOS DE BUSCA DE DADOS
    # ============================================
    
    def listar_componentes_disponiveis(self, ano_escolar: str) -> List[Dict[str, Any]]:
        """Lista componentes disponíveis para um ano escolar"""
        self._keep_alive()
        
        results = self.db.query(
            CurriculoNacional.componente,
            func.count(CurriculoNacional.id).label('total')
        ).filter(
            CurriculoNacional.ano_escolar == ano_escolar
        ).group_by(
            CurriculoNacional.componente
        ).all()
        
        return [{"componente": r[0], "total_habilidades": r[1]} for r in results]
    
    def buscar_todas_habilidades(
        self,
        ano_escolar: str,
        componente: Optional[str] = None
    ) -> List[CurriculoNacional]:
        """Busca todas as habilidades da BNCC"""
        self._keep_alive()
        
        query = self.db.query(CurriculoNacional).filter(
            CurriculoNacional.ano_escolar == ano_escolar
        )
        
        if componente:
            query = query.filter(CurriculoNacional.componente == componente)
        
        return query.order_by(
            CurriculoNacional.componente,
            CurriculoNacional.trimestre_sugerido,
            CurriculoNacional.codigo_bncc
        ).all()
    
    def obter_perfil_aluno(self, student_id: int) -> Dict[str, Any]:
        """Obtém perfil completo do aluno"""
        self._keep_alive()
        
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return {}
        
        relatorios = self.db.query(Relatorio).filter(
            Relatorio.student_id == student_id
        ).order_by(Relatorio.created_at.desc()).all()
        
        diagnosticos = student.diagnosis or {}
        dados_relatorios = []
        adaptacoes_consolidadas = []
        pontos_fortes = []
        dificuldades = []
        
        for rel in relatorios:
            if rel.dados_extraidos:
                dados = rel.dados_extraidos
                dados_relatorios.append({
                    "tipo": rel.tipo,
                    "resumo": dados.get("resumo_clinico", ""),
                })
                
                if "adaptacoes_sugeridas" in dados:
                    for key, value in dados["adaptacoes_sugeridas"].items():
                        if value:
                            adaptacoes_consolidadas.append(value)
                
                if "pontos_fortes" in dados:
                    pontos_fortes.extend(dados["pontos_fortes"])
                if "dificuldades" in dados:
                    dificuldades.extend(dados["dificuldades"])
                
                if "condicoes_identificadas" in dados:
                    condicoes = dados["condicoes_identificadas"]
                    if condicoes.get("tea"):
                        diagnosticos["tea"] = {"nivel": condicoes.get("tea_nivel")}
                    if condicoes.get("tdah"):
                        diagnosticos["tdah"] = True
                    if condicoes.get("dislexia"):
                        diagnosticos["dislexia"] = True
        
        return {
            "id": student.id,
            "nome": student.name,
            "ano_escolar": student.grade_level,
            "turma": student.turma,
            "diagnosticos": diagnosticos,
            "notes": student.notes,
            "adaptacoes_recomendadas": list(set(adaptacoes_consolidadas))[:10],
            "pontos_fortes": list(set(pontos_fortes))[:5],
            "dificuldades": list(set(dificuldades))[:5]
        }
    
    def _criar_perfil_resumido(self, perfil: Dict) -> str:
        """Cria versão resumida do perfil"""
        return f"""
ALUNO: {perfil.get('nome', 'N/A')} - {perfil.get('ano_escolar', 'N/A')}

DIAGNÓSTICOS:
{json.dumps(perfil.get('diagnosticos', {}), ensure_ascii=False)}

ADAPTAÇÕES RECOMENDADAS:
{chr(10).join(['- ' + a for a in perfil.get('adaptacoes_recomendadas', [])[:8]]) or '- Nenhuma específica'}

PONTOS FORTES:
{chr(10).join(['- ' + p for p in perfil.get('pontos_fortes', [])[:5]]) or '- A identificar'}

DIFICULDADES:
{chr(10).join(['- ' + d for d in perfil.get('dificuldades', [])[:5]]) or '- A identificar'}
""".strip()
    
    # ============================================
    # PROCESSAMENTO COM RETRY
    # ============================================
    
    async def _processar_lote_com_retry(
        self,
        job: PlanejamentoJob,
        perfil_resumido: str,
        componente: str,
        habilidades: List[Dict],
        ano_letivo: str,
        lote_numero: int
    ) -> Dict[str, Any]:
        """
        Processa um lote de habilidades COM RETRY automático.
        Tenta até MAX_RETRIES vezes em caso de falha.
        Inclui tratamento específico para rate limits (429).
        """
        ultimo_erro = None
        RATE_LIMIT_BASE_WAIT = 4  # Base para backoff em rate limit
        
        for tentativa in range(1, MAX_RETRIES + 1):
            try:
                self._keep_alive()  # Manter conexão ativa antes de cada tentativa
                
                # Atualizar heartbeat do job
                if hasattr(job, 'last_heartbeat'):
                    job.last_heartbeat = _utcnow()
                    job.heartbeat_count = (job.heartbeat_count or 0) + 1
                    self.db.commit()
                
                self._registrar_log(
                    job, "lote_iniciado", componente, lote_numero,
                    f"Tentativa {tentativa}/{MAX_RETRIES}",
                    {"habilidades": len(habilidades)}
                )
                
                resultado = await self._processar_lote_habilidades(
                    perfil_resumido, componente, habilidades, ano_letivo, lote_numero
                )
                
                if resultado.get("objetivos"):
                    self._registrar_log(
                        job, "lote_sucesso", componente, lote_numero,
                        f"Gerados {len(resultado['objetivos'])} objetivos",
                        {"objetivos_gerados": len(resultado['objetivos'])}
                    )
                    return resultado
                else:
                    raise Exception("Nenhum objetivo gerado")
                    
            except Exception as e:
                ultimo_erro = str(e)
                erro_lower = ultimo_erro.lower()
                
                # Tratamento específico para rate limit (429)
                is_rate_limit = "rate" in erro_lower or "429" in erro_lower or "too many" in erro_lower
                
                if is_rate_limit:
                    wait_time = RATE_LIMIT_BASE_WAIT ** tentativa  # 4s, 16s, 64s
                    logger.warning(
                        "rate limit: lote %s de %s - tentativa %s/%s aguardando %ss",
                        lote_numero, componente, tentativa, MAX_RETRIES, wait_time,
                    )
                    
                    self._registrar_log(
                        job, "rate_limit", componente, lote_numero,
                        f"Rate limit - aguardando {wait_time}s",
                        {"wait_seconds": wait_time, "tentativa": tentativa}
                    )
                    
                    await asyncio.sleep(wait_time)
                    self._keep_alive()
                    continue
                
                logger.warning(f"[RETRY] Lote {lote_numero} de {componente} - Tentativa {tentativa} falhou: {e}")
                
                self._registrar_log(
                    job, "lote_erro", componente, lote_numero,
                    f"Erro na tentativa {tentativa}: {ultimo_erro}",
                    {"erro": ultimo_erro}
                )
                
                if tentativa < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY * tentativa)  # Backoff progressivo
                    self._keep_alive()
        
        # Todas as tentativas falharam
        logger.error(f"[ERRO] Lote {lote_numero} de {componente} falhou após {MAX_RETRIES} tentativas")
        job.tentativas += 1
        self._atualizar_job(job, ultimo_erro=ultimo_erro)
        
        return {
            "componente": componente,
            "lote": lote_numero,
            "objetivos": [],
            "erro": f"Falhou após {MAX_RETRIES} tentativas: {ultimo_erro}"
        }
    
    async def _processar_lote_habilidades(
        self,
        perfil_resumido: str,
        componente: str,
        habilidades: List[Dict],
        ano_letivo: str,
        lote_numero: int
    ) -> Dict[str, Any]:
        """Processa um lote de habilidades (sem retry) - com validação robusta de JSON"""
        
        habilidades_texto = "\n".join([
            f"- [{h['codigo']}] T{h.get('trimestre', '?')}: {h['descricao'][:180]}"
            for h in habilidades
        ])
        
        prompt = f"""Você é um especialista em educação inclusiva.

Gere adaptações para TODAS as habilidades listadas, considerando o perfil do aluno.

{perfil_resumido}

## COMPONENTE: {componente}
## ANO LETIVO: {ano_letivo}

## HABILIDADES PARA ADAPTAR:
{habilidades_texto}

## INSTRUÇÕES:
Para CADA habilidade, gere uma adaptação específica considerando o diagnóstico do aluno.

## FORMATO DE RESPOSTA (JSON):
{{
    "objetivos": [
        {{
            "codigo_bncc": "EFXXXX",
            "area": "{componente.lower()}",
            "trimestre": 1,
            "titulo": "Título adaptado",
            "descricao_original": "Descrição da BNCC",
            "descricao_adaptada": "Como trabalhar com este aluno",
            "adaptacoes": ["Adaptação 1", "Adaptação 2"],
            "estrategias_ensino": ["Estratégia 1"],
            "materiais_recursos": ["Material 1"],
            "criterios_avaliacao": ["Critério adaptado"],
            "nivel_suporte": "alto|medio|baixo",
            "prioridade": "essencial|importante|complementar"
        }}
    ]
}}

IMPORTANTE:
- Gere UM objetivo para CADA habilidade listada
- Mantenha o código BNCC original
- Retorne APENAS o JSON válido, sem texto adicional"""

        message = self.client.messages.create(
            model=get_default_model(),
            max_tokens=6000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # Usar validação robusta com fallback
        resultado = self._validar_e_extrair_json(response_text, habilidades)
        
        return {
            "componente": componente,
            "lote": lote_numero,
            "objetivos": resultado.get("objetivos", [])
        }
    
    # ============================================
    # PROCESSAMENTO PRINCIPAL
    # ============================================
    
    async def gerar_planejamento_completo(
        self,
        student_id: int,
        ano_letivo: str,
        componentes: List[str] = None,
        user_id: int = None,
        task_id: str = None,
        task_manager = None,
        retomar_job: bool = True
    ) -> Dict[str, Any]:
        """
        Gera planejamento COMPLETO para TODAS as habilidades.
        Com persistência, keep-alive, retry, lock anti-duplicação e compressão.
        """
        
        def update_progress(progress: int, message: str):
            if task_manager and task_id:
                task_manager.update_task(task_id, progress=progress, message=message)
            logger.info(f"[{progress}%] {message}")
        
        if not self.client:
            raise Exception("Serviço de IA não disponível")
        
        # Gerar task_id se não fornecido
        if not task_id:
            task_id = str(uuid.uuid4())
        
        # PROTEÇÃO: Verificar se já existe job em andamento (evita duplicação)
        job_ativo = self.verificar_job_em_andamento(student_id, ano_letivo)
        if job_ativo:
            raise Exception(
                f"Já existe job em processamento para este aluno (ID: {job_ativo.id}). "
                f"Aguarde a conclusão ou aguarde o timeout automático."
            )
        
        # Tentar retomar job existente
        job = None
        if retomar_job:
            job = self.obter_job_para_retomar(student_id, ano_letivo)
            if job:
                logger.info(f"[INFO] Retomando job existente: {job.task_id}")
                self._registrar_log(job, "job_retomado", mensagem="Job retomado")
        
        update_progress(5, "Carregando perfil do aluno...")
        
        # Obter perfil
        perfil = self.obter_perfil_aluno(student_id)
        if not perfil:
            raise Exception("Aluno não encontrado")
        
        ano_escolar = perfil["ano_escolar"]
        
        # Se não tem componentes, buscar todos
        if not componentes:
            componentes_info = self.listar_componentes_disponiveis(ano_escolar)
            componentes = [c["componente"] for c in componentes_info]
        
        # Criar novo job se não estiver retomando
        if not job:
            job = self._criar_job(
                task_id=task_id,
                student_id=student_id,
                user_id=user_id or 0,
                ano_letivo=ano_letivo,
                componentes=componentes
            )
            self._registrar_log(job, "job_criado", mensagem=f"Componentes: {', '.join(componentes)}")
        
        # Atualizar status
        job.started_at = _utcnow()
        self._atualizar_job(job, status=JobStatus.PROCESSING.value, message="Processando...")
        
        update_progress(10, f"Processando {len(componentes)} componentes...")
        
        # Determinar componentes já processados (para retomada)
        componentes_processados = job.componentes_processados or []
        componentes_pendentes = [c for c in componentes if c not in componentes_processados]
        
        if componentes_processados:
            logger.info(f"[INFO] Componentes já processados: {componentes_processados}")
            logger.info(f"[INFO] Componentes pendentes: {componentes_pendentes}")
        
        # Carregar resultados parciais existentes (com descompressão se necessário)
        resultados_parciais = job.resultados_parciais or {}
        if isinstance(resultados_parciais, str):
            resultados_parciais = json.loads(resultados_parciais)
        resultados_parciais = self._descomprimir_se_necessario(resultados_parciais)
        
        perfil_resumido = self._criar_perfil_resumido(perfil)
        
        # Processar cada componente pendente
        progresso_base = 10
        progresso_por_componente = 80 / len(componentes)
        
        for idx, componente in enumerate(componentes):
            # Calcular progresso considerando já processados
            idx_real = componentes.index(componente)
            progresso_atual = progresso_base + (idx_real * progresso_por_componente)
            
            # Pular se já processado
            if componente in componentes_processados:
                update_progress(int(progresso_atual + progresso_por_componente), 
                              f"{componente} já processado anteriormente")
                continue
            
            self._atualizar_job(job, 
                              progress=int(progresso_atual),
                              message=f"Processando {componente}...",
                              componente_atual=componente,
                              lote_atual=0)
            
            update_progress(int(progresso_atual), f"Processando {componente}...")
            
            # Buscar habilidades
            self._keep_alive()
            habilidades_db = self.buscar_todas_habilidades(ano_escolar, componente)
            
            if not habilidades_db:
                logger.warning(f"[AVISO] Nenhuma habilidade para {componente} no {ano_escolar}")
                continue
            
            habilidades = [
                {
                    "id": h.id,
                    "codigo": h.codigo_bncc,
                    "descricao": h.habilidade_descricao,
                    "objeto_conhecimento": h.objeto_conhecimento,
                    "trimestre": h.trimestre_sugerido,
                    "dificuldade": h.dificuldade
                }
                for h in habilidades_db
            ]
            
            self._registrar_log(
                job, "componente_iniciado", componente,
                mensagem=f"{len(habilidades)} habilidades encontradas"
            )
            
            # CHECKPOINT GRANULAR: Recuperar lotes já processados
            lotes_ja_processados, objetivos_recuperados = self._obter_lotes_ja_processados(job, componente)
            todos_objetivos = objetivos_recuperados.copy() if objetivos_recuperados else []
            
            # Processar em lotes
            total_lotes = (len(habilidades) + LOTE_SIZE - 1) // LOTE_SIZE
            
            for lote_idx in range(0, len(habilidades), LOTE_SIZE):
                lote_numero = lote_idx // LOTE_SIZE + 1
                
                # PULAR lotes já processados (recuperação granular)
                if lote_numero in lotes_ja_processados:
                    logger.info(f"[⏭️ SKIP] {componente} lote {lote_numero}/{total_lotes} já processado")
                    continue
                
                lote = habilidades[lote_idx:lote_idx + LOTE_SIZE]
                
                self._atualizar_job(job, lote_atual=lote_numero,
                                  message=f"{componente}: lote {lote_numero}/{total_lotes}")
                
                progresso_lote = progresso_atual + (lote_numero / total_lotes * progresso_por_componente * 0.8)
                update_progress(int(progresso_lote), 
                              f"{componente}: processando lote {lote_numero}/{total_lotes}")
                
                # Processar lote COM RETRY
                resultado = await self._processar_lote_com_retry(
                    job, perfil_resumido, componente, lote, ano_letivo, lote_numero
                )
                
                if resultado.get("objetivos"):
                    todos_objetivos.extend(resultado["objetivos"])
                    
                    # CHECKPOINT: Salvar após cada lote processado com sucesso
                    self._salvar_checkpoint_lote(
                        job, componente, lote_numero,
                        resultado["objetivos"], todos_objetivos
                    )
                
                # Pequena pausa entre lotes
                await asyncio.sleep(0.5)
                self._keep_alive()
            
            # Salvar resultado do componente
            self._salvar_resultado_parcial(job, componente, todos_objetivos)
            resultados_parciais[componente] = {
                "total_habilidades": len(habilidades),
                "objetivos": todos_objetivos
            }
            
            self._registrar_log(
                job, "componente_concluido", componente,
                mensagem=f"{len(todos_objetivos)} objetivos gerados",
                dados={"objetivos_gerados": len(todos_objetivos)}
            )
            
            update_progress(int(progresso_atual + progresso_por_componente),
                          f"{componente} concluído: {len(todos_objetivos)} objetivos")
        
        # Montar resultado final
        update_progress(95, "Finalizando planejamento...")
        
        planejamento_completo = {
            "aluno": {
                "id": perfil["id"],
                "nome": perfil["nome"],
                "ano_escolar": ano_escolar
            },
            "ano_letivo": ano_letivo,
            "componentes": resultados_parciais,
            "resumo": {
                "total_habilidades": sum(c.get("total_habilidades", 0) for c in resultados_parciais.values()),
                "total_objetivos_gerados": sum(len(c.get("objetivos", [])) for c in resultados_parciais.values()),
                "por_componente": {
                    comp: {
                        "habilidades": dados.get("total_habilidades", 0),
                        "objetivos_gerados": len(dados.get("objetivos", []))
                    }
                    for comp, dados in resultados_parciais.items()
                }
            },
            "orientacoes_gerais": self._gerar_orientacoes_gerais(perfil)
        }
        
        # Atualizar job como concluído (com compressão se necessário)
        resultado_para_salvar = self._comprimir_se_necessario(planejamento_completo)
        # FIX: dict direto, nao json.dumps (ver comentario em _salvar_checkpoint_lote).
        job.resultado_final = resultado_para_salvar
        job.completed_at = _utcnow()
        self._atualizar_job(job, 
                          status=JobStatus.COMPLETED.value,
                          progress=100,
                          message="Planejamento completo gerado com sucesso!")
        
        self._registrar_log(job, "job_concluido", 
                          mensagem=f"Total: {planejamento_completo['resumo']['total_objetivos_gerados']} objetivos")
        
        update_progress(100, "Planejamento completo gerado!")
        
        return {
            "success": True,
            "job_id": job.id,
            "task_id": task_id,
            "planejamento": planejamento_completo
        }
    
    def _gerar_orientacoes_gerais(self, perfil: Dict) -> Dict[str, Any]:
        """Gera orientações baseadas no perfil"""
        diagnosticos = perfil.get("diagnosticos", {})
        
        orientacoes = {
            "ambiente": [],
            "comunicacao": [],
            "avaliacao": [],
            "rotina": []
        }
        
        if diagnosticos.get("tea"):
            orientacoes["ambiente"].extend([
                "Manter ambiente organizado e previsível",
                "Usar apoios visuais (cronogramas, pictogramas)",
                "Reduzir estímulos sensoriais quando necessário"
            ])
            orientacoes["comunicacao"].extend([
                "Usar linguagem clara e direta",
                "Dar tempo para processamento",
                "Evitar expressões figuradas"
            ])
            orientacoes["rotina"].extend([
                "Antecipar mudanças na rotina",
                "Usar timer visual para transições"
            ])
        
        if diagnosticos.get("tdah"):
            orientacoes["ambiente"].extend([
                "Sentar próximo ao professor",
                "Minimizar distrações visuais",
                "Permitir pausas para movimento"
            ])
            orientacoes["avaliacao"].extend([
                "Dividir tarefas em etapas menores",
                "Dar instruções uma de cada vez",
                "Usar reforço positivo frequente"
            ])
        
        if diagnosticos.get("dislexia"):
            orientacoes["comunicacao"].extend([
                "Usar fonte maior e espaçamento adequado",
                "Permitir leitura em voz alta",
                "Dar tempo extra para leitura"
            ])
            orientacoes["avaliacao"].extend([
                "Permitir avaliação oral quando possível",
                "Não penalizar erros ortográficos",
                "Usar recursos de áudio"
            ])
        
        for key in orientacoes:
            orientacoes[key] = list(set(orientacoes[key]))
        
        return orientacoes
    
    # ============================================
    # SALVAR COMO PEI
    # ============================================
    
    def salvar_planejamento_completo(
        self,
        student_id: int,
        planejamento: Dict[str, Any],
        user_id: int,
        ano_letivo: str,
        job_id: int = None
    ) -> PEI:
        """Salva o planejamento completo como PEI"""
        self._keep_alive()
        
        ano = int(ano_letivo)
        data_inicio = date(ano, 2, 1)
        data_fim = date(ano, 12, 15)
        
        pei = PEI(
            student_id=student_id,
            created_by=user_id,
            ano_letivo=ano_letivo,
            tipo_periodo="anual",
            data_inicio=data_inicio,
            data_fim=data_fim,
            data_proxima_revisao=data_inicio + timedelta(days=90),
            ia_sugestoes_originais=planejamento,
            status="rascunho"
        )
        
        self.db.add(pei)
        self.db.flush()
        
        # Criar objetivos
        total_objetivos = 0
        for componente, dados in planejamento.get("componentes", {}).items():
            for obj_data in dados.get("objetivos", []):
                codigo_bncc = obj_data.get("codigo_bncc")
                
                curriculo_id = None
                if codigo_bncc:
                    curriculo = self.db.query(CurriculoNacional).filter(
                        CurriculoNacional.codigo_bncc == codigo_bncc
                    ).first()
                    if curriculo:
                        curriculo_id = curriculo.id
                
                trimestre = obj_data.get("trimestre", 1)
                prazo = self._calcular_prazo_trimestre(ano, trimestre)
                
                objetivo = PEIObjetivo(
                    pei_id=pei.id,
                    area=obj_data.get("area", componente.lower()),
                    curriculo_nacional_id=curriculo_id,
                    codigo_bncc=codigo_bncc,
                    titulo=obj_data.get("titulo", ""),
                    descricao=obj_data.get("descricao_adaptada", obj_data.get("descricao", "")),
                    meta_especifica=obj_data.get("meta_especifica", ""),
                    criterio_medicao=obj_data.get("criterios_avaliacao", [""])[0] if obj_data.get("criterios_avaliacao") else "",
                    valor_alvo=80,
                    prazo=prazo,
                    trimestre=trimestre,
                    adaptacoes=obj_data.get("adaptacoes"),
                    estrategias=obj_data.get("estrategias_ensino"),
                    materiais_recursos=obj_data.get("materiais_recursos"),
                    criterios_avaliacao=obj_data.get("criterios_avaliacao"),
                    origem="ia_sugestao",
                    ia_sugestao_original=obj_data
                )
                
                self.db.add(objetivo)
                total_objetivos += 1
                
                # Commit a cada 50 objetivos para evitar timeout
                if total_objetivos % 50 == 0:
                    self.db.flush()
                    self._keep_alive()
        
        self.db.commit()
        self.db.refresh(pei)
        
        # Atualizar job se fornecido
        if job_id:
            job = self.db.query(PlanejamentoJob).filter(PlanejamentoJob.id == job_id).first()
            if job:
                job.pei_id = pei.id
                self.db.commit()
        
        return pei
    
    def _limpar_json(self, text: str) -> str:
        """Remove marcadores de código do texto"""
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    
    def _validar_e_extrair_json(self, response_text: str, habilidades: List[Dict]) -> Dict[str, Any]:
        """
        Validação ROBUSTA de JSON retornado pela IA.
        Tenta múltiplas estratégias para extrair dados válidos.
        """
        
        # Estratégia 1: Parse direto do JSON limpo
        try:
            texto_limpo = self._limpar_json(response_text)
            resultado = json.loads(texto_limpo)
            
            # Validar estrutura básica
            if self._validar_estrutura_objetivos(resultado, habilidades):
                return resultado
            
            logger.warning(f"[⚠️ JSON] Estrutura inválida, tentando recuperação...")
        except json.JSONDecodeError as e:
            logger.exception(f"[⚠️ JSON] Parse falhou: {e}. Tentando recuperação...")
        
        # Estratégia 2: Encontrar JSON dentro do texto com regex
        try:
            # Procurar por {"objetivos": [...]} no texto
            json_match = re.search(r'\{\s*["\']objetivos["\']\s*:\s*\[.*\]\s*\}', response_text, re.DOTALL)
            if json_match:
                resultado = json.loads(json_match.group())
                if self._validar_estrutura_objetivos(resultado, habilidades):
                    logger.info(f"[✅ JSON] Recuperado via regex (padrão 1)")
                    return resultado
        except Exception as e:
            logger.exception(f"[⚠️ JSON] Regex padrão 1 falhou: {e}")
        
        # Estratégia 3: Extrair array de objetivos diretamente
        try:
            # Procurar por array de objetivos
            array_match = re.search(r'\[\s*\{.*?"codigo_bncc".*?\}\s*\]', response_text, re.DOTALL)
            if array_match:
                objetivos = json.loads(array_match.group())
                resultado = {"objetivos": objetivos}
                if self._validar_estrutura_objetivos(resultado, habilidades):
                    logger.info(f"[✅ JSON] Recuperado via regex (array direto)")
                    return resultado
        except Exception as e:
            logger.exception(f"[⚠️ JSON] Regex array falhou: {e}")
        
        # Estratégia 4: Consertar JSON com problemas comuns
        try:
            texto_consertado = self._consertar_json(response_text)
            resultado = json.loads(texto_consertado)
            if self._validar_estrutura_objetivos(resultado, habilidades):
                logger.info(f"[✅ JSON] Recuperado após conserto")
                return resultado
        except Exception as e:
            logger.exception(f"[⚠️ JSON] Conserto falhou: {e}")
        
        # Estratégia 5: Gerar objetivos mínimos de fallback
        logger.info(f"[🔄 FALLBACK] Gerando objetivos mínimos para {len(habilidades)} habilidades")
        return self._gerar_objetivos_fallback(habilidades)
    
    def _validar_estrutura_objetivos(self, resultado: Dict, habilidades: List[Dict]) -> bool:
        """
        Valida se o resultado tem estrutura correta e quantidade mínima de objetivos.
        """
        if not isinstance(resultado, dict):
            return False
        
        objetivos = resultado.get("objetivos", [])
        if not isinstance(objetivos, list):
            return False
        
        # Deve ter pelo menos 50% dos objetivos esperados
        minimo_esperado = max(1, len(habilidades) // 2)
        if len(objetivos) < minimo_esperado:
            logger.warning(f"[⚠️ VALID] Poucos objetivos: {len(objetivos)}/{len(habilidades)} (mínimo: {minimo_esperado})")
            return False
        
        # Validar estrutura de cada objetivo
        campos_obrigatorios = ["codigo_bncc"]
        for obj in objetivos:
            if not isinstance(obj, dict):
                return False
            for campo in campos_obrigatorios:
                if campo not in obj:
                    logger.warning(f"[⚠️ VALID] Campo '{campo}' ausente em objetivo")
                    return False
        
        return True
    
    def _consertar_json(self, texto: str) -> str:
        """
        Tenta consertar problemas comuns em JSON malformado.
        """
        # Remover texto antes/depois do JSON
        texto = self._limpar_json(texto)
        
        # Encontrar início e fim do JSON
        inicio = texto.find('{')
        fim = texto.rfind('}')
        if inicio != -1 and fim != -1:
            texto = texto[inicio:fim+1]
        
        # Consertar vírgulas extras
        texto = re.sub(r',\s*}', '}', texto)
        texto = re.sub(r',\s*]', ']', texto)
        
        # Consertar aspas simples para duplas
        # Cuidado: não substituir aspas dentro de strings
        texto = re.sub(r"(?<![\w])'([^']*)'(?![\w])", r'"\1"', texto)
        
        # Remover comentários
        texto = re.sub(r'//.*?\n', '\n', texto)
        texto = re.sub(r'/\*.*?\*/', '', texto, flags=re.DOTALL)
        
        return texto
    
    def _gerar_objetivos_fallback(self, habilidades: List[Dict]) -> Dict[str, Any]:
        """
        Gera objetivos mínimos quando a IA falha completamente.
        Permite que o processamento continue sem perder as habilidades.
        """
        objetivos = []
        
        for h in habilidades:
            objetivo = {
                "codigo_bncc": h.get("codigo", "UNKNOWN"),
                "area": "geral",
                "trimestre": h.get("trimestre", 1),
                "titulo": f"Objetivo para {h.get('codigo', 'habilidade')}",
                "descricao_original": h.get("descricao", "")[:200],
                "descricao_adaptada": f"Trabalhar a habilidade {h.get('codigo', '')} com adaptações individualizadas.",
                "adaptacoes": ["Adaptar conforme necessidade do aluno"],
                "estrategias_ensino": ["Usar recursos visuais e concretos"],
                "materiais_recursos": ["Material adaptado"],
                "criterios_avaliacao": ["Avaliação processual"],
                "nivel_suporte": "medio",
                "prioridade": "importante",
                "_fallback": True  # Marca que foi gerado automaticamente
            }
            objetivos.append(objetivo)
        
        return {"objetivos": objetivos}
    
    def _calcular_prazo_trimestre(self, ano: int, trimestre: int) -> date:
        """Calcula data limite de um trimestre"""
        if trimestre == 1:
            return date(ano, 4, 30)
        elif trimestre == 2:
            return date(ano, 7, 15)
        elif trimestre == 3:
            return date(ano, 10, 15)
        else:
            return date(ano, 12, 15)
