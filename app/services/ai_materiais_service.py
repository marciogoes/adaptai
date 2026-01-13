"""
Service para geração de materiais adaptados com IA
ATUALIZADO: Novos tipos de materiais (história social, sequenciamento, linha do tempo, jogo da memória)
"""
import json
from typing import Dict, Any, List
from anthropic import Anthropic
from app.core.config import settings


class MaterialAdaptadoService:
    """Serviço para gerar materiais educacionais adaptados"""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
    
    def gerar_texto_3_niveis(
        self, 
        disciplina: str, 
        serie: str, 
        conteudo: str,
        diagnosticos: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera texto adaptado em 3 níveis de complexidade"""
        
        prompt = f"""Você é um especialista em educação inclusiva e adaptação curricular.

TAREFA: Criar um texto explicativo sobre o tema em 3 NÍVEIS de complexidade.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}
- Diagnósticos do aluno: {json.dumps(diagnosticos, ensure_ascii=False)}

NÍVEIS DE ADAPTAÇÃO:

NÍVEL 1 (Básico): Frases curtas, vocabulário simples, emojis, 3-4 parágrafos.
NÍVEL 2 (Intermediário): Frases médias, termos técnicos explicados, bullets, 5-7 parágrafos.
NÍVEL 3 (Avançado): Texto acadêmico completo com aprofundamentos.

FORMATO DE RESPOSTA (JSON):
{{
  "basico": "texto do nível 1",
  "intermediario": "texto do nível 2",
  "avancado": "texto do nível 3",
  "vocabulario": {{"termo1": "definição simples"}}
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_infografico(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera infográfico em formato texto estruturado"""
        
        prompt = f"""Você é um designer educacional especializado em infográficos.

TAREFA: Criar um INFOGRÁFICO sobre {conteudo} ({disciplina}, {serie}).

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "título do infográfico",
  "conteudo_markdown": "infográfico formatado em markdown",
  "elementos_visuais": ["sugestão 1", "sugestão 2"]
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_flashcards(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera conjunto de flashcards"""
        
        prompt = f"""Criar 10-15 FLASHCARDS sobre {conteudo} ({disciplina}, {serie}).

FORMATO DE RESPOSTA (JSON):
{{
  "cards": [
    {{"pergunta": "Pergunta", "resposta": "Resposta", "dica": "Dica opcional"}}
  ]
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_caca_palavras(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera caça-palavras adaptado"""
        
        prompt = f"""Criar CAÇA-PALAVRAS sobre {conteudo} ({disciplina}, {serie}).

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "BUSCA DE TERMOS: [tema]",
  "palavras": ["palavra1", "palavra2"],
  "matriz": [["A", "B", "C"]],
  "tamanho": "12x12"
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_bingo_educativo(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera bingo educativo"""
        
        prompt = f"""Criar BINGO EDUCATIVO sobre {conteudo} ({disciplina}, {serie}).

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "BINGO: [tema]",
  "cartelas": [["item1", "item2", "LIVRE", "item3"]],
  "chamadas": [{{"chamada": "Professor diz...", "resposta": "Aluno marca..."}}]
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_avaliacao_multiformato(
        self, disciplina: str, serie: str, conteudo: str, diagnosticos: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera avaliação em 3 formatos diferentes"""
        
        prompt = f"""Criar AVALIAÇÃO em 3 FORMATOS sobre {conteudo} ({disciplina}, {serie}).
Diagnósticos: {json.dumps(diagnosticos, ensure_ascii=False)}

FORMATO A - Prova Escrita Padrão (10 questões)
FORMATO B - Prova Adaptada (5-7 questões simplificadas)
FORMATO C - Roteiro de Avaliação Oral (5 perguntas)

FORMATO DE RESPOSTA (JSON):
{{
  "formato_a": {{"titulo": "...", "questoes": [...]}},
  "formato_b": {{"titulo": "...", "questoes": [...], "observacoes": "..."}},
  "formato_c": {{"titulo": "...", "questoes": [...]}}
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_mapa_mental(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera mapa mental"""
        
        prompt = f"""Criar MAPA MENTAL sobre {conteudo} ({disciplina}, {serie}).

FORMATO DE RESPOSTA (JSON):
{{
  "tema_central": "tema principal",
  "ramos": [
    {{"titulo": "Ramo 1", "subtopicos": ["sub1", "sub2"]}}
  ]
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)

    # ==========================================
    # NOVOS MATERIAIS ADAPTADOS
    # ==========================================
    
    def gerar_historia_social(
        self,
        disciplina: str,
        serie: str,
        conteudo: str,
        diagnosticos: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Gera História Social - muito útil para TEA e TDAH
        Narrativas que ensinam comportamentos e situações sociais
        """
        
        prompt = f"""Você é um especialista em educação inclusiva e histórias sociais para crianças com TEA.

TAREFA: Criar uma HISTÓRIA SOCIAL sobre o tema/situação.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema/Situação: {conteudo}

O QUE É UMA HISTÓRIA SOCIAL:
- Narrativa curta em 1ª pessoa
- Descreve uma situação específica
- Explica comportamentos esperados
- Usa linguagem CONCRETA e LITERAL
- Ajuda a entender regras sociais implícitas

ESTRUTURA:
1. Introdução: Descreve a situação/contexto
2. Desenvolvimento: O que acontece, o que as pessoas fazem/sentem
3. Comportamento Esperado: O que EU devo fazer
4. Consequência Positiva: O que acontece quando faço certo

REGRAS:
- Frases curtas e diretas
- Evite metáforas, ironias ou linguagem figurada
- Use "Eu posso...", "Eu vou tentar...", "Está tudo bem se..."
- Máximo 8-10 frases

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "Título da História",
  "situacao": "Descrição breve da situação",
  "historia": "Texto completo da história social",
  "frases_chave": ["frase 1 para memorizar", "frase 2"],
  "icones": ["🏫", "👋", "😊"],
  "dica_professor": "Como usar esta história"
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_sequenciamento(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """
        Gera Sequenciamento Visual - etapas ilustradas de uma tarefa/processo
        Muito útil para TEA, DI e TDAH
        """
        
        prompt = f"""Você é um especialista em educação inclusiva e análise de tarefas.

TAREFA: Criar um SEQUENCIAMENTO VISUAL (passo a passo) para: {conteudo}

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}

ESTRUTURA:
1. Objetivo final claro
2. 5-8 etapas sequenciais
3. Cada etapa com: número, ação, ícone
4. Checklist para marcar

REGRAS:
- 1 ação por etapa
- Verbos no imperativo
- Frases de no máximo 8 palavras

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "Como fazer [atividade]",
  "objetivo": "O que vai conseguir fazer no final",
  "materiais": ["item 1", "item 2"],
  "etapas": [
    {{"numero": 1, "acao": "Ação curta", "icone": "📝", "dica": "Dica opcional"}}
  ],
  "verificacao": "Pergunta para confirmar que terminou",
  "parabens": "Mensagem de parabéns"
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_linha_tempo(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """
        Gera Linha do Tempo - eventos em ordem cronológica
        Útil para História, Ciências, Português
        """
        
        prompt = f"""Criar LINHA DO TEMPO sobre {conteudo} ({disciplina}, {serie}).

ESTRUTURA:
- 5-8 eventos/marcos principais
- Cada evento com: data/período, título, descrição curta
- Conexões entre eventos

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "Linha do Tempo: [tema]",
  "periodo": "De [início] até [fim]",
  "eventos": [
    {{
      "ordem": 1,
      "data": "Data ou período",
      "titulo": "Nome do evento",
      "descricao": "Descrição curta",
      "icone": "🔹",
      "importancia": "alta/media/baixa"
    }}
  ],
  "curiosidade": "Fato interessante"
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_jogo_memoria(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """
        Gera Jogo da Memória - pares de cartas com conceitos
        Útil para memorização e associação
        """
        
        prompt = f"""Criar JOGO DA MEMÓRIA educativo sobre {conteudo} ({disciplina}, {serie}).

ESTRUTURA:
- 8-12 pares de cartas
- Cada par conecta: conceito + definição, pergunta + resposta, etc.

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "Jogo da Memória: [tema]",
  "instrucoes": "Como jogar",
  "pares": [
    {{
      "id": 1,
      "carta_a": {{"texto": "Conceito", "tipo": "conceito", "cor": "🔵"}},
      "carta_b": {{"texto": "Definição", "tipo": "definicao", "cor": "🔵"}}
    }}
  ],
  "dica_impressao": "Imprimir em cartolina"
}}

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
