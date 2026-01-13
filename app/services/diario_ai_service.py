"""
🤖 Service - Análise Inteligente do Diário de Aprendizagem
Usa Claude para extrair disciplinas, tópicos, conceitos e gerar insights
"""
import json
from typing import Dict, Any, List, Optional
from datetime import date, datetime, timedelta, timezone
from anthropic import Anthropic
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.config import settings
from app.models.diario_aprendizagem import (
    DiarioAprendizagem, 
    ConteudoExtraido, 
    ResumoSemanalAprendizagem,
    HumorEstudo,
    NivelCompreensao
)
from app.models.student import Student


class DiarioAIService:
    """
    🧠 Serviço de IA para análise do diário de aprendizagem
    """
    
    def __init__(self):
        self._client = None
        self.model = "claude-3-5-sonnet-20241022"
    
    @property
    def client(self):
        if self._client is None:
            self._client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client
    
    async def analisar_registro(
        self,
        db: Session,
        diario: DiarioAprendizagem,
        student: Student
    ) -> Dict[str, Any]:
        """
        📝 Analisa um registro do diário e extrai informações estruturadas
        """
        
        # Preparar contexto do aluno
        diagnosticos = student.diagnosis or {}
        serie = student.grade_level or "Não informada"
        
        prompt = f"""Você é um especialista em educação inclusiva analisando o registro de estudo de um aluno.

## PERFIL DO ALUNO
- Nome: {student.name}
- Série: {serie}
- Diagnósticos: {json.dumps(diagnosticos, ensure_ascii=False) if diagnosticos else 'Não informado'}

## REGISTRO DO DIÁRIO (Data: {diario.data_estudo})
{diario.registro_texto}

## AUTO-AVALIAÇÃO DO ALUNO
- Humor durante estudo: {diario.humor.value if diario.humor else 'Não informado'}
- Nível de compreensão: {diario.nivel_compreensao.value if diario.nivel_compreensao else 'Não informado'}
- Tempo de estudo: {diario.tempo_estudo_minutos or 'Não informado'} minutos

## SUA MISSÃO
Analise o registro e extraia informações estruturadas para ajudar no acompanhamento pedagógico.

## FORMATO DE RESPOSTA (JSON):
{{
    "disciplinas_detectadas": ["Disciplina 1", "Disciplina 2"],
    "topicos_extraidos": [
        {{
            "disciplina": "Matemática",
            "topico_principal": "Frações",
            "subtopicos": ["Numerador", "Denominador", "Frações equivalentes"],
            "conceitos_chave": ["fração", "parte", "todo", "divisão"],
            "nivel_dificuldade": "medio",
            "contexto": "Trecho relevante do registro"
        }}
    ],
    "conceitos_chave_geral": ["conceito1", "conceito2", "conceito3"],
    "dificuldades_identificadas": [
        {{
            "descricao": "Dificuldade mencionada",
            "disciplina": "Matemática",
            "gravidade": "leve|moderada|alta"
        }}
    ],
    "pontos_positivos": ["O que foi bem", "Progresso observado"],
    "sugestoes_revisao": [
        {{
            "topico": "Tópico para revisar",
            "motivo": "Por que revisar",
            "prioridade": "alta|media|baixa"
        }}
    ],
    "conexoes_bncc": [
        {{
            "codigo": "EF05MA03",
            "descricao_resumida": "Identificar frações equivalentes"
        }}
    ],
    "sentimento_geral": "positivo|neutro|negativo|misto",
    "resumo": "Resumo de 2-3 frases do que foi estudado",
    "tags": ["tag1", "tag2", "tag3"],
    "insights_professor": "Observação útil para o professor",
    "sugestao_proximo_passo": "O que estudar em seguida"
}}

IMPORTANTE:
- Seja específico nos tópicos (não genérico)
- Identifique padrões de dificuldade
- Sugira revisões baseadas no perfil do aluno
- Use códigos BNCC reais quando possível
- Se não conseguir identificar algo, use null ou lista vazia

Retorne APENAS o JSON, sem explicações."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            response_text = self._limpar_json(response_text)
            analise = json.loads(response_text)
            
            # Atualizar o diário com a análise
            diario.ia_processado = True
            diario.ia_disciplinas_detectadas = analise.get("disciplinas_detectadas", [])
            diario.ia_topicos_extraidos = analise.get("topicos_extraidos", [])
            diario.ia_conceitos_chave = analise.get("conceitos_chave_geral", [])
            diario.ia_dificuldades_identificadas = analise.get("dificuldades_identificadas", [])
            diario.ia_pontos_positivos = analise.get("pontos_positivos", [])
            diario.ia_sugestoes_revisao = analise.get("sugestoes_revisao", [])
            diario.ia_conexoes_bncc = analise.get("conexoes_bncc", [])
            diario.ia_sentimento_geral = analise.get("sentimento_geral")
            diario.ia_resumo = analise.get("resumo")
            diario.ia_tags = analise.get("tags", [])
            
            db.commit()
            
            # Criar registros de conteúdo extraído
            await self._criar_conteudos_extraidos(db, diario, analise)
            
            return {
                "success": True,
                "analise": analise
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _criar_conteudos_extraidos(
        self,
        db: Session,
        diario: DiarioAprendizagem,
        analise: Dict
    ):
        """
        📚 Cria registros de conteúdo extraído para uso futuro
        """
        
        topicos = analise.get("topicos_extraidos", [])
        
        for topico_data in topicos:
            # Verificar se já existe conteúdo similar
            existente = db.query(ConteudoExtraido).filter(
                ConteudoExtraido.student_id == diario.student_id,
                ConteudoExtraido.disciplina == topico_data.get("disciplina"),
                ConteudoExtraido.topico == topico_data.get("topico_principal")
            ).first()
            
            if existente:
                # Atualizar contador e data
                existente.vezes_mencionado += 1
                existente.ultima_mencao = diario.data_estudo
                
                # Adicionar subtópicos novos
                if existente.subtopicos and topico_data.get("subtopicos"):
                    existente.subtopicos = list(set(existente.subtopicos + topico_data.get("subtopicos", [])))
                elif topico_data.get("subtopicos"):
                    existente.subtopicos = topico_data.get("subtopicos")
                    
                # Adicionar conceitos novos
                if existente.conceitos and topico_data.get("conceitos_chave"):
                    existente.conceitos = list(set(existente.conceitos + topico_data.get("conceitos_chave", [])))
                elif topico_data.get("conceitos_chave"):
                    existente.conceitos = topico_data.get("conceitos_chave")
            else:
                # Criar novo
                area = self._identificar_area_conhecimento(topico_data.get("disciplina", ""))
                
                # Buscar código BNCC relacionado
                codigo_bncc = None
                habilidade_bncc = None
                conexoes = analise.get("conexoes_bncc", [])
                for conexao in conexoes:
                    codigo_bncc = conexao.get("codigo")
                    habilidade_bncc = conexao.get("descricao_resumida")
                    break
                
                conteudo = ConteudoExtraido(
                    diario_id=diario.id,
                    student_id=diario.student_id,
                    disciplina=topico_data.get("disciplina", "Geral"),
                    area_conhecimento=area,
                    topico=topico_data.get("topico_principal", ""),
                    subtopicos=topico_data.get("subtopicos"),
                    conceitos=topico_data.get("conceitos_chave"),
                    contexto_original=topico_data.get("contexto"),
                    nivel_dificuldade_percebido=topico_data.get("nivel_dificuldade"),
                    codigo_bncc=codigo_bncc,
                    habilidade_bncc=habilidade_bncc,
                    prioridade_revisao=self._calcular_prioridade(topico_data, analise),
                    ultima_mencao=diario.data_estudo
                )
                db.add(conteudo)
        
        db.commit()
    
    def _identificar_area_conhecimento(self, disciplina: str) -> str:
        """Identifica a área do conhecimento baseado na disciplina"""
        disciplina_lower = disciplina.lower()
        
        if any(d in disciplina_lower for d in ["matemática", "física", "química"]):
            return "Ciências Exatas"
        elif any(d in disciplina_lower for d in ["português", "inglês", "espanhol", "literatura", "redação"]):
            return "Linguagens"
        elif any(d in disciplina_lower for d in ["história", "geografia", "sociologia", "filosofia"]):
            return "Ciências Humanas"
        elif any(d in disciplina_lower for d in ["biologia", "ciências"]):
            return "Ciências da Natureza"
        elif any(d in disciplina_lower for d in ["arte", "música", "educação física"]):
            return "Linguagens e Artes"
        else:
            return "Outras"
    
    def _calcular_prioridade(self, topico_data: Dict, analise: Dict) -> int:
        """Calcula prioridade de revisão (0-10)"""
        prioridade = 5  # Base
        
        # Aumentar se há dificuldade
        nivel_dif = topico_data.get("nivel_dificuldade", "").lower()
        if nivel_dif == "dificil":
            prioridade += 2
        elif nivel_dif == "muito_dificil":
            prioridade += 3
        
        # Aumentar se está nas sugestões de revisão
        sugestoes = analise.get("sugestoes_revisao", [])
        for sug in sugestoes:
            if sug.get("prioridade") == "alta":
                prioridade += 2
            elif sug.get("prioridade") == "media":
                prioridade += 1
        
        # Aumentar se sentimento é negativo
        if analise.get("sentimento_geral") == "negativo":
            prioridade += 1
        
        return min(10, prioridade)
    
    async def gerar_resumo_semanal(
        self,
        db: Session,
        student_id: int,
        data_referencia: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        📊 Gera resumo semanal consolidando todos os diários
        """
        
        if not data_referencia:
            data_referencia = date.today()
        
        # Calcular início e fim da semana
        inicio_semana = data_referencia - timedelta(days=data_referencia.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        
        # Buscar diários da semana
        diarios = db.query(DiarioAprendizagem).filter(
            DiarioAprendizagem.student_id == student_id,
            DiarioAprendizagem.data_estudo >= inicio_semana,
            DiarioAprendizagem.data_estudo <= fim_semana
        ).order_by(DiarioAprendizagem.data_estudo).all()
        
        if not diarios:
            return {
                "success": False,
                "error": "Nenhum registro encontrado nesta semana"
            }
        
        # Buscar aluno
        student = db.query(Student).filter(Student.id == student_id).first()
        
        # Consolidar dados
        registros_texto = []
        disciplinas_count = {}
        humor_count = {}
        total_minutos = 0
        todos_topicos = []
        todas_dificuldades = []
        todos_positivos = []
        
        for diario in diarios:
            registros_texto.append(f"[{diario.data_estudo}] {diario.registro_texto}")
            
            if diario.ia_disciplinas_detectadas:
                for disc in diario.ia_disciplinas_detectadas:
                    disciplinas_count[disc] = disciplinas_count.get(disc, 0) + 1
            
            if diario.humor:
                humor_count[diario.humor.value] = humor_count.get(diario.humor.value, 0) + 1
            
            if diario.tempo_estudo_minutos:
                total_minutos += diario.tempo_estudo_minutos
            
            if diario.ia_topicos_extraidos:
                todos_topicos.extend(diario.ia_topicos_extraidos)
            
            if diario.ia_dificuldades_identificadas:
                todas_dificuldades.extend(diario.ia_dificuldades_identificadas)
            
            if diario.ia_pontos_positivos:
                todos_positivos.extend(diario.ia_pontos_positivos)
        
        # Gerar análise semanal com IA
        prompt = f"""Você é um especialista em educação inclusiva gerando um relatório semanal.

## ALUNO
- Nome: {student.name}
- Série: {student.grade_level}
- Diagnósticos: {json.dumps(student.diagnosis, ensure_ascii=False) if student.diagnosis else 'Não informado'}

## SEMANA: {inicio_semana} a {fim_semana}

## REGISTROS DA SEMANA
{chr(10).join(registros_texto)}

## ESTATÍSTICAS
- Total de registros: {len(diarios)}
- Tempo total de estudo: {total_minutos} minutos
- Disciplinas estudadas: {json.dumps(disciplinas_count, ensure_ascii=False)}
- Distribuição de humor: {json.dumps(humor_count, ensure_ascii=False)}

## TÓPICOS ESTUDADOS
{json.dumps(todos_topicos, ensure_ascii=False, indent=2)}

## DIFICULDADES IDENTIFICADAS
{json.dumps(todas_dificuldades, ensure_ascii=False, indent=2)}

## PONTOS POSITIVOS
{json.dumps(todos_positivos, ensure_ascii=False)}

## SUA MISSÃO
Gere um relatório semanal completo e motivador.

## FORMATO DE RESPOSTA (JSON):
{{
    "resumo_geral": "Resumo geral da semana em 3-4 frases",
    "principais_conquistas": [
        "Conquista 1 específica",
        "Conquista 2 específica"
    ],
    "areas_atencao": [
        {{
            "area": "Área/Disciplina",
            "descricao": "O que precisa de atenção",
            "sugestao": "Como melhorar"
        }}
    ],
    "recomendacoes": [
        {{
            "tipo": "revisao|aprofundamento|pratica",
            "disciplina": "Disciplina",
            "topico": "Tópico específico",
            "descricao": "O que fazer"
        }}
    ],
    "progresso_observado": "Descrição do progresso durante a semana",
    "mensagem_motivacional": "Mensagem personalizada para o aluno",
    "nota_para_professor": "Observação importante para o professor",
    "prioridades_proxima_semana": ["Prioridade 1", "Prioridade 2"]
}}

Retorne APENAS o JSON."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = self._limpar_json(message.content[0].text.strip())
            analise_semanal = json.loads(response_text)
            
            # Salvar resumo
            numero_semana = data_referencia.isocalendar()[1]
            ano = data_referencia.year
            
            # Verificar se já existe
            existente = db.query(ResumoSemanalAprendizagem).filter(
                ResumoSemanalAprendizagem.student_id == student_id,
                ResumoSemanalAprendizagem.ano == ano,
                ResumoSemanalAprendizagem.numero_semana == numero_semana
            ).first()
            
            if existente:
                resumo = existente
            else:
                resumo = ResumoSemanalAprendizagem(
                    student_id=student_id,
                    semana_inicio=inicio_semana,
                    semana_fim=fim_semana,
                    ano=ano,
                    numero_semana=numero_semana
                )
                db.add(resumo)
            
            resumo.total_registros = len(diarios)
            resumo.total_minutos_estudo = total_minutos
            resumo.disciplinas_estudadas = disciplinas_count
            resumo.resumo_geral = analise_semanal.get("resumo_geral")
            resumo.principais_conquistas = analise_semanal.get("principais_conquistas")
            resumo.areas_atencao = analise_semanal.get("areas_atencao")
            resumo.recomendacoes = analise_semanal.get("recomendacoes")
            resumo.progresso_observado = analise_semanal.get("progresso_observado")
            resumo.dados_grafico_disciplinas = disciplinas_count
            resumo.dados_grafico_humor = humor_count
            resumo.dados_grafico_tempo = {
                d.data_estudo.isoformat(): d.tempo_estudo_minutos or 0 
                for d in diarios
            }
            
            db.commit()
            db.refresh(resumo)
            
            return {
                "success": True,
                "resumo_id": resumo.id,
                "analise": analise_semanal,
                "estatisticas": {
                    "total_registros": len(diarios),
                    "total_minutos": total_minutos,
                    "disciplinas": disciplinas_count,
                    "humor": humor_count
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obter_conteudos_para_material(
        self,
        db: Session,
        student_id: int,
        disciplina: Optional[str] = None,
        limite: int = 10
    ) -> List[Dict]:
        """
        🎯 Obtém conteúdos prioritários para geração de material
        Usado como insumo para materiais adaptados
        """
        
        query = db.query(ConteudoExtraido).filter(
            ConteudoExtraido.student_id == student_id,
            ConteudoExtraido.material_gerado == False
        )
        
        if disciplina:
            query = query.filter(ConteudoExtraido.disciplina == disciplina)
        
        conteudos = query.order_by(
            ConteudoExtraido.prioridade_revisao.desc(),
            ConteudoExtraido.vezes_mencionado.desc()
        ).limit(limite).all()
        
        return [
            {
                "id": c.id,
                "disciplina": c.disciplina,
                "topico": c.topico,
                "subtopicos": c.subtopicos,
                "conceitos": c.conceitos,
                "prioridade": c.prioridade_revisao,
                "vezes_mencionado": c.vezes_mencionado,
                "codigo_bncc": c.codigo_bncc,
                "nivel_dificuldade": c.nivel_dificuldade_percebido
            }
            for c in conteudos
        ]
    
    def _limpar_json(self, text: str) -> str:
        """Remove marcadores de código"""
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()


# Instância global
diario_ai_service = DiarioAIService()
