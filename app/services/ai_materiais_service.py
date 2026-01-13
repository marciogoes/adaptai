"""
Service para geração de materiais adaptados com IA
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

NÍVEL 1 (Básico - Deficiência Intelectual, TEA severo):
- Frases MUITO curtas (máx 5-7 palavras)
- Vocabulário SIMPLES
- 1 ideia por parágrafo
- Use emojis e símbolos
- Conceitos concretos, evite abstrações
- Tamanho: 3-4 parágrafos pequenos

NÍVEL 2 (Intermediário - TDAH, Dislexia, TEA leve/moderado):
- Frases médias (8-12 palavras)
- Vocabulário acessível com alguns termos técnicos EXPLICADOS
- Use bullets, numeração, destaques
- Organize informação em blocos visuais
- Tamanho: 5-7 parágrafos ou tópicos

NÍVEL 3 (Avançado - Superdotação, sem dificuldades):
- Texto acadêmico completo
- Vocabulário técnico apropriado
- Conexões interdisciplinares
- Aprofundamentos e desafios
- Tamanho: texto completo detalhado

Além dos 3 textos, crie um GLOSSÁRIO com 5-8 termos técnicos principais e suas definições simples.

FORMATO DE RESPOSTA (JSON):
{{
  "nivel_1": "texto do nível 1",
  "nivel_2": "texto do nível 2",
  "nivel_3": "texto do nível 3",
  "vocabulario_tecnico": {{
    "termo1": "definição simples",
    "termo2": "definição simples"
  }}
}}

Retorne APENAS o JSON, sem markdown nem explicações."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        # Limpar markdown se houver
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_infografico(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """Gera infográfico em formato markdown/texto estruturado"""
        
        prompt = f"""Você é um designer educacional especializado em infográficos.

TAREFA: Criar um INFOGRÁFICO em formato texto/markdown sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}

ESTRUTURA DO INFOGRÁFICO:
1. Título impactante
2. Conceito central grande
3. 3-5 blocos de informação visual
4. Use símbolos, emojis, setas (→, ←, ↓, ↑)
5. Boxes, tabelas, diagramas em texto
6. Destaque números e dados importantes

Além do infográfico, sugira 3-5 elementos visuais que podem ser adicionados (fotos, ícones, gráficos).

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "título do infográfico",
  "conteudo_markdown": "infográfico formatado em markdown/texto",
  "elementos_visuais": ["sugestão 1", "sugestão 2", "sugestão 3"]
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
    
    def gerar_flashcards(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """Gera conjunto de flashcards"""
        
        prompt = f"""Você é um especialista em técnicas de memorização e estudo.

TAREFA: Criar 10-15 FLASHCARDS sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}

ESTRUTURA DE CADA FLASHCARD:
- FRENTE: Pergunta, termo, conceito, fórmula
- VERSO: Resposta, definição, explicação
- DICA: (opcional) Mnemônico, exemplo, imagem sugerida

TIPOS DE CARDS:
- Definições (O que é...?)
- Fórmulas (Qual a fórmula de...?)
- Aplicações (Quando usar...?)
- Exemplos (Dê um exemplo de...)
- Comparações (Diferença entre... e...?)

FORMATO DE RESPOSTA (JSON):
{{
  "cards": [
    {{
      "frente": "Pergunta ou termo",
      "verso": "Resposta ou definição",
      "dica": "Dica opcional"
    }}
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
    
    def gerar_caca_palavras(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """Gera caça-palavras adaptado"""
        
        prompt = f"""Você é um criador de atividades educativas.

TAREFA: Criar CAÇA-PALAVRAS (ou "BUSCA DE TERMOS") sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}

INSTRUÇÕES:
1. Liste 8-12 TERMOS-CHAVE relacionados ao tema
2. Termos devem ser técnicos/acadêmicos (não infantilizar)
3. Crie uma matriz 12x12 com as palavras escondidas
4. Palavras podem estar: horizontal →, vertical ↓, diagonal ↘
5. Preencha espaços vazios com letras aleatórias

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "BUSCA DE TERMOS: [tema]",
  "palavras": ["palavra1", "palavra2", ...],
  "matriz": [
    ["A", "B", "C", ...],
    ["D", "E", "F", ...],
    ...
  ],
  "tamanho": "12x12",
  "nivel_dificuldade": "médio"
}}

IMPORTANTE: A matriz deve ser uma lista de 12 listas, cada uma com 12 letras.

Retorne APENAS o JSON."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3072,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    def gerar_bingo_educativo(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """Gera bingo educativo"""
        
        prompt = f"""Você é um criador de jogos educativos.

TAREFA: Criar BINGO EDUCATIVO sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}

ESTRUTURA:
1. Determine o tipo de bingo:
   - Termos técnicos
   - Fórmulas
   - Conceitos
   - Símbolos/elementos

2. Crie 4 cartelas diferentes (5x5 cada)

3. Para cada item possível:
   - CHAMADA: O que o professor vai dizer/perguntar
   - RESPOSTA: O que está na cartela

EXEMPLO:
Professor chama: "Número atômico 6"
Aluno marca na cartela: "C" (Carbono)

FORMATO DE RESPOSTA (JSON):
{{
  "titulo": "BINGO: [tema]",
  "tipo": "termos/formulas/conceitos",
  "cartelas": [
    ["item1", "item2", "item3", "item4", "item5",
     "item6", "item7", "LIVRE", "item8", "item9",
     ...],
    [cartela 2],
    [cartela 3],
    [cartela 4]
  ],
  "chamadas": [
    {{"chamada": "Professor diz...", "resposta": "Aluno marca..."}},
    ...
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
    
    def gerar_avaliacao_multiformato(
        self,
        disciplina: str,
        serie: str,
        conteudo: str,
        diagnosticos: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera avaliação em 3 formatos diferentes"""
        
        prompt = f"""Você é um especialista em avaliação educacional inclusiva.

TAREFA: Criar AVALIAÇÃO em 3 FORMATOS sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}
- Diagnósticos: {json.dumps(diagnosticos, ensure_ascii=False)}

FORMATO A - Prova Escrita Padrão:
- 10 questões
- Múltipla escolha e discursivas
- Formato tradicional

FORMATO B - Prova Adaptada:
- 5-7 questões
- Uma questão por página
- Enunciados curtos e claros
- Imagens/diagramas quando possível
- Espaço ampliado para respostas
- Banco de palavras para completar

FORMATO C - Avaliação Oral (Roteiro para Professor):
- 5 perguntas-chave
- Como fazer a pergunta
- O que aceitar como resposta correta
- Critérios de avaliação

FORMATO DE RESPOSTA (JSON):
{{
  "formato_a": {{
    "titulo": "Avaliação - [tema]",
    "questoes": [
      {{
        "numero": 1,
        "tipo": "multipla_escolha",
        "enunciado": "...",
        "alternativas": ["a) ...", "b) ...", "c) ...", "d) ..."],
        "resposta_correta": "b"
      }},
      {{
        "numero": 2,
        "tipo": "discursiva",
        "enunciado": "...",
        "criterios_correcao": "..."
      }}
    ]
  }},
  "formato_b": {{
    "titulo": "Avaliação Adaptada - [tema]",
    "questoes": [...],
    "observacoes": "Tempo estendido: 2x. Permitido uso de calculadora."
  }},
  "formato_c": {{
    "titulo": "Roteiro de Avaliação Oral - [tema]",
    "questoes": [
      {{
        "numero": 1,
        "pergunta_professor": "Como fazer a pergunta",
        "respostas_aceitas": ["resposta 1", "resposta 2"],
        "criterios": [
          "Critério 1 para avaliar",
          "Critério 2 para avaliar"
        ]
      }}
    ]
  }}
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
    
    def gerar_mapa_mental(
        self,
        disciplina: str,
        serie: str,
        conteudo: str
    ) -> Dict[str, Any]:
        """Gera mapa mental em formato Mermaid"""
        
        prompt = f"""Você é um especialista em organização visual de conhecimento.

TAREFA: Criar MAPA MENTAL sobre o tema.

INFORMAÇÕES:
- Disciplina: {disciplina}
- Série: {serie}
- Tema: {conteudo}

ESTRUTURA:
1. Conceito central
2. 4-6 ramos principais
3. Cada ramo com 2-4 sub-ramos
4. Use cores/ícones para categorizar

Além da estrutura em JSON, crie o código MERMAID para visualização.

FORMATO DE RESPOSTA (JSON):
{{
  "conceito_central": "tema principal",
  "ramos_principais": [
    {{
      "titulo": "Ramo 1",
      "cor": "azul",
      "subramos": ["sub1", "sub2", "sub3"]
    }}
  ],
  "markdown_mermaid": "código mermaid aqui"
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
