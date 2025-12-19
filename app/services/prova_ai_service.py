"""
🤖 AdaptAI - Serviço de Geração de Questões com IA
Integração com Claude API da Anthropic
"""
import anthropic
import json
from typing import List, Dict, Any
from app.core.config import settings
from app.models.prova import TipoQuestao, DificuldadeQuestao


class ProvaAIService:
    """Serviço para gerar questões usando Claude AI"""
    
    def __init__(self):
        self._client = None
        self.model = settings.CLAUDE_MODEL
    
    @property
    def client(self):
        """Lazy initialization do cliente Anthropic"""
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client
    
    async def gerar_questoes(
        self,
        conteudo_prompt: str,
        materia: str,
        serie_nivel: str,
        quantidade: int,
        tipo_questao: TipoQuestao,
        dificuldade: DificuldadeQuestao
    ) -> List[Dict[str, Any]]:
        """
        Gera questões usando Claude AI
        
        Args:
            conteudo_prompt: Descrição do conteúdo/tema
            materia: Matéria da prova
            serie_nivel: Série/nível escolar
            quantidade: Quantidade de questões
            tipo_questao: Tipo das questões
            dificuldade: Nível de dificuldade
            
        Returns:
            Lista de questões geradas
        """
        
        # Monta o prompt para Claude
        prompt = self._criar_prompt_geracao(
            conteudo_prompt=conteudo_prompt,
            materia=materia,
            serie_nivel=serie_nivel,
            quantidade=quantidade,
            tipo_questao=tipo_questao,
            dificuldade=dificuldade
        )
        
        try:
            # Chama Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extrai o conteúdo da resposta
            resposta = message.content[0].text
            
            # Parse do JSON
            questoes = self._parse_questoes_json(resposta)
            
            return questoes
            
        except Exception as e:
            print(f"❌ Erro ao gerar questões com IA: {e}")
            raise Exception(f"Erro ao gerar questões: {str(e)}")
    
    def _criar_prompt_geracao(
        self,
        conteudo_prompt: str,
        materia: str,
        serie_nivel: str,
        quantidade: int,
        tipo_questao: TipoQuestao,
        dificuldade: DificuldadeQuestao
    ) -> str:
        """Cria o prompt para Claude gerar as questões"""
        
        tipo_descricao = {
            TipoQuestao.MULTIPLA_ESCOLHA: "múltipla escolha com 4 alternativas (A, B, C, D)",
            TipoQuestao.VERDADEIRO_FALSO: "verdadeiro ou falso",
            TipoQuestao.DISSERTATIVA: "dissertativa (resposta aberta)",
            TipoQuestao.LACUNAS: "completar lacunas"
        }
        
        dificuldade_descricao = {
            DificuldadeQuestao.FACIL: "fácil - conceitos básicos",
            DificuldadeQuestao.MEDIO: "médio - aplicação de conceitos",
            DificuldadeQuestao.DIFICIL: "difícil - análise e síntese",
            DificuldadeQuestao.MUITO_DIFICIL: "muito difícil - pensamento crítico avançado"
        }
        
        prompt = f"""Você é um especialista em educação e criação de avaliações pedagógicas.

**TAREFA:** Criar {quantidade} questões de {materia} para {serie_nivel or 'estudantes'}.

**CONTEXTO DO CONTEÚDO:**
{conteudo_prompt}

**ESPECIFICAÇÕES:**
- Tipo: {tipo_descricao.get(tipo_questao, 'múltipla escolha')}
- Dificuldade: {dificuldade_descricao.get(dificuldade, 'médio')}
- Quantidade: {quantidade} questões
- Matéria: {materia}
- Nível: {serie_nivel or 'Não especificado'}

**FORMATO DE SAÍDA:**
Retorne APENAS um JSON válido (sem markdown, sem ```json) com a seguinte estrutura:

{{
  "questoes": [
    {{
      "numero": 1,
      "enunciado": "Texto da questão...",
      "tipo": "{tipo_questao.value}",
      "dificuldade": "{dificuldade.value}",
      "opcoes": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "resposta_correta": "A",
      "explicacao": "Explicação detalhada da resposta correta...",
      "tags": ["tag1", "tag2"]
    }}
  ]
}}

**INSTRUÇÕES IMPORTANTES:**
1. Cada questão deve ser clara, objetiva e pedagogicamente adequada
2. Para múltipla escolha: sempre 4 alternativas (A, B, C, D)
3. Para verdadeiro/falso: use opcoes: ["Verdadeiro", "Falso"]
4. Para dissertativa: deixe opcoes como null e forneça criterios_avaliacao
5. A resposta_correta deve ser apenas a letra (ex: "A") ou o texto exato da opção correta
6. Inclua explicações detalhadas para cada resposta
7. Use tags relevantes para categorizar o conteúdo
8. Varie os assuntos dentro do tema proposto
9. As questões devem estar adequadas ao nível de {serie_nivel or 'escolar'}
10. RETORNE APENAS O JSON, sem texto adicional antes ou depois

Gere as {quantidade} questões agora:"""
        
        return prompt
    
    def _parse_questoes_json(self, resposta: str) -> List[Dict[str, Any]]:
        """Parse da resposta JSON de Claude"""
        try:
            # Remove possíveis markdown
            resposta = resposta.strip()
            if resposta.startswith("```json"):
                resposta = resposta[7:]
            if resposta.startswith("```"):
                resposta = resposta[3:]
            if resposta.endswith("```"):
                resposta = resposta[:-3]
            resposta = resposta.strip()
            
            # Parse JSON
            data = json.loads(resposta)
            
            if "questoes" in data:
                return data["questoes"]
            else:
                return data
                
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao fazer parse do JSON: {e}")
            print(f"Resposta recebida: {resposta[:500]}...")
            raise Exception("Erro ao processar resposta da IA. Formato JSON inválido.")
    
    async def analisar_desempenho(
        self,
        questoes: List[Dict],
        respostas: List[Dict],
        aluno_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analisa o desempenho do aluno usando IA
        
        Args:
            questoes: Lista de questões da prova
            respostas: Lista de respostas do aluno
            aluno_info: Informações do aluno
            
        Returns:
            Análise detalhada do desempenho
        """
        
        prompt = f"""Você é um especialista em análise pedagógica e educação inclusiva.

**TAREFA:** Analisar o desempenho de um aluno em uma prova.

**INFORMAÇÕES DO ALUNO:**
Nome: {aluno_info.get('nome', 'Não informado')}
Série: {aluno_info.get('serie', 'Não informado')}
Diagnósticos: {aluno_info.get('diagnosticos', 'Nenhum')}

**QUESTÕES E RESPOSTAS:**
{json.dumps({'questoes': questoes, 'respostas': respostas}, ensure_ascii=False, indent=2)}

**INSTRUÇÕES:**
Forneça uma análise detalhada em JSON com:

1. **pontos_fortes**: Lista de áreas onde o aluno foi bem
2. **pontos_melhoria**: Lista de áreas que precisam de atenção
3. **conceitos_dominados**: Conceitos que o aluno demonstrou dominar
4. **conceitos_revisar**: Conceitos que precisam ser revisados
5. **recomendacoes**: Recomendações pedagógicas específicas
6. **adaptacoes_sugeridas**: Sugestões de adaptações para próximas atividades
7. **nivel_compreensao**: Nível geral de compreensão (0-100)

**FORMATO DE SAÍDA:**
Retorne APENAS um JSON válido (sem markdown):

{{
  "pontos_fortes": ["...", "..."],
  "pontos_melhoria": ["...", "..."],
  "conceitos_dominados": ["...", "..."],
  "conceitos_revisar": ["...", "..."],
  "recomendacoes": ["...", "..."],
  "adaptacoes_sugeridas": ["...", "..."],
  "nivel_compreensao": 75
}}

Gere a análise agora:"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.5,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            resposta = message.content[0].text
            analise = self._parse_questoes_json(resposta)
            
            return analise
            
        except Exception as e:
            print(f"❌ Erro ao analisar desempenho: {e}")
            return {
                "pontos_fortes": [],
                "pontos_melhoria": [],
                "conceitos_dominados": [],
                "conceitos_revisar": [],
                "recomendacoes": ["Análise detalhada não disponível"],
                "adaptacoes_sugeridas": [],
                "nivel_compreensao": 0
            }
    
    async def gerar_feedback_personalizado(
        self,
        questoes: List[Dict],
        respostas: List[Dict],
        analise: Dict[str, Any],
        aluno_info: Dict[str, Any]
    ) -> str:
        """
        Gera feedback personalizado para o aluno
        
        Args:
            questoes: Questões da prova
            respostas: Respostas do aluno
            analise: Análise de desempenho
            aluno_info: Informações do aluno
            
        Returns:
            Texto de feedback personalizado
        """
        
        prompt = f"""Você é um educador empático e motivador.

**TAREFA:** Escrever um feedback personalizado e encorajador para o aluno.

**ALUNO:**
{json.dumps(aluno_info, ensure_ascii=False, indent=2)}

**ANÁLISE DE DESEMPENHO:**
{json.dumps(analise, ensure_ascii=False, indent=2)}

**INSTRUÇÕES:**
1. Seja positivo e encorajador
2. Destaque os pontos fortes primeiro
3. Sugira melhorias de forma construtiva
4. Use linguagem adequada à idade/série do aluno
5. Considere os diagnósticos para personalizar o feedback
6. Seja específico sobre o que fazer para melhorar
7. Termine com uma mensagem motivadora

Escreva o feedback (máximo 300 palavras):"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.8,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            feedback = message.content[0].text.strip()
            return feedback
            
        except Exception as e:
            print(f"❌ Erro ao gerar feedback: {e}")
            return "Parabéns por completar a prova! Continue estudando e se esforçando."


# Instância global do serviço
prova_ai_service = ProvaAIService()
