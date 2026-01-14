"""
Service para geração de materiais adaptados com IA
VERSÃO MEGA COMPLETA: 25+ tipos de materiais
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
    
    def _chamar_ia(self, prompt: str, max_tokens: int = 2048) -> Dict[str, Any]:
        """Método auxiliar para chamar a IA e processar resposta JSON"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.content[0].text.strip()
        result = result.replace("```json", "").replace("```", "").strip()
        return json.loads(result)
    
    # ==========================================
    # 📚 MATERIAIS DE LEITURA
    # ==========================================
    
    def gerar_texto_3_niveis(self, disciplina: str, serie: str, conteudo: str, diagnosticos: Dict[str, Any]) -> Dict[str, Any]:
        """Gera texto adaptado em 3 níveis de complexidade"""
        prompt = f"""Criar texto sobre "{conteudo}" ({disciplina}, {serie}) em 3 NÍVEIS:
BÁSICO: Frases curtas, vocabulário simples, emojis.
INTERMEDIÁRIO: Frases médias, termos explicados.
AVANÇADO: Texto acadêmico completo.

FORMATO JSON:
{{"basico": "texto", "intermediario": "texto", "avancado": "texto", "vocabulario": {{"termo": "definição"}}}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 4096)
    
    def gerar_resumo_estruturado(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera resumo com estrutura visual clara"""
        prompt = f"""Criar RESUMO ESTRUTURADO sobre "{conteudo}" ({disciplina}, {serie}).

Formato: Título → Pontos principais → Detalhes → Conclusão
Use boxes, bullets, numeração.

FORMATO JSON:
{{
  "titulo": "Resumo: [tema]",
  "introducao": "1-2 frases de contexto",
  "pontos_principais": [
    {{"titulo": "Ponto 1", "explicacao": "Explicação", "exemplo": "Exemplo prático", "icone": "📌"}}
  ],
  "palavras_chave": ["termo1", "termo2"],
  "conclusao": "Fechamento",
  "dica_estudo": "Como revisar este conteúdo"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_ficha_leitura(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera ficha de leitura para textos/livros"""
        prompt = f"""Criar FICHA DE LEITURA sobre "{conteudo}" ({disciplina}, {serie}).

FORMATO JSON:
{{
  "titulo": "Ficha de Leitura",
  "dados_obra": {{"titulo": "", "autor": "", "genero": ""}},
  "personagens": [{{"nome": "", "caracteristicas": "", "papel": ""}}],
  "cenario": {{"tempo": "", "lugar": "", "ambiente": ""}},
  "enredo": {{"inicio": "", "desenvolvimento": "", "climax": "", "desfecho": ""}},
  "tema_central": "",
  "mensagem": "",
  "opiniao_pessoal": "Espaço para o aluno escrever",
  "perguntas_reflexao": ["Pergunta 1?", "Pergunta 2?"],
  "conexao_vida": "Como isso se conecta com sua vida?"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    # ==========================================
    # 🎨 MATERIAIS VISUAIS
    # ==========================================
    
    def gerar_infografico(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera infográfico em formato texto estruturado"""
        prompt = f"""Criar INFOGRÁFICO sobre "{conteudo}" ({disciplina}, {serie}).
Use símbolos, emojis, setas, boxes.

FORMATO JSON:
{{"titulo": "título", "conteudo_markdown": "infográfico em markdown", "elementos_visuais": ["sugestão1"]}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_mapa_mental(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera mapa mental"""
        prompt = f"""Criar MAPA MENTAL sobre "{conteudo}" ({disciplina}, {serie}).
Conceito central + 4-6 ramos + sub-ramos.

FORMATO JSON:
{{"tema_central": "tema", "ramos": [{{"titulo": "Ramo", "cor": "azul", "subtopicos": ["sub1", "sub2"]}}]}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_linha_tempo(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Linha do Tempo - eventos em ordem cronológica"""
        prompt = f"""Criar LINHA DO TEMPO sobre "{conteudo}" ({disciplina}, {serie}).
5-8 eventos principais, ordem cronológica.

FORMATO JSON:
{{
  "titulo": "Linha do Tempo: [tema]",
  "periodo": "De X até Y",
  "eventos": [{{"ordem": 1, "data": "Data", "titulo": "Evento", "descricao": "Descrição", "icone": "🔹", "importancia": "alta"}}],
  "curiosidade": "Fato interessante"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_hq_tirinha(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera roteiro de HQ/Tirinha educativa"""
        prompt = f"""Criar roteiro de HQ/TIRINHA sobre "{conteudo}" ({disciplina}, {serie}).
4-6 quadrinhos contando história que ensina o conceito.

FORMATO JSON:
{{
  "titulo": "Título da HQ",
  "personagens": [{{"nome": "Nome", "descricao": "Visual"}}],
  "quadrinhos": [
    {{"numero": 1, "cenario": "Descrição", "acao": "O que acontece", "dialogo": [{{"personagem": "Nome", "fala": "Texto"}}]}}
  ],
  "moral_historia": "O que aprendemos"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_diagrama_venn(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Diagrama de Venn para comparações"""
        prompt = f"""Criar DIAGRAMA DE VENN sobre "{conteudo}" ({disciplina}, {serie}).
Comparar 2 ou 3 conceitos mostrando semelhanças e diferenças.

FORMATO JSON:
{{
  "titulo": "Comparando: [conceitos]",
  "conceito_a": {{"nome": "Conceito A", "cor": "azul", "exclusivo": ["característica só de A"]}},
  "conceito_b": {{"nome": "Conceito B", "cor": "verde", "exclusivo": ["característica só de B"]}},
  "intersecao": ["o que têm em comum"],
  "conclusao": "O que aprendemos com essa comparação"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_tabela_comparativa(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera tabela comparativa"""
        prompt = f"""Criar TABELA COMPARATIVA sobre "{conteudo}" ({disciplina}, {serie}).
Comparar 2-4 elementos em diferentes aspectos.

FORMATO JSON:
{{
  "titulo": "Comparando: [elementos]",
  "elementos": ["Elemento 1", "Elemento 2", "Elemento 3"],
  "criterios": [
    {{"criterio": "Aspecto 1", "valores": ["valor A", "valor B", "valor C"]}},
    {{"criterio": "Aspecto 2", "valores": ["valor A", "valor B", "valor C"]}}
  ],
  "conclusao": "Síntese da comparação"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_arvore_decisao(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera árvore de decisão/fluxograma"""
        prompt = f"""Criar ÁRVORE DE DECISÃO sobre "{conteudo}" ({disciplina}, {serie}).
Fluxo de perguntas sim/não que leva a diferentes conclusões.

FORMATO JSON:
{{
  "titulo": "Árvore de Decisão: [tema]",
  "pergunta_inicial": "Primeira pergunta?",
  "nos": [
    {{
      "id": 1,
      "pergunta": "Pergunta?",
      "sim": {{"vai_para": 2, "ou_resultado": null}},
      "nao": {{"vai_para": null, "ou_resultado": "Conclusão X"}}
    }}
  ],
  "resultados_possiveis": ["Resultado A", "Resultado B"],
  "como_usar": "Instrução de uso"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    # ==========================================
    # 🧠 MATERIAIS DE MEMORIZAÇÃO
    # ==========================================
    
    def gerar_flashcards(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera conjunto de flashcards"""
        prompt = f"""Criar 10-15 FLASHCARDS sobre "{conteudo}" ({disciplina}, {serie}).

FORMATO JSON:
{{"cards": [{{"pergunta": "Pergunta", "resposta": "Resposta", "dica": "Dica opcional"}}]}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_jogo_memoria(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Jogo da Memória - pares de cartas"""
        prompt = f"""Criar JOGO DA MEMÓRIA sobre "{conteudo}" ({disciplina}, {serie}).
8-12 pares de cartas (conceito + definição).

FORMATO JSON:
{{
  "titulo": "Jogo da Memória: [tema]",
  "instrucoes": "Como jogar",
  "pares": [{{"id": 1, "carta_a": {{"texto": "Conceito", "cor": "🔵"}}, "carta_b": {{"texto": "Definição", "cor": "🔵"}}}}],
  "dica_impressao": "Imprimir em cartolina"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_album_figurinhas(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera álbum de figurinhas educativo"""
        prompt = f"""Criar ÁLBUM DE FIGURINHAS sobre "{conteudo}" ({disciplina}, {serie}).
Coleção de "figurinhas" com informações para colecionar.

FORMATO JSON:
{{
  "titulo": "Álbum: [tema]",
  "introducao": "Sobre este álbum",
  "categorias": [
    {{
      "nome": "Categoria 1",
      "cor": "azul",
      "figurinhas": [
        {{
          "numero": 1,
          "nome": "Nome da figurinha",
          "imagem_descricao": "O que desenhar",
          "informacao": "Texto informativo",
          "curiosidade": "Você sabia?",
          "raridade": "comum/rara/lendária"
        }}
      ]
    }}
  ],
  "desafio_completar": "Meta ao completar o álbum"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    # ==========================================
    # 🎮 JOGOS EDUCATIVOS
    # ==========================================
    
    def gerar_caca_palavras(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera caça-palavras adaptado"""
        prompt = f"""Criar CAÇA-PALAVRAS sobre "{conteudo}" ({disciplina}, {serie}).
8-12 palavras-chave, matriz 12x12.

FORMATO JSON:
{{"titulo": "Busca de Termos", "palavras": ["palavra1"], "matriz": [["A","B","C"]], "dicas": ["Dica para palavra1"]}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_cruzadinha(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera palavras cruzadas educativas"""
        prompt = f"""Criar CRUZADINHA sobre "{conteudo}" ({disciplina}, {serie}).
8-12 palavras com dicas.

FORMATO JSON:
{{
  "titulo": "Cruzadinha: [tema]",
  "horizontais": [{{"numero": 1, "dica": "Dica", "resposta": "RESPOSTA"}}],
  "verticais": [{{"numero": 1, "dica": "Dica", "resposta": "RESPOSTA"}}],
  "gabarito": "Lista de respostas"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_bingo_educativo(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera bingo educativo"""
        prompt = f"""Criar BINGO EDUCATIVO sobre "{conteudo}" ({disciplina}, {serie}).
4 cartelas diferentes (5x5).

FORMATO JSON:
{{
  "titulo": "Bingo: [tema]",
  "cartelas": [["item1", "item2", "LIVRE", "item3"]],
  "chamadas": [{{"chamada": "Professor diz...", "resposta": "Aluno marca..."}}]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_domino(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera dominó educativo"""
        prompt = f"""Criar DOMINÓ EDUCATIVO sobre "{conteudo}" ({disciplina}, {serie}).
12-16 peças que conectam conceitos.

FORMATO JSON:
{{
  "titulo": "Dominó: [tema]",
  "instrucoes": "Como jogar",
  "pecas": [{{"id": 1, "lado_a": {{"texto": "Conceito"}}, "lado_b": {{"texto": "Definição"}}}}],
  "regra_conexao": "Como conectar"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_quiz_interativo(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera quiz interativo com feedback"""
        prompt = f"""Criar QUIZ INTERATIVO sobre "{conteudo}" ({disciplina}, {serie}).
10 perguntas com feedback.

FORMATO JSON:
{{
  "titulo": "Quiz: [tema]",
  "perguntas": [
    {{
      "numero": 1,
      "pergunta": "Pergunta",
      "alternativas": ["a) opção", "b) opção"],
      "correta": "b",
      "feedback_correto": "Parabéns!",
      "feedback_incorreto": "Tente novamente...",
      "dica": "Dica"
    }}
  ]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_trilha_aprendizagem(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera trilha/jogo de tabuleiro educativo"""
        prompt = f"""Criar TRILHA DE APRENDIZAGEM (jogo de tabuleiro) sobre "{conteudo}" ({disciplina}, {serie}).
20-25 casas com desafios, perguntas e ações.

FORMATO JSON:
{{
  "titulo": "Trilha: [tema]",
  "instrucoes": "Como jogar (dado, peões)",
  "casas": [
    {{
      "numero": 1,
      "tipo": "pergunta/desafio/sorte/azar/bonus",
      "conteudo": "O que acontece nesta casa",
      "acao": "avance X casas / volte X casas / fique 1 rodada",
      "cor": "verde"
    }}
  ],
  "casa_final": "O que acontece ao chegar",
  "materiais_necessarios": ["dado", "peões"]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 3072)
    
    def gerar_roleta_perguntas(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera roleta de perguntas"""
        prompt = f"""Criar ROLETA DE PERGUNTAS sobre "{conteudo}" ({disciplina}, {serie}).
8 categorias com 3-4 perguntas cada.

FORMATO JSON:
{{
  "titulo": "Roleta: [tema]",
  "instrucoes": "Gire a roleta e responda!",
  "categorias": [
    {{
      "nome": "Categoria",
      "cor": "azul",
      "perguntas": [
        {{"pergunta": "Pergunta?", "resposta": "Resposta", "pontos": 10}}
      ]
    }}
  ]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    # ==========================================
    # 💙 MATERIAIS PARA TEA/TDAH/DI
    # ==========================================
    
    def gerar_historia_social(self, disciplina: str, serie: str, conteudo: str, diagnosticos: Dict[str, Any] = None) -> Dict[str, Any]:
        """Gera História Social - narrativas para TEA/TDAH"""
        prompt = f"""Criar HISTÓRIA SOCIAL sobre "{conteudo}" ({disciplina}, {serie}).

História em 1ª pessoa, linguagem CONCRETA e LITERAL.
Estrutura: Situação → O que acontece → O que EU devo fazer → Resultado positivo.

REGRAS IMPORTANTES:
- Frases curtas (máx 10 palavras)
- EVITE metáforas, ironias, linguagem figurada
- Use "Eu posso...", "Eu vou tentar...", "Está tudo bem se..."
- 8-10 frases no total
- Inclua emojis para reforço visual

FORMATO JSON:
{{
  "titulo": "Título da História",
  "situacao": "Descrição da situação",
  "historia": "Texto completo da história social (cada frase em linha nova)",
  "frases_chave": ["frase 1 para memorizar", "frase 2"],
  "icones": ["🏫", "👋", "😊"],
  "dica_professor": "Como usar esta história",
  "frequencia_uso": "Quando ler com o aluno"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_sequenciamento(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Sequenciamento Visual - passo a passo de tarefas"""
        prompt = f"""Criar SEQUENCIAMENTO VISUAL (passo a passo) para "{conteudo}" ({disciplina}, {serie}).

5-8 etapas simples, 1 ÚNICA AÇÃO por etapa.
Verbos no imperativo. Frases CURTAS.

FORMATO JSON:
{{
  "titulo": "Como fazer: [atividade]",
  "objetivo": "O que vai conseguir fazer",
  "materiais": ["item 1", "item 2"],
  "etapas": [
    {{
      "numero": 1,
      "acao": "Ação curta (máx 6 palavras)",
      "icone": "📝",
      "imagem_sugerida": "Descrição do que desenhar",
      "dica": "Dica opcional",
      "checkpoint": "Como saber que fez certo"
    }}
  ],
  "verificacao_final": "Pergunta para confirmar término",
  "parabens": "Mensagem de parabéns",
  "proximo_passo": "O que fazer depois"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_quadro_rotina(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Quadro de Rotina visual"""
        prompt = f"""Criar QUADRO DE ROTINA para "{conteudo}" ({disciplina}, {serie}).

Estrutura visual de atividades com horários e ícones.
Previsibilidade e organização.

FORMATO JSON:
{{
  "titulo": "Minha Rotina: [atividade]",
  "periodo": "Manhã/Tarde/Dia todo",
  "itens": [
    {{
      "ordem": 1,
      "horario": "08:00",
      "atividade": "Nome da atividade",
      "icone": "📚",
      "duracao": "30 min",
      "local": "Onde fazer",
      "material": "O que precisa",
      "cor": "azul"
    }}
  ],
  "transicoes": ["Aviso 5 min antes de trocar"],
  "recompensa": "O que ganho ao completar",
  "dica_uso": "Colocar em local visível"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_cartoes_comunicacao(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Cartões de Comunicação Alternativa (CAA)"""
        prompt = f"""Criar CARTÕES DE COMUNICAÇÃO (CAA) sobre "{conteudo}" ({disciplina}, {serie}).

Cartões visuais para comunicação alternativa.
Cada cartão: símbolo + palavra + categoria.

FORMATO JSON:
{{
  "titulo": "Cartões: [tema]",
  "categoria_principal": "Categoria",
  "cartoes": [
    {{
      "id": 1,
      "palavra": "Palavra",
      "descricao_imagem": "O que desenhar",
      "categoria": "substantivo/verbo/adjetivo/frase",
      "cor_fundo": "azul/verde/amarelo/vermelho",
      "tamanho": "grande/medio",
      "uso_frase": "Como usar: Eu quero [palavra]"
    }}
  ],
  "frases_modelo": ["Frase 1", "Frase 2"],
  "dica_impressao": "Plastificar para durabilidade"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_termometro_emocoes(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Termômetro de Emoções"""
        prompt = f"""Criar TERMÔMETRO DE EMOÇÕES relacionado a "{conteudo}" ({disciplina}, {serie}).

Escala visual de emoções/estados com estratégias.

FORMATO JSON:
{{
  "titulo": "Como estou me sentindo?",
  "contexto": "Situação/atividade",
  "niveis": [
    {{
      "nivel": 5,
      "cor": "vermelho",
      "emocao": "Muito nervoso/bravo",
      "sinais_corpo": ["coração acelerado", "mãos suadas"],
      "o_que_fazer": ["respirar fundo", "pedir ajuda"],
      "icone": "🔴"
    }},
    {{
      "nivel": 4,
      "cor": "laranja",
      "emocao": "Irritado",
      "sinais_corpo": ["inquieto"],
      "o_que_fazer": ["contar até 10"],
      "icone": "🟠"
    }},
    {{
      "nivel": 3,
      "cor": "amarelo",
      "emocao": "Preocupado",
      "sinais_corpo": ["pensamentos rápidos"],
      "o_que_fazer": ["falar com alguém"],
      "icone": "🟡"
    }},
    {{
      "nivel": 2,
      "cor": "azul claro",
      "emocao": "Calmo",
      "sinais_corpo": ["respiração normal"],
      "o_que_fazer": ["continuar assim"],
      "icone": "🔵"
    }},
    {{
      "nivel": 1,
      "cor": "verde",
      "emocao": "Tranquilo e feliz",
      "sinais_corpo": ["relaxado", "sorrindo"],
      "o_que_fazer": ["aproveitar o momento"],
      "icone": "🟢"
    }}
  ],
  "como_usar": "Aponte como está se sentindo"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_contrato_comportamento(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Contrato de Comportamento"""
        prompt = f"""Criar CONTRATO DE COMPORTAMENTO para "{conteudo}" ({disciplina}, {serie}).

Acordo visual com regras, recompensas e consequências.

FORMATO JSON:
{{
  "titulo": "Meu Contrato",
  "objetivo": "O que queremos alcançar",
  "regras": [
    {{"numero": 1, "regra": "Regra clara e positiva", "icone": "✅"}}
  ],
  "recompensas": [
    {{"conquista": "Se eu fizer...", "ganho": "Eu ganho...", "icone": "⭐"}}
  ],
  "consequencias": [
    {{"se": "Se eu não fizer...", "entao": "Então...", "icone": "⚠️"}}
  ],
  "assinaturas": ["Aluno: ___", "Professor: ___", "Família: ___"],
  "data_inicio": "___/___/___",
  "revisao": "Vamos revisar em: ___"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_checklist_tarefas(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Checklist de Tarefas visual"""
        prompt = f"""Criar CHECKLIST DE TAREFAS para "{conteudo}" ({disciplina}, {serie}).

Lista visual com boxes para marcar.

FORMATO JSON:
{{
  "titulo": "Checklist: [atividade]",
  "instrucao": "Marque cada item ao completar",
  "itens": [
    {{
      "ordem": 1,
      "tarefa": "Tarefa curta",
      "detalhes": "O que significa",
      "icone": "📝",
      "checkbox": "[ ]"
    }}
  ],
  "ao_completar": "O que fazer quando terminar tudo",
  "recompensa": "Parabéns por completar!"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_painel_primeiro_depois(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera Painel Primeiro-Depois (First-Then)"""
        prompt = f"""Criar PAINEL PRIMEIRO-DEPOIS para "{conteudo}" ({disciplina}, {serie}).

Estrutura visual: PRIMEIRO faço X, DEPOIS ganho Y.

FORMATO JSON:
{{
  "titulo": "Primeiro - Depois",
  "contexto": "Situação/atividade",
  "sequencias": [
    {{
      "primeiro": {{
        "atividade": "O que preciso fazer",
        "icone": "📚",
        "tempo": "15 minutos",
        "descricao_visual": "Imagem sugerida"
      }},
      "depois": {{
        "recompensa": "O que vou ganhar/fazer",
        "icone": "🎮",
        "descricao_visual": "Imagem sugerida"
      }}
    }}
  ],
  "dica_uso": "Como usar este painel"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    # ==========================================
    # ✍️ ATIVIDADES DE COMPLETAR
    # ==========================================
    
    def gerar_complete_lacunas(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera atividade de completar lacunas"""
        prompt = f"""Criar COMPLETE AS LACUNAS sobre "{conteudo}" ({disciplina}, {serie}).
8-10 frases com lacunas + banco de palavras.

FORMATO JSON:
{{
  "titulo": "Complete as Lacunas: [tema]",
  "banco_palavras": ["palavra1", "palavra2"],
  "frases": [{{"numero": 1, "texto": "O _____ é...", "resposta": "termo", "dica": "Dica"}}],
  "gabarito": ["1-termo"]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_ligue_colunas(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera atividade de ligar colunas"""
        prompt = f"""Criar LIGUE AS COLUNAS sobre "{conteudo}" ({disciplina}, {serie}).
8-10 pares para conectar.

FORMATO JSON:
{{
  "titulo": "Ligue as Colunas: [tema]",
  "coluna_a": [{{"id": 1, "texto": "Conceito"}}],
  "coluna_b": [{{"id": "A", "texto": "Definição"}}],
  "gabarito": [{{"a": 1, "b": "A"}}]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_verdadeiro_falso(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera atividade de Verdadeiro ou Falso"""
        prompt = f"""Criar VERDADEIRO OU FALSO sobre "{conteudo}" ({disciplina}, {serie}).
10-12 afirmações.

FORMATO JSON:
{{
  "titulo": "V ou F: [tema]",
  "afirmacoes": [{{"numero": 1, "texto": "Afirmação", "resposta": "V", "explicacao": "Por quê"}}],
  "gabarito": ["1-V", "2-F"]
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_ordenar_sequencia(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera atividade de ordenar sequência"""
        prompt = f"""Criar ORDENE A SEQUÊNCIA sobre "{conteudo}" ({disciplina}, {serie}).
6-8 itens para colocar em ordem.

FORMATO JSON:
{{
  "titulo": "Ordene: [tema]",
  "instrucao": "Coloque em ordem",
  "itens_embaralhados": [
    {{"letra": "A", "texto": "Item fora de ordem"}}
  ],
  "ordem_correta": ["C", "A", "B", "D"],
  "dica": "Como pensar na ordem"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    # ==========================================
    # 📝 AVALIAÇÕES
    # ==========================================
    
    def gerar_avaliacao_multiformato(self, disciplina: str, serie: str, conteudo: str, diagnosticos: Dict[str, Any]) -> Dict[str, Any]:
        """Gera avaliação em 3 formatos diferentes"""
        prompt = f"""Criar AVALIAÇÃO em 3 FORMATOS sobre "{conteudo}" ({disciplina}, {serie}).

FORMATO A - Prova Padrão: 10 questões mistas
FORMATO B - Prova Adaptada: 5-7 questões simplificadas
FORMATO C - Roteiro Oral: 5 perguntas para professor

FORMATO JSON:
{{
  "formato_a": {{"titulo": "Avaliação", "questoes": [{{"numero": 1, "tipo": "multipla_escolha", "enunciado": "...", "alternativas": ["a).."], "correta": "a"}}]}},
  "formato_b": {{"titulo": "Avaliação Adaptada", "questoes": [...], "adaptacoes": "Tempo estendido"}},
  "formato_c": {{"titulo": "Roteiro Oral", "questoes": [{{"pergunta": "...", "respostas_aceitas": ["..."]}}]}}
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 4096)
    
    # ==========================================
    # 🔬 MATERIAIS PRÁTICOS
    # ==========================================
    
    def gerar_experimento(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera roteiro de experimento/atividade prática"""
        prompt = f"""Criar EXPERIMENTO sobre "{conteudo}" ({disciplina}, {serie}).

FORMATO JSON:
{{
  "titulo": "Experimento: [tema]",
  "objetivo": "O que vamos descobrir",
  "materiais": [{{"item": "Material", "quantidade": "X", "alternativa": "Substituição"}}],
  "procedimento": [{{"passo": 1, "acao": "O que fazer", "cuidado": "Atenção"}}],
  "resultado_esperado": "O que deve acontecer",
  "explicacao": "Por que acontece",
  "perguntas": ["Pergunta 1?"],
  "seguranca": "Cuidados"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_receita_procedimento(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera formato receita/procedimento"""
        prompt = f"""Criar RECEITA/PROCEDIMENTO sobre "{conteudo}" ({disciplina}, {serie}).
Formato de receita culinária aplicado ao conteúdo.

FORMATO JSON:
{{
  "titulo": "Receita de: [conceito]",
  "tempo": "X minutos",
  "ingredientes": [{{"item": "Conceito", "quantidade": "Como usar"}}],
  "modo_preparo": [{{"passo": 1, "instrucao": "Fazer X", "dica": "Dica"}}],
  "resultado": "O que esperar"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_estudo_caso(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera estudo de caso"""
        prompt = f"""Criar ESTUDO DE CASO sobre "{conteudo}" ({disciplina}, {serie}).

FORMATO JSON:
{{
  "titulo": "Caso: [nome]",
  "contexto": "Descrição da situação",
  "personagens": [{{"nome": "Nome", "papel": "Quem é"}}],
  "problema": "O desafio a resolver",
  "perguntas": [{{"numero": 1, "pergunta": "Pergunta"}}],
  "possiveis_solucoes": ["Solução 1"],
  "conclusao": "O que aprender"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
    
    def gerar_diario_bordo(self, disciplina: str, serie: str, conteudo: str) -> Dict[str, Any]:
        """Gera modelo de Diário de Bordo"""
        prompt = f"""Criar DIÁRIO DE BORDO para "{conteudo}" ({disciplina}, {serie}).

Modelo para o aluno registrar aprendizados.

FORMATO JSON:
{{
  "titulo": "Meu Diário de Bordo: [tema]",
  "paginas": [
    {{
      "data": "___/___/___",
      "secoes": [
        {{"titulo": "O que aprendi hoje", "espaco": "linhas para escrever", "icone": "📚"}},
        {{"titulo": "Minhas dúvidas", "espaco": "linhas", "icone": "❓"}},
        {{"titulo": "O que mais gostei", "espaco": "linhas", "icone": "⭐"}},
        {{"titulo": "Desenho/Esquema", "espaco": "área para desenhar", "icone": "🎨"}}
      ]
    }}
  ],
  "reflexao_final": "Espaço para reflexão ao terminar o tema"
}}
Retorne APENAS o JSON."""
        return self._chamar_ia(prompt, 2048)
