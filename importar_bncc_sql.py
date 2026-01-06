# ============================================
# Script de Importação da BNCC - SQL Direto
# AdaptAI - Planejamento Curricular
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

# Criar engine diretamente
engine = create_engine(settings.db_url, echo=False)

# Dados da BNCC - Ensino Fundamental Anos Iniciais
BNCC_MATEMATICA = [
    # 1º ANO
    ("EF01MA01", "1º ano", "Matemática", "Números", "Contagem", "Utilizar números naturais como indicador de quantidade ou de ordem em diferentes situações cotidianas e reconhecer situações em que os números não indicam contagem nem ordem, mas sim código de identificação.", "Contagem de rotina, Contagem ascendente e descendente, Reconhecimento de números no contexto diário", "fundamental", 1),
    ("EF01MA02", "1º ano", "Matemática", "Números", "Contagem", "Contar de maneira exata ou aproximada, utilizando diferentes estratégias como o pareamento e outros agrupamentos.", "Quantificação de elementos de uma coleção: estimativas, contagem um a um, pareamento ou outros agrupamentos", "fundamental", 1),
    ("EF01MA03", "1º ano", "Matemática", "Números", "Escrita numérica", "Estimar e comparar quantidades de objetos de dois conjuntos (em torno de 20 elementos), por estimativa e/ou por correspondência (um a um, dois a dois) para indicar 'tem mais', 'tem menos' ou 'tem a mesma quantidade'.", "Leitura, escrita e comparação de números naturais (até 100)", "fundamental", 1),
    ("EF01MA04", "1º ano", "Matemática", "Números", "Operações", "Contar a quantidade de objetos de coleções até 100 unidades e apresentar o resultado por registros verbais e simbólicos, em situações de seu interesse, como jogos, brincadeiras, materiais da sala de aula, entre outros.", "Leitura, escrita e comparação de números naturais (até 100)", "fundamental", 2),
    ("EF01MA05", "1º ano", "Matemática", "Números", "Operações", "Comparar números naturais de até duas ordens em situações cotidianas, com e sem suporte da reta numérica.", "Reta numérica", "fundamental", 2),
    ("EF01MA06", "1º ano", "Matemática", "Números", "Operações", "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo para resolver problemas.", "Construção de fatos fundamentais da adição", "intermediario", 3),
    ("EF01MA07", "1º ano", "Matemática", "Números", "Operações", "Compor e decompor número de até duas ordens, por meio de diferentes adições, com o suporte de material manipulável, contribuindo para a compreensão de características do sistema de numeração decimal e o desenvolvimento de estratégias de cálculo.", "Composição e decomposição de números naturais", "intermediario", 3),
    ("EF01MA08", "1º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até dois algarismos, com os significados de juntar, acrescentar, separar e retirar, com o suporte de imagens e/ou material manipulável, utilizando estratégias e formas de registro pessoais.", "Problemas envolvendo diferentes significados da adição e da subtração", "intermediario", 4),
    
    # 2º ANO
    ("EF02MA01", "2º ano", "Matemática", "Números", "Leitura e escrita", "Comparar e ordenar números naturais (até a ordem de centenas) pela compreensão de características do sistema de numeração decimal (valor posicional e função do zero).", "Leitura, escrita, comparação e ordenação de números de até três ordens", "fundamental", 1),
    ("EF02MA02", "2º ano", "Matemática", "Números", "Operações", "Fazer estimativas por meio de estratégias diversas a respeito da quantidade de objetos de coleções e registrar o resultado da contagem desses objetos.", "Leitura, escrita, comparação e ordenação de números de até três ordens", "fundamental", 1),
    ("EF02MA03", "2º ano", "Matemática", "Números", "Composição", "Comparar quantidades de objetos de dois conjuntos, por estimativa e/ou por correspondência (um a um, dois a dois, entre outros), para indicar 'tem mais', 'tem menos' ou 'tem a mesma quantidade', indicando, quando for o caso, quantos a mais e quantos a menos.", "Composição e decomposição de números naturais (até 1000)", "fundamental", 2),
    ("EF02MA04", "2º ano", "Matemática", "Números", "Composição", "Compor e decompor números naturais de até três ordens, com suporte de material manipulável, por meio de diferentes adições.", "Composição e decomposição de números naturais (até 1000)", "intermediario", 2),
    ("EF02MA05", "2º ano", "Matemática", "Números", "Operações", "Construir fatos básicos da adição e subtração e utilizá-los no cálculo mental ou escrito.", "Construção de fatos fundamentais da adição e da subtração", "intermediario", 3),
    ("EF02MA06", "2º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas de adição e de subtração, envolvendo números de até três ordens, com os significados de juntar, acrescentar, separar, retirar, utilizando estratégias pessoais.", "Problemas envolvendo diferentes significados da adição e da subtração", "intermediario", 3),
    ("EF02MA07", "2º ano", "Matemática", "Números", "Multiplicação", "Resolver e elaborar problemas de multiplicação (por 2, 3, 4 e 5) com a ideia de adição de parcelas iguais por meio de estratégias e formas de registro pessoais, utilizando ou não suporte de imagens e/ou material manipulável.", "Problemas envolvendo adição de parcelas iguais (multiplicação)", "avancado", 4),
    
    # 3º ANO
    ("EF03MA01", "3º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e comparar números naturais de até a ordem de unidade de milhar, estabelecendo relações entre os registros numéricos e em língua materna.", "Leitura, escrita, comparação e ordenação de números naturais de quatro ordens", "fundamental", 1),
    ("EF03MA02", "3º ano", "Matemática", "Números", "Composição", "Identificar características do sistema de numeração decimal, utilizando a composição e a decomposição de número natural de até quatro ordens.", "Composição e decomposição de números naturais", "fundamental", 1),
    ("EF03MA03", "3º ano", "Matemática", "Números", "Operações", "Construir e utilizar fatos básicos da adição e da multiplicação para o cálculo mental ou escrito.", "Construção de fatos fundamentais da adição, subtração e multiplicação", "intermediario", 2),
    ("EF03MA04", "3º ano", "Matemática", "Números", "Algoritmos", "Estabelecer a relação entre números naturais e pontos da reta numérica para utilizá-la na ordenação dos números naturais e também na construção de fatos da adição e da subtração, relacionando-os com deslocamentos para a direita ou para a esquerda.", "Reta numérica", "intermediario", 2),
    ("EF03MA05", "3º ano", "Matemática", "Números", "Algoritmos", "Utilizar diferentes procedimentos de cálculo mental e escrito para resolver problemas significativos envolvendo adição e subtração com números naturais.", "Procedimentos de cálculo (mental e escrito) com números naturais: adição e subtração", "intermediario", 3),
    ("EF03MA06", "3º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas de adição e subtração com os significados de juntar, acrescentar, separar, retirar, comparar e completar quantidades, utilizando diferentes estratégias de cálculo exato ou aproximado, incluindo cálculo mental.", "Problemas envolvendo significados da adição e da subtração: juntar, acrescentar, separar, retirar, comparar e completar quantidades", "intermediario", 3),
    ("EF03MA07", "3º ano", "Matemática", "Números", "Multiplicação", "Resolver e elaborar problemas de multiplicação (por 2, 3, 4, 5 e 10) com os significados de adição de parcelas iguais e elementos apresentados em disposição retangular, utilizando diferentes estratégias de cálculo e registros.", "Significados da multiplicação: adição de parcelas iguais e configuração retangular", "avancado", 4),
    ("EF03MA08", "3º ano", "Matemática", "Números", "Divisão", "Resolver e elaborar problemas de divisão de um número natural por outro (até 10), com resto zero e com resto diferente de zero, com os significados de repartição equitativa e de medida, por meio de estratégias e registros pessoais.", "Significados da divisão: repartição equitativa e medida", "avancado", 4),
    ("EF03MA09", "3º ano", "Matemática", "Números", "Frações", "Associar o quociente de uma divisão com resto zero de um número natural por 2, 3, 4, 5 e 10 às ideias de metade, terça, quarta, quinta e décima partes.", "Significados de metade, terça parte, quarta parte, quinta parte e décima parte", "avancado", 4),
    
    # 4º ANO
    ("EF04MA01", "4º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números naturais até a ordem de dezenas de milhar.", "Sistema de numeração decimal: leitura, escrita, comparação e ordenação de números naturais de até cinco ordens", "fundamental", 1),
    ("EF04MA02", "4º ano", "Matemática", "Números", "Composição", "Mostrar, por decomposição e composição, que todo número natural pode ser escrito por meio de adições e multiplicações por potências de dez, para compreender o sistema de numeração decimal e desenvolver estratégias de cálculo.", "Composição e decomposição de um número natural de até cinco ordens", "intermediario", 1),
    ("EF04MA03", "4º ano", "Matemática", "Números", "Operações", "Resolver e elaborar problemas com números naturais envolvendo adição e subtração, utilizando estratégias diversas, como cálculo, cálculo mental e algoritmos, além de fazer estimativas do resultado.", "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais", "intermediario", 2),
    ("EF04MA04", "4º ano", "Matemática", "Números", "Multiplicação", "Utilizar as relações entre adição e subtração, bem como entre multiplicação e divisão, para ampliar as estratégias de cálculo.", "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais", "intermediario", 2),
    ("EF04MA05", "4º ano", "Matemática", "Números", "Multiplicação", "Utilizar as propriedades das operações para desenvolver estratégias de cálculo.", "Propriedades das operações para o desenvolvimento de diferentes estratégias de cálculo com números naturais", "intermediario", 3),
    ("EF04MA06", "4º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas envolvendo diferentes significados da multiplicação: adição de parcelas iguais, organização retangular, proporcionalidade, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.", "Problemas envolvendo diferentes significados da multiplicação e da divisão: adição de parcelas iguais, configuração retangular, proporcionalidade, repartição equitativa e medida", "intermediario", 3),
    ("EF04MA07", "4º ano", "Matemática", "Números", "Divisão", "Resolver e elaborar problemas de divisão cujo divisor tenha no máximo dois algarismos, envolvendo os significados de repartição equitativa e de medida, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.", "Problemas envolvendo diferentes significados da multiplicação e da divisão", "avancado", 4),
    ("EF04MA09", "4º ano", "Matemática", "Números", "Frações", "Reconhecer as frações unitárias mais usuais (1/2, 1/3, 1/4, 1/5, 1/10 e 1/100) como unidades de medida menores do que uma unidade, utilizando a reta numérica como recurso.", "Números racionais: frações unitárias mais usuais", "intermediario", 3),
    ("EF04MA10", "4º ano", "Matemática", "Números", "Frações", "Reconhecer que as regras do sistema de numeração decimal podem ser estendidas para a representação decimal de um número racional e relacionar décimos e centésimos com a representação do sistema monetário brasileiro.", "Números racionais: representação decimal para escrever valores do sistema monetário brasileiro", "intermediario", 4),
    
    # 5º ANO
    ("EF05MA01", "5º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números naturais até a ordem das centenas de milhar com compreensão das principais características do sistema de numeração decimal.", "Sistema de numeração decimal: leitura, escrita e ordenação de números naturais", "fundamental", 1),
    ("EF05MA02", "5º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números racionais na forma decimal com compreensão das principais características do sistema de numeração decimal, utilizando, como recursos, a composição e decomposição e a reta numérica.", "Números racionais expressos na forma decimal e sua representação na reta numérica", "intermediario", 1),
    ("EF05MA03", "5º ano", "Matemática", "Números", "Frações", "Identificar e representar frações (menores e maiores que a unidade), associando-as ao resultado de uma divisão ou à ideia de parte de um todo, utilizando a reta numérica como recurso.", "Representação fracionária dos números racionais: reconhecimento, significados, leitura e representação na reta numérica", "intermediario", 2),
    ("EF05MA04", "5º ano", "Matemática", "Números", "Frações", "Identificar frações equivalentes.", "Comparação e ordenação de números racionais na representação decimal e na fracionária utilizando a noção de equivalência", "intermediario", 2),
    ("EF05MA05", "5º ano", "Matemática", "Números", "Frações", "Comparar e ordenar números racionais positivos (representações fracionária e decimal), relacionando-os a pontos na reta numérica.", "Comparação e ordenação de números racionais na representação decimal e na fracionária utilizando a noção de equivalência", "intermediario", 2),
    ("EF05MA06", "5º ano", "Matemática", "Números", "Frações", "Associar as representações 10%, 25%, 50%, 75% e 100% respectivamente à décima parte, quarta parte, metade, três quartos e um inteiro, para calcular porcentagens, utilizando estratégias pessoais, cálculo mental e calculadora, em contextos de educação financeira, entre outros.", "Cálculo de porcentagens e representação fracionária", "intermediario", 3),
    ("EF05MA07", "5º ano", "Matemática", "Números", "Operações", "Resolver e elaborar problemas de adição e subtração com números naturais e com números racionais, cuja representação decimal seja finita, utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.", "Problemas: adição e subtração de números naturais e números racionais cuja representação decimal é finita", "intermediario", 3),
    ("EF05MA08", "5º ano", "Matemática", "Números e Álgebra", "Operações", "Resolver e elaborar problemas de multiplicação e divisão com números naturais e com números racionais cuja representação decimal seja finita (com multiplicador natural e divisor natural e diferente de zero), utilizando estratégias diversas, como cálculo por estimativa, cálculo mental e algoritmos.", "Problemas: multiplicação e divisão de números racionais cuja representação decimal é finita por números naturais", "avancado", 3),
    ("EF05MA09", "5º ano", "Matemática", "Números", "Operações", "Resolver e elaborar problemas simples de contagem envolvendo o princípio multiplicativo, como a determinação do número de agrupamentos possíveis ao se combinar cada elemento de uma coleção com todos os elementos de outra coleção, por meio de diagramas de árvore ou por tabelas.", "Problemas de contagem do tipo: Se cada expression tiver expression escolhas, de quantas maneiras expression?", "avancado", 4),
    ("EF05MA17", "5º ano", "Matemática", "Geometria", "Formas Geométricas", "Reconhecer, nomear e comparar polígonos, considerando lados, vértices e ângulos, e desenhá-los, utilizando material de desenho ou tecnologias digitais.", "Figuras geométricas planas: características, representações e ângulos", "fundamental", 1),
]

# Dados da BNCC - Língua Portuguesa Anos Iniciais
BNCC_PORTUGUES = [
    # 1º ANO
    ("EF01LP01", "1º ano", "Língua Portuguesa", "Leitura/escuta", "Alfabetização", "Reconhecer que textos são lidos e escritos da esquerda para a direita e de cima para baixo da página.", "Protocolos de leitura", "fundamental", 1),
    ("EF01LP02", "1º ano", "Língua Portuguesa", "Leitura/escuta", "Alfabetização", "Escrever, espontaneamente ou por ditado, palavras e frases de forma alfabética – usando letras/grafemas que representem fonemas.", "Correspondência fonema-grafema", "fundamental", 1),
    ("EF01LP03", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Observar escritas convencionais, comparando-as às suas produções escritas, percebendo semelhanças e diferenças.", "Construção do sistema alfabético e da ortografia", "fundamental", 2),
    ("EF01LP04", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Distinguir as letras do alfabeto de outros sinais gráficos.", "Conhecimento do alfabeto do português do Brasil", "fundamental", 1),
    ("EF01LP05", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Reconhecer o sistema de escrita alfabética como representação dos sons da fala.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF01LP06", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Segmentar oralmente palavras em sílabas.", "Segmentação de palavras e consciência silábica", "fundamental", 2),
    ("EF01LP07", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Identificar fonemas e sua representação por letras.", "Correspondência fonema-grafema", "intermediario", 3),
    ("EF01LP08", "1º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Relacionar elementos sonoros (sílabas, fonemas, partes de palavras) com sua representação escrita.", "Construção do sistema alfabético e da ortografia", "intermediario", 3),
    
    # 2º ANO
    ("EF02LP01", "2º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Utilizar, ao produzir o texto, grafia correta de palavras conhecidas ou com estruturas silábicas já dominadas, letras maiúsculas em início de frases e em substantivos próprios, segmentação entre as palavras, ponto final, ponto de interrogação e ponto de exclamação.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF02LP02", "2º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Segmentar palavras em sílabas e remover e substituir sílabas iniciais, mediais ou finais para criar novas palavras.", "Construção do sistema alfabético e da ortografia", "intermediario", 2),
    ("EF02LP03", "2º ano", "Língua Portuguesa", "Análise linguística", "Alfabetização", "Ler e escrever palavras com correspondências regulares diretas entre letras e fonemas (f, v, t, d, p, b) e correspondências regulares contextuais (c e q; e e o, em posição átona em final de palavra).", "Construção do sistema alfabético e da ortografia", "intermediario", 2),
    ("EF02LP04", "2º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, identificando que existem vogais em todas as sílabas.", "Construção do sistema alfabético e da ortografia", "intermediario", 3),
    
    # 3º ANO
    ("EF03LP01", "3º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever palavras com correspondências regulares contextuais entre grafemas e fonemas – c/qu; g/gu; r/rr; s/ss; o (e não u) e e (e não i) em sílaba átona em final de palavra – e com marcas de nasalidade (til, m, n).", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF03LP02", "3º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever corretamente palavras com sílabas CV, V, CVC, CCV, VC, VV, CVV, identificando que existem vogais em todas as sílabas.", "Construção do sistema alfabético e da ortografia", "intermediario", 2),
    ("EF03LP03", "3º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever corretamente palavras com os dígrafos lh, nh, ch.", "Construção do sistema alfabético e da ortografia", "intermediario", 2),
    
    # 4º ANO
    ("EF04LP01", "4º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Grafar palavras utilizando regras de correspondência fonema-grafema regulares diretas e contextuais.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF04LP02", "4º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever, corretamente, palavras com sílabas VV e CVV em casos nos quais a combinação VV (ditongo) é reduzida na língua oral (ai, ei, ou).", "Construção do sistema alfabético e da ortografia", "intermediario", 2),
    
    # 5º ANO
    ("EF05LP01", "5º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Grafar palavras utilizando regras de correspondência fonema-grafema regulares, contextuais e morfológicas e palavras de uso frequente com correspondências irregulares.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF05LP02", "5º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Identificar o caráter polissêmico das palavras (uma mesma palavra com diferentes significados, de acordo com o contexto de uso), comparando o significado de determinados termos utilizados nas áreas científicas com esses mesmos termos utilizados na linguagem usual.", "Conhecimento das diversas grafias do alfabeto/Acentuação", "avancado", 2),
    ("EF05LP03", "5º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Acentuar corretamente palavras oxítonas, paroxítonas e proparoxítonas.", "Conhecimento das diversas grafias do alfabeto/Acentuação", "avancado", 3),
]

# Mapeamentos de pré-requisitos
PREREQUISITOS = [
    ("EF02MA01", "Comparar e ordenar números até centenas", "2º ano", "EF01MA03", "Estimar e comparar quantidades", "1º ano", True, 1.0),
    ("EF02MA05", "Fatos básicos adição e subtração", "2º ano", "EF01MA06", "Fatos básicos da adição", "1º ano", True, 1.0),
    ("EF03MA01", "Ler e escrever até milhar", "3º ano", "EF02MA01", "Comparar e ordenar até centenas", "2º ano", True, 1.0),
    ("EF03MA07", "Multiplicação", "3º ano", "EF02MA07", "Problemas de multiplicação por 2,3,4,5", "2º ano", True, 1.0),
    ("EF04MA09", "Frações unitárias", "4º ano", "EF03MA09", "Ideias de metade, terça, quarta parte", "3º ano", True, 1.0),
    ("EF05MA03", "Representar frações", "5º ano", "EF04MA09", "Frações unitárias", "4º ano", True, 1.0),
    ("EF05MA08", "Frações - Adição e Subtração", "5º ano", "EF04MA09", "Reconhecer frações", "4º ano", True, 1.0),
    ("EF05MA08", "Frações - Adição e Subtração", "5º ano", "EF04MA10", "Representar frações decimais", "4º ano", True, 1.0),
    ("EF05MA08", "Frações - Adição e Subtração", "5º ano", "EF03MA09", "Noção de fração", "3º ano", True, 0.8),
    ("EF02LP01", "Grafia correta palavras conhecidas", "2º ano", "EF01LP02", "Escrever palavras e frases", "1º ano", True, 1.0),
    ("EF03LP01", "Correspondências regulares contextuais", "3º ano", "EF02LP03", "Ler e escrever palavras regulares", "2º ano", True, 1.0),
    ("EF05LP01", "Regras fonema-grafema", "5º ano", "EF04LP01", "Grafar palavras regulares", "4º ano", True, 1.0),
]


def importar_bncc():
    """Importa os dados da BNCC para o banco de dados usando SQL direto"""
    
    print("=" * 60)
    print("📚 IMPORTANDO BNCC - BASE NACIONAL COMUM CURRICULAR")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Verificar se a tabela existe
        result = conn.execute(text("SHOW TABLES LIKE 'curriculo_nacional'"))
        if not result.fetchone():
            print("\n❌ ERRO: Tabela 'curriculo_nacional' não existe!")
            print("   Execute primeiro: python criar_tabelas_bncc.py")
            return
        
        # Verificar se já existem dados
        result = conn.execute(text("SELECT COUNT(*) FROM curriculo_nacional"))
        count = result.scalar()
        
        if count > 10:
            print(f"⚠️  Já existem {count} habilidades no banco. Pulando importação duplicada.")
            print("    Se quiser reimportar, limpe a tabela curriculo_nacional primeiro.")
            return
        
        # Importar Matemática
        print("\n📐 Importando Matemática...")
        for item in BNCC_MATEMATICA:
            try:
                # Verificar se já existe
                result = conn.execute(
                    text("SELECT id FROM curriculo_nacional WHERE codigo_bncc = :codigo"),
                    {"codigo": item[0]}
                )
                if result.fetchone():
                    continue
                
                conn.execute(
                    text("""
                        INSERT INTO curriculo_nacional 
                        (codigo_bncc, ano_escolar, componente, campo_experiencia, eixo_tematico, 
                         habilidade_descricao, objeto_conhecimento, dificuldade, trimestre_sugerido, habilidade_codigo)
                        VALUES (:codigo, :ano, :comp, :campo, :eixo, :hab, :obj, :dif, :tri, :hab_cod)
                    """),
                    {
                        "codigo": item[0],
                        "ano": item[1],
                        "comp": item[2],
                        "campo": item[3],
                        "eixo": item[4],
                        "hab": item[5],
                        "obj": item[6],
                        "dif": item[7],
                        "tri": item[8],
                        "hab_cod": item[0]
                    }
                )
                conn.commit()
                print(f"   ✅ {item[0]} - {item[1]}")
            except Exception as e:
                print(f"   ⚠️  {item[0]}: {e}")
        
        # Importar Português
        print("\n📖 Importando Língua Portuguesa...")
        for item in BNCC_PORTUGUES:
            try:
                result = conn.execute(
                    text("SELECT id FROM curriculo_nacional WHERE codigo_bncc = :codigo"),
                    {"codigo": item[0]}
                )
                if result.fetchone():
                    continue
                
                conn.execute(
                    text("""
                        INSERT INTO curriculo_nacional 
                        (codigo_bncc, ano_escolar, componente, campo_experiencia, eixo_tematico, 
                         habilidade_descricao, objeto_conhecimento, dificuldade, trimestre_sugerido, habilidade_codigo)
                        VALUES (:codigo, :ano, :comp, :campo, :eixo, :hab, :obj, :dif, :tri, :hab_cod)
                    """),
                    {
                        "codigo": item[0],
                        "ano": item[1],
                        "comp": item[2],
                        "campo": item[3],
                        "eixo": item[4],
                        "hab": item[5],
                        "obj": item[6],
                        "dif": item[7],
                        "tri": item[8],
                        "hab_cod": item[0]
                    }
                )
                conn.commit()
                print(f"   ✅ {item[0]} - {item[1]}")
            except Exception as e:
                print(f"   ⚠️  {item[0]}: {e}")
        
        # Importar pré-requisitos
        print("\n🔗 Importando mapeamento de pré-requisitos...")
        for item in PREREQUISITOS:
            try:
                result = conn.execute(
                    text("""
                        SELECT id FROM mapeamento_prerequisitos 
                        WHERE habilidade_codigo = :hab AND prerequisito_codigo = :pre
                    """),
                    {"hab": item[0], "pre": item[3]}
                )
                if result.fetchone():
                    continue
                
                conn.execute(
                    text("""
                        INSERT INTO mapeamento_prerequisitos 
                        (habilidade_codigo, habilidade_titulo, ano_escolar, 
                         prerequisito_codigo, prerequisito_titulo, ano_prerequisito, essencial, peso)
                        VALUES (:hab_cod, :hab_tit, :ano, :pre_cod, :pre_tit, :pre_ano, :ess, :peso)
                    """),
                    {
                        "hab_cod": item[0],
                        "hab_tit": item[1],
                        "ano": item[2],
                        "pre_cod": item[3],
                        "pre_tit": item[4],
                        "pre_ano": item[5],
                        "ess": item[6],
                        "peso": item[7]
                    }
                )
                conn.commit()
                print(f"   ✅ {item[0]} <- {item[3]}")
            except Exception as e:
                print(f"   ⚠️  {item[0]}: {e}")
        
        # Contar resultados
        result = conn.execute(text("SELECT COUNT(*) FROM curriculo_nacional"))
        total_curriculo = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM mapeamento_prerequisitos"))
        total_prereqs = result.scalar()
        
        print("\n" + "=" * 60)
        print("✅ IMPORTAÇÃO CONCLUÍDA!")
        print("=" * 60)
        print(f"📚 Total de habilidades: {total_curriculo}")
        print(f"🔗 Total de pré-requisitos: {total_prereqs}")
        
        # Por componente
        print("\nPor componente:")
        for comp in ["Matemática", "Língua Portuguesa"]:
            result = conn.execute(
                text("SELECT COUNT(*) FROM curriculo_nacional WHERE componente = :comp"),
                {"comp": comp}
            )
            count = result.scalar()
            print(f"   • {comp}: {count}")
        
        # Por ano escolar
        print("\nPor ano escolar:")
        for ano in ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano"]:
            result = conn.execute(
                text("SELECT COUNT(*) FROM curriculo_nacional WHERE ano_escolar = :ano"),
                {"ano": ano}
            )
            count = result.scalar()
            print(f"   • {ano}: {count}")


if __name__ == "__main__":
    importar_bncc()
