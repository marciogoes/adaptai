# ============================================
# IMPORTAR BNCC ENSINO FUNDAMENTAL I - EXPANDIDO
# 1º ao 5º ano - Mais de 200 habilidades
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

# ============================================
# HABILIDADES EXPANDIDAS - ENSINO FUNDAMENTAL I
# ============================================

HABILIDADES_EF1 = [
    # ============================================
    # MATEMÁTICA - 1º ANO
    # ============================================
    {"codigo_bncc": "EF01MA01", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Contagem", "habilidade_descricao": "Utilizar números naturais como indicador de quantidade em diferentes situações cotidianas."},
    {"codigo_bncc": "EF01MA02", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Contagem", "habilidade_descricao": "Contar de maneira exata ou aproximada, utilizando diferentes estratégias como pareamento e outros agrupamentos."},
    {"codigo_bncc": "EF01MA03", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Leitura e escrita de números", "habilidade_descricao": "Estimar e comparar quantidades de objetos de dois conjuntos, por estimativa e/ou por correspondência."},
    {"codigo_bncc": "EF01MA04", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Sequência numérica", "habilidade_descricao": "Contar a quantidade de objetos de coleções até 100 unidades e apresentar o resultado por registros verbais e simbólicos."},
    {"codigo_bncc": "EF01MA05", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Comparação de números", "habilidade_descricao": "Comparar números naturais de até duas ordens em situações cotidianas, com e sem suporte da reta numérica."},
    {"codigo_bncc": "EF01MA06", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Adição e subtração", "habilidade_descricao": "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo para resolver problemas."},
    {"codigo_bncc": "EF01MA07", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Adição e subtração", "habilidade_descricao": "Compor e decompor números de até duas ordens, por meio de diferentes adições."},
    {"codigo_bncc": "EF01MA08", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Problemas", "habilidade_descricao": "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até dois algarismos."},
    {"codigo_bncc": "EF01MA09", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Figuras geométricas", "habilidade_descricao": "Relacionar figuras geométricas espaciais (cones, cilindros, esferas e blocos retangulares) a objetos do mundo físico."},
    {"codigo_bncc": "EF01MA10", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Medidas de tempo", "habilidade_descricao": "Reconhecer e relacionar períodos do dia, dias da semana e meses do ano, utilizando calendário."},
    {"codigo_bncc": "EF01MA11", "componente": "Matemática", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Medidas de comprimento", "habilidade_descricao": "Comparar comprimentos, capacidades ou massas, utilizando termos como mais alto, mais baixo, mais comprido."},
    
    # MATEMÁTICA - 2º ANO
    {"codigo_bncc": "EF02MA01", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Leitura e escrita de números", "habilidade_descricao": "Comparar e ordenar números naturais (até a ordem de centenas) pela compreensão de características do sistema de numeração decimal."},
    {"codigo_bncc": "EF02MA02", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Valor posicional", "habilidade_descricao": "Fazer estimativas por meio de estratégias diversas a respeito da quantidade de objetos de coleções."},
    {"codigo_bncc": "EF02MA03", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Composição e decomposição", "habilidade_descricao": "Comparar quantidades de objetos de dois conjuntos, por estimativa e/ou por correspondência, para indicar 'tem mais', 'tem menos' ou 'tem a mesma quantidade'."},
    {"codigo_bncc": "EF02MA04", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Adição e subtração", "habilidade_descricao": "Compor e decompor números naturais de até três ordens, com suporte de material manipulável."},
    {"codigo_bncc": "EF02MA05", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Fatos fundamentais", "habilidade_descricao": "Construir fatos básicos da adição e subtração e utilizá-los no cálculo mental ou escrito."},
    {"codigo_bncc": "EF02MA06", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Problemas de adição e subtração", "habilidade_descricao": "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até três ordens."},
    {"codigo_bncc": "EF02MA07", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Multiplicação", "habilidade_descricao": "Resolver e elaborar problemas de multiplicação (por 2, 3, 4 e 5) com a ideia de adição de parcelas iguais."},
    {"codigo_bncc": "EF02MA08", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Figuras geométricas planas", "habilidade_descricao": "Reconhecer e nomear figuras geométricas planas (círculo, quadrado, retângulo e triângulo)."},
    {"codigo_bncc": "EF02MA09", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Localização espacial", "habilidade_descricao": "Construir sequências de números naturais em ordem crescente ou decrescente a partir de um número qualquer."},
    {"codigo_bncc": "EF02MA10", "componente": "Matemática", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Medidas de tempo", "habilidade_descricao": "Indicar a duração de intervalos de tempo entre duas datas, como dias da semana e meses do ano."},
    
    # MATEMÁTICA - 3º ANO
    {"codigo_bncc": "EF03MA01", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Leitura e escrita de números", "habilidade_descricao": "Ler, escrever e comparar números naturais de até a ordem de unidade de milhar."},
    {"codigo_bncc": "EF03MA02", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Composição e decomposição", "habilidade_descricao": "Identificar características do sistema de numeração decimal, utilizando a composição e a decomposição de número natural de até quatro ordens."},
    {"codigo_bncc": "EF03MA03", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Sistema de numeração", "habilidade_descricao": "Construir e utilizar fatos básicos da adição e da multiplicação para o cálculo mental ou escrito."},
    {"codigo_bncc": "EF03MA04", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Adição e subtração", "habilidade_descricao": "Estabelecer a relação entre números naturais e pontos da reta numérica para utilizá-la na ordenação dos números naturais."},
    {"codigo_bncc": "EF03MA05", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Multiplicação e divisão", "habilidade_descricao": "Utilizar diferentes procedimentos de cálculo mental e escrito para resolver problemas de multiplicação e divisão."},
    {"codigo_bncc": "EF03MA06", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Tabuada", "habilidade_descricao": "Resolver e elaborar problemas de multiplicação (por 2, 3, 4, 5 e 10) com os significados de adição de parcelas iguais."},
    {"codigo_bncc": "EF03MA07", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Problemas", "habilidade_descricao": "Resolver e elaborar problemas de divisão de um número natural por outro, com resto zero e com resto diferente de zero."},
    {"codigo_bncc": "EF03MA08", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Figuras geométricas", "habilidade_descricao": "Descrever características de algumas figuras geométricas espaciais (prismas retos, pirâmides, cilindros, cones)."},
    {"codigo_bncc": "EF03MA09", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Perímetro", "habilidade_descricao": "Associar figuras geométricas espaciais (cubo, bloco retangular, pirâmide, cone, cilindro e esfera) a objetos do mundo físico."},
    {"codigo_bncc": "EF03MA10", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Medidas", "habilidade_descricao": "Identificar e relatar características de figuras geométricas planas (quadrado, retângulo, triângulo)."},
    {"codigo_bncc": "EF03MA11", "componente": "Matemática", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Sistema monetário", "habilidade_descricao": "Resolver e elaborar problemas que envolvam a comparação e a equivalência de valores monetários do sistema brasileiro."},
    
    # MATEMÁTICA - 4º ANO
    {"codigo_bncc": "EF04MA01", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Sistema de numeração decimal", "habilidade_descricao": "Ler, escrever e ordenar números naturais até a ordem de dezenas de milhar."},
    {"codigo_bncc": "EF04MA02", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Composição e decomposição", "habilidade_descricao": "Mostrar, por decomposição e composição, que todo número natural pode ser escrito por meio de adições e multiplicações por potências de dez."},
    {"codigo_bncc": "EF04MA03", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Operações fundamentais", "habilidade_descricao": "Resolver e elaborar problemas com números naturais envolvendo adição e subtração, utilizando estratégias diversas."},
    {"codigo_bncc": "EF04MA04", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Multiplicação e divisão", "habilidade_descricao": "Utilizar as relações entre adição e subtração, bem como entre multiplicação e divisão, para ampliar as estratégias de cálculo."},
    {"codigo_bncc": "EF04MA05", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Algoritmos", "habilidade_descricao": "Utilizar as propriedades das operações para desenvolver estratégias de cálculo."},
    {"codigo_bncc": "EF04MA06", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Problemas", "habilidade_descricao": "Resolver e elaborar problemas envolvendo diferentes significados da multiplicação e da divisão."},
    {"codigo_bncc": "EF04MA07", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Frações", "habilidade_descricao": "Reconhecer as frações unitárias mais usuais (1/2, 1/3, 1/4, 1/5, 1/10 e 1/100) como unidades de medida menores do que uma unidade."},
    {"codigo_bncc": "EF04MA08", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Números decimais", "habilidade_descricao": "Reconhecer que as regras do sistema de numeração decimal podem ser estendidas para a representação decimal de um número racional."},
    {"codigo_bncc": "EF04MA09", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Figuras geométricas", "habilidade_descricao": "Reconhecer simetria de reflexão em figuras e em pares de figuras geométricas planas e utilizá-la na construção de figuras congruentes."},
    {"codigo_bncc": "EF04MA10", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Ângulos", "habilidade_descricao": "Reconhecer ângulos retos e não retos em figuras poligonais com o uso de dobraduras, esquadros ou softwares."},
    {"codigo_bncc": "EF04MA11", "componente": "Matemática", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Área e perímetro", "habilidade_descricao": "Medir e estimar comprimentos, incluindo perímetros, áreas de figuras planas e capacidades, utilizando unidades de medida padronizadas."},
    
    # MATEMÁTICA - 5º ANO
    {"codigo_bncc": "EF05MA01", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Sistema de numeração decimal", "habilidade_descricao": "Ler, escrever e ordenar números naturais até a ordem das centenas de milhar com compreensão das principais características do sistema de numeração decimal."},
    {"codigo_bncc": "EF05MA02", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Números racionais", "habilidade_descricao": "Ler, escrever e ordenar números racionais na forma decimal com compreensão das principais características do sistema de numeração decimal."},
    {"codigo_bncc": "EF05MA03", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Operações com naturais", "habilidade_descricao": "Identificar e representar frações (menores e maiores que a unidade), associando-as ao resultado de uma divisão ou à ideia de parte de um todo."},
    {"codigo_bncc": "EF05MA04", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Frações", "habilidade_descricao": "Identificar frações equivalentes."},
    {"codigo_bncc": "EF05MA05", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Comparação de frações", "habilidade_descricao": "Comparar e ordenar números racionais positivos (representações fracionária e decimal), relacionando-os a pontos na reta numérica."},
    {"codigo_bncc": "EF05MA06", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Adição e subtração de frações", "habilidade_descricao": "Associar as representações 10%, 25%, 50%, 75% e 100% respectivamente à décima parte, quarta parte, metade, três quartos e um inteiro."},
    {"codigo_bncc": "EF05MA07", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Problemas com frações", "habilidade_descricao": "Resolver e elaborar problemas de adição e subtração com números naturais e com números racionais, cuja representação decimal seja finita."},
    {"codigo_bncc": "EF05MA08", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Multiplicação e divisão", "habilidade_descricao": "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal é finita."},
    {"codigo_bncc": "EF05MA09", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Expressões numéricas", "habilidade_descricao": "Resolver e elaborar problemas simples de contagem envolvendo o princípio multiplicativo, como a determinação do número de agrupamentos possíveis."},
    {"codigo_bncc": "EF05MA10", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Geometria", "habilidade_descricao": "Concluir, por meio de investigações, que a soma das medidas dos ângulos internos de um triângulo é 180°."},
    {"codigo_bncc": "EF05MA11", "componente": "Matemática", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Estatística", "habilidade_descricao": "Interpretar dados estatísticos apresentados em textos, tabelas e gráficos (colunas ou linhas), referentes a outras áreas do conhecimento."},
    
    # ============================================
    # LÍNGUA PORTUGUESA - 1º ANO
    # ============================================
    {"codigo_bncc": "EF01LP01", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Protocolos de leitura", "habilidade_descricao": "Reconhecer que textos são lidos e escritos da esquerda para a direita e de cima para baixo da página."},
    {"codigo_bncc": "EF01LP02", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Correspondência fonema-grafema", "habilidade_descricao": "Escrever, espontaneamente ou por ditado, palavras e frases de forma alfabética."},
    {"codigo_bncc": "EF01LP03", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Construção do sistema alfabético", "habilidade_descricao": "Comparar escritas convencionais, identificando semelhanças e diferenças entre elas."},
    {"codigo_bncc": "EF01LP04", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Conhecimento do alfabeto", "habilidade_descricao": "Distinguir as letras do alfabeto de outros sinais gráficos."},
    {"codigo_bncc": "EF01LP05", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Segmentação de palavras", "habilidade_descricao": "Reconhecer o sistema de escrita alfabética como representação dos sons da fala."},
    {"codigo_bncc": "EF01LP06", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Leitura", "habilidade_descricao": "Segmentar oralmente palavras em sílabas."},
    {"codigo_bncc": "EF01LP07", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Escrita", "habilidade_descricao": "Identificar fonemas e sua representação por letras."},
    {"codigo_bncc": "EF01LP08", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Formação do leitor", "habilidade_descricao": "Relacionar elementos sonoros (sílabas, fonemas, partes de palavras) com sua representação escrita."},
    {"codigo_bncc": "EF01LP09", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Compreensão em leitura", "habilidade_descricao": "Comparar palavras, identificando semelhanças e diferenças entre sons de sílabas iniciais, mediais e finais."},
    {"codigo_bncc": "EF01LP10", "componente": "Língua Portuguesa", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Produção de texto", "habilidade_descricao": "Nomear as letras do alfabeto e recitá-lo na ordem das letras."},
    
    # LÍNGUA PORTUGUESA - 2º ANO
    {"codigo_bncc": "EF02LP01", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Leitura e compreensão", "habilidade_descricao": "Utilizar, ao produzir o texto, grafia correta de palavras conhecidas ou com estruturas silábicas já dominadas."},
    {"codigo_bncc": "EF02LP02", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Escrita de palavras", "habilidade_descricao": "Segmentar palavras em sílabas e remover e substituir sílabas iniciais, mediais ou finais para criar novas palavras."},
    {"codigo_bncc": "EF02LP03", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Construção do sistema alfabético", "habilidade_descricao": "Ler e escrever palavras com correspondências regulares diretas entre letras e fonemas."},
    {"codigo_bncc": "EF02LP04", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Pontuação", "habilidade_descricao": "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, identificando que existem vogais em todas as sílabas."},
    {"codigo_bncc": "EF02LP05", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Acentuação", "habilidade_descricao": "Ler e escrever corretamente palavras com marcas de nasalidade (til, m, n)."},
    {"codigo_bncc": "EF02LP06", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Compreensão em leitura", "habilidade_descricao": "Perceber o princípio acrofônico que opera nos nomes das letras do alfabeto."},
    {"codigo_bncc": "EF02LP07", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Fluência de leitura", "habilidade_descricao": "Escrever palavras, frases, textos curtos nas formas imprensa e cursiva."},
    {"codigo_bncc": "EF02LP08", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Produção de texto", "habilidade_descricao": "Segmentar corretamente as palavras ao escrever frases e textos."},
    {"codigo_bncc": "EF02LP09", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Revisão de texto", "habilidade_descricao": "Usar adequadamente ponto final, ponto de interrogação e ponto de exclamação."},
    {"codigo_bncc": "EF02LP10", "componente": "Língua Portuguesa", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Gêneros textuais", "habilidade_descricao": "Identificar gêneros do discurso oral, utilizados em diferentes situações e contextos comunicativos."},
    
    # LÍNGUA PORTUGUESA - 3º ANO
    {"codigo_bncc": "EF03LP01", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Leitura e compreensão", "habilidade_descricao": "Ler e escrever palavras com correspondências regulares contextuais entre grafemas e fonemas."},
    {"codigo_bncc": "EF03LP02", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Construção do sistema alfabético", "habilidade_descricao": "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, VC, VV, CVV, identificando que existem vogais em todas as sílabas."},
    {"codigo_bncc": "EF03LP03", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ortografia", "habilidade_descricao": "Ler e escrever corretamente palavras com os dígrafos lh, nh, ch."},
    {"codigo_bncc": "EF03LP04", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Acentuação", "habilidade_descricao": "Usar acento gráfico (agudo ou circunflexo) em monossílabos tônicos terminados em a, e, o."},
    {"codigo_bncc": "EF03LP05", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Segmentação de palavras", "habilidade_descricao": "Identificar o número de sílabas de palavras, classificando-as em monossílabas, dissílabas, trissílabas e polissílabas."},
    {"codigo_bncc": "EF03LP06", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Pontuação", "habilidade_descricao": "Identificar a sílaba tônica em palavras, classificando-as em oxítonas, paroxítonas e proparoxítonas."},
    {"codigo_bncc": "EF03LP07", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Morfologia", "habilidade_descricao": "Identificar a função na leitura e usar na escrita ponto final, ponto de interrogação, ponto de exclamação e, em diálogos, dois-pontos e travessão."},
    {"codigo_bncc": "EF03LP08", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Substantivos e adjetivos", "habilidade_descricao": "Identificar e diferenciar substantivos, verbos e adjetivos, compreendendo sua função no texto."},
    {"codigo_bncc": "EF03LP09", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Produção de texto", "habilidade_descricao": "Planejar e produzir textos em sequências que tratem de uma mesma informação."},
    {"codigo_bncc": "EF03LP10", "componente": "Língua Portuguesa", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Revisão de texto", "habilidade_descricao": "Utilizar, ao produzir um texto, conhecimentos linguísticos e gramaticais, tais como ortografia, regras básicas de concordância nominal e verbal."},
    
    # LÍNGUA PORTUGUESA - 4º ANO
    {"codigo_bncc": "EF04LP01", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Leitura e fluência", "habilidade_descricao": "Grafar palavras utilizando regras de correspondência fonema-grafema regulares diretas e contextuais."},
    {"codigo_bncc": "EF04LP02", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ortografia", "habilidade_descricao": "Ler e escrever, corretamente, palavras com sílabas VV e CVV em casos nos quais a combinação VV (hiato) e CVV (ditongo) se reduzem a uma sílaba."},
    {"codigo_bncc": "EF04LP03", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Acentuação", "habilidade_descricao": "Localizar palavras no dicionário para esclarecer significados, reconhecendo o significado mais plausível para o contexto que deu origem à consulta."},
    {"codigo_bncc": "EF04LP04", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Pontuação", "habilidade_descricao": "Usar acento gráfico (agudo ou circunflexo) em paroxítonas terminadas em -i(s), -l, -r, -ão(s)."},
    {"codigo_bncc": "EF04LP05", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Morfossintaxe", "habilidade_descricao": "Identificar a função na leitura e usar, adequadamente, na escrita ponto final, de interrogação, de exclamação, dois-pontos e travessão em diálogos, vírgula em enumerações."},
    {"codigo_bncc": "EF04LP06", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Concordância nominal e verbal", "habilidade_descricao": "Identificar em textos e usar na produção textual a concordância entre substantivo ou pronome pessoal e verbo."},
    {"codigo_bncc": "EF04LP07", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Compreensão", "habilidade_descricao": "Identificar em textos e usar na produção textual a concordância entre artigo, substantivo e adjetivo."},
    {"codigo_bncc": "EF04LP08", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Produção de texto", "habilidade_descricao": "Reconhecer e grafar, corretamente, palavras derivadas com os sufixos -agem, -oso, -eza, -izar/-isar."},
    {"codigo_bncc": "EF04LP09", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Revisão de texto", "habilidade_descricao": "Ler e compreender, com autonomia, boletos, faturas e carnês, dentre outros gêneros do campo da vida cotidiana."},
    {"codigo_bncc": "EF04LP10", "componente": "Língua Portuguesa", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais", "habilidade_descricao": "Ler e compreender, com autonomia, cartas pessoais de reclamação, dentre outros gêneros do campo da vida cotidiana."},
    
    # LÍNGUA PORTUGUESA - 5º ANO
    {"codigo_bncc": "EF05LP01", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ortografia", "habilidade_descricao": "Grafar palavras utilizando regras de correspondência fonema-grafema regulares, contextuais e morfológicas e palavras de uso frequente com correspondências irregulares."},
    {"codigo_bncc": "EF05LP02", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Acentuação", "habilidade_descricao": "Identificar o caráter polissêmico das palavras, conforme o contexto de uso."},
    {"codigo_bncc": "EF05LP03", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Pontuação", "habilidade_descricao": "Acentuar corretamente palavras oxítonas, paroxítonas e proparoxítonas."},
    {"codigo_bncc": "EF05LP04", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Morfossintaxe", "habilidade_descricao": "Diferenciar, na leitura de textos, vírgula, ponto e vírgula, dois-pontos, reticências, aspas e parênteses."},
    {"codigo_bncc": "EF05LP05", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Concordância", "habilidade_descricao": "Identificar a expressão de presente, passado e futuro em tempos verbais do modo indicativo."},
    {"codigo_bncc": "EF05LP06", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Compreensão em leitura", "habilidade_descricao": "Flexionar, adequadamente, na escrita e na oralidade, os verbos em concordância com pronomes pessoais/nomes sujeitos da oração."},
    {"codigo_bncc": "EF05LP07", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Produção de texto", "habilidade_descricao": "Identificar, em textos, o uso de conjunções e a relação que estabelecem entre partes do texto."},
    {"codigo_bncc": "EF05LP08", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Parágrafo e período", "habilidade_descricao": "Diferenciar palavras primitivas, derivadas e compostas, e derivadas por adição de prefixo e de sufixo."},
    {"codigo_bncc": "EF05LP09", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Gêneros textuais", "habilidade_descricao": "Ler e compreender, com autonomia, textos instrucional de regras de jogo, dentre outros gêneros do campo da vida cotidiana."},
    {"codigo_bncc": "EF05LP10", "componente": "Língua Portuguesa", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Coesão e coerência", "habilidade_descricao": "Ler e compreender, com autonomia, anedotas, piadas e cartuns, dentre outros gêneros do campo da vida cotidiana."},
    
    # ============================================
    # CIÊNCIAS - 1º ao 5º ANO
    # ============================================
    # 1º ANO
    {"codigo_bncc": "EF01CI01", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Corpo humano", "habilidade_descricao": "Comparar características físicas entre os colegas, reconhecendo a diversidade e a importância da valorização, do acolhimento e do respeito às diferenças."},
    {"codigo_bncc": "EF01CI02", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Corpo humano", "habilidade_descricao": "Localizar, nomear e representar graficamente (por meio de desenhos) partes do corpo humano e explicar suas funções."},
    {"codigo_bncc": "EF01CI03", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Respeito à diversidade", "habilidade_descricao": "Discutir as razões pelas quais os hábitos de higiene do corpo (lavar as mãos antes de comer, escovar os dentes, limpar os olhos, o nariz e as orelhas etc.) são necessários para a manutenção da saúde."},
    {"codigo_bncc": "EF01CI04", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Materiais", "habilidade_descricao": "Comparar características de diferentes materiais presentes em objetos de uso cotidiano, discutindo sua origem, os modos como são descartados e como podem ser usados de forma mais consciente."},
    {"codigo_bncc": "EF01CI05", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Escalas de tempo", "habilidade_descricao": "Identificar e nomear diferentes escalas de tempo: os períodos diários (manhã, tarde, noite) e a sucessão de dias, semanas, meses e anos."},
    {"codigo_bncc": "EF01CI06", "componente": "Ciências", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Movimento do Sol", "habilidade_descricao": "Selecionar exemplos de como a sucessão de dias e noites orienta o ritmo de atividades diárias de seres humanos e de outros seres vivos."},
    
    # 2º ANO
    {"codigo_bncc": "EF02CI01", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Seres vivos", "habilidade_descricao": "Identificar de que materiais (metais, madeira, vidro etc.) são feitos os objetos que fazem parte da vida cotidiana, como esses objetos são utilizados e com quais materiais eram produzidos no passado."},
    {"codigo_bncc": "EF02CI02", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Propriedades dos materiais", "habilidade_descricao": "Propor o uso de diferentes materiais para a construção de objetos de uso cotidiano, tendo em vista algumas propriedades desses materiais."},
    {"codigo_bncc": "EF02CI03", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Prevenção de acidentes", "habilidade_descricao": "Discutir os cuidados necessários à prevenção de acidentes domésticos (objetos cortantes e inflamáveis, eletricidade, produtos de limpeza, medicamentos etc.)."},
    {"codigo_bncc": "EF02CI04", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Plantas", "habilidade_descricao": "Descrever características de plantas e animais (tamanho, forma, cor, fase da vida, local onde se desenvolvem etc.) que fazem parte de seu cotidiano e relacioná-las ao ambiente em que eles vivem."},
    {"codigo_bncc": "EF02CI05", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Animais", "habilidade_descricao": "Investigar a importância da água e da luz para a manutenção da vida de plantas em geral."},
    {"codigo_bncc": "EF02CI06", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Água e luz", "habilidade_descricao": "Identificar as principais partes de uma planta (raiz, caule, folhas, flores e frutos) e a função desempenhada por cada uma delas."},
    {"codigo_bncc": "EF02CI07", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Movimento aparente do Sol", "habilidade_descricao": "Descrever as posições do Sol em diversos horários do dia e associá-las ao tamanho da sombra projetada."},
    {"codigo_bncc": "EF02CI08", "componente": "Ciências", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Sol como fonte de luz e calor", "habilidade_descricao": "Comparar o efeito da radiação solar (aquecimento e reflexão) em diferentes tipos de superfície."},
    
    # 3º ANO
    {"codigo_bncc": "EF03CI01", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Produção de som", "habilidade_descricao": "Produzir diferentes sons a partir da vibração de variados objetos e identificar variáveis que influem nesse fenômeno."},
    {"codigo_bncc": "EF03CI02", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Efeitos da luz", "habilidade_descricao": "Experimentar e relatar o que ocorre com a passagem da luz através de objetos transparentes, opacos e translúcidos."},
    {"codigo_bncc": "EF03CI03", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Saúde auditiva e visual", "habilidade_descricao": "Discutir hábitos necessários para a manutenção da saúde auditiva e visual considerando as condições do ambiente."},
    {"codigo_bncc": "EF03CI04", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Características dos animais", "habilidade_descricao": "Identificar características sobre o modo de vida dos animais (o que comem, como se reproduzem, como se deslocam etc.)."},
    {"codigo_bncc": "EF03CI05", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Características dos animais", "habilidade_descricao": "Descrever e comunicar as alterações que ocorrem desde o nascimento em animais de diferentes meios terrestres ou aquáticos."},
    {"codigo_bncc": "EF03CI06", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Ciclo de vida", "habilidade_descricao": "Comparar alguns animais e organizar grupos com base em características externas comuns."},
    {"codigo_bncc": "EF03CI07", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Características da Terra", "habilidade_descricao": "Identificar características da Terra (formato, estrutura, temperatura), com base na observação, manipulação e comparação de diferentes formas de representação do planeta."},
    {"codigo_bncc": "EF03CI08", "componente": "Ciências", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Usos do solo", "habilidade_descricao": "Observar, identificar e registrar os períodos diários (manhã, tarde, noite) em que o Sol, demais estrelas, Lua e planetas estão visíveis no céu."},
    
    # 4º ANO
    {"codigo_bncc": "EF04CI01", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Misturas", "habilidade_descricao": "Identificar misturas na vida diária, com base em suas propriedades físicas observáveis, reconhecendo sua composição."},
    {"codigo_bncc": "EF04CI02", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Transformações reversíveis e não reversíveis", "habilidade_descricao": "Testar e relatar transformações nos materiais do dia a dia quando expostos a diferentes condições (aquecimento, resfriamento, luz e umidade)."},
    {"codigo_bncc": "EF04CI03", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Cadeias alimentares", "habilidade_descricao": "Concluir que algumas mudanças causadas por aquecimento ou resfriamento são reversíveis e outras não."},
    {"codigo_bncc": "EF04CI04", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Cadeias alimentares", "habilidade_descricao": "Analisar e construir cadeias alimentares simples, reconhecendo a posição ocupada pelos seres vivos nessas cadeias."},
    {"codigo_bncc": "EF04CI05", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Microrganismos", "habilidade_descricao": "Descrever e destacar semelhanças e diferenças entre o ciclo da matéria e o fluxo de energia entre os componentes vivos e não vivos de um ecossistema."},
    {"codigo_bncc": "EF04CI06", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Microrganismos", "habilidade_descricao": "Relacionar a participação de fungos e bactérias no processo de decomposição, reconhecendo a importância ambiental desse processo."},
    {"codigo_bncc": "EF04CI07", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Pontos cardeais", "habilidade_descricao": "Verificar a participação de microrganismos na produção de alimentos, combustíveis, medicamentos, entre outros."},
    {"codigo_bncc": "EF04CI08", "componente": "Ciências", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Calendários e cultura", "habilidade_descricao": "Propor, a partir do conhecimento das formas de transmissão de alguns microrganismos, atitudes e medidas adequadas para prevenção de doenças a eles associadas."},
    
    # 5º ANO
    {"codigo_bncc": "EF05CI01", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Propriedades físicas dos materiais", "habilidade_descricao": "Explorar fenômenos da vida cotidiana que evidenciem propriedades físicas dos materiais – como densidade, condutibilidade térmica e elétrica, respostas a forças magnéticas, solubilidade, respostas a forças mecânicas."},
    {"codigo_bncc": "EF05CI02", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Ciclo hidrológico", "habilidade_descricao": "Aplicar os conhecimentos sobre as mudanças de estado físico da água para explicar o ciclo hidrológico e analisar suas implicações na agricultura, no clima, na geração de energia elétrica, no provimento de água potável e no equilíbrio dos ecossistemas regionais."},
    {"codigo_bncc": "EF05CI03", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Consumo consciente", "habilidade_descricao": "Selecionar argumentos que justifiquem a importância da cobertura vegetal para a manutenção do ciclo da água, a conservação dos solos, dos cursos de água e da qualidade do ar atmosférico."},
    {"codigo_bncc": "EF05CI04", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Reciclagem", "habilidade_descricao": "Identificar os principais usos da água e de outros materiais nas atividades cotidianas para discutir e propor formas sustentáveis de utilização desses recursos."},
    {"codigo_bncc": "EF05CI05", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Nutrição do organismo", "habilidade_descricao": "Construir propostas coletivas para um consumo mais consciente e criar soluções tecnológicas para o descarte adequado e a reutilização ou reciclagem de materiais consumidos na escola e/ou na vida cotidiana."},
    {"codigo_bncc": "EF05CI06", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Nutrição do organismo", "habilidade_descricao": "Selecionar argumentos que justifiquem por que os sistemas digestório e respiratório são considerados corresponsáveis pelo processo de nutrição do organismo."},
    {"codigo_bncc": "EF05CI07", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Integração dos sistemas", "habilidade_descricao": "Justificar a relação entre o funcionamento do sistema circulatório, a distribuição dos nutrientes pelo organismo e a eliminação dos resíduos produzidos."},
    {"codigo_bncc": "EF05CI08", "componente": "Ciências", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Sistema Solar", "habilidade_descricao": "Organizar um cardápio equilibrado com base nas características dos grupos alimentares (nutrientes e calorias) e nas necessidades individuais para a manutenção da saúde do organismo."},
    
    # ============================================
    # HISTÓRIA - 1º ao 5º ANO
    # ============================================
    # 1º ANO
    {"codigo_bncc": "EF01HI01", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "As fases da vida", "habilidade_descricao": "Identificar aspectos do seu crescimento por meio do registro das lembranças particulares ou de lembranças dos membros de sua família e/ou de sua comunidade."},
    {"codigo_bncc": "EF01HI02", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "As diferentes formas de organização da família", "habilidade_descricao": "Identificar a relação entre as suas histórias e as histórias de sua família e de sua comunidade."},
    {"codigo_bncc": "EF01HI03", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "A escola e a diversidade do grupo social envolvido", "habilidade_descricao": "Descrever e distinguir os seus papéis e responsabilidades relacionados à família, à escola e à comunidade."},
    {"codigo_bncc": "EF01HI04", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "A vida em casa, a vida na escola", "habilidade_descricao": "Identificar as diferenças entre os variados ambientes em que vive (doméstico, escolar e da comunidade), reconhecendo as especificidades dos hábitos e das regras que os regem."},
    {"codigo_bncc": "EF01HI05", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "A vida em família: diferentes configurações", "habilidade_descricao": "Identificar semelhanças e diferenças entre jogos e brincadeiras atuais e de outras épocas e lugares."},
    {"codigo_bncc": "EF01HI06", "componente": "História", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "A escola, sua representação espacial", "habilidade_descricao": "Conhecer as histórias da família e da escola e identificar o papel desempenhado por diferentes sujeitos em diferentes espaços."},
    
    # 2º ANO
    {"codigo_bncc": "EF02HI01", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "A noção do Eu e do Outro", "habilidade_descricao": "Reconhecer espaços de sociabilidade e identificar os motivos que aproximam e separam as pessoas em diferentes grupos sociais ou de parentesco."},
    {"codigo_bncc": "EF02HI02", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "A comunidade e seus registros", "habilidade_descricao": "Identificar e descrever práticas e papéis sociais que as pessoas exercem em diferentes comunidades."},
    {"codigo_bncc": "EF02HI03", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "As formas de registrar as experiências da comunidade", "habilidade_descricao": "Selecionar situações cotidianas que remetam à percepção de mudança, pertencimento e memória."},
    {"codigo_bncc": "EF02HI04", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "O tempo como medida", "habilidade_descricao": "Selecionar e compreender o significado de objetos e documentos pessoais como fontes de memórias e histórias nos âmbitos pessoal, familiar, escolar e comunitário."},
    {"codigo_bncc": "EF02HI05", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "As fontes: relatos orais, objetos, imagens", "habilidade_descricao": "Selecionar objetos e documentos pessoais e de grupos próximos ao seu convívio e compreender sua função, seu uso e seu significado."},
    {"codigo_bncc": "EF02HI06", "componente": "História", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "A sobrevivência e a relação com a natureza", "habilidade_descricao": "Identificar e organizar, temporalmente, fatos da vida cotidiana, usando noções relacionadas ao tempo (antes, durante, ao mesmo tempo e depois)."},
    
    # 3º ANO
    {"codigo_bncc": "EF03HI01", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "As pessoas e os grupos que compõem a cidade e o município", "habilidade_descricao": "Identificar os grupos populacionais que formam a cidade, o município e a região, as relações estabelecidas entre eles e os eventos que marcam a formação da cidade."},
    {"codigo_bncc": "EF03HI02", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "O Eu, o Outro e os diferentes grupos sociais e étnicos", "habilidade_descricao": "Selecionar, por meio da consulta de fontes de diferentes naturezas, e registrar acontecimentos ocorridos ao longo do tempo na cidade ou região em que vive."},
    {"codigo_bncc": "EF03HI03", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Os patrimônios históricos e culturais da cidade e/ou do município", "habilidade_descricao": "Identificar e comparar pontos de vista em relação a eventos significativos do local em que vive, aspectos relacionados a condições sociais e à presença de diferentes grupos sociais e culturais."},
    {"codigo_bncc": "EF03HI04", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "A produção dos marcos da memória", "habilidade_descricao": "Identificar os patrimônios históricos e culturais de sua cidade ou região e discutir as razões culturais, sociais e políticas para que assim sejam considerados."},
    {"codigo_bncc": "EF03HI05", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "A cidade e o campo: aproximações e diferenças", "habilidade_descricao": "Identificar os marcos históricos do lugar em que vive e compreender seus significados."},
    {"codigo_bncc": "EF03HI06", "componente": "História", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "A cidade, seus espaços públicos e privados e suas áreas de conservação ambiental", "habilidade_descricao": "Identificar os registros de memória na cidade (nomes de ruas, monumentos, edifícios etc.), discutindo os critérios que explicam a escolha desses nomes."},
    
    # 4º ANO
    {"codigo_bncc": "EF04HI01", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "A ação das pessoas, grupos sociais e comunidades no tempo e no espaço", "habilidade_descricao": "Reconhecer a história como resultado da ação do ser humano no tempo e no espaço, com base na identificação de mudanças e permanências ao longo do tempo."},
    {"codigo_bncc": "EF04HI02", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "O passado e o presente: a noção de permanência e as lentas transformações sociais e culturais", "habilidade_descricao": "Identificar mudanças e permanências ao longo do tempo, discutindo os sentidos dos grandes marcos da história da humanidade."},
    {"codigo_bncc": "EF04HI03", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "A circulação de pessoas e as transformações no meio natural", "habilidade_descricao": "Identificar as transformações ocorridas na cidade ao longo do tempo e discutir suas interferências nos modos de vida de seus habitantes."},
    {"codigo_bncc": "EF04HI04", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "A invenção do comércio e a circulação de produtos", "habilidade_descricao": "Identificar as relações entre os indivíduos e a natureza e discutir o significado do nomadismo e da fixação das primeiras comunidades humanas."},
    {"codigo_bncc": "EF04HI05", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "As rotas terrestres, fluviais e marítimas e seus impactos para a formação de cidades e as transformações do meio natural", "habilidade_descricao": "Relacionar os processos de ocupação do campo a intervenções na natureza, avaliando os resultados dessas intervenções."},
    {"codigo_bncc": "EF04HI06", "componente": "História", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "O mundo da tecnologia", "habilidade_descricao": "Identificar as transformações ocorridas nos processos de deslocamento das pessoas e mercadorias, analisando as formas de adaptação ou marginalização."},
    
    # 5º ANO
    {"codigo_bncc": "EF05HI01", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Povos e culturas: meu lugar no mundo e meu grupo social", "habilidade_descricao": "Identificar os processos de formação das culturas e dos povos, relacionando-os com o espaço geográfico ocupado."},
    {"codigo_bncc": "EF05HI02", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "As formas de organização social e política: a noção de Estado", "habilidade_descricao": "Identificar os mecanismos de organização do poder político com vistas à compreensão da ideia de Estado e/ou de outras formas de ordenação social."},
    {"codigo_bncc": "EF05HI03", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "O papel das religiões e da cultura para a formação dos povos antigos", "habilidade_descricao": "Analisar o papel das culturas e das religiões na composição identitária dos povos antigos."},
    {"codigo_bncc": "EF05HI04", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Cidadania, diversidade cultural e respeito às diferenças sociais, culturais e históricas", "habilidade_descricao": "Associar a noção de cidadania com os princípios de respeito à diversidade, à pluralidade e aos direitos humanos."},
    {"codigo_bncc": "EF05HI05", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Os patrimônios materiais e imateriais da humanidade", "habilidade_descricao": "Associar o conceito de cidadania à conquista de direitos dos povos e das sociedades, compreendendo-o como conquista histórica."},
    {"codigo_bncc": "EF05HI06", "componente": "História", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "As tradições orais e a valorização da memória", "habilidade_descricao": "Comparar o uso de diferentes linguagens e tecnologias no processo de comunicação e avaliar os significados sociais, políticos e culturais atribuídos a elas."},
    
    # ============================================
    # GEOGRAFIA - 1º ao 5º ANO
    # ============================================
    # 1º ANO
    {"codigo_bncc": "EF01GE01", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "O modo de vida das crianças em diferentes lugares", "habilidade_descricao": "Descrever características observadas de seus lugares de vivência (moradia, escola etc.) e identificar semelhanças e diferenças entre esses lugares."},
    {"codigo_bncc": "EF01GE02", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Situações de convívio em diferentes lugares", "habilidade_descricao": "Identificar semelhanças e diferenças entre jogos e brincadeiras de diferentes épocas e lugares."},
    {"codigo_bncc": "EF01GE03", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Sistemas de orientação", "habilidade_descricao": "Identificar e relatar semelhanças e diferenças de usos do espaço público (praças, parques) para o lazer e diferentes manifestações."},
    {"codigo_bncc": "EF01GE04", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Pontos de referência", "habilidade_descricao": "Discutir e elaborar, coletivamente, regras de convívio em diferentes espaços (sala de aula, escola etc.)."},
    {"codigo_bncc": "EF01GE05", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Localização, orientação e representação espacial", "habilidade_descricao": "Observar e descrever ritmos naturais (dia e noite, variação de temperatura e umidade etc.) em diferentes escalas espaciais e temporais."},
    {"codigo_bncc": "EF01GE06", "componente": "Geografia", "ano_escolar": "1º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Condições de vida nos lugares de vivência", "habilidade_descricao": "Comparar tipos variados de moradia ou objetos de uso cotidiano, considerando técnicas e materiais utilizados em sua produção."},
    
    # 2º ANO
    {"codigo_bncc": "EF02GE01", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Convivência e interações entre pessoas na comunidade", "habilidade_descricao": "Descrever a história das migrações no bairro ou comunidade em que vive."},
    {"codigo_bncc": "EF02GE02", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Riscos e cuidados nos meios de transporte e de comunicação", "habilidade_descricao": "Comparar costumes e tradições de diferentes populações inseridas no bairro ou comunidade em que vive, reconhecendo a importância do respeito às diferenças."},
    {"codigo_bncc": "EF02GE03", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Meios de transporte", "habilidade_descricao": "Comparar diferentes meios de transporte e de comunicação, indicando o seu papel na conexão entre lugares."},
    {"codigo_bncc": "EF02GE04", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Tipos de trabalho em lugares e tempos diferentes", "habilidade_descricao": "Reconhecer semelhanças e diferenças nos hábitos, nas relações com a natureza e no modo de viver de pessoas em diferentes lugares."},
    {"codigo_bncc": "EF02GE05", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Localização, orientação e representação espacial", "habilidade_descricao": "Analisar mudanças e permanências, comparando imagens de um mesmo lugar em diferentes tempos."},
    {"codigo_bncc": "EF02GE06", "componente": "Geografia", "ano_escolar": "2º ano", "trimestre_sugerido": 4, "dificuldade": "facil", "objeto_conhecimento": "Os usos dos recursos naturais: solo e água no campo e na cidade", "habilidade_descricao": "Comparar os diferentes modos de viver de pessoas que trabalham no campo e na cidade."},
    
    # 3º ANO
    {"codigo_bncc": "EF03GE01", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "A cidade e o campo: aproximações e diferenças", "habilidade_descricao": "Identificar e comparar aspectos culturais dos grupos sociais de seus lugares de vivência, seja na cidade, seja no campo."},
    {"codigo_bncc": "EF03GE02", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Paisagens naturais e antrópicas em transformação", "habilidade_descricao": "Identificar, em seus lugares de vivência, marcas de contribuição cultural e econômica de grupos de diferentes origens."},
    {"codigo_bncc": "EF03GE03", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Matérias-primas e indústria", "habilidade_descricao": "Reconhecer os diferentes modos de vida de povos e comunidades tradicionais em distintos lugares."},
    {"codigo_bncc": "EF03GE04", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Representações cartográficas", "habilidade_descricao": "Explicar como os processos naturais e históricos atuam na produção e na mudança das paisagens naturais e antrópicas nos seus lugares de vivência."},
    {"codigo_bncc": "EF03GE05", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Diferentes tipos de mapas", "habilidade_descricao": "Identificar alimentos, minerais e outros produtos cultivados e extraídos da natureza, comparando as atividades de trabalho em diferentes lugares."},
    {"codigo_bncc": "EF03GE06", "componente": "Geografia", "ano_escolar": "3º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Produção, circulação e consumo", "habilidade_descricao": "Identificar e interpretar imagens bidimensionais e tridimensionais em diferentes tipos de representação cartográfica."},
    
    # 4º ANO
    {"codigo_bncc": "EF04GE01", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Território e diversidade cultural", "habilidade_descricao": "Selecionar, em seus lugares de vivência e em suas histórias familiares e/ou da comunidade, elementos de distintas culturas."},
    {"codigo_bncc": "EF04GE02", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Processos migratórios no Brasil", "habilidade_descricao": "Descrever processos migratórios e suas contribuições para a formação da sociedade brasileira."},
    {"codigo_bncc": "EF04GE03", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Instâncias do poder público e canais de participação social", "habilidade_descricao": "Distinguir funções e papéis dos órgãos do poder público municipal e canais de participação social na gestão do Município."},
    {"codigo_bncc": "EF04GE04", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Sistema de orientação", "habilidade_descricao": "Reconhecer especificidades e analisar a interdependência do campo e da cidade, considerando fluxos econômicos, de informações, de ideias e de pessoas."},
    {"codigo_bncc": "EF04GE05", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Elementos constitutivos dos mapas", "habilidade_descricao": "Distinguir unidades político-administrativas oficiais nacionais (Distrito, Município, Unidade da Federação e grande região)."},
    {"codigo_bncc": "EF04GE06", "componente": "Geografia", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Conservação e degradação da natureza", "habilidade_descricao": "Identificar e descrever territórios étnico-culturais existentes no Brasil, tais como terras indígenas e de comunidades remanescentes de quilombos."},
    
    # 5º ANO
    {"codigo_bncc": "EF05GE01", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Dinâmica populacional", "habilidade_descricao": "Descrever e analisar dinâmicas populacionais na Unidade da Federação em que vive, estabelecendo relações entre migrações e condições de infraestrutura."},
    {"codigo_bncc": "EF05GE02", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Diferenças étnico-raciais e étnico-culturais e desigualdades sociais", "habilidade_descricao": "Identificar diferenças étnico-raciais e étnico-culturais e desigualdades sociais entre grupos em diferentes territórios."},
    {"codigo_bncc": "EF05GE03", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Cidadania e diversidade", "habilidade_descricao": "Identificar as formas e funções das cidades e analisar as mudanças sociais, econômicas e ambientais provocadas pelo seu crescimento."},
    {"codigo_bncc": "EF05GE04", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Representação das cidades e do espaço urbano", "habilidade_descricao": "Reconhecer as características da cidade e analisar as interações entre a cidade e o campo e entre cidades na rede urbana."},
    {"codigo_bncc": "EF05GE05", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Qualidade ambiental", "habilidade_descricao": "Identificar e comparar as mudanças dos tipos de trabalho e desenvolvimento tecnológico na agropecuária, na indústria, no comércio e nos serviços."},
    {"codigo_bncc": "EF05GE06", "componente": "Geografia", "ano_escolar": "5º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Diferentes tipos de poluição", "habilidade_descricao": "Identificar e comparar transformações dos meios de transporte e de comunicação."},
    
    # ============================================
    # SOCIOEMOCIONAL / AUTONOMIA - FUNDAMENTAL I
    # ============================================
    {"codigo_bncc": "SOCIOEF101", "componente": "Socioemocional", "ano_escolar": "1º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Autoconhecimento", "habilidade_descricao": "Identificar e nomear as próprias emoções básicas (alegria, tristeza, medo, raiva)."},
    {"codigo_bncc": "SOCIOEF102", "componente": "Socioemocional", "ano_escolar": "1º ano", "trimestre_sugerido": 2, "dificuldade": "facil", "objeto_conhecimento": "Convivência", "habilidade_descricao": "Praticar o compartilhamento e a cooperação em atividades de grupo."},
    {"codigo_bncc": "SOCIOEF201", "componente": "Socioemocional", "ano_escolar": "2º ano", "trimestre_sugerido": 1, "dificuldade": "facil", "objeto_conhecimento": "Organização", "habilidade_descricao": "Organizar materiais escolares e seguir rotinas básicas de estudo."},
    {"codigo_bncc": "SOCIOEF202", "componente": "Socioemocional", "ano_escolar": "2º ano", "trimestre_sugerido": 3, "dificuldade": "facil", "objeto_conhecimento": "Comunicação", "habilidade_descricao": "Expressar necessidades e sentimentos de forma respeitosa."},
    {"codigo_bncc": "SOCIOEF301", "componente": "Socioemocional", "ano_escolar": "3º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Autorregulação", "habilidade_descricao": "Desenvolver estratégias para lidar com frustrações e situações difíceis."},
    {"codigo_bncc": "SOCIOEF302", "componente": "Socioemocional", "ano_escolar": "3º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Empatia", "habilidade_descricao": "Reconhecer e respeitar os sentimentos e perspectivas dos colegas."},
    {"codigo_bncc": "SOCIOEF401", "componente": "Socioemocional", "ano_escolar": "4º ano", "trimestre_sugerido": 2, "dificuldade": "media", "objeto_conhecimento": "Responsabilidade", "habilidade_descricao": "Assumir responsabilidades em tarefas escolares e domésticas adequadas à idade."},
    {"codigo_bncc": "SOCIOEF402", "componente": "Socioemocional", "ano_escolar": "4º ano", "trimestre_sugerido": 4, "dificuldade": "media", "objeto_conhecimento": "Trabalho em equipe", "habilidade_descricao": "Colaborar efetivamente em trabalhos em grupo, respeitando diferentes opiniões."},
    {"codigo_bncc": "SOCIOEF501", "componente": "Socioemocional", "ano_escolar": "5º ano", "trimestre_sugerido": 1, "dificuldade": "media", "objeto_conhecimento": "Autonomia", "habilidade_descricao": "Desenvolver rotinas de estudo independente com mínima supervisão."},
    {"codigo_bncc": "SOCIOEF502", "componente": "Socioemocional", "ano_escolar": "5º ano", "trimestre_sugerido": 3, "dificuldade": "media", "objeto_conhecimento": "Resolução de conflitos", "habilidade_descricao": "Resolver conflitos interpessoais de forma pacífica e construtiva."},
]


def importar_bncc_ef1_expandido():
    print("=" * 70)
    print("IMPORTAÇÃO EXPANDIDA - BNCC ENSINO FUNDAMENTAL I")
    print(f"Total de habilidades: {len(HABILIDADES_EF1)}")
    print("=" * 70)
    
    with engine.connect() as conn:
        inseridos = 0
        atualizados = 0
        
        for hab in HABILIDADES_EF1:
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
        
        # Contagem por componente e ano
        print("\n" + "-" * 70)
        print("POR ANO ESCOLAR (Fundamental I):")
        print("-" * 70)
        
        for ano in ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"]:
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
    importar_bncc_ef1_expandido()
