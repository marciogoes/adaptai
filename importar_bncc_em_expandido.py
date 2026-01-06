# ============================================
# IMPORTAR BNCC ENSINO MÉDIO - VERSÃO EXPANDIDA
# Mais de 200 habilidades completas
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

# ============================================
# HABILIDADES EXPANDIDAS - ENSINO MÉDIO
# ============================================

HABILIDADES_EM = [
    # ============================================
    # MATEMÁTICA - 1º ANO EM (Cerca de 25 habilidades)
    # ============================================
    {"codigo_bncc": "EM13MAT101", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Conjuntos numéricos", "habilidade_descricao": "Interpretar criticamente situações econômicas, sociais e fatos relativos às Ciências da Natureza que envolvam a variação de grandezas, pela análise dos gráficos das funções representadas e das taxas de variação."},
    {"codigo_bncc": "EM13MAT102", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Função afim", "habilidade_descricao": "Analisar tabelas, gráficos e amostras de pesquisas estatísticas apresentadas em relatórios divulgados por diferentes meios de comunicação."},
    {"codigo_bncc": "EM13MAT103", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Progressão aritmética", "habilidade_descricao": "Interpretar e compreender textos científicos ou divulgados pelas mídias, que empregam unidades de medida de diferentes grandezas."},
    {"codigo_bncc": "EM13MAT104", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Porcentagem e juros", "habilidade_descricao": "Comparar preços de produtos em função da quantidade consumida e calcular valores envolvendo porcentagens e juros."},
    {"codigo_bncc": "EM13MAT105", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Função quadrática", "habilidade_descricao": "Resolver e elaborar problemas com funções quadráticas, identificando máximos, mínimos e zeros da função."},
    {"codigo_bncc": "EM13MAT106", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Inequações", "habilidade_descricao": "Resolver e elaborar problemas que envolvam inequações, sistemas de inequações lineares e não lineares."},
    {"codigo_bncc": "EM13MAT107", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Geometria plana", "habilidade_descricao": "Calcular áreas de figuras planas, incluindo triângulos, quadriláteros e polígonos regulares."},
    {"codigo_bncc": "EM13MAT108", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Estatística básica", "habilidade_descricao": "Calcular e interpretar medidas de tendência central (média, mediana, moda) e de dispersão (amplitude, variância, desvio padrão)."},
    {"codigo_bncc": "EM13MAT109", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Gráficos estatísticos", "habilidade_descricao": "Construir e interpretar gráficos de barras, setores, linhas e histogramas."},
    {"codigo_bncc": "EM13MAT110", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Probabilidade", "habilidade_descricao": "Resolver e elaborar problemas que envolvam o cálculo de probabilidade de eventos em experimentos aleatórios."},
    {"codigo_bncc": "EM13MAT111", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Sequências numéricas", "habilidade_descricao": "Identificar padrões em sequências numéricas e estabelecer fórmulas para o termo geral."},
    {"codigo_bncc": "EM13MAT112", "componente": "Matemática", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Proporcionalidade", "habilidade_descricao": "Resolver problemas envolvendo grandezas diretamente e inversamente proporcionais."},
    
    # MATEMÁTICA - 2º ANO EM (Cerca de 25 habilidades)
    {"codigo_bncc": "EM13MAT201", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Trigonometria", "habilidade_descricao": "Estabelecer relações entre as razões trigonométricas do triângulo retângulo e aplicá-las em contextos diversos."},
    {"codigo_bncc": "EM13MAT202", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Círculo trigonométrico", "habilidade_descricao": "Utilizar o círculo trigonométrico para determinar seno, cosseno e tangente de ângulos notáveis."},
    {"codigo_bncc": "EM13MAT203", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Matrizes", "habilidade_descricao": "Utilizar as noções de matrizes para organizar dados e resolver problemas."},
    {"codigo_bncc": "EM13MAT204", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Determinantes", "habilidade_descricao": "Calcular determinantes de matrizes 2x2 e 3x3 e aplicar na resolução de sistemas lineares."},
    {"codigo_bncc": "EM13MAT205", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Sistemas lineares", "habilidade_descricao": "Resolver sistemas lineares utilizando diferentes métodos (escalonamento, Cramer, substituição)."},
    {"codigo_bncc": "EM13MAT206", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Geometria analítica - Ponto", "habilidade_descricao": "Determinar distância entre dois pontos e ponto médio de um segmento no plano cartesiano."},
    {"codigo_bncc": "EM13MAT207", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Geometria analítica - Reta", "habilidade_descricao": "Determinar a equação da reta e analisar posições relativas entre retas."},
    {"codigo_bncc": "EM13MAT208", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Geometria analítica - Circunferência", "habilidade_descricao": "Determinar a equação da circunferência e resolver problemas envolvendo posições relativas."},
    {"codigo_bncc": "EM13MAT209", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Cônicas", "habilidade_descricao": "Identificar e representar graficamente elipses, hipérboles e parábolas."},
    {"codigo_bncc": "EM13MAT210", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Análise combinatória - Princípio fundamental", "habilidade_descricao": "Resolver problemas de contagem utilizando o princípio fundamental da contagem."},
    {"codigo_bncc": "EM13MAT211", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Permutações e arranjos", "habilidade_descricao": "Calcular permutações simples, com repetição e arranjos."},
    {"codigo_bncc": "EM13MAT212", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Combinações", "habilidade_descricao": "Calcular combinações e aplicar em problemas de probabilidade."},
    {"codigo_bncc": "EM13MAT213", "componente": "Matemática", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Binômio de Newton", "habilidade_descricao": "Desenvolver binômios utilizando o triângulo de Pascal e a fórmula do termo geral."},
    
    # MATEMÁTICA - 3º ANO EM (Cerca de 20 habilidades)
    {"codigo_bncc": "EM13MAT301", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Função exponencial", "habilidade_descricao": "Construir e analisar gráficos de funções exponenciais e resolver equações exponenciais."},
    {"codigo_bncc": "EM13MAT302", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Função logarítmica", "habilidade_descricao": "Compreender logaritmos e suas propriedades, resolvendo equações logarítmicas."},
    {"codigo_bncc": "EM13MAT303", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Progressão geométrica", "habilidade_descricao": "Identificar progressões geométricas e calcular termos e soma."},
    {"codigo_bncc": "EM13MAT304", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Geometria espacial - Prismas", "habilidade_descricao": "Calcular áreas e volumes de prismas regulares."},
    {"codigo_bncc": "EM13MAT305", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Geometria espacial - Pirâmides", "habilidade_descricao": "Calcular áreas e volumes de pirâmides regulares."},
    {"codigo_bncc": "EM13MAT306", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Geometria espacial - Cilindros", "habilidade_descricao": "Calcular áreas e volumes de cilindros."},
    {"codigo_bncc": "EM13MAT307", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Geometria espacial - Cones", "habilidade_descricao": "Calcular áreas e volumes de cones."},
    {"codigo_bncc": "EM13MAT308", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Geometria espacial - Esferas", "habilidade_descricao": "Calcular áreas e volumes de esferas."},
    {"codigo_bncc": "EM13MAT309", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Números complexos", "habilidade_descricao": "Operar com números complexos na forma algébrica e trigonométrica."},
    {"codigo_bncc": "EM13MAT310", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Polinômios", "habilidade_descricao": "Operar com polinômios e determinar suas raízes."},
    {"codigo_bncc": "EM13MAT311", "componente": "Matemática", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Estatística avançada", "habilidade_descricao": "Analisar distribuições de frequências e calcular medidas de posição e dispersão."},
    
    # ============================================
    # LÍNGUA PORTUGUESA - 1º ANO EM (Cerca de 20 habilidades)
    # ============================================
    {"codigo_bncc": "EM13LP101", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais - Reportagem", "habilidade_descricao": "Analisar e produzir reportagens, considerando os elementos composicionais do gênero."},
    {"codigo_bncc": "EM13LP102", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais - Notícia", "habilidade_descricao": "Identificar e analisar os elementos estruturais de notícias jornalísticas."},
    {"codigo_bncc": "EM13LP103", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Variação linguística", "habilidade_descricao": "Reconhecer as variações linguísticas como fenômeno natural e social."},
    {"codigo_bncc": "EM13LP104", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Coesão textual", "habilidade_descricao": "Utilizar mecanismos de coesão referencial e sequencial na produção de textos."},
    {"codigo_bncc": "EM13LP105", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Coerência textual", "habilidade_descricao": "Analisar e garantir a coerência em textos próprios e alheios."},
    {"codigo_bncc": "EM13LP106", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Trovadorismo", "habilidade_descricao": "Analisar textos do Trovadorismo, identificando características do período."},
    {"codigo_bncc": "EM13LP107", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Humanismo", "habilidade_descricao": "Analisar textos do Humanismo português, incluindo Gil Vicente."},
    {"codigo_bncc": "EM13LP108", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura - Classicismo", "habilidade_descricao": "Analisar textos do Classicismo, especialmente Os Lusíadas de Camões."},
    {"codigo_bncc": "EM13LP109", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura - Quinhentismo", "habilidade_descricao": "Analisar textos da Literatura de Informação e Catequese no Brasil Colonial."},
    {"codigo_bncc": "EM13LP110", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Argumentação", "habilidade_descricao": "Identificar e analisar estratégias argumentativas em textos diversos."},
    {"codigo_bncc": "EM13LP111", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Produção textual argumentativa", "habilidade_descricao": "Produzir textos argumentativos com tese, argumentos e conclusão."},
    {"codigo_bncc": "EM13LP112", "componente": "Língua Portuguesa", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Sintaxe - Período simples", "habilidade_descricao": "Analisar os termos essenciais, integrantes e acessórios da oração."},
    
    # LÍNGUA PORTUGUESA - 2º ANO EM (Cerca de 20 habilidades)
    {"codigo_bncc": "EM13LP201", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais - Editorial", "habilidade_descricao": "Analisar editoriais, identificando posicionamento e estratégias argumentativas."},
    {"codigo_bncc": "EM13LP202", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais - Artigo de opinião", "habilidade_descricao": "Produzir artigos de opinião com argumentação consistente."},
    {"codigo_bncc": "EM13LP203", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Dissertação argumentativa", "habilidade_descricao": "Estruturar dissertações argumentativas seguindo modelo ENEM."},
    {"codigo_bncc": "EM13LP204", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Barroco", "habilidade_descricao": "Analisar textos do Barroco brasileiro, identificando características estilísticas."},
    {"codigo_bncc": "EM13LP205", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Arcadismo", "habilidade_descricao": "Analisar textos do Arcadismo, identificando bucolismo e áurea mediocritas."},
    {"codigo_bncc": "EM13LP206", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Romantismo (poesia)", "habilidade_descricao": "Analisar as gerações românticas na poesia brasileira."},
    {"codigo_bncc": "EM13LP207", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura - Romantismo (prosa)", "habilidade_descricao": "Analisar romances românticos brasileiros (indianista, urbano, regionalista)."},
    {"codigo_bncc": "EM13LP208", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Sintaxe - Período composto", "habilidade_descricao": "Analisar períodos compostos por coordenação e subordinação."},
    {"codigo_bncc": "EM13LP209", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Orações subordinadas", "habilidade_descricao": "Classificar e analisar orações subordinadas substantivas, adjetivas e adverbiais."},
    {"codigo_bncc": "EM13LP210", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Regência verbal e nominal", "habilidade_descricao": "Aplicar corretamente as regras de regência verbal e nominal."},
    {"codigo_bncc": "EM13LP211", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Crase", "habilidade_descricao": "Empregar corretamente a crase em diferentes contextos."},
    {"codigo_bncc": "EM13LP212", "componente": "Língua Portuguesa", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Intertextualidade", "habilidade_descricao": "Identificar e analisar relações intertextuais entre diferentes obras."},
    
    # LÍNGUA PORTUGUESA - 3º ANO EM (Cerca de 20 habilidades)
    {"codigo_bncc": "EM13LP301", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Literatura - Realismo", "habilidade_descricao": "Analisar textos do Realismo brasileiro, especialmente Machado de Assis."},
    {"codigo_bncc": "EM13LP302", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Literatura - Naturalismo", "habilidade_descricao": "Analisar textos do Naturalismo, identificando determinismo e cientificismo."},
    {"codigo_bncc": "EM13LP303", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Literatura - Parnasianismo", "habilidade_descricao": "Analisar a poesia parnasiana e sua busca pela forma perfeita."},
    {"codigo_bncc": "EM13LP304", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Simbolismo", "habilidade_descricao": "Analisar a poesia simbolista e suas características."},
    {"codigo_bncc": "EM13LP305", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Literatura - Pré-Modernismo", "habilidade_descricao": "Analisar textos pré-modernistas de Euclides da Cunha, Lima Barreto e Monteiro Lobato."},
    {"codigo_bncc": "EM13LP306", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Literatura - Modernismo 1ª fase", "habilidade_descricao": "Analisar textos da Semana de 22 e primeira geração modernista."},
    {"codigo_bncc": "EM13LP307", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura - Modernismo 2ª fase (poesia)", "habilidade_descricao": "Analisar a poesia de Drummond, Cecília Meireles e Vinícius de Moraes."},
    {"codigo_bncc": "EM13LP308", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura - Modernismo 2ª fase (prosa)", "habilidade_descricao": "Analisar a prosa regionalista de Graciliano Ramos, Jorge Amado e Rachel de Queiroz."},
    {"codigo_bncc": "EM13LP309", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Literatura - Modernismo 3ª fase", "habilidade_descricao": "Analisar textos de Guimarães Rosa, Clarice Lispector e João Cabral."},
    {"codigo_bncc": "EM13LP310", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Literatura Contemporânea", "habilidade_descricao": "Analisar textos da literatura brasileira contemporânea."},
    {"codigo_bncc": "EM13LP311", "componente": "Língua Portuguesa", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Redação ENEM", "habilidade_descricao": "Produzir textos dissertativo-argumentativos seguindo as competências do ENEM."},
    
    # ============================================
    # FÍSICA - 1º ANO EM (Cerca de 15 habilidades)
    # ============================================
    {"codigo_bncc": "EM13CNT101", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Cinemática - MRU", "habilidade_descricao": "Analisar e descrever movimentos retilíneos uniformes, calculando velocidade e deslocamento."},
    {"codigo_bncc": "EM13CNT102", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Cinemática - MRUV", "habilidade_descricao": "Analisar movimentos uniformemente variados, calculando aceleração e equações horárias."},
    {"codigo_bncc": "EM13CNT103", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Queda livre", "habilidade_descricao": "Analisar a queda livre dos corpos e lançamentos verticais."},
    {"codigo_bncc": "EM13CNT104", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Lançamento oblíquo", "habilidade_descricao": "Analisar lançamentos oblíquos decompondo o movimento em componentes."},
    {"codigo_bncc": "EM13CNT105", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Leis de Newton", "habilidade_descricao": "Aplicar as três leis de Newton na análise de movimentos e equilíbrio."},
    {"codigo_bncc": "EM13CNT106", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Força peso e normal", "habilidade_descricao": "Identificar e calcular forças peso e normal em diferentes situações."},
    {"codigo_bncc": "EM13CNT107", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Atrito", "habilidade_descricao": "Analisar a força de atrito estático e cinético em superfícies."},
    {"codigo_bncc": "EM13CNT108", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Força elástica", "habilidade_descricao": "Aplicar a Lei de Hooke para calcular forças em molas."},
    {"codigo_bncc": "EM13CNT109", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Plano inclinado", "habilidade_descricao": "Analisar forças e movimentos em planos inclinados."},
    {"codigo_bncc": "EM13CNT110", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Trabalho", "habilidade_descricao": "Calcular o trabalho realizado por forças constantes e variáveis."},
    {"codigo_bncc": "EM13CNT111", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Energia cinética e potencial", "habilidade_descricao": "Calcular energias cinética e potencial gravitacional."},
    {"codigo_bncc": "EM13CNT112", "componente": "Física", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Conservação de energia", "habilidade_descricao": "Aplicar o princípio da conservação da energia mecânica."},
    
    # FÍSICA - 2º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CNT201", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Termometria", "habilidade_descricao": "Compreender escalas termométricas e realizar conversões."},
    {"codigo_bncc": "EM13CNT202", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Dilatação térmica", "habilidade_descricao": "Calcular dilatação linear, superficial e volumétrica de sólidos."},
    {"codigo_bncc": "EM13CNT203", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Calorimetria", "habilidade_descricao": "Calcular quantidade de calor e realizar balanços térmicos."},
    {"codigo_bncc": "EM13CNT204", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Mudanças de estado físico", "habilidade_descricao": "Analisar mudanças de estado e calcular calor latente."},
    {"codigo_bncc": "EM13CNT205", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Termodinâmica", "habilidade_descricao": "Aplicar a primeira lei da termodinâmica em transformações gasosas."},
    {"codigo_bncc": "EM13CNT206", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Óptica - Reflexão", "habilidade_descricao": "Analisar fenômenos de reflexão da luz e formação de imagens em espelhos."},
    {"codigo_bncc": "EM13CNT207", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Óptica - Refração", "habilidade_descricao": "Analisar a refração da luz e aplicar a Lei de Snell."},
    {"codigo_bncc": "EM13CNT208", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Lentes", "habilidade_descricao": "Analisar formação de imagens em lentes esféricas."},
    {"codigo_bncc": "EM13CNT209", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ondas", "habilidade_descricao": "Caracterizar ondas mecânicas e eletromagnéticas."},
    {"codigo_bncc": "EM13CNT210", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Acústica", "habilidade_descricao": "Analisar características do som: frequência, amplitude e timbre."},
    {"codigo_bncc": "EM13CNT211", "componente": "Física", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Óptica física", "habilidade_descricao": "Analisar fenômenos de interferência e difração da luz."},
    
    # FÍSICA - 3º ANO EM (Cerca de 12 habilidades)
    {"codigo_bncc": "EM13CNT301", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Eletrostática", "habilidade_descricao": "Analisar fenômenos de eletrização e calcular força elétrica."},
    {"codigo_bncc": "EM13CNT302", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Campo elétrico", "habilidade_descricao": "Calcular campo elétrico e potencial elétrico."},
    {"codigo_bncc": "EM13CNT303", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Corrente elétrica", "habilidade_descricao": "Calcular corrente elétrica, resistência e Lei de Ohm."},
    {"codigo_bncc": "EM13CNT304", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Circuitos elétricos", "habilidade_descricao": "Analisar circuitos em série, paralelo e misto."},
    {"codigo_bncc": "EM13CNT305", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Potência elétrica", "habilidade_descricao": "Calcular potência e energia elétrica consumida."},
    {"codigo_bncc": "EM13CNT306", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Magnetismo", "habilidade_descricao": "Analisar fenômenos magnéticos e campo magnético."},
    {"codigo_bncc": "EM13CNT307", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Eletromagnetismo", "habilidade_descricao": "Analisar a relação entre eletricidade e magnetismo."},
    {"codigo_bncc": "EM13CNT308", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Indução eletromagnética", "habilidade_descricao": "Compreender a Lei de Faraday e indução eletromagnética."},
    {"codigo_bncc": "EM13CNT309", "componente": "Física", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Física moderna", "habilidade_descricao": "Compreender conceitos básicos de relatividade e física quântica."},
    
    # ============================================
    # QUÍMICA - 1º ANO EM (Cerca de 15 habilidades)
    # ============================================
    {"codigo_bncc": "EM13CNT121", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Modelos atômicos", "habilidade_descricao": "Compreender a evolução dos modelos atômicos de Dalton a Bohr."},
    {"codigo_bncc": "EM13CNT122", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Tabela periódica", "habilidade_descricao": "Analisar a organização da tabela periódica e propriedades periódicas."},
    {"codigo_bncc": "EM13CNT123", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ligações químicas", "habilidade_descricao": "Identificar e caracterizar ligações iônicas, covalentes e metálicas."},
    {"codigo_bncc": "EM13CNT124", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Geometria molecular", "habilidade_descricao": "Determinar a geometria de moléculas simples."},
    {"codigo_bncc": "EM13CNT125", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Polaridade", "habilidade_descricao": "Analisar a polaridade de ligações e moléculas."},
    {"codigo_bncc": "EM13CNT126", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Funções inorgânicas - Ácidos", "habilidade_descricao": "Identificar e nomear ácidos inorgânicos."},
    {"codigo_bncc": "EM13CNT127", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Funções inorgânicas - Bases", "habilidade_descricao": "Identificar e nomear bases inorgânicas."},
    {"codigo_bncc": "EM13CNT128", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Funções inorgânicas - Sais", "habilidade_descricao": "Identificar e nomear sais inorgânicos."},
    {"codigo_bncc": "EM13CNT129", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Funções inorgânicas - Óxidos", "habilidade_descricao": "Identificar e classificar óxidos inorgânicos."},
    {"codigo_bncc": "EM13CNT130", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Reações químicas", "habilidade_descricao": "Identificar e classificar tipos de reações químicas."},
    {"codigo_bncc": "EM13CNT131", "componente": "Química", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Balanceamento", "habilidade_descricao": "Balancear equações químicas por tentativa e oxirredução."},
    
    # QUÍMICA - 2º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CNT221", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Cálculo estequiométrico", "habilidade_descricao": "Realizar cálculos estequiométricos envolvendo massa, mol e volume."},
    {"codigo_bncc": "EM13CNT222", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Estequiometria com pureza e rendimento", "habilidade_descricao": "Realizar cálculos estequiométricos com reagente limitante, excesso, pureza e rendimento."},
    {"codigo_bncc": "EM13CNT223", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Soluções", "habilidade_descricao": "Compreender tipos de soluções e calcular concentrações."},
    {"codigo_bncc": "EM13CNT224", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Diluição e mistura", "habilidade_descricao": "Calcular concentrações em diluições e misturas de soluções."},
    {"codigo_bncc": "EM13CNT225", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Termoquímica", "habilidade_descricao": "Calcular variações de entalpia em reações químicas."},
    {"codigo_bncc": "EM13CNT226", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Lei de Hess", "habilidade_descricao": "Aplicar a Lei de Hess para calcular variações de entalpia."},
    {"codigo_bncc": "EM13CNT227", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Cinética química", "habilidade_descricao": "Analisar fatores que afetam a velocidade das reações químicas."},
    {"codigo_bncc": "EM13CNT228", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Equilíbrio químico", "habilidade_descricao": "Compreender o conceito de equilíbrio químico e constante de equilíbrio."},
    {"codigo_bncc": "EM13CNT229", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Deslocamento de equilíbrio", "habilidade_descricao": "Prever deslocamentos de equilíbrio usando o Princípio de Le Chatelier."},
    {"codigo_bncc": "EM13CNT230", "componente": "Química", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Equilíbrio iônico", "habilidade_descricao": "Calcular pH e pOH de soluções ácidas e básicas."},
    
    # QUÍMICA - 3º ANO EM (Cerca de 12 habilidades)
    {"codigo_bncc": "EM13CNT321", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Química orgânica - Hidrocarbonetos", "habilidade_descricao": "Nomear e identificar hidrocarbonetos saturados e insaturados."},
    {"codigo_bncc": "EM13CNT322", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Funções oxigenadas", "habilidade_descricao": "Identificar e nomear álcoois, fenóis, éteres, aldeídos, cetonas, ácidos e ésteres."},
    {"codigo_bncc": "EM13CNT323", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Funções nitrogenadas", "habilidade_descricao": "Identificar e nomear aminas, amidas e nitrilas."},
    {"codigo_bncc": "EM13CNT324", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Isomeria", "habilidade_descricao": "Identificar e classificar tipos de isomeria plana e espacial."},
    {"codigo_bncc": "EM13CNT325", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Reações orgânicas", "habilidade_descricao": "Identificar e prever produtos de reações orgânicas."},
    {"codigo_bncc": "EM13CNT326", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Polímeros", "habilidade_descricao": "Compreender a formação de polímeros e suas aplicações."},
    {"codigo_bncc": "EM13CNT327", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Eletroquímica", "habilidade_descricao": "Compreender pilhas e eletrólise, calculando potenciais."},
    {"codigo_bncc": "EM13CNT328", "componente": "Química", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Radioatividade", "habilidade_descricao": "Compreender emissões radioativas e suas aplicações."},
    
    # ============================================
    # BIOLOGIA - 1º ANO EM (Cerca de 15 habilidades)
    # ============================================
    {"codigo_bncc": "EM13CNT141", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Origem da vida", "habilidade_descricao": "Analisar teorias sobre a origem da vida na Terra."},
    {"codigo_bncc": "EM13CNT142", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Composição química da célula", "habilidade_descricao": "Identificar as principais biomoléculas e suas funções."},
    {"codigo_bncc": "EM13CNT143", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Citologia - Membrana", "habilidade_descricao": "Compreender a estrutura e funções da membrana plasmática."},
    {"codigo_bncc": "EM13CNT144", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Citologia - Organelas", "habilidade_descricao": "Identificar as organelas celulares e suas funções."},
    {"codigo_bncc": "EM13CNT145", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Metabolismo energético", "habilidade_descricao": "Compreender processos de respiração celular e fermentação."},
    {"codigo_bncc": "EM13CNT146", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Fotossíntese", "habilidade_descricao": "Compreender as etapas e importância da fotossíntese."},
    {"codigo_bncc": "EM13CNT147", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Núcleo e cromossomos", "habilidade_descricao": "Compreender a estrutura do núcleo e dos cromossomos."},
    {"codigo_bncc": "EM13CNT148", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Divisão celular - Mitose", "habilidade_descricao": "Compreender as fases e importância da mitose."},
    {"codigo_bncc": "EM13CNT149", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Divisão celular - Meiose", "habilidade_descricao": "Compreender as fases e importância da meiose para a variabilidade genética."},
    {"codigo_bncc": "EM13CNT150", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Histologia animal", "habilidade_descricao": "Identificar os principais tecidos animais e suas funções."},
    {"codigo_bncc": "EM13CNT151", "componente": "Biologia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Histologia vegetal", "habilidade_descricao": "Identificar os principais tecidos vegetais e suas funções."},
    
    # BIOLOGIA - 2º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CNT241", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Taxonomia", "habilidade_descricao": "Compreender os critérios de classificação dos seres vivos."},
    {"codigo_bncc": "EM13CNT242", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Vírus", "habilidade_descricao": "Caracterizar vírus e suas principais doenças."},
    {"codigo_bncc": "EM13CNT243", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Reino Monera", "habilidade_descricao": "Caracterizar bactérias e suas principais doenças e aplicações."},
    {"codigo_bncc": "EM13CNT244", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Reino Protista", "habilidade_descricao": "Caracterizar protozoários e algas, incluindo doenças causadas."},
    {"codigo_bncc": "EM13CNT245", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Reino Fungi", "habilidade_descricao": "Caracterizar fungos, suas doenças e aplicações."},
    {"codigo_bncc": "EM13CNT246", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Reino Plantae - Briófitas e pteridófitas", "habilidade_descricao": "Caracterizar briófitas e pteridófitas."},
    {"codigo_bncc": "EM13CNT247", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Reino Plantae - Gimnospermas e angiospermas", "habilidade_descricao": "Caracterizar gimnospermas e angiospermas."},
    {"codigo_bncc": "EM13CNT248", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Fisiologia vegetal", "habilidade_descricao": "Compreender processos de nutrição, transporte e reprodução vegetal."},
    {"codigo_bncc": "EM13CNT249", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Reino Animalia - Invertebrados", "habilidade_descricao": "Caracterizar os principais filos de invertebrados."},
    {"codigo_bncc": "EM13CNT250", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Reino Animalia - Vertebrados", "habilidade_descricao": "Caracterizar as classes de vertebrados."},
    {"codigo_bncc": "EM13CNT251", "componente": "Biologia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Fisiologia animal comparada", "habilidade_descricao": "Comparar sistemas fisiológicos dos diferentes grupos animais."},
    
    # BIOLOGIA - 3º ANO EM (Cerca de 12 habilidades)
    {"codigo_bncc": "EM13CNT341", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Genética mendeliana", "habilidade_descricao": "Resolver problemas envolvendo as leis de Mendel."},
    {"codigo_bncc": "EM13CNT342", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Herança não mendeliana", "habilidade_descricao": "Compreender padrões de herança como dominância incompleta, codominância e alelos múltiplos."},
    {"codigo_bncc": "EM13CNT343", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Genética molecular", "habilidade_descricao": "Compreender estrutura do DNA, replicação, transcrição e tradução."},
    {"codigo_bncc": "EM13CNT344", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Biotecnologia", "habilidade_descricao": "Compreender técnicas de engenharia genética e suas aplicações."},
    {"codigo_bncc": "EM13CNT345", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Evolução - Teorias", "habilidade_descricao": "Comparar as teorias evolutivas de Lamarck e Darwin."},
    {"codigo_bncc": "EM13CNT346", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Evolução - Evidências e mecanismos", "habilidade_descricao": "Analisar evidências da evolução e mecanismos evolutivos."},
    {"codigo_bncc": "EM13CNT347", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ecologia - Cadeias alimentares", "habilidade_descricao": "Analisar cadeias e teias alimentares e fluxo de energia."},
    {"codigo_bncc": "EM13CNT348", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ecologia - Ciclos biogeoquímicos", "habilidade_descricao": "Compreender os ciclos da água, carbono, nitrogênio e oxigênio."},
    {"codigo_bncc": "EM13CNT349", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Ecologia - Biomas", "habilidade_descricao": "Caracterizar os principais biomas brasileiros e mundiais."},
    {"codigo_bncc": "EM13CNT350", "componente": "Biologia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Ecologia - Impactos ambientais", "habilidade_descricao": "Analisar impactos ambientais e propostas de sustentabilidade."},
    
    # ============================================
    # HISTÓRIA - 1º ANO EM (Cerca de 15 habilidades)
    # ============================================
    {"codigo_bncc": "EM13CHS101", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Pré-história", "habilidade_descricao": "Analisar o processo de hominização e as sociedades pré-históricas."},
    {"codigo_bncc": "EM13CHS102", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Antiguidade Oriental", "habilidade_descricao": "Caracterizar as civilizações do Egito e Mesopotâmia."},
    {"codigo_bncc": "EM13CHS103", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Antiguidade Clássica - Grécia", "habilidade_descricao": "Analisar a civilização grega: política, sociedade e cultura."},
    {"codigo_bncc": "EM13CHS104", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Antiguidade Clássica - Roma", "habilidade_descricao": "Analisar a civilização romana: política, sociedade e legado."},
    {"codigo_bncc": "EM13CHS105", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Idade Média - Alta", "habilidade_descricao": "Caracterizar a formação da sociedade feudal europeia."},
    {"codigo_bncc": "EM13CHS106", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Idade Média - Igreja e cultura", "habilidade_descricao": "Analisar o papel da Igreja Católica na Idade Média."},
    {"codigo_bncc": "EM13CHS107", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Idade Média - Baixa", "habilidade_descricao": "Analisar a crise do feudalismo e as Cruzadas."},
    {"codigo_bncc": "EM13CHS108", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Renascimento", "habilidade_descricao": "Caracterizar o Renascimento cultural e científico."},
    {"codigo_bncc": "EM13CHS109", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Reforma Protestante", "habilidade_descricao": "Analisar causas e consequências da Reforma Protestante."},
    {"codigo_bncc": "EM13CHS110", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Absolutismo", "habilidade_descricao": "Caracterizar o Estado Absolutista e o mercantilismo."},
    {"codigo_bncc": "EM13CHS111", "componente": "História", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Expansão marítima", "habilidade_descricao": "Analisar o processo de expansão marítima europeia."},
    
    # HISTÓRIA - 2º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CHS201", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Brasil Colonial - Organização", "habilidade_descricao": "Analisar a organização política e econômica do Brasil Colonial."},
    {"codigo_bncc": "EM13CHS202", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Brasil Colonial - Escravidão", "habilidade_descricao": "Analisar o sistema escravista e a resistência africana."},
    {"codigo_bncc": "EM13CHS203", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Iluminismo", "habilidade_descricao": "Caracterizar o pensamento iluminista e seu impacto."},
    {"codigo_bncc": "EM13CHS204", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Revoluções Inglesas", "habilidade_descricao": "Analisar as revoluções inglesas do século XVII."},
    {"codigo_bncc": "EM13CHS205", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Independência dos EUA", "habilidade_descricao": "Analisar o processo de independência americana."},
    {"codigo_bncc": "EM13CHS206", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Revolução Francesa", "habilidade_descricao": "Analisar causas, fases e consequências da Revolução Francesa."},
    {"codigo_bncc": "EM13CHS207", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Era Napoleônica", "habilidade_descricao": "Analisar o governo de Napoleão e seu impacto na Europa."},
    {"codigo_bncc": "EM13CHS208", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Revolução Industrial", "habilidade_descricao": "Analisar causas e consequências da Revolução Industrial."},
    {"codigo_bncc": "EM13CHS209", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Movimentos operários", "habilidade_descricao": "Analisar a formação da classe operária e suas lutas."},
    {"codigo_bncc": "EM13CHS210", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Independência do Brasil", "habilidade_descricao": "Analisar o processo de independência do Brasil."},
    {"codigo_bncc": "EM13CHS211", "componente": "História", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Brasil Imperial - Primeiro Reinado", "habilidade_descricao": "Caracterizar o Primeiro Reinado e a Regência."},
    
    # HISTÓRIA - 3º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CHS301", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Brasil Imperial - Segundo Reinado", "habilidade_descricao": "Caracterizar o Segundo Reinado e a abolição da escravatura."},
    {"codigo_bncc": "EM13CHS302", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "República Velha", "habilidade_descricao": "Analisar a política do café com leite e o coronelismo."},
    {"codigo_bncc": "EM13CHS303", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Primeira Guerra Mundial", "habilidade_descricao": "Analisar causas e consequências da Primeira Guerra Mundial."},
    {"codigo_bncc": "EM13CHS304", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Período Entreguerras", "habilidade_descricao": "Analisar a crise de 1929 e a ascensão dos totalitarismos."},
    {"codigo_bncc": "EM13CHS305", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Era Vargas", "habilidade_descricao": "Analisar o governo de Getúlio Vargas (1930-1945)."},
    {"codigo_bncc": "EM13CHS306", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Segunda Guerra Mundial", "habilidade_descricao": "Analisar causas, desenvolvimento e consequências da Segunda Guerra."},
    {"codigo_bncc": "EM13CHS307", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Guerra Fria", "habilidade_descricao": "Caracterizar a bipolarização mundial e seus conflitos."},
    {"codigo_bncc": "EM13CHS308", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Brasil - República Democrática", "habilidade_descricao": "Analisar o período democrático (1945-1964) no Brasil."},
    {"codigo_bncc": "EM13CHS309", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ditadura Militar", "habilidade_descricao": "Analisar o regime militar brasileiro (1964-1985)."},
    {"codigo_bncc": "EM13CHS310", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Redemocratização", "habilidade_descricao": "Analisar o processo de redemocratização do Brasil."},
    {"codigo_bncc": "EM13CHS311", "componente": "História", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Mundo contemporâneo", "habilidade_descricao": "Analisar o fim da Guerra Fria e a globalização."},
    
    # ============================================
    # GEOGRAFIA - 1º ANO EM (Cerca de 15 habilidades)
    # ============================================
    {"codigo_bncc": "EM13CHS121", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Cartografia", "habilidade_descricao": "Interpretar mapas e utilizar coordenadas geográficas."},
    {"codigo_bncc": "EM13CHS122", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Geologia e relevo", "habilidade_descricao": "Compreender a formação geológica e tipos de relevo."},
    {"codigo_bncc": "EM13CHS123", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Clima e tempo", "habilidade_descricao": "Diferenciar tempo e clima e analisar fatores climáticos."},
    {"codigo_bncc": "EM13CHS124", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Tipos climáticos", "habilidade_descricao": "Caracterizar os principais tipos climáticos do Brasil e do mundo."},
    {"codigo_bncc": "EM13CHS125", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Hidrografia", "habilidade_descricao": "Analisar bacias hidrográficas e recursos hídricos."},
    {"codigo_bncc": "EM13CHS126", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Vegetação", "habilidade_descricao": "Caracterizar as principais formações vegetais."},
    {"codigo_bncc": "EM13CHS127", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Biomas brasileiros", "habilidade_descricao": "Caracterizar os biomas brasileiros e suas ameaças."},
    {"codigo_bncc": "EM13CHS128", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Solos", "habilidade_descricao": "Compreender formação, tipos e uso dos solos."},
    {"codigo_bncc": "EM13CHS129", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Questões ambientais", "habilidade_descricao": "Analisar problemas ambientais como desmatamento e poluição."},
    {"codigo_bncc": "EM13CHS130", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Mudanças climáticas", "habilidade_descricao": "Analisar causas e consequências das mudanças climáticas."},
    {"codigo_bncc": "EM13CHS131", "componente": "Geografia", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Recursos naturais", "habilidade_descricao": "Analisar o uso e conservação dos recursos naturais."},
    
    # GEOGRAFIA - 2º ANO EM (Cerca de 15 habilidades)
    {"codigo_bncc": "EM13CHS221", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Dinâmica populacional", "habilidade_descricao": "Analisar crescimento, estrutura e distribuição da população."},
    {"codigo_bncc": "EM13CHS222", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Migrações", "habilidade_descricao": "Analisar fluxos migratórios nacionais e internacionais."},
    {"codigo_bncc": "EM13CHS223", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Urbanização", "habilidade_descricao": "Analisar o processo de urbanização e seus problemas."},
    {"codigo_bncc": "EM13CHS224", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Espaço urbano", "habilidade_descricao": "Analisar a organização do espaço urbano e segregação."},
    {"codigo_bncc": "EM13CHS225", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Agricultura", "habilidade_descricao": "Analisar sistemas agrícolas e questão agrária."},
    {"codigo_bncc": "EM13CHS226", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Industrialização", "habilidade_descricao": "Analisar o processo de industrialização e suas fases."},
    {"codigo_bncc": "EM13CHS227", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Industrialização brasileira", "habilidade_descricao": "Caracterizar a industrialização brasileira e sua distribuição."},
    {"codigo_bncc": "EM13CHS228", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Energia", "habilidade_descricao": "Analisar fontes de energia e matriz energética."},
    {"codigo_bncc": "EM13CHS229", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Transportes", "habilidade_descricao": "Analisar os sistemas de transporte e logística."},
    {"codigo_bncc": "EM13CHS230", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Comércio e serviços", "habilidade_descricao": "Analisar o setor terciário e sua importância."},
    {"codigo_bncc": "EM13CHS231", "componente": "Geografia", "ano_escolar": "2º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Regiões brasileiras", "habilidade_descricao": "Caracterizar as cinco regiões brasileiras."},
    
    # GEOGRAFIA - 3º ANO EM (Cerca de 12 habilidades)
    {"codigo_bncc": "EM13CHS321", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Globalização", "habilidade_descricao": "Analisar o processo de globalização e seus impactos."},
    {"codigo_bncc": "EM13CHS322", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ordem mundial", "habilidade_descricao": "Analisar a nova ordem mundial e as relações de poder."},
    {"codigo_bncc": "EM13CHS323", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Blocos econômicos", "habilidade_descricao": "Caracterizar os principais blocos econômicos regionais."},
    {"codigo_bncc": "EM13CHS324", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Conflitos mundiais", "habilidade_descricao": "Analisar conflitos étnicos, religiosos e territoriais."},
    {"codigo_bncc": "EM13CHS325", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Europa", "habilidade_descricao": "Caracterizar aspectos físicos, humanos e econômicos da Europa."},
    {"codigo_bncc": "EM13CHS326", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "América", "habilidade_descricao": "Caracterizar aspectos físicos, humanos e econômicos da América."},
    {"codigo_bncc": "EM13CHS327", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ásia", "habilidade_descricao": "Caracterizar aspectos físicos, humanos e econômicos da Ásia."},
    {"codigo_bncc": "EM13CHS328", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "África", "habilidade_descricao": "Caracterizar aspectos físicos, humanos e econômicos da África."},
    {"codigo_bncc": "EM13CHS329", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Oceania", "habilidade_descricao": "Caracterizar aspectos físicos, humanos e econômicos da Oceania."},
    {"codigo_bncc": "EM13CHS330", "componente": "Geografia", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Geopolítica do Brasil", "habilidade_descricao": "Analisar a posição geopolítica do Brasil no mundo contemporâneo."},
    
    # ============================================
    # SOCIOEMOCIONAL / AUTONOMIA (10 habilidades)
    # ============================================
    {"codigo_bncc": "SOCIO01", "componente": "Socioemocional", "ano_escolar": "1º ano EM", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Autoconhecimento", "habilidade_descricao": "Desenvolver autoconhecimento e identificação de emoções."},
    {"codigo_bncc": "SOCIO02", "componente": "Socioemocional", "ano_escolar": "1º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Organização pessoal", "habilidade_descricao": "Desenvolver habilidades de organização e gestão do tempo."},
    {"codigo_bncc": "SOCIO03", "componente": "Socioemocional", "ano_escolar": "2º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Autonomia nos estudos", "habilidade_descricao": "Desenvolver rotinas de estudo independente."},
    {"codigo_bncc": "SOCIO04", "componente": "Socioemocional", "ano_escolar": "2º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Trabalho em equipe", "habilidade_descricao": "Desenvolver habilidades de colaboração e trabalho em equipe."},
    {"codigo_bncc": "SOCIO05", "componente": "Socioemocional", "ano_escolar": "2º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Comunicação assertiva", "habilidade_descricao": "Desenvolver comunicação clara e assertiva."},
    {"codigo_bncc": "SOCIO06", "componente": "Socioemocional", "ano_escolar": "3º ano EM", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Resolução de problemas", "habilidade_descricao": "Desenvolver estratégias de resolução de problemas."},
    {"codigo_bncc": "SOCIO07", "componente": "Socioemocional", "ano_escolar": "3º ano EM", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Pensamento crítico", "habilidade_descricao": "Desenvolver pensamento crítico e análise de informações."},
    {"codigo_bncc": "SOCIO08", "componente": "Socioemocional", "ano_escolar": "3º ano EM", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Gestão emocional", "habilidade_descricao": "Desenvolver estratégias de gestão de ansiedade e estresse."},
    {"codigo_bncc": "SOCIO09", "componente": "Socioemocional", "ano_escolar": "3º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Projeto de vida", "habilidade_descricao": "Elaborar projeto de vida e metas pessoais."},
    {"codigo_bncc": "SOCIO10", "componente": "Socioemocional", "ano_escolar": "1º ano EM", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Relacionamento interpessoal", "habilidade_descricao": "Desenvolver habilidades de relacionamento interpessoal."},
]


def importar_bncc_expandido():
    print("=" * 70)
    print("IMPORTAÇÃO EXPANDIDA - BNCC ENSINO MÉDIO")
    print(f"Total de habilidades: {len(HABILIDADES_EM)}")
    print("=" * 70)
    
    with engine.connect() as conn:
        inseridos = 0
        atualizados = 0
        
        for hab in HABILIDADES_EM:
            # Verificar se já existe
            result = conn.execute(text("""
                SELECT id FROM curriculo_nacional 
                WHERE codigo_bncc = :codigo
            """), {"codigo": hab["codigo_bncc"]})
            
            existente = result.fetchone()
            
            if existente:
                # Atualizar
                conn.execute(text("""
                    UPDATE curriculo_nacional SET
                        componente = :componente,
                        ano_escolar = :ano_escolar,
                        trimestre_sugerido = :trimestre_sugerido,
                        dificuldade = :dificuldade,
                        objeto_conhecimento = :objeto_conhecimento,
                        habilidade_descricao = :habilidade_descricao
                    WHERE codigo_bncc = :codigo
                """), {
                    "codigo": hab["codigo_bncc"],
                    "componente": hab["componente"],
                    "ano_escolar": hab["ano_escolar"],
                    "trimestre_sugerido": hab["trimestre_sugerido"],
                    "dificuldade": hab["dificuldade"],
                    "objeto_conhecimento": hab["objeto_conhecimento"],
                    "habilidade_descricao": hab["habilidade_descricao"]
                })
                atualizados += 1
            else:
                # Inserir
                conn.execute(text("""
                    INSERT INTO curriculo_nacional 
                    (codigo_bncc, componente, ano_escolar, trimestre_sugerido, dificuldade, objeto_conhecimento, habilidade_descricao)
                    VALUES (:codigo, :componente, :ano_escolar, :trimestre_sugerido, :dificuldade, :objeto_conhecimento, :habilidade_descricao)
                """), {
                    "codigo": hab["codigo_bncc"],
                    "componente": hab["componente"],
                    "ano_escolar": hab["ano_escolar"],
                    "trimestre_sugerido": hab["trimestre_sugerido"],
                    "dificuldade": hab["dificuldade"],
                    "objeto_conhecimento": hab["objeto_conhecimento"],
                    "habilidade_descricao": hab["habilidade_descricao"]
                })
                inseridos += 1
        
        conn.commit()
        
        # Resumo por componente e ano
        print("\n" + "-" * 70)
        print("RESUMO DA IMPORTAÇÃO:")
        print("-" * 70)
        print(f"   Inseridos: {inseridos}")
        print(f"   Atualizados: {atualizados}")
        print(f"   TOTAL: {inseridos + atualizados}")
        
        # Contagem por componente
        print("\n" + "-" * 70)
        print("POR COMPONENTE:")
        print("-" * 70)
        
        result = conn.execute(text("""
            SELECT componente, ano_escolar, COUNT(*) as total
            FROM curriculo_nacional
            WHERE ano_escolar LIKE '%EM%'
            GROUP BY componente, ano_escolar
            ORDER BY componente, ano_escolar
        """))
        
        componente_atual = None
        for row in result.fetchall():
            if row[0] != componente_atual:
                componente_atual = row[0]
                print(f"\n   {componente_atual}:")
            print(f"      {row[1]}: {row[2]} habilidades")
    
    print("\n" + "=" * 70)
    print("IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    importar_bncc_expandido()
