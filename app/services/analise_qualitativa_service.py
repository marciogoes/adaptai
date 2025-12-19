"""
Service de Análise Qualitativa com IA
Analisa respostas dos alunos e gera insights sobre o que melhorar
"""
import anthropic
from typing import Dict, List
from app.core.config import settings
from app.models.prova import ProvaAluno, RespostaAluno, QuestaoGerada, StatusProvaAluno


class AnaliseQualitativaService:
    """
    Service para gerar análises qualitativas das provas usando Claude API
    """
    
    def __init__(self):
        self._client = None
        self.model = "claude-3-haiku-20240307"
    
    @property
    def client(self):
        """Lazy initialization do cliente Anthropic"""
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client
    
    def gerar_analise(self, prova_aluno: ProvaAluno) -> Dict:
        """
        Gera análise qualitativa completa de uma prova
        
        Args:
            prova_aluno: ProvaAluno com respostas
            
        Returns:
            Dict com análise completa
        """
        
        # Verificar se prova está corrigida
        if prova_aluno.status != StatusProvaAluno.CORRIGIDA:
            raise ValueError("Prova precisa estar corrigida para gerar análise")
        
        # Preparar dados para análise
        dados_prova = self._preparar_dados_prova(prova_aluno)
        
        # Gerar prompt para Claude
        prompt = self._criar_prompt_analise(dados_prova, prova_aluno)
        
        # Chamar Claude API
        analise_ia = self._chamar_claude_api(prompt)
        
        # Processar resposta
        analise_processada = self._processar_resposta_ia(analise_ia, dados_prova)
        
        return analise_processada
    
    def _preparar_dados_prova(self, prova_aluno: ProvaAluno) -> Dict:
        """Prepara dados da prova para análise"""
        
        # Agrupar questões por conteúdo/tag
        por_conteudo = {}
        por_dificuldade = {
            'facil': {'acertos': 0, 'erros': 0},
            'medio': {'acertos': 0, 'erros': 0},
            'dificil': {'acertos': 0, 'erros': 0},
            'muito_dificil': {'acertos': 0, 'erros': 0}
        }
        
        questoes_erradas = []
        questoes_certas = []
        
        for resposta in prova_aluno.respostas:
            questao = resposta.questao
            
            # Análise por tags/conteúdo
            if questao.tags:
                for tag in questao.tags:
                    if tag not in por_conteudo:
                        por_conteudo[tag] = {
                            'total': 0,
                            'acertos': 0,
                            'erros': 0,
                            'questoes': []
                        }
                    
                    por_conteudo[tag]['total'] += 1
                    if resposta.esta_correta:
                        por_conteudo[tag]['acertos'] += 1
                    else:
                        por_conteudo[tag]['erros'] += 1
                    
                    por_conteudo[tag]['questoes'].append({
                        'numero': questao.numero,
                        'enunciado': questao.enunciado[:100] + '...',
                        'correta': resposta.esta_correta
                    })
            
            # Análise por dificuldade
            dif = questao.dificuldade.value if questao.dificuldade else 'medio'
            if resposta.esta_correta:
                por_dificuldade[dif]['acertos'] += 1
                questoes_certas.append({
                    'numero': questao.numero,
                    'enunciado': questao.enunciado[:150],
                    'dificuldade': dif,
                    'tags': questao.tags
                })
            else:
                por_dificuldade[dif]['erros'] += 1
                questoes_erradas.append({
                    'numero': questao.numero,
                    'enunciado': questao.enunciado[:150],
                    'resposta_aluno': resposta.resposta_aluno[:200] if resposta.resposta_aluno else '',
                    'resposta_correta': questao.resposta_correta[:200] if questao.resposta_correta else '',
                    'dificuldade': dif,
                    'tags': questao.tags
                })
        
        return {
            'prova': {
                'titulo': prova_aluno.prova.titulo,
                'materia': prova_aluno.prova.materia,
                'serie_nivel': prova_aluno.prova.serie_nivel,
                'nota_final': prova_aluno.nota_final,
                'aprovado': prova_aluno.aprovado
            },
            'aluno': {
                'nome': prova_aluno.aluno.name,
                'serie': prova_aluno.aluno.grade_level
            },
            'desempenho': {
                'total_questoes': len(prova_aluno.respostas),
                'acertos': sum(1 for r in prova_aluno.respostas if r.esta_correta),
                'erros': sum(1 for r in prova_aluno.respostas if not r.esta_correta),
                'percentual_acerto': (sum(1 for r in prova_aluno.respostas if r.esta_correta) / len(prova_aluno.respostas) * 100) if prova_aluno.respostas else 0
            },
            'por_conteudo': por_conteudo,
            'por_dificuldade': por_dificuldade,
            'questoes_erradas': questoes_erradas,
            'questoes_certas': questoes_certas
        }
    
    def _criar_prompt_analise(self, dados: Dict, prova_aluno: ProvaAluno) -> str:
        """Cria prompt para Claude API"""
        
        prompt = f"""Você é um professor especialista em {dados['prova']['materia']} analisando o desempenho de um aluno.

**DADOS DA PROVA:**
- Título: {dados['prova']['titulo']}
- Matéria: {dados['prova']['materia']}
- Nível: {dados['prova']['serie_nivel']}
- Nota Final: {dados['prova']['nota_final']:.1f}/10
- Aprovado: {'Sim' if dados['prova']['aprovado'] else 'Não'}

**ALUNO:**
- Nome: {dados['aluno']['nome']}
- Série: {dados['aluno']['serie']}

**DESEMPENHO GERAL:**
- Total de questões: {dados['desempenho']['total_questoes']}
- Acertos: {dados['desempenho']['acertos']} ({dados['desempenho']['percentual_acerto']:.1f}%)
- Erros: {dados['desempenho']['erros']}

**DESEMPENHO POR DIFICULDADE:**
"""
        
        for dif, stats in dados['por_dificuldade'].items():
            if stats['acertos'] + stats['erros'] > 0:
                prompt += f"- {dif.capitalize()}: {stats['acertos']} acertos, {stats['erros']} erros\n"
        
        if dados['por_conteudo']:
            prompt += "\n**DESEMPENHO POR CONTEÚDO:**\n"
            for conteudo, stats in sorted(dados['por_conteudo'].items(), key=lambda x: x[1]['erros'], reverse=True):
                total = stats['total']
                acertos = stats['acertos']
                erros = stats['erros']
                perc = (acertos / total * 100) if total > 0 else 0
                prompt += f"- {conteudo}: {acertos}/{total} ({perc:.0f}%) - {erros} erros\n"
        
        if dados['questoes_erradas']:
            prompt += f"\n**PRINCIPAIS QUESTÕES ERRADAS ({min(5, len(dados['questoes_erradas']))}):**\n"
            for i, q in enumerate(dados['questoes_erradas'][:5], 1):
                prompt += f"\nQuestão {q['numero']} [{q['dificuldade']}]:\n"
                prompt += f"Enunciado: {q['enunciado']}\n"
                prompt += f"Resposta do aluno: {q['resposta_aluno']}\n"
                prompt += f"Resposta correta: {q['resposta_correta']}\n"
                if q['tags']:
                    prompt += f"Conteúdos: {', '.join(q['tags'])}\n"
        
        prompt += """

**SUA MISSÃO:**
Analise o desempenho do aluno e forneça uma análise qualitativa profunda e construtiva. Responda APENAS com um JSON válido no seguinte formato (sem markdown, sem ```json):

{
  "pontos_fortes": "Descrição dos pontos fortes do aluno (2-3 parágrafos)",
  "pontos_fracos": "Descrição dos pontos fracos e padrões de erros (2-3 parágrafos)",
  "conteudos_revisar": ["Conteúdo 1", "Conteúdo 2", "Conteúdo 3"],
  "recomendacoes": "Recomendações específicas de estudo (2-3 parágrafos com ações concretas)",
  "nivel_dominio": "excelente|bom|regular|precisa_melhorar",
  "areas_prioridade": ["Área prioritária 1", "Área prioritária 2", "Área prioritária 3"],
  "analise_detalhada": "Análise pedagógica detalhada (3-4 parágrafos) explicando o perfil de aprendizado do aluno, padrões observados, e estratégias específicas"
}

IMPORTANTE: 
- Seja específico e construtivo
- Identifique padrões (não só listar erros)
- Dê recomendações ACIONÁVEIS
- Use linguagem pedagógica e empática
- Responda APENAS com o JSON, sem nenhum texto adicional
"""
        
        return prompt
    
    def _chamar_claude_api(self, prompt: str) -> str:
        """Chama Claude API"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            raise Exception(f"Erro ao chamar Claude API: {str(e)}")
    
    def _processar_resposta_ia(self, resposta_ia: str, dados: Dict) -> Dict:
        """Processa resposta da IA e adiciona métricas"""
        
        import json
        
        try:
            # Limpar resposta (remover markdown se houver)
            resposta_limpa = resposta_ia.strip()
            if resposta_limpa.startswith('```json'):
                resposta_limpa = resposta_limpa[7:]
            if resposta_limpa.startswith('```'):
                resposta_limpa = resposta_limpa[3:]
            if resposta_limpa.endswith('```'):
                resposta_limpa = resposta_limpa[:-3]
            resposta_limpa = resposta_limpa.strip()
            
            analise = json.loads(resposta_limpa)
            
            # Adicionar métricas calculadas
            analise['analise_por_conteudo'] = dados['por_conteudo']
            analise['metricas'] = {
                'total_questoes': dados['desempenho']['total_questoes'],
                'acertos': dados['desempenho']['acertos'],
                'erros': dados['desempenho']['erros'],
                'percentual_acerto': dados['desempenho']['percentual_acerto'],
                'nota_final': dados['prova']['nota_final']
            }
            
            return analise
            
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao processar resposta da IA: {str(e)}\nResposta: {resposta_ia[:200]}")


# Instância global
analise_service = AnaliseQualitativaService()
