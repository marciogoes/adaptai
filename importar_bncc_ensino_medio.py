# ============================================
# IMPORTAR HABILIDADES BNCC - ENSINO MÉDIO
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

# BNCC Ensino Médio - Organizado por Áreas do Conhecimento
HABILIDADES_ENSINO_MEDIO = [
    # ============================================
    # MATEMÁTICA E SUAS TECNOLOGIAS
    # ============================================
    # 1º Ano
    {"codigo_bncc": "EM13MAT101", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Conjuntos numéricos",
     "habilidade_descricao": "Interpretar criticamente situações econômicas, sociais e fatos relativos às Ciências da Natureza que envolvam a variação de grandezas, pela análise dos gráficos das funções representadas e das taxas de variação."},
    
    {"codigo_bncc": "EM13MAT102", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Funções",
     "habilidade_descricao": "Analisar funções definidas por uma ou mais sentenças, identificando domínio, imagem, crescimento, decrescimento e zeros."},
    
    {"codigo_bncc": "EM13MAT103", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Função afim",
     "habilidade_descricao": "Interpretar e compreender o conceito de função afim, representando-a graficamente e identificando suas características."},
    
    {"codigo_bncc": "EM13MAT104", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Função quadrática",
     "habilidade_descricao": "Analisar e compreender a função quadrática, identificando vértice, zeros, concavidade e representação gráfica."},
    
    {"codigo_bncc": "EM13MAT105", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Progressões",
     "habilidade_descricao": "Resolver e elaborar problemas com sequências, identificando padrões e utilizando progressões aritméticas e geométricas."},
    
    {"codigo_bncc": "EM13MAT106", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Matemática financeira",
     "habilidade_descricao": "Compreender e utilizar conceitos de matemática financeira como juros simples e compostos, descontos e taxas."},
    
    {"codigo_bncc": "EM13MAT107", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Estatística",
     "habilidade_descricao": "Interpretar e comparar conjuntos de dados estatísticos por meio de medidas de tendência central e dispersão."},
    
    # 2º Ano
    {"codigo_bncc": "EM13MAT201", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Trigonometria",
     "habilidade_descricao": "Estabelecer relações entre as razões trigonométricas e aplicá-las em diferentes contextos."},
    
    {"codigo_bncc": "EM13MAT202", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Funções trigonométricas",
     "habilidade_descricao": "Analisar e interpretar funções trigonométricas, identificando amplitude, período e deslocamentos."},
    
    {"codigo_bncc": "EM13MAT203", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Matrizes",
     "habilidade_descricao": "Utilizar matrizes para organizar dados e resolver sistemas lineares."},
    
    {"codigo_bncc": "EM13MAT204", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Determinantes",
     "habilidade_descricao": "Calcular determinantes e aplicá-los na resolução de sistemas lineares e geometria analítica."},
    
    {"codigo_bncc": "EM13MAT205", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Geometria analítica",
     "habilidade_descricao": "Utilizar conceitos de geometria analítica para calcular distâncias, áreas e estudar retas e circunferências."},
    
    {"codigo_bncc": "EM13MAT206", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Probabilidade",
     "habilidade_descricao": "Resolver e elaborar problemas de contagem e probabilidade utilizando diferentes técnicas."},
    
    # 3º Ano
    {"codigo_bncc": "EM13MAT301", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Geometria espacial",
     "habilidade_descricao": "Calcular volumes, áreas de superfícies e resolver problemas envolvendo sólidos geométricos."},
    
    {"codigo_bncc": "EM13MAT302", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Funções exponenciais e logarítmicas",
     "habilidade_descricao": "Analisar funções exponenciais e logarítmicas e suas aplicações em fenômenos naturais e sociais."},
    
    {"codigo_bncc": "EM13MAT303", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Números complexos",
     "habilidade_descricao": "Realizar operações com números complexos e compreender suas representações."},
    
    {"codigo_bncc": "EM13MAT304", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Polinômios",
     "habilidade_descricao": "Operar com polinômios, fatorar e resolver equações polinomiais."},

    # ============================================
    # LÍNGUA PORTUGUESA
    # ============================================
    # 1º Ano
    {"codigo_bncc": "EM13LP101", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Gêneros textuais",
     "habilidade_descricao": "Analisar e utilizar diferentes gêneros textuais, considerando suas características e contextos de circulação."},
    
    {"codigo_bncc": "EM13LP102", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Leitura e interpretação",
     "habilidade_descricao": "Analisar textos de diferentes gêneros, identificando tema, propósito, recursos linguísticos e efeitos de sentido."},
    
    {"codigo_bncc": "EM13LP103", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Produção textual",
     "habilidade_descricao": "Produzir textos em diferentes gêneros, atendendo às características do gênero e ao contexto de produção."},
    
    {"codigo_bncc": "EM13LP104", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Análise linguística",
     "habilidade_descricao": "Analisar recursos linguísticos e semióticos que operam nos textos e seus efeitos de sentido."},
    
    {"codigo_bncc": "EM13LP105", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Literatura brasileira",
     "habilidade_descricao": "Analisar obras literárias brasileiras, identificando características de escolas literárias e contextos históricos."},
    
    {"codigo_bncc": "EM13LP106", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Argumentação",
     "habilidade_descricao": "Construir argumentação consistente, utilizando diferentes tipos de argumento e estratégias retóricas."},
    
    # 2º Ano
    {"codigo_bncc": "EM13LP201", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Gêneros jornalísticos",
     "habilidade_descricao": "Analisar e produzir textos jornalísticos, considerando características do gênero e questões éticas."},
    
    {"codigo_bncc": "EM13LP202", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Literatura portuguesa",
     "habilidade_descricao": "Analisar obras da literatura portuguesa, estabelecendo relações com a literatura brasileira."},
    
    {"codigo_bncc": "EM13LP203", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Texto dissertativo-argumentativo",
     "habilidade_descricao": "Produzir textos dissertativo-argumentativos com domínio da estrutura e recursos argumentativos."},
    
    {"codigo_bncc": "EM13LP204", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Oralidade",
     "habilidade_descricao": "Participar de debates e apresentações orais, utilizando recursos linguísticos adequados."},
    
    # 3º Ano
    {"codigo_bncc": "EM13LP301", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Modernismo brasileiro",
     "habilidade_descricao": "Analisar obras do Modernismo brasileiro, identificando suas características e contextos."},
    
    {"codigo_bncc": "EM13LP302", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Literatura contemporânea",
     "habilidade_descricao": "Analisar obras da literatura contemporânea brasileira e suas relações com a atualidade."},
    
    {"codigo_bncc": "EM13LP303", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Redação ENEM",
     "habilidade_descricao": "Produzir textos dissertativo-argumentativos seguindo os critérios de avaliação do ENEM."},
    
    {"codigo_bncc": "EM13LP304", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Intertextualidade",
     "habilidade_descricao": "Analisar relações intertextuais entre obras de diferentes épocas e mídias."},

    # ============================================
    # FÍSICA
    # ============================================
    {"codigo_bncc": "EM13CNT101", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Cinemática",
     "habilidade_descricao": "Analisar movimentos retilíneos e suas grandezas: posição, velocidade e aceleração."},
    
    {"codigo_bncc": "EM13CNT102", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Dinâmica",
     "habilidade_descricao": "Aplicar as leis de Newton para analisar situações envolvendo forças e movimento."},
    
    {"codigo_bncc": "EM13CNT103", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Energia",
     "habilidade_descricao": "Compreender os conceitos de trabalho, energia e potência e suas transformações."},
    
    {"codigo_bncc": "EM13CNT201", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Termologia",
     "habilidade_descricao": "Analisar fenômenos térmicos, calor e suas aplicações tecnológicas."},
    
    {"codigo_bncc": "EM13CNT202", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Óptica",
     "habilidade_descricao": "Compreender fenômenos ópticos e suas aplicações em instrumentos e tecnologias."},
    
    {"codigo_bncc": "EM13CNT203", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Ondas",
     "habilidade_descricao": "Analisar fenômenos ondulatórios, incluindo som e luz."},
    
    {"codigo_bncc": "EM13CNT301", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Eletricidade",
     "habilidade_descricao": "Compreender circuitos elétricos, corrente, tensão e resistência."},
    
    {"codigo_bncc": "EM13CNT302", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Eletromagnetismo",
     "habilidade_descricao": "Analisar fenômenos eletromagnéticos e suas aplicações tecnológicas."},
    
    {"codigo_bncc": "EM13CNT303", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Física moderna",
     "habilidade_descricao": "Compreender conceitos de física moderna: relatividade, quântica e suas aplicações."},

    # ============================================
    # QUÍMICA
    # ============================================
    {"codigo_bncc": "EM13CNT104", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Estrutura atômica",
     "habilidade_descricao": "Compreender os modelos atômicos e a estrutura da matéria."},
    
    {"codigo_bncc": "EM13CNT105", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Tabela periódica",
     "habilidade_descricao": "Utilizar a tabela periódica para prever propriedades dos elementos."},
    
    {"codigo_bncc": "EM13CNT106", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Ligações químicas",
     "habilidade_descricao": "Identificar e comparar tipos de ligações químicas e suas propriedades."},
    
    {"codigo_bncc": "EM13CNT204", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Reações químicas",
     "habilidade_descricao": "Balancear e interpretar equações químicas e suas relações estequiométricas."},
    
    {"codigo_bncc": "EM13CNT205", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Soluções",
     "habilidade_descricao": "Compreender propriedades de soluções e realizar cálculos de concentração."},
    
    {"codigo_bncc": "EM13CNT206", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Termoquímica",
     "habilidade_descricao": "Analisar variações de energia em reações químicas."},
    
    {"codigo_bncc": "EM13CNT304", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Química orgânica",
     "habilidade_descricao": "Identificar e nomear compostos orgânicos e suas funções."},
    
    {"codigo_bncc": "EM13CNT305", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Eletroquímica",
     "habilidade_descricao": "Compreender processos eletroquímicos: pilhas, baterias e eletrólise."},

    # ============================================
    # BIOLOGIA
    # ============================================
    {"codigo_bncc": "EM13CNT107", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Citologia",
     "habilidade_descricao": "Compreender a estrutura e funcionamento das células."},
    
    {"codigo_bncc": "EM13CNT108", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Metabolismo",
     "habilidade_descricao": "Analisar processos metabólicos: respiração, fotossíntese e fermentação."},
    
    {"codigo_bncc": "EM13CNT109", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Reprodução celular",
     "habilidade_descricao": "Compreender os processos de mitose e meiose e sua importância."},
    
    {"codigo_bncc": "EM13CNT207", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Genética",
     "habilidade_descricao": "Aplicar conceitos de genética mendeliana e molecular."},
    
    {"codigo_bncc": "EM13CNT208", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Evolução",
     "habilidade_descricao": "Compreender mecanismos evolutivos e evidências da evolução."},
    
    {"codigo_bncc": "EM13CNT209", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Taxonomia",
     "habilidade_descricao": "Classificar seres vivos e compreender relações filogenéticas."},
    
    {"codigo_bncc": "EM13CNT306", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Fisiologia humana",
     "habilidade_descricao": "Compreender o funcionamento dos sistemas do corpo humano."},
    
    {"codigo_bncc": "EM13CNT307", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Ecologia",
     "habilidade_descricao": "Analisar relações ecológicas e impactos ambientais."},
    
    {"codigo_bncc": "EM13CNT308", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Biotecnologia",
     "habilidade_descricao": "Compreender aplicações da biotecnologia e questões bioéticas."},

    # ============================================
    # HISTÓRIA
    # ============================================
    {"codigo_bncc": "EM13CHS101", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Antiguidade",
     "habilidade_descricao": "Analisar as civilizações antigas e suas contribuições para a humanidade."},
    
    {"codigo_bncc": "EM13CHS102", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Idade Média",
     "habilidade_descricao": "Compreender o período medieval europeu e suas características."},
    
    {"codigo_bncc": "EM13CHS103", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Expansão marítima",
     "habilidade_descricao": "Analisar o processo de expansão marítima e colonização."},
    
    {"codigo_bncc": "EM13CHS201", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Revoluções modernas",
     "habilidade_descricao": "Analisar as revoluções burguesas e suas consequências."},
    
    {"codigo_bncc": "EM13CHS202", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Brasil colonial",
     "habilidade_descricao": "Compreender o período colonial brasileiro e suas estruturas."},
    
    {"codigo_bncc": "EM13CHS203", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Independência e Império",
     "habilidade_descricao": "Analisar o processo de independência e o período imperial brasileiro."},
    
    {"codigo_bncc": "EM13CHS301", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "República brasileira",
     "habilidade_descricao": "Compreender os diferentes períodos republicanos no Brasil."},
    
    {"codigo_bncc": "EM13CHS302", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Guerras mundiais",
     "habilidade_descricao": "Analisar as guerras mundiais e seus impactos globais."},
    
    {"codigo_bncc": "EM13CHS303", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Brasil contemporâneo",
     "habilidade_descricao": "Compreender a história recente do Brasil: ditadura e redemocratização."},

    # ============================================
    # GEOGRAFIA
    # ============================================
    {"codigo_bncc": "EM13CHS104", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Cartografia",
     "habilidade_descricao": "Utilizar recursos cartográficos para análise espacial."},
    
    {"codigo_bncc": "EM13CHS105", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Geologia e relevo",
     "habilidade_descricao": "Compreender a estrutura geológica da Terra e formação do relevo."},
    
    {"codigo_bncc": "EM13CHS106", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Clima e vegetação",
     "habilidade_descricao": "Analisar os climas e biomas brasileiros e mundiais."},
    
    {"codigo_bncc": "EM13CHS204", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "População",
     "habilidade_descricao": "Analisar dinâmicas populacionais e suas implicações."},
    
    {"codigo_bncc": "EM13CHS205", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Urbanização",
     "habilidade_descricao": "Compreender o processo de urbanização e seus desafios."},
    
    {"codigo_bncc": "EM13CHS206", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Geopolítica",
     "habilidade_descricao": "Analisar conflitos geopolíticos e relações internacionais."},
    
    {"codigo_bncc": "EM13CHS304", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Globalização",
     "habilidade_descricao": "Compreender o processo de globalização e suas consequências."},
    
    {"codigo_bncc": "EM13CHS305", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Meio ambiente",
     "habilidade_descricao": "Analisar questões ambientais e desenvolvimento sustentável."},
    
    {"codigo_bncc": "EM13CHS306", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Brasil no mundo",
     "habilidade_descricao": "Compreender a inserção do Brasil no contexto mundial."},
]


def importar_bncc_ensino_medio():
    print("=" * 60)
    print("📚 IMPORTANDO BNCC - ENSINO MÉDIO")
    print("=" * 60)
    
    with engine.connect() as conn:
        importados = 0
        atualizados = 0
        
        for hab in HABILIDADES_ENSINO_MEDIO:
            # Verificar se já existe
            result = conn.execute(text("""
                SELECT id FROM curriculo_nacional WHERE codigo_bncc = :codigo
            """), {"codigo": hab["codigo_bncc"]})
            
            existente = result.fetchone()
            
            if existente:
                # Atualizar
                conn.execute(text("""
                    UPDATE curriculo_nacional 
                    SET componente = :componente,
                        ano_escolar = :ano_escolar,
                        trimestre_sugerido = :trimestre,
                        dificuldade = :dificuldade,
                        objeto_conhecimento = :objeto,
                        habilidade_descricao = :descricao
                    WHERE codigo_bncc = :codigo
                """), {
                    "codigo": hab["codigo_bncc"],
                    "componente": hab["componente"],
                    "ano_escolar": hab["ano_escolar"],
                    "trimestre": hab["trimestre_sugerido"],
                    "dificuldade": hab["dificuldade"],
                    "objeto": hab["objeto_conhecimento"],
                    "descricao": hab["habilidade_descricao"]
                })
                atualizados += 1
            else:
                # Inserir
                conn.execute(text("""
                    INSERT INTO curriculo_nacional 
                    (codigo_bncc, componente, ano_escolar, trimestre_sugerido, dificuldade, objeto_conhecimento, habilidade_descricao)
                    VALUES (:codigo, :componente, :ano_escolar, :trimestre, :dificuldade, :objeto, :descricao)
                """), {
                    "codigo": hab["codigo_bncc"],
                    "componente": hab["componente"],
                    "ano_escolar": hab["ano_escolar"],
                    "trimestre": hab["trimestre_sugerido"],
                    "dificuldade": hab["dificuldade"],
                    "objeto": hab["objeto_conhecimento"],
                    "descricao": hab["habilidade_descricao"]
                })
                importados += 1
        
        conn.commit()
        
        print(f"\n✅ Importados: {importados}")
        print(f"🔄 Atualizados: {atualizados}")
        
        # Mostrar resumo
        print("\n" + "=" * 60)
        print("📊 RESUMO POR ANO E COMPONENTE:")
        print("-" * 60)
        
        result = conn.execute(text("""
            SELECT ano_escolar, componente, COUNT(*) as total
            FROM curriculo_nacional
            WHERE ano_escolar LIKE '%EM%'
            GROUP BY ano_escolar, componente
            ORDER BY ano_escolar, componente
        """))
        
        for row in result.fetchall():
            print(f"   • {row[0]} - {row[1]}: {row[2]} habilidades")
    
    print("\n" + "=" * 60)
    print("✅ IMPORTAÇÃO CONCLUÍDA!")
    print("=" * 60)


if __name__ == "__main__":
    importar_bncc_ensino_medio()
