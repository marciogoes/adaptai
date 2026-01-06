# ============================================
# IMPORTAR BNCC ENSINO FUNDAMENTAL II - EXPANDIDO
# 6º ao 9º ano - Mais de 250 habilidades
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

# ============================================
# HABILIDADES EXPANDIDAS - ENSINO FUNDAMENTAL II
# ============================================

HABILIDADES_EF2 = [
    # ============================================
    # MATEMÁTICA - 6º ANO (15+ habilidades)
    # ============================================
    {"codigo_bncc": "EF06MA01", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Sistema de numeração decimal", "habilidade_descricao": "Comparar, ordenar, ler e escrever números naturais e números racionais cuja representação decimal é finita, fazendo uso da reta numérica."},
    {"codigo_bncc": "EF06MA02", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Operações com naturais", "habilidade_descricao": "Reconhecer o sistema de numeração decimal, como o que prevaleceu no mundo ocidental, e destacar semelhanças e diferenças com outros sistemas."},
    {"codigo_bncc": "EF06MA03", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Múltiplos e divisores", "habilidade_descricao": "Resolver e elaborar problemas que envolvam cálculos (mentais ou escritos, exatos ou aproximados) com números naturais."},
    {"codigo_bncc": "EF06MA04", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "MMC e MDC", "habilidade_descricao": "Construir algoritmo em linguagem natural e representá-lo por fluxograma que indique a resolução de um problema simples."},
    {"codigo_bncc": "EF06MA05", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Números primos e compostos", "habilidade_descricao": "Classificar números naturais em primos e compostos, estabelecer relações entre números, expressas pelos termos 'é múltiplo de', 'é divisor de', 'é fator de'."},
    {"codigo_bncc": "EF06MA06", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Frações", "habilidade_descricao": "Resolver e elaborar problemas que envolvam as ideias de múltiplo e de divisor."},
    {"codigo_bncc": "EF06MA07", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Operações com frações", "habilidade_descricao": "Compreender, comparar e ordenar frações associadas às ideias de partes de inteiros e resultado de divisão."},
    {"codigo_bncc": "EF06MA08", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Números decimais", "habilidade_descricao": "Reconhecer que os números racionais positivos podem ser expressos nas formas fracionária e decimal."},
    {"codigo_bncc": "EF06MA09", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Operações com decimais", "habilidade_descricao": "Resolver e elaborar problemas que envolvam o cálculo da fração de uma quantidade e cujo resultado seja um número natural."},
    {"codigo_bncc": "EF06MA10", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Porcentagem", "habilidade_descricao": "Resolver e elaborar problemas que envolvam porcentagens, com base na ideia de proporcionalidade."},
    {"codigo_bncc": "EF06MA11", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Geometria plana", "habilidade_descricao": "Resolver problemas que envolvam a noção de ângulo em diferentes contextos e em situações reais."},
    {"codigo_bncc": "EF06MA12", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Polígonos", "habilidade_descricao": "Identificar características dos triângulos e classificá-los em relação às medidas dos lados e dos ângulos."},
    {"codigo_bncc": "EF06MA13", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Perímetro e área", "habilidade_descricao": "Resolver e elaborar problemas que envolvam o cálculo do perímetro de figuras planas."},
    {"codigo_bncc": "EF06MA14", "componente": "Matemática", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Estatística", "habilidade_descricao": "Interpretar e resolver situações que envolvam dados de pesquisas sobre contextos ambientais, sustentabilidade, trânsito."},
    
    # MATEMÁTICA - 7º ANO (15+ habilidades)
    {"codigo_bncc": "EF07MA01", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Números inteiros", "habilidade_descricao": "Resolver e elaborar problemas com números naturais, envolvendo as noções de divisor e de múltiplo."},
    {"codigo_bncc": "EF07MA02", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Operações com inteiros", "habilidade_descricao": "Resolver e elaborar problemas que envolvam porcentagens, como os que lidam com acréscimos e decréscimos simples."},
    {"codigo_bncc": "EF07MA03", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Reta numérica", "habilidade_descricao": "Comparar e ordenar números inteiros em diferentes contextos, incluindo o histórico, associá-los a pontos da reta numérica."},
    {"codigo_bncc": "EF07MA04", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Potenciação", "habilidade_descricao": "Resolver e elaborar problemas que envolvam operações com números inteiros."},
    {"codigo_bncc": "EF07MA05", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Números racionais", "habilidade_descricao": "Resolver um mesmo problema utilizando diferentes algoritmos."},
    {"codigo_bncc": "EF07MA06", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Operações com racionais", "habilidade_descricao": "Reconhecer que as resoluções de um grupo de problemas que têm a mesma estrutura podem ser obtidas utilizando os mesmos procedimentos."},
    {"codigo_bncc": "EF07MA07", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Equações do 1º grau", "habilidade_descricao": "Representar por meio de um fluxograma os passos utilizados para resolver um grupo de problemas."},
    {"codigo_bncc": "EF07MA08", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Inequações", "habilidade_descricao": "Comparar e ordenar frações e números decimais em diferentes contextos por meio de estratégias variadas."},
    {"codigo_bncc": "EF07MA09", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Razão e proporção", "habilidade_descricao": "Utilizar, na resolução de problemas, a associação entre razão e fração, como a expression três é para quatro."},
    {"codigo_bncc": "EF07MA10", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Grandezas proporcionais", "habilidade_descricao": "Comparar e ordenar números racionais em diferentes contextos e associá-los a pontos da reta numérica."},
    {"codigo_bncc": "EF07MA11", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Regra de três", "habilidade_descricao": "Compreender e utilizar a multiplicação e a divisão de números racionais, a relação entre elas e suas propriedades operatórias."},
    {"codigo_bncc": "EF07MA12", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Ângulos", "habilidade_descricao": "Resolver e elaborar problemas que envolvam as operações com números racionais."},
    {"codigo_bncc": "EF07MA13", "componente": "Matemática", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Triângulos", "habilidade_descricao": "Verificar relações entre os ângulos formados por retas paralelas cortadas por uma transversal."},
    
    # MATEMÁTICA - 8º ANO (15+ habilidades)
    {"codigo_bncc": "EF08MA01", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Notação científica", "habilidade_descricao": "Efetuar cálculos com potências de expoentes inteiros e aplicar esse conhecimento na representação de números em notação científica."},
    {"codigo_bncc": "EF08MA02", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Potenciação e radiciação", "habilidade_descricao": "Resolver e elaborar problemas usando a relação entre potenciação e radiciação, para representar uma raiz como potência de expoente fracionário."},
    {"codigo_bncc": "EF08MA03", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Números irracionais", "habilidade_descricao": "Resolver e elaborar problemas de contagem cuja resolução envolva a aplicação do princípio multiplicativo."},
    {"codigo_bncc": "EF08MA04", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Dízimas periódicas", "habilidade_descricao": "Resolver e elaborar problemas, envolvendo cálculo de porcentagens, incluindo o uso de tecnologias digitais."},
    {"codigo_bncc": "EF08MA05", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Expressões algébricas", "habilidade_descricao": "Reconhecer e utilizar procedimentos para a obtenção de uma fração geratriz para uma dízima periódica."},
    {"codigo_bncc": "EF08MA06", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Monômios e polinômios", "habilidade_descricao": "Resolver e elaborar problemas que envolvam cálculo do valor numérico de expressões algébricas."},
    {"codigo_bncc": "EF08MA07", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Fatoração", "habilidade_descricao": "Associar uma equação linear de 1o grau com duas incógnitas a uma reta no plano cartesiano."},
    {"codigo_bncc": "EF08MA08", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Sistemas de equações", "habilidade_descricao": "Resolver e elaborar problemas relacionados ao seu contexto próximo, que possam ser representados por sistemas de equações de 1º grau."},
    {"codigo_bncc": "EF08MA09", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Equações do 2º grau", "habilidade_descricao": "Resolver e elaborar, com e sem uso de tecnologias, problemas que possam ser representados por equações polinomiais de 2º grau do tipo ax² = b."},
    {"codigo_bncc": "EF08MA10", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Congruência de triângulos", "habilidade_descricao": "Identificar a relação entre duas grandezas em gráficos que representem relações não proporcionais."},
    {"codigo_bncc": "EF08MA11", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Teorema de Tales", "habilidade_descricao": "Aplicar as relações métricas, incluindo as relações de proporcionalidade, em figuras planas."},
    {"codigo_bncc": "EF08MA12", "componente": "Matemática", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Teorema de Pitágoras", "habilidade_descricao": "Demonstrar propriedades de quadriláteros por meio da identificação da congruência de triângulos."},
    
    # MATEMÁTICA - 9º ANO (15+ habilidades)
    {"codigo_bncc": "EF09MA01", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Números reais", "habilidade_descricao": "Reconhecer que, uma vez fixada uma unidade de comprimento, existem segmentos de reta cujo comprimento não é expresso por número racional."},
    {"codigo_bncc": "EF09MA02", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Radiciação", "habilidade_descricao": "Reconhecer um número irracional como um número real cuja representação decimal é infinita e não periódica."},
    {"codigo_bncc": "EF09MA03", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Potências com expoentes negativos", "habilidade_descricao": "Efetuar cálculos com números reais, inclusive potências com expoentes negativos e radicais."},
    {"codigo_bncc": "EF09MA04", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Equações do 2º grau", "habilidade_descricao": "Resolver e elaborar problemas com números reais, inclusive em notação científica, envolvendo diferentes operações."},
    {"codigo_bncc": "EF09MA05", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Fórmula de Bhaskara", "habilidade_descricao": "Reconhecer e empregar unidades usadas para expressar medidas muito grandes ou muito pequenas."},
    {"codigo_bncc": "EF09MA06", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Função afim", "habilidade_descricao": "Compreender as funções como relações de dependência unívoca entre duas variáveis e suas representações numérica, algébrica e gráfica."},
    {"codigo_bncc": "EF09MA07", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Função quadrática", "habilidade_descricao": "Resolver problemas que envolvam a razão entre duas grandezas de espécies diferentes, como velocidade e densidade demográfica."},
    {"codigo_bncc": "EF09MA08", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Gráficos de funções", "habilidade_descricao": "Resolver e elaborar problemas que envolvam relações de proporcionalidade direta e inversa entre duas ou mais grandezas."},
    {"codigo_bncc": "EF09MA09", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Semelhança de triângulos", "habilidade_descricao": "Compreender os processos de fatoração de expressões algébricas, com base em suas relações com os produtos notáveis."},
    {"codigo_bncc": "EF09MA10", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Relações métricas", "habilidade_descricao": "Demonstrar relações simples entre os ângulos formados por retas paralelas cortadas por uma transversal."},
    {"codigo_bncc": "EF09MA11", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Trigonometria no triângulo retângulo", "habilidade_descricao": "Resolver problemas por meio do estabelecimento de relações entre razões trigonométricas (seno, cosseno, tangente) e aplicá-las em contextos diversos."},
    {"codigo_bncc": "EF09MA12", "componente": "Matemática", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Probabilidade", "habilidade_descricao": "Reconhecer, em experimentos aleatórios, eventos independentes e dependentes e calcular a probabilidade de sua ocorrência."},
    
    # ============================================
    # LÍNGUA PORTUGUESA - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06LP01", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Variação linguística", "habilidade_descricao": "Reconhecer a impossibilidade de uma língua ser totalmente homogênea, considerando as variações dialetais."},
    {"codigo_bncc": "EF06LP02", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Concordância", "habilidade_descricao": "Estabelecer relação entre partes do texto, identificando substituições lexicais ou pronominais que contribuem para a continuidade do texto."},
    {"codigo_bncc": "EF06LP03", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais - Notícia", "habilidade_descricao": "Analisar diferenças de sentido entre palavras de uma série sinonímica."},
    {"codigo_bncc": "EF06LP04", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Estrutura da notícia", "habilidade_descricao": "Analisar a estrutura e os procedimentos de construção de textos do gênero notícia."},
    {"codigo_bncc": "EF06LP05", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Coesão textual", "habilidade_descricao": "Identificar os efeitos de sentido dos processos de coesão textual (referenciação e sequenciação)."},
    {"codigo_bncc": "EF06LP06", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Pontuação", "habilidade_descricao": "Empregar, adequadamente, as regras de concordância nominal (relações entre os substantivos e seus determinantes) e as regras de concordância verbal."},
    {"codigo_bncc": "EF06LP07", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Narrativa", "habilidade_descricao": "Identificar, em texto narrativo ficcional, a estrutura da narração – Loss personagens, o tempo e o espaço."},
    {"codigo_bncc": "EF06LP08", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Produção textual", "habilidade_descricao": "Identificar, em texto ou sequência textual, orações como unidades constituídas em torno de um núcleo verbal."},
    {"codigo_bncc": "EF06LP09", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Classe de palavras", "habilidade_descricao": "Classificar, em texto ou sequência textual, os períodos simples compostos."},
    {"codigo_bncc": "EF06LP10", "componente": "Língua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Substantivos e adjetivos", "habilidade_descricao": "Identificar, em texto ou sequência textual, substantivos, verbos e adjetivos."},
    
    # LÍNGUA PORTUGUESA - 7º ANO
    {"codigo_bncc": "EF07LP01", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Textualização", "habilidade_descricao": "Distinguir diferentes propostas editoriais – Loss diferentes textos que compõem, distribuição das informações, imagens."},
    {"codigo_bncc": "EF07LP02", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Gêneros jornalísticos", "habilidade_descricao": "Comparar notícias e reportagens sobre um mesmo fato divulgadas em diferentes mídias."},
    {"codigo_bncc": "EF07LP03", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Argumentação", "habilidade_descricao": "Formar, com base em texto ou livro lido, opinião própria sobre os procedimentos argumentativos utilizados."},
    {"codigo_bncc": "EF07LP04", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Carta do leitor", "habilidade_descricao": "Reconhecer, em textos, os efeitos de sentido do uso de elementos da morfossintaxe."},
    {"codigo_bncc": "EF07LP05", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Coerência", "habilidade_descricao": "Identificar, em orações de textos lidos ou de produção própria, verbos de predicação completa e incompleta."},
    {"codigo_bncc": "EF07LP06", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Poesia", "habilidade_descricao": "Empregar as regras básicas de concordância nominal e verbal em situações comunicativas e na produção de textos."},
    {"codigo_bncc": "EF07LP07", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Figuras de linguagem", "habilidade_descricao": "Identificar, em textos lidos ou de produção própria, a estrutura básica da oração: sujeito, predicado, complemento."},
    {"codigo_bncc": "EF07LP08", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Crônica", "habilidade_descricao": "Identificar, em textos lidos ou de produção própria, adjetivos que ampliam o sentido do substantivo sujeito ou complemento verbal."},
    {"codigo_bncc": "EF07LP09", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Verbos", "habilidade_descricao": "Identificar, em textos lidos ou de produção própria, advérbios e locuções adverbiais."},
    {"codigo_bncc": "EF07LP10", "componente": "Língua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Tempos verbais", "habilidade_descricao": "Utilizar, ao produzir texto, conhecimentos linguísticos e gramaticais: modos e tempos verbais, concordância nominal e verbal."},
    
    # LÍNGUA PORTUGUESA - 8º ANO
    {"codigo_bncc": "EF08LP01", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Textualidade", "habilidade_descricao": "Identificar e comparar as várias editorias de jornais impressos e digitais e de sites noticiosos."},
    {"codigo_bncc": "EF08LP02", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Reportagem", "habilidade_descricao": "Justificar diferenças ou semelhanças no tratamento dado a uma mesma informação veiculada em textos diferentes."},
    {"codigo_bncc": "EF08LP03", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Artigo de opinião", "habilidade_descricao": "Produzir artigos de opinião, tendo em vista o contexto de produção dado, a defesa de um ponto de vista."},
    {"codigo_bncc": "EF08LP04", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Período composto", "habilidade_descricao": "Utilizar, ao produzir texto, conhecimentos linguísticos e gramaticais: ortografia, regências e concordâncias nominal e verbal."},
    {"codigo_bncc": "EF08LP05", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Orações coordenadas", "habilidade_descricao": "Analisar processos de formação de palavras por composição e derivação, inferindo seus significados."},
    {"codigo_bncc": "EF08LP06", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Orações subordinadas", "habilidade_descricao": "Identificar, em textos lidos ou de produção própria, os termos constitutivos da oração (sujeito e seus modificadores)."},
    {"codigo_bncc": "EF08LP07", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Regência", "habilidade_descricao": "Diferenciar, em textos lidos ou de produção própria, complementos diretos e indiretos de verbos transitivos."},
    {"codigo_bncc": "EF08LP08", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Romance", "habilidade_descricao": "Identificar, em textos lidos ou de produção própria, verbos na voz ativa e na voz passiva, interpretando os efeitos de sentido."},
    {"codigo_bncc": "EF08LP09", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Discurso direto e indireto", "habilidade_descricao": "Interpretar, em textos lidos ou de produção própria, efeitos de sentido de modificadores do verbo."},
    {"codigo_bncc": "EF08LP10", "componente": "Língua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Intertextualidade", "habilidade_descricao": "Interpretar, em textos lidos ou de produção própria, quantificadores indefinidos, definidos e distributivos."},
    
    # LÍNGUA PORTUGUESA - 9º ANO
    {"codigo_bncc": "EF09LP01", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Texto dissertativo-argumentativo", "habilidade_descricao": "Analisar o fenômeno da disseminação de notícias falsas nas redes sociais e desenvolver estratégias para reconhecê-las."},
    {"codigo_bncc": "EF09LP02", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Estratégias argumentativas", "habilidade_descricao": "Analisar e comentar a cobertura da imprensa sobre fatos de relevância social, comparando diferentes enfoques por meio do uso de ferramentas de curadoria."},
    {"codigo_bncc": "EF09LP03", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Debate regrado", "habilidade_descricao": "Produzir artigos de opinião, tendo em vista o contexto de produção dado, assumindo posição diante de tema polêmico."},
    {"codigo_bncc": "EF09LP04", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Orações complexas", "habilidade_descricao": "Escrever textos corretamente, de acordo com a norma-padrão, com estruturas sintáticas complexas no nível da oração e do período."},
    {"codigo_bncc": "EF09LP05", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Crase", "habilidade_descricao": "Identificar, em textos lidos e em produções próprias, orações com a estrutura sujeito-verbo de ligação-predicativo."},
    {"codigo_bncc": "EF09LP06", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Colocação pronominal", "habilidade_descricao": "Diferenciar, em textos lidos e em produções próprias, o efeito de sentido do uso dos verbos de ligação."},
    {"codigo_bncc": "EF09LP07", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Literatura brasileira", "habilidade_descricao": "Comparar o uso de regência verbal e regência nominal na norma-padrão com seu uso no português brasileiro coloquial oral."},
    {"codigo_bncc": "EF09LP08", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Modernismo", "habilidade_descricao": "Identificar, em textos lidos e em produções próprias, a relação que conjunções (e locuções conjuntivas) coordenativas e subordinativas estabelecem entre as orações que conectam."},
    {"codigo_bncc": "EF09LP09", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Revisão e reescrita", "habilidade_descricao": "Identificar efeitos de sentido do uso de orações adjetivas restritivas e explicativas em um período composto."},
    {"codigo_bncc": "EF09LP10", "componente": "Língua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Redação ENEM preparatória", "habilidade_descricao": "Comparar as regras de colocação pronominal na norma-padrão com o seu uso no português brasileiro coloquial."},
    
    # ============================================
    # CIÊNCIAS - 6º ao 9º ANO
    # ============================================
    # 6º ANO
    {"codigo_bncc": "EF06CI01", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Misturas homogêneas e heterogêneas", "habilidade_descricao": "Classificar como homogênea ou heterogênea a mistura de dois ou mais materiais."},
    {"codigo_bncc": "EF06CI02", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Separação de materiais", "habilidade_descricao": "Identificar evidências de transformações químicas a partir do resultado de misturas de materiais."},
    {"codigo_bncc": "EF06CI03", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Materiais sintéticos", "habilidade_descricao": "Selecionar métodos mais adequados para a separação de diferentes sistemas heterogêneos."},
    {"codigo_bncc": "EF06CI04", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Célula como unidade da vida", "habilidade_descricao": "Associar a produção de medicamentos e outros materiais sintéticos ao desenvolvimento científico e tecnológico."},
    {"codigo_bncc": "EF06CI05", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Níveis de organização dos seres vivos", "habilidade_descricao": "Explicar a organização básica das células e seu papel como unidade estrutural e funcional dos seres vivos."},
    {"codigo_bncc": "EF06CI06", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Interação entre os sistemas locomotor e nervoso", "habilidade_descricao": "Concluir, com base na análise de ilustrações e/ou modelos, que os organismos são um complexo arranjo de sistemas."},
    {"codigo_bncc": "EF06CI07", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Forma, estrutura e movimentos da Terra", "habilidade_descricao": "Justificar o papel do sistema nervoso na coordenação das ações motoras e sensoriais do corpo."},
    {"codigo_bncc": "EF06CI08", "componente": "Ciências", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Sol como fonte de energia", "habilidade_descricao": "Explicar a importância da visão na interação do organismo com o ambiente e os cuidados necessários à manutenção da saúde visual."},
    
    # 7º ANO
    {"codigo_bncc": "EF07CI01", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Máquinas simples", "habilidade_descricao": "Discutir a aplicação, ao longo da história, das máquinas simples e propor soluções e invenções para a realização de tarefas mecânicas cotidianas."},
    {"codigo_bncc": "EF07CI02", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Formas de propagação do calor", "habilidade_descricao": "Diferenciar temperatura, calor e sensação térmica nas diferentes situações de equilíbrio termodinâmico cotidianas."},
    {"codigo_bncc": "EF07CI03", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Equilíbrio termodinâmico", "habilidade_descricao": "Utilizar o conhecimento das formas de propagação do calor para justificar a utilização de determinados materiais."},
    {"codigo_bncc": "EF07CI04", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "História dos combustíveis", "habilidade_descricao": "Avaliar o papel do equilíbrio termodinâmico para a manutenção da vida na Terra, para o funcionamento de máquinas térmicas."},
    {"codigo_bncc": "EF07CI05", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Diversidade de ecossistemas", "habilidade_descricao": "Discutir o uso de diferentes tipos de combustível e máquinas térmicas ao longo do tempo, para avaliar avanços, questões econômicas e problemas socioambientais."},
    {"codigo_bncc": "EF07CI06", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Fenômenos naturais e impactos ambientais", "habilidade_descricao": "Discutir e avaliar mudanças econômicas, culturais e sociais, tanto na vida cotidiana quanto no mundo do trabalho, decorrentes do desenvolvimento de novos materiais e tecnologias."},
    {"codigo_bncc": "EF07CI07", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Programas de saúde pública", "habilidade_descricao": "Caracterizar os principais ecossistemas brasileiros quanto à paisagem, à quantidade de água, ao tipo de solo, à disponibilidade de luz solar, à temperatura etc."},
    {"codigo_bncc": "EF07CI08", "componente": "Ciências", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Composição do ar", "habilidade_descricao": "Avaliar como os impactos provocados por catástrofes naturais ou mudanças nos componentes físicos, biológicos ou sociais de um ecossistema afetam suas populações."},
    
    # 8º ANO
    {"codigo_bncc": "EF08CI01", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Fontes e tipos de energia", "habilidade_descricao": "Identificar e classificar diferentes fontes (renováveis e não renováveis) e tipos de energia utilizados em residências, comunidades ou cidades."},
    {"codigo_bncc": "EF08CI02", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Transformação de energia", "habilidade_descricao": "Construir circuitos elétricos com pilha/bateria, fios e lâmpada ou outros dispositivos e compará-los a circuitos elétricos residenciais."},
    {"codigo_bncc": "EF08CI03", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Cálculo de consumo de energia elétrica", "habilidade_descricao": "Classificar equipamentos elétricos residenciais (chuveiro, ferro, lâmpadas, TV, rádio, geladeira etc.) de acordo com o tipo de transformação de energia."},
    {"codigo_bncc": "EF08CI04", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Uso consciente de energia elétrica", "habilidade_descricao": "Calcular o consumo de eletrodomésticos a partir dos dados de potência (descritos no próprio equipamento) e tempo médio de uso."},
    {"codigo_bncc": "EF08CI05", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Mecanismos reprodutivos", "habilidade_descricao": "Propor ações coletivas para otimizar o uso de energia elétrica em sua escola e/ou comunidade, com base na seleção de equipamentos segundo critérios de sustentabilidade."},
    {"codigo_bncc": "EF08CI06", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Sexualidade", "habilidade_descricao": "Discutir e avaliar usinas de geração de energia elétrica, considerando os impactos socioambientais, os recursos disponíveis e os tipos de energia empregados."},
    {"codigo_bncc": "EF08CI07", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Doenças sexualmente transmissíveis", "habilidade_descricao": "Comparar diferentes processos reprodutivos em plantas e animais em relação aos mecanismos adaptativos e evolutivos."},
    {"codigo_bncc": "EF08CI08", "componente": "Ciências", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Clima", "habilidade_descricao": "Analisar e explicar as transformações que ocorrem na puberdade considerando a atuação dos hormônios sexuais."},
    
    # 9º ANO
    {"codigo_bncc": "EF09CI01", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Aspectos quantitativos das transformações químicas", "habilidade_descricao": "Investigar as mudanças de estado físico da matéria e explicar essas transformações com base no modelo de constituição submicroscópica."},
    {"codigo_bncc": "EF09CI02", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Estrutura da matéria", "habilidade_descricao": "Comparar quantidades de reagentes e produtos envolvidos em transformações químicas, estabelecendo a proporção entre as suas massas."},
    {"codigo_bncc": "EF09CI03", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Radiação e ondas eletromagnéticas", "habilidade_descricao": "Identificar modelos que descrevem a estrutura da matéria e reconhecer sua evolução histórica."},
    {"codigo_bncc": "EF09CI04", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Hereditariedade", "habilidade_descricao": "Planejar e executar experimentos que evidenciem que todas as cores de luz podem ser formadas pela composição das três cores primárias da luz."},
    {"codigo_bncc": "EF09CI05", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Ideias evolucionistas", "habilidade_descricao": "Investigar os principais mecanismos envolvidos na transmissão e recepção de imagem e som que revolucionaram os sistemas de comunicação humana."},
    {"codigo_bncc": "EF09CI06", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Preservação da biodiversidade", "habilidade_descricao": "Classificar as radiações eletromagnéticas por suas frequências, fontes e aplicações, discutindo e avaliando as implicações de seu uso em controle remoto, telefone celular, raio X, forno de micro-ondas, fotocélulas etc."},
    {"codigo_bncc": "EF09CI07", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Composição e estrutura do Sistema Solar", "habilidade_descricao": "Discutir o papel do avanço tecnológico na aplicação das radiações na medicina diagnóstica e no tratamento de doenças."},
    {"codigo_bncc": "EF09CI08", "componente": "Ciências", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Ordem de grandeza astronômica", "habilidade_descricao": "Associar os gametas à transmissão das características hereditárias, estabelecendo relações entre ancestrais e descendentes."},
    
    # ============================================
    # HISTÓRIA - 6º ao 9º ANO
    # ============================================
    # 6º ANO
    {"codigo_bncc": "EF06HI01", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Tempo e história", "habilidade_descricao": "Identificar diferentes formas de compreensão da noção de tempo e de periodização dos processos históricos."},
    {"codigo_bncc": "EF06HI02", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Fontes históricas", "habilidade_descricao": "Identificar a gênese da produção do saber histórico e analisar o significado das fontes que originaram determinadas formas de registro em sociedades e épocas distintas."},
    {"codigo_bncc": "EF06HI03", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Povos da Antiguidade", "habilidade_descricao": "Identificar as hipóteses científicas sobre o surgimento da espécie humana e sua historicidade e analisar os significados dos mitos de fundação."},
    {"codigo_bncc": "EF06HI04", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Civilizações do Oriente Próximo", "habilidade_descricao": "Conhecer as teorias sobre a origem do homem americano."},
    {"codigo_bncc": "EF06HI05", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Grécia Antiga", "habilidade_descricao": "Descrever modificações da natureza e da paisagem realizadas por diferentes tipos de sociedade, com destaque para os povos indígenas originários e povos africanos."},
    {"codigo_bncc": "EF06HI06", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Roma Antiga", "habilidade_descricao": "Identificar geograficamente as rotas de povoamento no território americano."},
    {"codigo_bncc": "EF06HI07", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Culturas e povos africanos", "habilidade_descricao": "Identificar aspectos e formas de registro das sociedades antigas na África, no Oriente Médio e nas Américas."},
    {"codigo_bncc": "EF06HI08", "componente": "História", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Relações entre Estado e religião", "habilidade_descricao": "Identificar os espaços territoriais ocupados e os aportes culturais, científicos, sociais e econômicos dos astecas, maias e incas e dos povos indígenas de diversas regiões brasileiras."},
    
    # 7º ANO
    {"codigo_bncc": "EF07HI01", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "A construção da ideia de modernidade", "habilidade_descricao": "Explicar o significado de 'modernidade' e suas lógicas de inclusão e exclusão, com base em uma concepção europeia."},
    {"codigo_bncc": "EF07HI02", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Reformas religiosas", "habilidade_descricao": "Identificar conexões e interações entre as sociedades do Novo Mundo, da Europa, da África e da Ásia no contexto das navegações."},
    {"codigo_bncc": "EF07HI03", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Absolutismo", "habilidade_descricao": "Identificar aspectos e processos específicos das sociedades africanas e americanas antes da chegada dos europeus."},
    {"codigo_bncc": "EF07HI04", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Colonização da América portuguesa", "habilidade_descricao": "Identificar e relacionar as vinculações entre as reformas religiosas e os processos culturais e sociais do período moderno na Europa e na América."},
    {"codigo_bncc": "EF07HI05", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Colonização da América espanhola", "habilidade_descricao": "Identificar e relacionar as vinculações da história da América Latina com a história geral."},
    {"codigo_bncc": "EF07HI06", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Escravidão africana na América", "habilidade_descricao": "Comparar as navegações no Atlântico e no Pacífico entre os séculos XIV e XVI."},
    {"codigo_bncc": "EF07HI07", "componente": "História", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Resistências indígenas e africanas", "habilidade_descricao": "Descrever os processos de formação e consolidação das monarquias e suas principais características com vistas à compreensão das razões da centralização política."},
    
    # 8º ANO
    {"codigo_bncc": "EF08HI01", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Revolução Industrial", "habilidade_descricao": "Identificar os principais aspectos conceituais do iluminismo e do liberalismo e discutir a relação entre eles e a organização do mundo contemporâneo."},
    {"codigo_bncc": "EF08HI02", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Revoluções burguesas", "habilidade_descricao": "Identificar as particularidades político-sociais da Inglaterra do século XVII e analisar os desdobramentos posteriores à Revolução Gloriosa."},
    {"codigo_bncc": "EF08HI03", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Independência das colônias americanas", "habilidade_descricao": "Analisar os impactos da Revolução Industrial na produção e circulação de povos, produtos e culturas."},
    {"codigo_bncc": "EF08HI04", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Brasil: Primeiro e Segundo Reinado", "habilidade_descricao": "Identificar e relacionar os processos da Revolução Francesa e seus desdobramentos na Europa e no mundo."},
    {"codigo_bncc": "EF08HI05", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Processo de independência do Brasil", "habilidade_descricao": "Explicar os movimentos e as rebeliões da América portuguesa, articulando as temáticas locais e suas interfaces com processos ocorridos na Europa e nas Américas."},
    {"codigo_bncc": "EF08HI06", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Abolição da escravatura", "habilidade_descricao": "Aplicar os conceitos de Estado, nação, território, governo e país para o entendimento de conflitos e tensões."},
    {"codigo_bncc": "EF08HI07", "componente": "História", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "República no Brasil", "habilidade_descricao": "Identificar e contextualizar as especificidades dos diversos processos de independência nas Américas, seus aspectos populacionais e suas conformações territoriais."},
    
    # 9º ANO
    {"codigo_bncc": "EF09HI01", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Primeira Guerra Mundial", "habilidade_descricao": "Descrever e contextualizar os principais aspectos sociais, culturais, econômicos e políticos da emergência da República no Brasil."},
    {"codigo_bncc": "EF09HI02", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Revolução Russa", "habilidade_descricao": "Caracterizar e compreender os ciclos da história republicana, identificando particularidades da história local e regional até 1954."},
    {"codigo_bncc": "EF09HI03", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Totalitarismos", "habilidade_descricao": "Identificar os mecanismos de inserção dos negros na sociedade brasileira pós-abolição e avaliar os seus resultados."},
    {"codigo_bncc": "EF09HI04", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Segunda Guerra Mundial", "habilidade_descricao": "Discutir a importância da participação da população negra na formação econômica, política e social do Brasil."},
    {"codigo_bncc": "EF09HI05", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Guerra Fria", "habilidade_descricao": "Identificar os processos de urbanização e modernização da sociedade brasileira e avaliar suas contradições e impactos na região em que vive."},
    {"codigo_bncc": "EF09HI06", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Ditaduras na América Latina", "habilidade_descricao": "Identificar e discutir o papel do trabalhismo como força política, social e cultural no Brasil, em diferentes escalas."},
    {"codigo_bncc": "EF09HI07", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Ditadura Militar no Brasil", "habilidade_descricao": "Identificar e explicar, em meio a lógicas de inclusão e exclusão, as pautas dos povos indígenas, no contexto republicano."},
    {"codigo_bncc": "EF09HI08", "componente": "História", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Redemocratização no Brasil", "habilidade_descricao": "Identificar as transformações ocorridas no debate sobre as questões da diversidade no Brasil durante o século XX e compreender o significado das mudanças de abordagem em relação ao tema."},
    
    # ============================================
    # GEOGRAFIA - 6º ao 9º ANO
    # ============================================
    # 6º ANO
    {"codigo_bncc": "EF06GE01", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Identidade sociocultural", "habilidade_descricao": "Comparar modificações das paisagens nos lugares de vivência e os usos desses lugares em diferentes tempos."},
    {"codigo_bncc": "EF06GE02", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Território e territorialidade", "habilidade_descricao": "Analisar modificações de paisagens por diferentes tipos de sociedade, com destaque para os povos originários."},
    {"codigo_bncc": "EF06GE03", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Relações campo-cidade", "habilidade_descricao": "Descrever os movimentos do planeta e sua relação com a circulação geral da atmosfera, o tempo atmosférico e os padrões climáticos."},
    {"codigo_bncc": "EF06GE04", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Fenômenos naturais e sociais", "habilidade_descricao": "Identificar o consumo dos recursos hídricos e o uso das principais bacias hidrográficas no Brasil e no mundo."},
    {"codigo_bncc": "EF06GE05", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Relevo", "habilidade_descricao": "Relacionar padrões climáticos, tipos de solo, relevo e formações vegetais."},
    {"codigo_bncc": "EF06GE06", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Transformação das paisagens naturais e antrópicas", "habilidade_descricao": "Identificar as características das paisagens transformadas pelo trabalho humano a partir do desenvolvimento da agropecuária e do processo de industrialização."},
    
    # 7º ANO
    {"codigo_bncc": "EF07GE01", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Formação territorial do Brasil", "habilidade_descricao": "Avaliar, por meio de exemplos extraídos dos meios de comunicação, ideias e estereótipos acerca das paisagens e da formação territorial do Brasil."},
    {"codigo_bncc": "EF07GE02", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Características da população brasileira", "habilidade_descricao": "Analisar a influência dos fluxos econômicos e populacionais na formação socioeconômica e territorial do Brasil."},
    {"codigo_bncc": "EF07GE03", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Produção, circulação e consumo de mercadorias", "habilidade_descricao": "Selecionar argumentos que reconheçam as territorialidades dos povos indígenas originários, das comunidades remanescentes de quilombos."},
    {"codigo_bncc": "EF07GE04", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Desigualdade social e trabalho", "habilidade_descricao": "Analisar a distribuição territorial da população brasileira, considerando a diversidade étnico-cultural, assim como aspectos de renda, sexo e idade nas regiões brasileiras."},
    {"codigo_bncc": "EF07GE05", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Mapas temáticos do Brasil", "habilidade_descricao": "Analisar fatos e situações representativas das alterações ocorridas entre o período mercantilista e o advento do capitalismo."},
    {"codigo_bncc": "EF07GE06", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Biodiversidade brasileira", "habilidade_descricao": "Discutir em que medida a produção, a circulação e o consumo de mercadorias provocam impactos ambientais."},
    
    # 8º ANO
    {"codigo_bncc": "EF08GE01", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Distribuição da população mundial", "habilidade_descricao": "Descrever as rotas de dispersão da população humana pelo planeta e os principais fluxos migratórios em diferentes períodos da história."},
    {"codigo_bncc": "EF08GE02", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Corporações e organismos internacionais", "habilidade_descricao": "Relacionar fatos e situações representativas da história das famílias do Município em que se localiza a escola."},
    {"codigo_bncc": "EF08GE03", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Globalização e mundialização", "habilidade_descricao": "Analisar aspectos representativos da dinâmica demográfica, considerando características da população."},
    {"codigo_bncc": "EF08GE04", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Os diferentes contextos da América Latina", "habilidade_descricao": "Compreender os fluxos de migração na América Latina e suas principais motivações."},
    {"codigo_bncc": "EF08GE05", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Transformação do espaço na América Latina", "habilidade_descricao": "Aplicar os conceitos de Estado, nação, território, governo e país para o entendimento de conflitos e tensões na contemporaneidade."},
    {"codigo_bncc": "EF08GE06", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Cartografia: anamorfose, croquis e mapas temáticos", "habilidade_descricao": "Analisar a atuação das organizações mundiais nos processos de integração cultural e econômica nos contextos americano e africano."},
    
    # 9º ANO
    {"codigo_bncc": "EF09GE01", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "A hegemonia europeia na economia, política e cultura", "habilidade_descricao": "Analisar criticamente de que forma a hegemonia europeia foi exercida em várias regiões do planeta."},
    {"codigo_bncc": "EF09GE02", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "dificil", "objeto_conhecimento": "Corporações e organismos internacionais", "habilidade_descricao": "Analisar a atuação das corporações internacionais e das organizações econômicas mundiais na vida da população."},
    {"codigo_bncc": "EF09GE03", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "As manifestações culturais na formação populacional", "habilidade_descricao": "Identificar diferentes manifestações culturais de minorias étnicas como forma de compreender a multiplicidade cultural na escala mundial."},
    {"codigo_bncc": "EF09GE04", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "dificil", "objeto_conhecimento": "Integração mundial e suas interpretações: globalização e mundialização", "habilidade_descricao": "Relacionar diferenças de paisagens aos modos de viver de diferentes povos na Europa, Ásia e Oceania."},
    {"codigo_bncc": "EF09GE05", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "dificil", "objeto_conhecimento": "Intercâmbios históricos e culturais entre Europa, Ásia e Oceania", "habilidade_descricao": "Analisar fatos e situações para compreender a integração mundial, com destaque para as situações de interdependência."},
    {"codigo_bncc": "EF09GE06", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "dificil", "objeto_conhecimento": "Leitura e elaboração de mapas temáticos", "habilidade_descricao": "Associar o critério de divisão do mundo em Ocidente e Oriente com o poder hegemônico europeu, identificando permanências e mudanças de significado."},
    
    # ============================================
    # SOCIOEMOCIONAL - FUNDAMENTAL II
    # ============================================
    {"codigo_bncc": "SOCIOEF601", "componente": "Socioemocional", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Transição escolar", "habilidade_descricao": "Adaptar-se às novas demandas do Ensino Fundamental II com autonomia e organização."},
    {"codigo_bncc": "SOCIOEF602", "componente": "Socioemocional", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Gestão do tempo", "habilidade_descricao": "Desenvolver estratégias de gestão do tempo para múltiplas disciplinas e tarefas."},
    {"codigo_bncc": "SOCIOEF701", "componente": "Socioemocional", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Pensamento crítico", "habilidade_descricao": "Desenvolver pensamento crítico e capacidade de análise de informações."},
    {"codigo_bncc": "SOCIOEF702", "componente": "Socioemocional", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Comunicação", "habilidade_descricao": "Aprimorar habilidades de comunicação oral e escrita em diferentes contextos."},
    {"codigo_bncc": "SOCIOEF801", "componente": "Socioemocional", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Autogestão", "habilidade_descricao": "Desenvolver autonomia na gestão de estudos e projetos pessoais."},
    {"codigo_bncc": "SOCIOEF802", "componente": "Socioemocional", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Liderança", "habilidade_descricao": "Desenvolver habilidades de liderança e trabalho colaborativo."},
    {"codigo_bncc": "SOCIOEF901", "componente": "Socioemocional", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Projeto de vida", "habilidade_descricao": "Refletir sobre escolhas futuras e construir projeto de vida."},
    {"codigo_bncc": "SOCIOEF902", "componente": "Socioemocional", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Preparação para o Ensino Médio", "habilidade_descricao": "Preparar-se para a transição ao Ensino Médio com maturidade e planejamento."},
]


def importar_bncc_ef2_expandido():
    print("=" * 70)
    print("IMPORTAÇÃO EXPANDIDA - BNCC ENSINO FUNDAMENTAL II")
    print(f"Total de habilidades: {len(HABILIDADES_EF2)}")
    print("=" * 70)
    
    with engine.connect() as conn:
        inseridos = 0
        atualizados = 0
        
        for hab in HABILIDADES_EF2:
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
        
        print("\n" + "-" * 70)
        print("RESUMO DA IMPORTAÇÃO:")
        print("-" * 70)
        print(f"   Inseridos: {inseridos}")
        print(f"   Atualizados: {atualizados}")
        print(f"   TOTAL: {inseridos + atualizados}")
        
        # Contagem por ano
        print("\n" + "-" * 70)
        print("POR ANO ESCOLAR (Fundamental II):")
        print("-" * 70)
        
        for ano in ["6 ano", "7 ano", "8 ano", "9 ano"]:
            result = conn.execute(text("""
                SELECT componente, COUNT(*) as total
                FROM curriculo_nacional
                WHERE ano_escolar = :ano
                GROUP BY componente
                ORDER BY componente
            """), {"ano": ano})
            
            habs = result.fetchall()
            total_ano = sum(h[1] for h in habs)
            print(f"\n   {ano}: {total_ano} habilidades")
            for h in habs:
                print(f"      - {h[0]}: {h[1]}")
    
    print("\n" + "=" * 70)
    print("IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    importar_bncc_ef2_expandido()
