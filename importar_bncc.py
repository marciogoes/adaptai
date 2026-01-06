# ============================================
# Script de Importação da BNCC
# AdaptAI - Planejamento Curricular
# ============================================

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.curriculo import CurriculoNacional, MapeamentoPrerequisitos

# Dados da BNCC - Ensino Fundamental Anos Iniciais
BNCC_MATEMATICA = [
    # 1º ANO
    {
        "codigo_bncc": "EF01MA01",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Contagem",
        "habilidade_descricao": "Utilizar números naturais como indicador de quantidade ou de ordem em diferentes situações cotidianas e reconhecer situações em que os números não indicam contagem nem ordem, mas sim código de identificação.",
        "objeto_conhecimento": "Contagem de rotina, Contagem ascendente e descendente, Reconhecimento de números no contexto diário",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01MA02",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Contagem",
        "habilidade_descricao": "Contar de maneira exata ou aproximada, utilizando diferentes estratégias como o pareamento e outros agrupamentos.",
        "objeto_conhecimento": "Quantificação de elementos de uma coleção: estimativas, contagem um a um, pareamento ou outros agrupamentos",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01MA03",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Escrita numérica",
        "habilidade_descricao": "Estimar e comparar quantidades de objetos de dois conjuntos (em torno de 20 elementos), por estimativa e/ou por correspondência (um a um, dois a dois) para indicar 'tem mais', 'tem menos' ou 'tem a mesma quantidade'.",
        "objeto_conhecimento": "Leitura, escrita e comparação de números naturais (até 100)",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01MA04",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Contar a quantidade de objetos de coleções até 100 unidades e apresentar o resultado por registros verbais e simbólicos, em situações de seu interesse, como jogos, brincadeiras, materiais da sala de aula, entre outros.",
        "objeto_conhecimento": "Leitura, escrita e comparação de números naturais (até 100)",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF01MA05",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Comparar números naturais de até duas ordens em situações cotidianas, com e sem suporte da reta numérica.",
        "objeto_conhecimento": "Reta numérica",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF01MA06",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo para resolver problemas.",
        "objeto_conhecimento": "Construção de fatos fundamentais da adição",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF01MA07",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Compor e decompor número de até duas ordens, por meio de diferentes adições, com o suporte de material manipulável, contribuindo para a compreensão de características do sistema de numeração decimal e o desenvolvimento de estratégias de cálculo.",
        "objeto_conhecimento": "Composição e decomposição de números naturais",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF01MA08",
        "ano_escolar": "1º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Problemas",
        "habilidade_descricao": "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até dois algarismos, com os significados de juntar, acrescentar, separar e retirar, com o suporte de imagens e/ou material manipulável, utilizando estratégias e formas de registro pessoais.",
        "objeto_conhecimento": "Problemas envolvendo diferentes significados da adição e da subtração",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 4
    },
    
    # 2º ANO
    {
        "codigo_bncc": "EF02MA01",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Leitura e escrita",
        "habilidade_descricao": "Comparar e ordenar números naturais (até a ordem de centenas) pela compreensão de características do sistema de numeração decimal (valor posicional e função do zero).",
        "objeto_conhecimento": "Leitura, escrita, comparação e ordenação de números de até três ordens",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF02MA02",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Fazer estimativas por meio de estratégias diversas a respeito da quantidade de objetos de coleções e registrar o resultado da contagem desses objetos.",
        "objeto_conhecimento": "Leitura, escrita, comparação e ordenação de números de até três ordens",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF02MA03",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Composição",
        "habilidade_descricao": "Comparar quantidades de objetos de dois conjuntos, por estimativa e/ou por correspondência (um a um, dois a dois, entre outros), para indicar 'tem mais', 'tem menos' ou 'tem a mesma quantidade', indicando, quando for o caso, quantos a mais e quantos a menos.",
        "objeto_conhecimento": "Composição e decomposição de números naturais (até 1000)",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF02MA04",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Composição",
        "habilidade_descricao": "Compor e decompor números naturais de até três ordens, com suporte de material manipulável, por meio de diferentes adições.",
        "objeto_conhecimento": "Composição e decomposição de números naturais (até 1000)",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF02MA05",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Construir fatos básicos da adição e subtração e utilizá-los no cálculo mental ou escrito.",
        "objeto_conhecimento": "Construção de fatos fundamentais da adição e da subtração",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF02MA06",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Problemas",
        "habilidade_descricao": "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até três ordens, com os significados de juntar, acrescentar, separar, retirar, utilizando estratégias pessoais.",
        "objeto_conhecimento": "Problemas envolvendo diferentes significados da adição e da subtração",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF02MA07",
        "ano_escolar": "2º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Multiplicação",
        "habilidade_descricao": "Resolver e elaborar problemas de multiplicação (por 2, 3, 4 e 5) com a ideia de adição de parcelas iguais por meio de estratégias e formas de registro pessoais, utilizando ou não suporte de imagens e/ou material manipulável.",
        "objeto_conhecimento": "Problemas envolvendo adição de parcelas iguais (multiplicação)",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    
    # 3º ANO
    {
        "codigo_bncc": "EF03MA01",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Leitura e escrita",
        "habilidade_descricao": "Ler, escrever e comparar números naturais de até a ordem de unidade de milhar, estabelecendo relações entre os registros numéricos e em língua materna.",
        "objeto_conhecimento": "Leitura, escrita, comparação e ordenação de números naturais de quatro ordens",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF03MA02",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Composição",
        "habilidade_descricao": "Identificar características do sistema de numeração decimal, utilizando a composição e a decomposição de número natural de até quatro ordens.",
        "objeto_conhecimento": "Composição e decomposição de números naturais",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF03MA03",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Construir e utilizar fatos básicos da adição e da multiplicação para o cálculo mental ou escrito.",
        "objeto_conhecimento": "Construção de fatos fundamentais da adição, subtração e multiplicação",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF03MA04",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Algoritmos",
        "habilidade_descricao": "Estabelecer a relação entre números naturais e pontos da reta numérica para utilizá-la na ordenação dos números naturais e também na construção de fatos da adição e da subtração, relacionando-os com deslocamentos para a direita ou para a esquerda.",
        "objeto_conhecimento": "Reta numérica",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF03MA05",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Algoritmos",
        "habilidade_descricao": "Utilizar diferentes procedimentos de cálculo mental e escrito para resolver problemas significativos envolvendo adição e subtração com números naturais.",
        "objeto_conhecimento": "Procedimentos de cálculo (mental e escrito) com números naturais: adição e subtração",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF03MA06",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Problemas",
        "habilidade_descricao": "Resolver e elaborar problemas de adição e subtração com os significados de juntar, acrescentar, separar, retirar, comparar e completar quantidades, utilizando diferentes estratégias de cálculo exato ou aproximado, incluindo cálculo mental.",
        "objeto_conhecimento": "Problemas envolvendo significados da adição e da subtração: juntar, acrescentar, separar, retirar, comparar e completar quantidades",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF03MA07",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Multiplicação",
        "habilidade_descricao": "Resolver e elaborar problemas de multiplicação (por 2, 3, 4, 5 e 10) com os significados de adição de parcelas iguais e elementos apresentados em disposição retangular, utilizando diferentes estratégias de cálculo e registros.",
        "objeto_conhecimento": "Significados da multiplicação: adição de parcelas iguais e configuração retangular",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    {
        "codigo_bncc": "EF03MA08",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Divisão",
        "habilidade_descricao": "Resolver e elaborar problemas de divisão de um número natural por outro (até 10), com resto zero e com resto diferente de zero, com os significados de repartição equitativa e de medida, por meio de estratégias e registros pessoais.",
        "objeto_conhecimento": "Significados da divisão: repartição equitativa e medida",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    {
        "codigo_bncc": "EF03MA09",
        "ano_escolar": "3º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Associar o quociente de uma divisão com resto zero de um número natural por 2, 3, 4, 5 e 10 às ideias de metade, terça, quarta, quinta e décima partes.",
        "objeto_conhecimento": "Significados de metade, terça parte, quarta parte, quinta parte e décima parte",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    
    # 4º ANO
    {
        "codigo_bncc": "EF04MA01",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Leitura e escrita",
        "habilidade_descricao": "Ler, escrever e ordenar números naturais até a ordem de dezenas de milhar.",
        "objeto_conhecimento": "Sistema de numeração decimal: leitura, escrita, comparação e ordenação de números naturais de até cinco ordens",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF04MA02",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Composição",
        "habilidade_descricao": "Mostrar, por decomposição e composição, que todo número natural pode ser escrito por meio de adições e multiplicações por potências de dez, para compreender o sistema de numeração decimal e desenvolver estratégias de cálculo.",
        "objeto_conhecimento": "Composição e decomposição de um número natural de até cinco ordens",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF04MA03",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Resolver e elaborar problemas com números naturais envolvendo adição e subtração, utilizando estratégias diversas, como cálculo, cálculo mental e algoritmos, além de fazer estimativas do resultado.",
        "objeto_conhecimento": "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF04MA04",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Multiplicação",
        "habilidade_descricao": "Utilizar as relações entre adição e subtração, bem como entre multiplicação e divisão, para ampliar as estratégias de cálculo.",
        "objeto_conhecimento": "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF04MA05",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Multiplicação",
        "habilidade_descricao": "Utilizar as propriedades das operações para desenvolver estratégias de cálculo.",
        "objeto_conhecimento": "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF04MA06",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Problemas",
        "habilidade_descricao": "Resolver e elaborar problemas envolvendo diferentes significados da multiplicação: adição de parcelas iguais, organização retangular, proporcionalidade, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.",
        "objeto_conhecimento": "Problemas envolvendo diferentes significados da multiplicação e da divisão: adição de parcelas iguais, configuração retangular, proporcionalidade, repartição equitativa e medida",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF04MA07",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Divisão",
        "habilidade_descricao": "Resolver e elaborar problemas de divisão cujo divisor tenha no máximo dois algarismos, envolvendo os significados de repartição equitativa e de medida, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.",
        "objeto_conhecimento": "Problemas envolvendo diferentes significados da multiplicação e da divisão",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    {
        "codigo_bncc": "EF04MA08",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Resolver, com o suporte de imagem e/ou material manipulável, problemas simples de contagem, como a determinação do número de agrupamentos possíveis ao se combinar cada elemento de uma coleção com todos os elementos de outra, utilizando estratégias e formas de registro pessoais.",
        "objeto_conhecimento": "Problemas de contagem",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    {
        "codigo_bncc": "EF04MA09",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Reconhecer as frações unitárias mais usuais (1/2, 1/3, 1/4, 1/5, 1/10 e 1/100) como unidades de medida menores do que uma unidade, utilizando a reta numérica como recurso.",
        "objeto_conhecimento": "Números racionais: frações unitárias mais usuais",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF04MA10",
        "ano_escolar": "4º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Reconhecer que as regras do sistema de numeração decimal podem ser estendidas para a representação decimal de um número racional e relacionar décimos e centésimos com a representação do sistema monetário brasileiro.",
        "objeto_conhecimento": "Números racionais: representação decimal para escrever valores do sistema monetário brasileiro",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 4
    },
    
    # 5º ANO
    {
        "codigo_bncc": "EF05MA01",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Leitura e escrita",
        "habilidade_descricao": "Ler, escrever e ordenar números naturais até a ordem das centenas de milhar com compreensão das principais características do sistema de numeração decimal.",
        "objeto_conhecimento": "Sistema de numeração decimal: leitura, escrita e ordenação de números naturais",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF05MA02",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Leitura e escrita",
        "habilidade_descricao": "Ler, escrever e ordenar números racionais na forma decimal com compreensão das principais características do sistema de numeração decimal, utilizando, como recursos, a composição e decomposição e a reta numérica.",
        "objeto_conhecimento": "Números racionais expressos na forma decimal e sua representação na reta numérica",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF05MA03",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Identificar e representar frações (menores e maiores que a unidade), associando-as ao resultado de uma divisão ou à ideia de parte de um todo, utilizando a reta numérica como recurso.",
        "objeto_conhecimento": "Representação fracionária dos números racionais: reconhecimento, significados, leitura e representação na reta numérica",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF05MA04",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Identificar frações equivalentes.",
        "objeto_conhecimento": "Comparação e ordenação de números racionais na representação decimal e na fracionária utilizando a noção de equivalência",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF05MA05",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Comparar e ordenar números racionais positivos (representações fracionária e decimal), relacionando-os a pontos na reta numérica.",
        "objeto_conhecimento": "Comparação e ordenação de números racionais na representação decimal e na fracionária utilizando a noção de equivalência",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF05MA06",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Frações",
        "habilidade_descricao": "Associar as representações 10%, 25%, 50%, 75% e 100% respectivamente à décima parte, quarta parte, metade, três quartos e um inteiro, para calcular porcentagens, utilizando estratégias pessoais, cálculo mental e calculadora, em contextos de educação financeira, entre outros.",
        "objeto_conhecimento": "Cálculo de porcentagens e representação fracionária",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF05MA07",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Resolver e elaborar problemas de adição e subtração com números naturais e com números racionais, cuja representação decimal seja finita, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.",
        "objeto_conhecimento": "Problemas: adição e subtração de números naturais e números racionais cuja representação decimal é finita",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF05MA08",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números e Álgebra",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal seja finita (com multiplicador natural e divisor natural e diferente de zero), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.",
        "objeto_conhecimento": "Problemas: multiplicação e divisão de números racionais cuja representação decimal é finita por números naturais",
        "dificuldade": "avancado",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF05MA09",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Números",
        "eixo_tematico": "Operações",
        "habilidade_descricao": "Resolver e elaborar problemas simples de contagem envolvendo o princípio multiplicativo, como a determinação do número de agrupamentos possíveis ao se combinar cada elemento de uma coleção com todos os elementos de outra coleção, por meio de diagramas de árvore ou por tabelas.",
        "objeto_conhecimento": "Problemas de contagem do tipo: 'Se cada expression tiver expression escolhas, de quantas maneiras expression?'",
        "dificuldade": "avancado",
        "trimestre_sugerido": 4
    },
    {
        "codigo_bncc": "EF05MA17",
        "ano_escolar": "5º ano",
        "componente": "Matemática",
        "campo_experiencia": "Geometria",
        "eixo_tematico": "Formas Geométricas",
        "habilidade_descricao": "Reconhecer, nomear e comparar polígonos, considerando lados, vértices e ângulos, e desenhá-los, utilizando material de desenho ou tecnologias digitais.",
        "objeto_conhecimento": "Figuras geométricas planas: características, representações e ângulos",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
]

# Dados da BNCC - Língua Portuguesa Anos Iniciais
BNCC_PORTUGUES = [
    # 1º ANO
    {
        "codigo_bncc": "EF01LP01",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Leitura/escuta",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Reconhecer que textos são lidos e escritos da esquerda para a direita e de cima para baixo da página.",
        "objeto_conhecimento": "Protocolos de leitura",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01LP02",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Leitura/escuta",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Escrever, espontaneamente ou por ditado, palavras e frases de forma alfabética – usando letras/grafemas que representem fonemas.",
        "objeto_conhecimento": "Correspondência fonema-grafema",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01LP03",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Observar escritas convencionais, comparando-as às suas produções escritas, percebendo semelhanças e diferenças.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF01LP04",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Distinguir as letras do alfabeto de outros sinais gráficos.",
        "objeto_conhecimento": "Conhecimento do alfabeto do português do Brasil",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF01LP05",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Reconhecer o sistema de escrita alfabética como representação dos sons da fala.",
        "objeto_conhecimento": "Construção do sistema alfabético",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF01LP06",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Segmentar oralmente palavras em sílabas.",
        "objeto_conhecimento": "Segmentação de palavras e consciência silábica",
        "dificuldade": "fundamental",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF01LP07",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Identificar fonemas e sua representação por letras.",
        "objeto_conhecimento": "Correspondência fonema-grafema",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    {
        "codigo_bncc": "EF01LP08",
        "ano_escolar": "1º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Relacionar elementos sonoros (sílabas, fonemas, partes de palavras) com sua representação escrita.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    
    # 2º ANO
    {
        "codigo_bncc": "EF02LP01",
        "ano_escolar": "2º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Utilizar, ao produzir o texto, grafia correta de palavras conhecidas ou com estruturas silábicas já dominadas, letras maiúsculas em início de frases e em substantivos próprios, segmentação entre as palavras, ponto final, ponto de interrogação e ponto de exclamação.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF02LP02",
        "ano_escolar": "2º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Segmentar palavras em sílabas e remover e substituir sílabas iniciais, mediais ou finais para criar novas palavras.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF02LP03",
        "ano_escolar": "2º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Alfabetização",
        "habilidade_descricao": "Ler e escrever palavras com correspondências regulares diretas entre letras e fonemas (f, v, t, d, p, b) e correspondências regulares contextuais (c e q; e e o, em posição átona em final de palavra).",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF02LP04",
        "ano_escolar": "2º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, identificando que existem vogais em todas as sílabas.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 3
    },
    
    # 3º ANO
    {
        "codigo_bncc": "EF03LP01",
        "ano_escolar": "3º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Ler e escrever palavras com correspondências regulares contextuais entre grafemas e fonemas – c/qu; g/gu; r/rr; s/ss; o (e não u) e e (e não i) em sílaba átona em final de palavra – e com marcas de nasalidade (til, m, n).",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF03LP02",
        "ano_escolar": "3º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, VC, VV, CVV, identificando que existem vogais em todas as sílabas.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF03LP03",
        "ano_escolar": "3º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Ler e escrever corretamente palavras com os dígrafos lh, nh, ch.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    
    # 4º ANO
    {
        "codigo_bncc": "EF04LP01",
        "ano_escolar": "4º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Grafar palavras utilizando regras de correspondência fonema-grafema regulares diretas e contextuais.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF04LP02",
        "ano_escolar": "4º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Ler e escrever, corretamente, palavras com sílabas VV e CVV em casos nos quais a combinação VV (ditongo) é reduzida na língua oral (ai, ei, ou).",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 2
    },
    
    # 5º ANO
    {
        "codigo_bncc": "EF05LP01",
        "ano_escolar": "5º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Grafar palavras utilizando regras de correspondência fonema-grafema regulares, contextuais e morfológicas e palavras de uso frequente com correspondências irregulares.",
        "objeto_conhecimento": "Construção do sistema alfabético e da ortografia",
        "dificuldade": "intermediario",
        "trimestre_sugerido": 1
    },
    {
        "codigo_bncc": "EF05LP02",
        "ano_escolar": "5º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Identificar o caráter polissêmico das palavras (uma mesma palavra com diferentes significados, de acordo com o contexto de uso), comparando o significado de determinados termos utilizados nas áreas científicas com esses mesmos termos utilizados na linguagem usual.",
        "objeto_conhecimento": "Conhecimento das diversas grafias do alfabeto/Acentuação",
        "dificuldade": "avancado",
        "trimestre_sugerido": 2
    },
    {
        "codigo_bncc": "EF05LP03",
        "ano_escolar": "5º ano",
        "componente": "Língua Portuguesa",
        "campo_experiencia": "Análise linguística",
        "eixo_tematico": "Ortografia",
        "habilidade_descricao": "Acentuar corretamente palavras oxítonas, paroxítonas e proparoxítonas.",
        "objeto_conhecimento": "Conhecimento das diversas grafias do alfabeto/Acentuação",
        "dificuldade": "avancado",
        "trimestre_sugerido": 3
    },
]

# Mapeamentos de pré-requisitos
PREREQUISITOS = [
    # Matemática
    {"habilidade_codigo": "EF02MA01", "habilidade_titulo": "Comparar e ordenar números até centenas", "ano_escolar": "2º ano", "prerequisito_codigo": "EF01MA03", "prerequisito_titulo": "Estimar e comparar quantidades", "ano_prerequisito": "1º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF02MA05", "habilidade_titulo": "Fatos básicos adição e subtração", "ano_escolar": "2º ano", "prerequisito_codigo": "EF01MA06", "prerequisito_titulo": "Fatos básicos da adição", "ano_prerequisito": "1º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF03MA01", "habilidade_titulo": "Ler e escrever até milhar", "ano_escolar": "3º ano", "prerequisito_codigo": "EF02MA01", "prerequisito_titulo": "Comparar e ordenar até centenas", "ano_prerequisito": "2º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF03MA07", "habilidade_titulo": "Multiplicação", "ano_escolar": "3º ano", "prerequisito_codigo": "EF02MA07", "prerequisito_titulo": "Problemas de multiplicação por 2,3,4,5", "ano_prerequisito": "2º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF04MA09", "habilidade_titulo": "Frações unitárias", "ano_escolar": "4º ano", "prerequisito_codigo": "EF03MA09", "prerequisito_titulo": "Ideias de metade, terça, quarta parte", "ano_prerequisito": "3º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF05MA03", "habilidade_titulo": "Representar frações", "ano_escolar": "5º ano", "prerequisito_codigo": "EF04MA09", "prerequisito_titulo": "Frações unitárias", "ano_prerequisito": "4º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF05MA08", "habilidade_titulo": "Frações - Adição e Subtração", "ano_escolar": "5º ano", "prerequisito_codigo": "EF04MA09", "prerequisito_titulo": "Reconhecer frações", "ano_prerequisito": "4º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF05MA08", "habilidade_titulo": "Frações - Adição e Subtração", "ano_escolar": "5º ano", "prerequisito_codigo": "EF04MA10", "prerequisito_titulo": "Representar frações decimais", "ano_prerequisito": "4º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF05MA08", "habilidade_titulo": "Frações - Adição e Subtração", "ano_escolar": "5º ano", "prerequisito_codigo": "EF03MA09", "prerequisito_titulo": "Noção de fração", "ano_prerequisito": "3º ano", "essencial": True, "peso": 0.8},
    
    # Português
    {"habilidade_codigo": "EF02LP01", "habilidade_titulo": "Grafia correta palavras conhecidas", "ano_escolar": "2º ano", "prerequisito_codigo": "EF01LP02", "prerequisito_titulo": "Escrever palavras e frases", "ano_prerequisito": "1º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF03LP01", "habilidade_titulo": "Correspondências regulares contextuais", "ano_escolar": "3º ano", "prerequisito_codigo": "EF02LP03", "prerequisito_titulo": "Ler e escrever palavras regulares", "ano_prerequisito": "2º ano", "essencial": True, "peso": 1.0},
    {"habilidade_codigo": "EF05LP01", "habilidade_titulo": "Regras fonema-grafema", "ano_escolar": "5º ano", "prerequisito_codigo": "EF04LP01", "prerequisito_titulo": "Grafar palavras regulares", "ano_prerequisito": "4º ano", "essencial": True, "peso": 1.0},
]


def importar_bncc():
    """Importa os dados da BNCC para o banco de dados"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        count = db.query(CurriculoNacional).count()
        if count > 10:
            print(f"⚠️  Já existem {count} habilidades no banco. Pulando importação duplicada.")
            print("    Se quiser reimportar, limpe a tabela curriculo_nacional primeiro.")
            return
        
        print("=" * 60)
        print("📚 IMPORTANDO BNCC - BASE NACIONAL COMUM CURRICULAR")
        print("=" * 60)
        
        # Importar Matemática
        print("\n📐 Importando Matemática...")
        for item in BNCC_MATEMATICA:
            existente = db.query(CurriculoNacional).filter(
                CurriculoNacional.codigo_bncc == item["codigo_bncc"]
            ).first()
            
            if not existente:
                curriculo = CurriculoNacional(
                    codigo_bncc=item["codigo_bncc"],
                    ano_escolar=item["ano_escolar"],
                    componente=item["componente"],
                    campo_experiencia=item.get("campo_experiencia"),
                    eixo_tematico=item.get("eixo_tematico"),
                    habilidade_codigo=item["codigo_bncc"],
                    habilidade_descricao=item["habilidade_descricao"],
                    objeto_conhecimento=item.get("objeto_conhecimento"),
                    dificuldade=item.get("dificuldade", "intermediario"),
                    trimestre_sugerido=item.get("trimestre_sugerido")
                )
                db.add(curriculo)
                print(f"   ✅ {item['codigo_bncc']} - {item['ano_escolar']}")
        
        # Importar Português
        print("\n📖 Importando Língua Portuguesa...")
        for item in BNCC_PORTUGUES:
            existente = db.query(CurriculoNacional).filter(
                CurriculoNacional.codigo_bncc == item["codigo_bncc"]
            ).first()
            
            if not existente:
                curriculo = CurriculoNacional(
                    codigo_bncc=item["codigo_bncc"],
                    ano_escolar=item["ano_escolar"],
                    componente=item["componente"],
                    campo_experiencia=item.get("campo_experiencia"),
                    eixo_tematico=item.get("eixo_tematico"),
                    habilidade_codigo=item["codigo_bncc"],
                    habilidade_descricao=item["habilidade_descricao"],
                    objeto_conhecimento=item.get("objeto_conhecimento"),
                    dificuldade=item.get("dificuldade", "intermediario"),
                    trimestre_sugerido=item.get("trimestre_sugerido")
                )
                db.add(curriculo)
                print(f"   ✅ {item['codigo_bncc']} - {item['ano_escolar']}")
        
        # Importar pré-requisitos
        print("\n🔗 Importando mapeamento de pré-requisitos...")
        for item in PREREQUISITOS:
            existente = db.query(MapeamentoPrerequisitos).filter(
                MapeamentoPrerequisitos.habilidade_codigo == item["habilidade_codigo"],
                MapeamentoPrerequisitos.prerequisito_codigo == item["prerequisito_codigo"]
            ).first()
            
            if not existente:
                prereq = MapeamentoPrerequisitos(
                    habilidade_codigo=item["habilidade_codigo"],
                    habilidade_titulo=item["habilidade_titulo"],
                    ano_escolar=item["ano_escolar"],
                    prerequisito_codigo=item["prerequisito_codigo"],
                    prerequisito_titulo=item["prerequisito_titulo"],
                    ano_prerequisito=item["ano_prerequisito"],
                    essencial=item.get("essencial", True),
                    peso=item.get("peso", 1.0)
                )
                db.add(prereq)
                print(f"   ✅ {item['habilidade_codigo']} <- {item['prerequisito_codigo']}")
        
        db.commit()
        
        # Contar resultados
        total_curriculo = db.query(CurriculoNacional).count()
        total_prereqs = db.query(MapeamentoPrerequisitos).count()
        
        print("\n" + "=" * 60)
        print("✅ IMPORTAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print(f"📚 Total de habilidades: {total_curriculo}")
        print(f"🔗 Total de pré-requisitos: {total_prereqs}")
        print("\nPor componente:")
        
        for comp in ["Matemática", "Língua Portuguesa"]:
            count = db.query(CurriculoNacional).filter(
                CurriculoNacional.componente == comp
            ).count()
            print(f"   • {comp}: {count}")
        
        print("\nPor ano escolar:")
        for ano in ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"]:
            count = db.query(CurriculoNacional).filter(
                CurriculoNacional.ano_escolar == ano
            ).count()
            print(f"   • {ano}: {count}")
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    importar_bncc()
