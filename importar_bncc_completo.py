# ============================================
# Script de Importação COMPLETA da BNCC
# Todos os Componentes - Anos Iniciais (1º ao 5º)
# AdaptAI - Planejamento Curricular
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

# Criar engine diretamente
engine = create_engine(settings.db_url, echo=False)

# ============================================
# MATEMÁTICA - Anos Iniciais
# ============================================
BNCC_MATEMATICA = [
    # 1º ANO
    ("EF01MA01", "1º ano", "Matemática", "Números", "Contagem", "Utilizar números naturais como indicador de quantidade ou de ordem em diferentes situações cotidianas.", "Contagem de rotina", "fundamental", 1),
    ("EF01MA02", "1º ano", "Matemática", "Números", "Contagem", "Contar de maneira exata ou aproximada, utilizando diferentes estratégias como o pareamento.", "Quantificação de elementos", "fundamental", 1),
    ("EF01MA03", "1º ano", "Matemática", "Números", "Escrita numérica", "Estimar e comparar quantidades de objetos de dois conjuntos.", "Leitura, escrita e comparação de números naturais", "fundamental", 1),
    ("EF01MA04", "1º ano", "Matemática", "Números", "Operações", "Contar a quantidade de objetos de coleções até 100 unidades.", "Leitura, escrita e comparação de números naturais", "fundamental", 2),
    ("EF01MA05", "1º ano", "Matemática", "Números", "Operações", "Comparar números naturais de até duas ordens em situações cotidianas.", "Reta numérica", "fundamental", 2),
    ("EF01MA06", "1º ano", "Matemática", "Números", "Operações", "Construir fatos básicos da adição e utilizá-los em procedimentos de cálculo.", "Construção de fatos fundamentais da adição", "intermediario", 3),
    ("EF01MA07", "1º ano", "Matemática", "Números", "Operações", "Compor e decompor número de até duas ordens.", "Composição e decomposição de números naturais", "intermediario", 3),
    ("EF01MA08", "1º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas de adição e de subtração.", "Problemas de adição e subtração", "intermediario", 4),
    
    # 2º ANO
    ("EF02MA01", "2º ano", "Matemática", "Números", "Leitura e escrita", "Comparar e ordenar números naturais até a ordem de centenas.", "Leitura, escrita, comparação e ordenação", "fundamental", 1),
    ("EF02MA02", "2º ano", "Matemática", "Números", "Operações", "Fazer estimativas sobre quantidade de objetos.", "Leitura, escrita, comparação e ordenação", "fundamental", 1),
    ("EF02MA03", "2º ano", "Matemática", "Números", "Composição", "Comparar quantidades de objetos de dois conjuntos.", "Composição e decomposição", "fundamental", 2),
    ("EF02MA04", "2º ano", "Matemática", "Números", "Composição", "Compor e decompor números naturais de até três ordens.", "Composição e decomposição", "intermediario", 2),
    ("EF02MA05", "2º ano", "Matemática", "Números", "Operações", "Construir fatos básicos da adição e subtração.", "Fatos fundamentais da adição e subtração", "intermediario", 3),
    ("EF02MA06", "2º ano", "Matemática", "Números", "Problemas", "Resolver e elaborar problemas de adição e de subtração.", "Problemas de adição e subtração", "intermediario", 3),
    ("EF02MA07", "2º ano", "Matemática", "Números", "Multiplicação", "Resolver problemas de multiplicação por 2, 3, 4 e 5.", "Adição de parcelas iguais", "avancado", 4),
    
    # 3º ANO
    ("EF03MA01", "3º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e comparar números até a unidade de milhar.", "Números naturais de quatro ordens", "fundamental", 1),
    ("EF03MA02", "3º ano", "Matemática", "Números", "Composição", "Identificar características do sistema de numeração decimal.", "Composição e decomposição", "fundamental", 1),
    ("EF03MA03", "3º ano", "Matemática", "Números", "Operações", "Construir e utilizar fatos básicos da adição e multiplicação.", "Fatos fundamentais", "intermediario", 2),
    ("EF03MA04", "3º ano", "Matemática", "Números", "Algoritmos", "Estabelecer relação entre números naturais e pontos da reta numérica.", "Reta numérica", "intermediario", 2),
    ("EF03MA05", "3º ano", "Matemática", "Números", "Algoritmos", "Utilizar diferentes procedimentos de cálculo mental e escrito.", "Procedimentos de cálculo", "intermediario", 3),
    ("EF03MA06", "3º ano", "Matemática", "Números", "Problemas", "Resolver problemas de adição e subtração com diferentes significados.", "Problemas de adição e subtração", "intermediario", 3),
    ("EF03MA07", "3º ano", "Matemática", "Números", "Multiplicação", "Resolver problemas de multiplicação por 2, 3, 4, 5 e 10.", "Significados da multiplicação", "avancado", 4),
    ("EF03MA08", "3º ano", "Matemática", "Números", "Divisão", "Resolver problemas de divisão com números até 10.", "Significados da divisão", "avancado", 4),
    ("EF03MA09", "3º ano", "Matemática", "Números", "Frações", "Associar quocientes às ideias de metade, terça, quarta parte.", "Frações básicas", "avancado", 4),
    
    # 4º ANO
    ("EF04MA01", "4º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números até dezenas de milhar.", "Sistema de numeração decimal", "fundamental", 1),
    ("EF04MA02", "4º ano", "Matemática", "Números", "Composição", "Mostrar que todo número pode ser escrito por adições e multiplicações.", "Composição e decomposição", "intermediario", 1),
    ("EF04MA03", "4º ano", "Matemática", "Números", "Operações", "Resolver problemas com números naturais envolvendo adição e subtração.", "Propriedades das operações", "intermediario", 2),
    ("EF04MA04", "4º ano", "Matemática", "Números", "Multiplicação", "Utilizar relações entre operações para ampliar estratégias de cálculo.", "Propriedades das operações", "intermediario", 2),
    ("EF04MA05", "4º ano", "Matemática", "Números", "Multiplicação", "Utilizar as propriedades das operações para desenvolver estratégias.", "Propriedades das operações", "intermediario", 3),
    ("EF04MA06", "4º ano", "Matemática", "Números", "Problemas", "Resolver problemas de multiplicação com diferentes significados.", "Problemas de multiplicação e divisão", "intermediario", 3),
    ("EF04MA07", "4º ano", "Matemática", "Números", "Divisão", "Resolver problemas de divisão com divisor de até dois algarismos.", "Problemas de multiplicação e divisão", "avancado", 4),
    ("EF04MA09", "4º ano", "Matemática", "Números", "Frações", "Reconhecer frações unitárias mais usuais.", "Números racionais: frações unitárias", "intermediario", 3),
    ("EF04MA10", "4º ano", "Matemática", "Números", "Frações", "Reconhecer regras do sistema de numeração decimal para representação decimal.", "Representação decimal", "intermediario", 4),
    
    # 5º ANO
    ("EF05MA01", "5º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números até centenas de milhar.", "Sistema de numeração decimal", "fundamental", 1),
    ("EF05MA02", "5º ano", "Matemática", "Números", "Leitura e escrita", "Ler, escrever e ordenar números racionais na forma decimal.", "Números racionais decimais", "intermediario", 1),
    ("EF05MA03", "5º ano", "Matemática", "Números", "Frações", "Identificar e representar frações menores e maiores que a unidade.", "Representação fracionária", "intermediario", 2),
    ("EF05MA04", "5º ano", "Matemática", "Números", "Frações", "Identificar frações equivalentes.", "Comparação e ordenação de números racionais", "intermediario", 2),
    ("EF05MA05", "5º ano", "Matemática", "Números", "Frações", "Comparar e ordenar números racionais positivos.", "Comparação e ordenação de números racionais", "intermediario", 2),
    ("EF05MA06", "5º ano", "Matemática", "Números", "Frações", "Associar representações de porcentagem às frações.", "Cálculo de porcentagens", "intermediario", 3),
    ("EF05MA07", "5º ano", "Matemática", "Números", "Operações", "Resolver problemas de adição e subtração com números naturais e racionais.", "Problemas de adição e subtração", "intermediario", 3),
    ("EF05MA08", "5º ano", "Matemática", "Números", "Operações", "Resolver problemas de multiplicação e divisão com números racionais.", "Problemas de multiplicação e divisão", "avancado", 3),
    ("EF05MA09", "5º ano", "Matemática", "Números", "Operações", "Resolver problemas simples de contagem envolvendo o princípio multiplicativo.", "Problemas de contagem", "avancado", 4),
]

# ============================================
# LÍNGUA PORTUGUESA - Anos Iniciais
# ============================================
BNCC_PORTUGUES = [
    # 1º ANO
    ("EF01LP01", "1º ano", "Língua Portuguesa", "Leitura/escuta", "Protocolos de leitura", "Reconhecer que textos são lidos e escritos da esquerda para a direita.", "Protocolos de leitura", "fundamental", 1),
    ("EF01LP02", "1º ano", "Língua Portuguesa", "Escrita", "Correspondência fonema-grafema", "Escrever, espontaneamente ou por ditado, palavras e frases de forma alfabética.", "Correspondência fonema-grafema", "fundamental", 1),
    ("EF01LP03", "1º ano", "Língua Portuguesa", "Escrita", "Construção do sistema alfabético", "Observar escritas convencionais, comparando-as às suas produções.", "Construção do sistema alfabético", "fundamental", 2),
    ("EF01LP04", "1º ano", "Língua Portuguesa", "Análise linguística", "Conhecimento do alfabeto", "Distinguir as letras do alfabeto de outros sinais gráficos.", "Conhecimento do alfabeto", "fundamental", 1),
    ("EF01LP05", "1º ano", "Língua Portuguesa", "Análise linguística", "Sistema alfabético", "Reconhecer o sistema de escrita alfabética.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF01LP06", "1º ano", "Língua Portuguesa", "Análise linguística", "Segmentação", "Segmentar oralmente palavras em sílabas.", "Segmentação de palavras", "fundamental", 2),
    ("EF01LP07", "1º ano", "Língua Portuguesa", "Análise linguística", "Correspondência fonema-grafema", "Identificar fonemas e sua representação por letras.", "Correspondência fonema-grafema", "intermediario", 3),
    ("EF01LP08", "1º ano", "Língua Portuguesa", "Análise linguística", "Construção do sistema alfabético", "Relacionar elementos sonoros com sua representação escrita.", "Construção do sistema alfabético", "intermediario", 3),
    
    # 2º ANO
    ("EF02LP01", "2º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Utilizar grafia correta de palavras conhecidas.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF02LP02", "2º ano", "Língua Portuguesa", "Análise linguística", "Segmentação", "Segmentar palavras em sílabas e remover ou substituir sílabas.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF02LP03", "2º ano", "Língua Portuguesa", "Análise linguística", "Correspondência fonema-grafema", "Ler e escrever palavras com correspondências regulares diretas.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF02LP04", "2º ano", "Língua Portuguesa", "Análise linguística", "Estrutura silábica", "Ler e escrever palavras com sílabas CV, V, CVC, CCV.", "Construção do sistema alfabético", "intermediario", 3),
    
    # 3º ANO
    ("EF03LP01", "3º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever palavras com correspondências regulares contextuais.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF03LP02", "3º ano", "Língua Portuguesa", "Análise linguística", "Estrutura silábica", "Ler e escrever palavras com sílabas CV, V, CVC, CCV, VC, VV, CVV.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF03LP03", "3º ano", "Língua Portuguesa", "Análise linguística", "Dígrafos", "Ler e escrever palavras com os dígrafos lh, nh, ch.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF03LP04", "3º ano", "Língua Portuguesa", "Análise linguística", "Acentuação", "Usar acento gráfico em monossílabos tônicos e oxítonas.", "Acentuação", "avancado", 3),
    
    # 4º ANO
    ("EF04LP01", "4º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Grafar palavras utilizando regras de correspondência fonema-grafema.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF04LP02", "4º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Ler e escrever palavras com sílabas VV e CVV.", "Construção do sistema alfabético", "intermediario", 2),
    ("EF04LP04", "4º ano", "Língua Portuguesa", "Análise linguística", "Acentuação", "Usar acento gráfico em paroxítonas terminadas em -i(s), -l, -r, -ão(s).", "Acentuação", "avancado", 3),
    ("EF04LP05", "4º ano", "Língua Portuguesa", "Análise linguística", "Pontuação", "Identificar a função e usar adequadamente pontuação.", "Pontuação", "intermediario", 3),
    
    # 5º ANO
    ("EF05LP01", "5º ano", "Língua Portuguesa", "Análise linguística", "Ortografia", "Grafar palavras utilizando regras regulares, contextuais e morfológicas.", "Construção do sistema alfabético e da ortografia", "intermediario", 1),
    ("EF05LP02", "5º ano", "Língua Portuguesa", "Análise linguística", "Polissemia", "Identificar o caráter polissêmico das palavras.", "Acentuação", "avancado", 2),
    ("EF05LP03", "5º ano", "Língua Portuguesa", "Análise linguística", "Acentuação", "Acentuar corretamente palavras oxítonas, paroxítonas e proparoxítonas.", "Acentuação", "avancado", 3),
    ("EF05LP04", "5º ano", "Língua Portuguesa", "Análise linguística", "Pontuação", "Diferenciar vírgula, ponto e vírgula, dois-pontos.", "Pontuação", "avancado", 3),
]

# ============================================
# EDUCAÇÃO FÍSICA - Anos Iniciais
# ============================================
BNCC_EDUCACAO_FISICA = [
    # 1º e 2º ANO
    ("EF12EF01", "1º e 2º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras da cultura popular", "Experimentar, fruir e recriar diferentes brincadeiras e jogos da cultura popular.", "Brincadeiras e jogos da cultura popular", "fundamental", 1),
    ("EF12EF02", "1º e 2º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras da cultura popular", "Explicar as brincadeiras e os jogos populares do contexto comunitário e regional.", "Brincadeiras e jogos da cultura popular", "fundamental", 2),
    ("EF12EF03", "1º e 2º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras da cultura popular", "Planejar e utilizar estratégias para resolver desafios de brincadeiras e jogos populares.", "Brincadeiras e jogos da cultura popular", "intermediario", 2),
    ("EF12EF04", "1º e 2º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras da cultura popular", "Colaborar na produção de alternativas para a prática de brincadeiras e jogos.", "Brincadeiras e jogos da cultura popular", "intermediario", 3),
    ("EF12EF05", "1º e 2º ano", "Educação Física", "Esportes", "Esportes de marca e precisão", "Experimentar e fruir a prática de esportes de marca e de precisão.", "Esportes de marca", "fundamental", 3),
    ("EF12EF06", "1º e 2º ano", "Educação Física", "Esportes", "Esportes de marca e precisão", "Discutir a importância das normas e das regras dos esportes.", "Esportes de precisão", "fundamental", 3),
    ("EF12EF07", "1º e 2º ano", "Educação Física", "Ginásticas", "Ginástica geral", "Experimentar e identificar diferentes elementos básicos da ginástica.", "Ginástica geral", "fundamental", 2),
    ("EF12EF08", "1º e 2º ano", "Educação Física", "Ginásticas", "Ginástica geral", "Planejar e utilizar estratégias para a execução de elementos básicos da ginástica.", "Ginástica geral", "intermediario", 3),
    ("EF12EF09", "1º e 2º ano", "Educação Física", "Ginásticas", "Ginástica geral", "Participar da ginástica geral, respeitando as diferenças individuais.", "Ginástica geral", "fundamental", 3),
    ("EF12EF10", "1º e 2º ano", "Educação Física", "Danças", "Danças do contexto comunitário", "Experimentar, fruir e identificar elementos constitutivos das danças.", "Danças do contexto comunitário", "fundamental", 3),
    ("EF12EF11", "1º e 2º ano", "Educação Física", "Danças", "Danças do contexto comunitário", "Experimentar diferentes danças do contexto comunitário e regional.", "Danças do contexto comunitário", "fundamental", 4),
    ("EF12EF12", "1º e 2º ano", "Educação Física", "Danças", "Danças do contexto comunitário", "Identificar os elementos constitutivos das danças do contexto comunitário.", "Danças do contexto comunitário", "intermediario", 4),
    
    # 3º ao 5º ANO
    ("EF35EF01", "3º ao 5º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras e jogos do Brasil e do mundo", "Experimentar e fruir brincadeiras e jogos populares do Brasil e do mundo.", "Brincadeiras e jogos populares do Brasil e do mundo", "fundamental", 1),
    ("EF35EF02", "3º ao 5º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras e jogos do Brasil e do mundo", "Planejar e utilizar estratégias para possibilitar a participação segura de todos.", "Brincadeiras e jogos populares do Brasil e do mundo", "intermediario", 2),
    ("EF35EF03", "3º ao 5º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras e jogos do Brasil e do mundo", "Descrever as brincadeiras e os jogos populares, explicando suas características.", "Brincadeiras e jogos populares do Brasil e do mundo", "intermediario", 2),
    ("EF35EF04", "3º ao 5º ano", "Educação Física", "Brincadeiras e jogos", "Brincadeiras e jogos do Brasil e do mundo", "Recriar e propor novas brincadeiras e jogos.", "Brincadeiras e jogos populares do Brasil e do mundo", "intermediario", 3),
    ("EF35EF05", "3º ao 5º ano", "Educação Física", "Esportes", "Esportes de campo e taco, rede/parede e invasão", "Experimentar diversos tipos de esportes de campo e taco, rede/parede e invasão.", "Esportes de campo e taco", "intermediario", 3),
    ("EF35EF06", "3º ao 5º ano", "Educação Física", "Esportes", "Esportes de campo e taco, rede/parede e invasão", "Diferenciar os conceitos de jogo e esporte.", "Esportes de rede/parede", "intermediario", 3),
    ("EF35EF07", "3º ao 5º ano", "Educação Física", "Ginásticas", "Ginástica geral", "Experimentar e fruir combinações de diferentes elementos da ginástica geral.", "Ginástica geral", "intermediario", 3),
    ("EF35EF08", "3º ao 5º ano", "Educação Física", "Ginásticas", "Ginástica geral", "Planejar e utilizar estratégias para resolver desafios na ginástica geral.", "Ginástica geral", "intermediario", 4),
    ("EF35EF09", "3º ao 5º ano", "Educação Física", "Danças", "Danças do Brasil e do mundo", "Experimentar, recriar e fruir danças populares do Brasil e do mundo.", "Danças do Brasil e do mundo", "fundamental", 3),
    ("EF35EF10", "3º ao 5º ano", "Educação Física", "Danças", "Danças do Brasil e do mundo", "Comparar e identificar os elementos constitutivos das danças populares.", "Danças do Brasil e do mundo", "intermediario", 4),
    ("EF35EF11", "3º ao 5º ano", "Educação Física", "Danças", "Danças do Brasil e do mundo", "Formular e utilizar estratégias para a execução de elementos das danças.", "Danças do Brasil e do mundo", "intermediario", 4),
    ("EF35EF12", "3º ao 5º ano", "Educação Física", "Lutas", "Lutas do contexto comunitário", "Experimentar, fruir e recriar diferentes lutas presentes no contexto comunitário.", "Lutas do contexto comunitário", "intermediario", 3),
    ("EF35EF13", "3º ao 5º ano", "Educação Física", "Lutas", "Lutas de matriz indígena e africana", "Planejar e utilizar estratégias básicas das lutas.", "Lutas de matriz indígena e africana", "intermediario", 4),
    ("EF35EF14", "3º ao 5º ano", "Educação Física", "Lutas", "Lutas de matriz indígena e africana", "Identificar as características das lutas.", "Lutas de matriz indígena e africana", "intermediario", 4),
    ("EF35EF15", "3º ao 5º ano", "Educação Física", "Práticas corporais de aventura", "Práticas corporais de aventura urbanas", "Experimentar práticas corporais de aventura urbanas.", "Práticas corporais de aventura urbanas", "avancado", 4),
]

# ============================================
# PRÉ-REQUISITOS EXPANDIDOS
# ============================================
PREREQUISITOS_EXPANDIDOS = [
    # Matemática
    ("EF02MA01", "Comparar e ordenar números até centenas", "2º ano", "EF01MA03", "Estimar e comparar quantidades", "1º ano", True, 1.0),
    ("EF02MA05", "Fatos básicos adição e subtração", "2º ano", "EF01MA06", "Fatos básicos da adição", "1º ano", True, 1.0),
    ("EF03MA01", "Ler e escrever até milhar", "3º ano", "EF02MA01", "Comparar e ordenar até centenas", "2º ano", True, 1.0),
    ("EF03MA07", "Multiplicação", "3º ano", "EF02MA07", "Problemas de multiplicação por 2,3,4,5", "2º ano", True, 1.0),
    ("EF04MA09", "Frações unitárias", "4º ano", "EF03MA09", "Ideias de metade, terça, quarta parte", "3º ano", True, 1.0),
    ("EF05MA03", "Representar frações", "5º ano", "EF04MA09", "Frações unitárias", "4º ano", True, 1.0),
    ("EF05MA08", "Operações com frações", "5º ano", "EF04MA09", "Reconhecer frações", "4º ano", True, 1.0),
    
    # Língua Portuguesa
    ("EF02LP01", "Grafia correta palavras conhecidas", "2º ano", "EF01LP02", "Escrever palavras e frases", "1º ano", True, 1.0),
    ("EF03LP01", "Correspondências regulares contextuais", "3º ano", "EF02LP03", "Ler e escrever palavras regulares", "2º ano", True, 1.0),
    ("EF04LP01", "Grafar palavras regulares", "4º ano", "EF03LP01", "Correspondências contextuais", "3º ano", True, 1.0),
    ("EF05LP01", "Regras fonema-grafema", "5º ano", "EF04LP01", "Grafar palavras regulares", "4º ano", True, 1.0),
    ("EF05LP03", "Acentuação", "5º ano", "EF04LP04", "Acentuação paroxítonas", "4º ano", True, 1.0),
    
    # Ciências
    ("EF02CI04", "Plantas e animais", "2º ano", "EF01CI02", "Corpo humano", "1º ano", True, 0.8),
    ("EF03CI04", "Características dos animais", "3º ano", "EF02CI04", "Plantas e animais", "2º ano", True, 1.0),
    ("EF04CI04", "Cadeias alimentares", "4º ano", "EF03CI04", "Características dos animais", "3º ano", True, 1.0),
    ("EF05CI06", "Nutrição", "5º ano", "EF04CI04", "Cadeias alimentares", "4º ano", True, 0.9),
    
    # História
    ("EF02HI01", "Comunidade", "2º ano", "EF01HI02", "Família", "1º ano", True, 1.0),
    ("EF03HI01", "Cidade e município", "3º ano", "EF02HI01", "Comunidade", "2º ano", True, 1.0),
    ("EF04HI01", "Migrações", "4º ano", "EF03HI01", "Cidade e município", "3º ano", True, 0.9),
    ("EF05HI01", "Formação cultural", "5º ano", "EF04HI01", "Migrações", "4º ano", True, 1.0),
    
    # Geografia
    ("EF02GE01", "Convivência", "2º ano", "EF01GE01", "Identidade", "1º ano", True, 1.0),
    ("EF03GE01", "Cidade e campo", "3º ano", "EF02GE01", "Convivência", "2º ano", True, 1.0),
    ("EF04GE01", "Território", "4º ano", "EF03GE01", "Cidade e campo", "3º ano", True, 1.0),
    ("EF05GE01", "Dinâmicas populacionais", "5º ano", "EF04GE01", "Território", "4º ano", True, 1.0),
]

# ============================================
# CIÊNCIAS - Anos Iniciais (dados inline para evitar arquivo muito grande)
# ============================================
BNCC_CIENCIAS = [
    # 1º ANO
    ("EF01CI01", "1º ano", "Ciências", "Matéria e Energia", "Características dos materiais", "Comparar características de diferentes materiais presentes em objetos de uso cotidiano, discutindo sua origem, os modos como são descartados e como podem ser usados de forma mais consciente.", "Características dos materiais", "fundamental", 1),
    ("EF01CI02", "1º ano", "Ciências", "Vida e Evolução", "Corpo humano", "Localizar, nomear e representar graficamente (por meio de desenhos) partes do corpo humano e explicar suas funções.", "Corpo humano", "fundamental", 2),
    ("EF01CI03", "1º ano", "Ciências", "Vida e Evolução", "Higiene e saúde", "Discutir as razões pelas quais os hábitos de higiene do corpo são necessários para a manutenção da saúde.", "Respeito à diversidade", "fundamental", 2),
    ("EF01CI04", "1º ano", "Ciências", "Vida e Evolução", "Diversidade", "Comparar características físicas entre os colegas, reconhecendo a diversidade e a importância da valorização, do acolhimento e do respeito às diferenças.", "Respeito à diversidade", "fundamental", 3),
    ("EF01CI05", "1º ano", "Ciências", "Terra e Universo", "Escalas de tempo", "Identificar e nomear diferentes escalas de tempo: os períodos diários (manhã, tarde, noite) e a sucessão de dias, semanas, meses e anos.", "Escalas de tempo", "fundamental", 3),
    ("EF01CI06", "1º ano", "Ciências", "Terra e Universo", "Movimentos do Sol", "Selecionar exemplos de como a sucessão de dias e noites orienta o ritmo de atividades diárias de seres humanos e de outros seres vivos.", "Escalas de tempo", "intermediario", 4),
    
    # 2º ANO
    ("EF02CI01", "2º ano", "Ciências", "Matéria e Energia", "Propriedades dos materiais", "Identificar de que materiais (metais, madeira, vidro etc.) são feitos os objetos que fazem parte da vida cotidiana.", "Propriedades e usos dos materiais", "fundamental", 1),
    ("EF02CI02", "2º ano", "Ciências", "Matéria e Energia", "Transformações", "Propor o uso de diferentes materiais para a construção de objetos de uso cotidiano, tendo em vista algumas propriedades desses materiais.", "Propriedades e usos dos materiais", "intermediario", 2),
    ("EF02CI03", "2º ano", "Ciências", "Matéria e Energia", "Prevenção de acidentes", "Discutir os cuidados necessários à prevenção de acidentes domésticos.", "Prevenção de acidentes domésticos", "fundamental", 2),
    ("EF02CI04", "2º ano", "Ciências", "Vida e Evolução", "Plantas e animais", "Descrever características de plantas e animais que fazem parte de seu cotidiano e relacioná-las ao ambiente em que eles vivem.", "Seres vivos no ambiente", "fundamental", 3),
    ("EF02CI05", "2º ano", "Ciências", "Vida e Evolução", "Importância da água", "Investigar a importância da água e da luz para a manutenção da vida de plantas em geral.", "Plantas", "intermediario", 3),
    ("EF02CI06", "2º ano", "Ciências", "Vida e Evolução", "Partes das plantas", "Identificar as principais partes de uma planta (raiz, caule, folhas, flores e frutos) e a função desempenhada por cada uma delas.", "Plantas", "intermediario", 4),
    ("EF02CI07", "2º ano", "Ciências", "Terra e Universo", "Movimento do Sol", "Descrever as posições do Sol em diversos horários do dia e associá-las ao tamanho da sombra projetada.", "Movimento aparente do Sol no céu", "intermediario", 3),
    ("EF02CI08", "2º ano", "Ciências", "Terra e Universo", "Sol como fonte de luz", "Comparar o efeito da radiação solar em diferentes tipos de superfície.", "O Sol como fonte de luz e calor", "intermediario", 4),
    
    # 3º ANO
    ("EF03CI01", "3º ano", "Ciências", "Matéria e Energia", "Produção de som", "Produzir diferentes sons a partir da vibração de variados objetos e identificar variáveis que influem nesse fenômeno.", "Produção de som", "intermediario", 1),
    ("EF03CI02", "3º ano", "Ciências", "Matéria e Energia", "Propagação do som", "Experimentar e relatar o que ocorre com a propagação do som através de diferentes meios.", "Efeitos da luz nos materiais", "intermediario", 2),
    ("EF03CI03", "3º ano", "Ciências", "Matéria e Energia", "Saúde auditiva e visual", "Discutir hábitos necessários para a manutenção da saúde auditiva e visual.", "Saúde auditiva e visual", "fundamental", 2),
    ("EF03CI04", "3º ano", "Ciências", "Vida e Evolução", "Características dos animais", "Identificar características sobre o modo de vida dos animais mais comuns no ambiente próximo.", "Características e desenvolvimento dos animais", "fundamental", 3),
    ("EF03CI05", "3º ano", "Ciências", "Vida e Evolução", "Ciclo de vida", "Descrever e comunicar as alterações que ocorrem desde o nascimento em animais de diferentes meios terrestres ou aquáticos.", "Características e desenvolvimento dos animais", "intermediario", 3),
    ("EF03CI06", "3º ano", "Ciências", "Vida e Evolução", "Classificação", "Comparar alguns animais e organizar grupos com base em características externas comuns.", "Características e desenvolvimento dos animais", "intermediario", 4),
    ("EF03CI07", "3º ano", "Ciências", "Terra e Universo", "Características da Terra", "Identificar características da Terra (como seu formato esférico, a presença de água, solo etc.).", "Características da Terra", "fundamental", 3),
    ("EF03CI08", "3º ano", "Ciências", "Terra e Universo", "Observação do céu", "Observar, identificar e registrar os períodos diários em que o Sol, demais estrelas, Lua e planetas estão visíveis no céu.", "Observação do céu", "intermediario", 4),
    ("EF03CI09", "3º ano", "Ciências", "Terra e Universo", "Usos do solo", "Comparar diferentes amostras de solo do entorno da escola.", "Usos do solo", "intermediario", 4),
    ("EF03CI10", "3º ano", "Ciências", "Terra e Universo", "Importância do solo", "Identificar os diferentes usos do solo, reconhecendo sua importância para a agricultura e para a vida.", "Usos do solo", "intermediario", 4),
    
    # 4º ANO
    ("EF04CI01", "4º ano", "Ciências", "Matéria e Energia", "Misturas", "Identificar misturas na vida diária, com base em suas propriedades físicas observáveis.", "Misturas", "intermediario", 1),
    ("EF04CI02", "4º ano", "Ciências", "Matéria e Energia", "Transformações", "Testar e relatar transformações nos materiais do dia a dia quando expostos a diferentes condições.", "Transformações reversíveis e não reversíveis", "intermediario", 2),
    ("EF04CI03", "4º ano", "Ciências", "Matéria e Energia", "Reversibilidade", "Concluir que algumas mudanças causadas por aquecimento ou resfriamento são reversíveis e outras não.", "Transformações reversíveis e não reversíveis", "intermediario", 2),
    ("EF04CI04", "4º ano", "Ciências", "Vida e Evolução", "Cadeias alimentares", "Analisar e construir cadeias alimentares simples, reconhecendo a posição ocupada pelos seres vivos.", "Cadeias alimentares simples", "intermediario", 3),
    ("EF04CI05", "4º ano", "Ciências", "Vida e Evolução", "Ecossistemas", "Descrever e destacar semelhanças e diferenças entre o ciclo da matéria e o fluxo de energia.", "Microrganismos", "avancado", 3),
    ("EF04CI06", "4º ano", "Ciências", "Vida e Evolução", "Decomposição", "Relacionar a participação de fungos e bactérias no processo de decomposição.", "Microrganismos", "intermediario", 4),
    ("EF04CI07", "4º ano", "Ciências", "Vida e Evolução", "Microrganismos úteis", "Verificar a participação de microrganismos na produção de alimentos.", "Microrganismos", "intermediario", 4),
    ("EF04CI08", "4º ano", "Ciências", "Vida e Evolução", "Prevenção de doenças", "Propor atitudes e medidas adequadas para prevenção de doenças.", "Microrganismos", "avancado", 4),
    ("EF04CI09", "4º ano", "Ciências", "Terra e Universo", "Pontos cardeais", "Identificar os pontos cardeais, com base no registro de diferentes posições relativas do Sol.", "Pontos cardeais", "intermediario", 3),
    ("EF04CI10", "4º ano", "Ciências", "Terra e Universo", "Bússola", "Comparar as indicações dos pontos cardeais com aquelas obtidas por meio de uma bússola.", "Calendários, fenômenos cíclicos e cultura", "intermediario", 4),
    ("EF04CI11", "4º ano", "Ciências", "Terra e Universo", "Calendários", "Associar os movimentos cíclicos da Lua e da Terra a períodos de tempo regulares.", "Calendários, fenômenos cíclicos e cultura", "avancado", 4),
    
    # 5º ANO
    ("EF05CI01", "5º ano", "Ciências", "Matéria e Energia", "Propriedades físicas", "Explorar fenômenos da vida cotidiana que evidenciem propriedades físicas dos materiais.", "Propriedades físicas dos materiais", "intermediario", 1),
    ("EF05CI02", "5º ano", "Ciências", "Matéria e Energia", "Ciclo hidrológico", "Aplicar os conhecimentos sobre as mudanças de estado físico da água para explicar o ciclo hidrológico.", "Ciclo hidrológico", "intermediario", 2),
    ("EF05CI03", "5º ano", "Ciências", "Matéria e Energia", "Cobertura vegetal", "Selecionar argumentos que justifiquem a importância da cobertura vegetal.", "Consumo consciente", "intermediario", 2),
    ("EF05CI04", "5º ano", "Ciências", "Matéria e Energia", "Usos da água", "Identificar os principais usos da água e de outros materiais nas atividades cotidianas.", "Reciclagem", "intermediario", 3),
    ("EF05CI05", "5º ano", "Ciências", "Matéria e Energia", "Consumo consciente", "Construir propostas coletivas para um consumo mais consciente.", "Reciclagem", "avancado", 3),
    ("EF05CI06", "5º ano", "Ciências", "Vida e Evolução", "Nutrição", "Selecionar argumentos que justifiquem por que os sistemas digestório e respiratório são corresponsáveis pelo processo de nutrição.", "Nutrição do organismo", "intermediario", 3),
    ("EF05CI07", "5º ano", "Ciências", "Vida e Evolução", "Integração dos sistemas", "Comparar as relações entre alimentação e atividade física no funcionamento do organismo.", "Integração entre os sistemas", "intermediario", 4),
    ("EF05CI08", "5º ano", "Ciências", "Vida e Evolução", "Alimentação saudável", "Organizar um cardápio equilibrado com base nas características dos grupos alimentares.", "Nutrição do organismo", "intermediario", 4),
    ("EF05CI09", "5º ano", "Ciências", "Vida e Evolução", "Distúrbios nutricionais", "Discutir a ocorrência de distúrbios nutricionais entre crianças e jovens.", "Nutrição do organismo", "avancado", 4),
    ("EF05CI10", "5º ano", "Ciências", "Terra e Universo", "Constelações", "Identificar algumas constelações no céu.", "Constelações e mapas celestes", "intermediario", 3),
    ("EF05CI11", "5º ano", "Ciências", "Terra e Universo", "Rotação da Terra", "Associar o movimento diário do Sol e das demais estrelas no céu ao movimento de rotação da Terra.", "Movimento de rotação da Terra", "intermediario", 4),
    ("EF05CI12", "5º ano", "Ciências", "Terra e Universo", "Fases da Lua", "Concluir sobre a periodicidade das fases da Lua.", "Periodicidade das fases da Lua", "avancado", 4),
    ("EF05CI13", "5º ano", "Ciências", "Terra e Universo", "Instrumentos ópticos", "Projetar e construir dispositivos para observação à distância.", "Instrumentos óticos", "avancado", 4),
]

# ============================================
# HISTÓRIA - Anos Iniciais
# ============================================
BNCC_HISTORIA = [
    # 1º ANO
    ("EF01HI01", "1º ano", "História", "Mundo pessoal", "Identidade", "As fases da vida e a ideia de temporalidade (passado, presente, futuro).", "As fases da vida e a ideia de temporalidade", "fundamental", 1),
    ("EF01HI02", "1º ano", "História", "Mundo pessoal", "Família", "Identificar a relação entre as suas histórias e as histórias de sua família e de sua comunidade.", "As diferentes formas de organização da família e da comunidade", "fundamental", 1),
    ("EF01HI03", "1º ano", "História", "Mundo pessoal", "Comunidade", "Descrever e distinguir os seus papéis e responsabilidades relacionados à família, à escola e à comunidade.", "A escola e a diversidade do grupo social envolvido", "fundamental", 2),
    ("EF01HI04", "1º ano", "História", "Mundo pessoal", "Escola", "Identificar as diferenças entre os variados ambientes em que vive.", "A escola e a diversidade do grupo social envolvido", "fundamental", 2),
    ("EF01HI05", "1º ano", "História", "Mundo pessoal", "Brincadeiras", "Identificar semelhanças e diferenças entre jogos e brincadeiras atuais e de outras épocas e lugares.", "A vida em família", "intermediario", 3),
    ("EF01HI06", "1º ano", "História", "Mundo pessoal", "Histórias familiares", "Conhecer as histórias da família e da escola.", "A vida em casa, a vida na escola", "intermediario", 3),
    ("EF01HI07", "1º ano", "História", "Mundo pessoal", "Mudanças e permanências", "Identificar mudanças e permanências nas formas de organização familiar.", "A vida em casa, a vida na escola", "intermediario", 4),
    ("EF01HI08", "1º ano", "História", "Mundo pessoal", "Comemorações", "Reconhecer o significado das comemorações e festas escolares.", "A vida em casa, a vida na escola", "fundamental", 4),
    
    # 2º ANO
    ("EF02HI01", "2º ano", "História", "A comunidade e seus registros", "Sociabilidade", "Reconhecer espaços de sociabilidade e identificar os motivos que aproximam e separam as pessoas.", "A noção do Eu e do Outro", "fundamental", 1),
    ("EF02HI02", "2º ano", "História", "A comunidade e seus registros", "Papéis sociais", "Identificar e descrever práticas e papéis sociais que as pessoas exercem em diferentes comunidades.", "A noção do Eu e do Outro", "fundamental", 1),
    ("EF02HI03", "2º ano", "História", "A comunidade e seus registros", "Mudança e pertencimento", "Selecionar situações cotidianas que remetam à percepção de mudança, pertencimento e memória.", "A noção do Eu e do Outro", "intermediario", 2),
    ("EF02HI04", "2º ano", "História", "A comunidade e seus registros", "Objetos e documentos", "Selecionar e comparar objetos e documentos pessoais e de grupos próximos.", "As formas de registrar as experiências da comunidade", "intermediario", 2),
    ("EF02HI05", "2º ano", "História", "A comunidade e seus registros", "Memória", "Selecionar objetos e documentos pessoais e compreender sua função, seu uso e seu significado.", "As formas de registrar as experiências da comunidade", "intermediario", 3),
    ("EF02HI06", "2º ano", "História", "A comunidade e seus registros", "Organização temporal", "Identificar e organizar, temporalmente, fatos da vida cotidiana.", "As formas de registrar as experiências da comunidade", "fundamental", 3),
    ("EF02HI07", "2º ano", "História", "A comunidade e seus registros", "Marcadores do tempo", "Identificar e utilizar diferentes marcadores do tempo presentes na comunidade.", "As formas de registrar as experiências da comunidade", "fundamental", 4),
    ("EF02HI08", "2º ano", "História", "As formas de registrar", "Histórias da comunidade", "Compilar histórias da família e/ou da comunidade registradas em diferentes fontes.", "O tempo como medida", "intermediario", 4),
    ("EF02HI09", "2º ano", "História", "As formas de registrar", "Preservação", "Identificar objetos e documentos pessoais que remetam à própria experiência.", "O tempo como medida", "intermediario", 4),
    ("EF02HI10", "2º ano", "História", "O trabalho na comunidade", "Formas de trabalho", "Identificar diferentes formas de trabalho existentes na comunidade em que vive.", "As fontes", "intermediario", 4),
    ("EF02HI11", "2º ano", "História", "O trabalho na comunidade", "Impactos ambientais", "Identificar impactos no ambiente causados pelas diferentes formas de trabalho.", "A sobrevivência e a relação com a natureza", "avancado", 4),
    
    # 3º ANO
    ("EF03HI01", "3º ano", "História", "As pessoas e os grupos", "Formação da cidade", "Identificar os grupos populacionais que formam a cidade, o município e a região.", "O Eu, o Outro e os diferentes grupos", "fundamental", 1),
    ("EF03HI02", "3º ano", "História", "As pessoas e os grupos", "Fontes históricas", "Selecionar, por meio da consulta de fontes, acontecimentos ocorridos ao longo do tempo na cidade.", "Os patrimônios históricos e culturais", "intermediario", 2),
    ("EF03HI03", "3º ano", "História", "As pessoas e os grupos", "Pontos de vista", "Identificar e comparar pontos de vista em relação a eventos significativos do local.", "Os patrimônios históricos e culturais", "intermediario", 2),
    ("EF03HI04", "3º ano", "História", "As pessoas e os grupos", "Patrimônios", "Identificar os patrimônios históricos e culturais de sua cidade ou região.", "Os patrimônios históricos e culturais", "intermediario", 3),
    ("EF03HI05", "3º ano", "História", "O lugar em que vive", "Marcos históricos", "Identificar os marcos históricos do lugar em que vive e compreender seus significados.", "A cidade, seus espaços públicos e privados", "fundamental", 3),
    ("EF03HI06", "3º ano", "História", "O lugar em que vive", "Registros de memória", "Identificar os registros de memória na cidade.", "A cidade, seus espaços públicos e privados", "intermediario", 3),
    ("EF03HI07", "3º ano", "História", "O lugar em que vive", "Comunidades", "Identificar semelhanças e diferenças existentes entre comunidades de sua cidade.", "A cidade e suas atividades", "intermediario", 4),
    ("EF03HI08", "3º ano", "História", "O lugar em que vive", "Cidade e campo", "Identificar modos de vida na cidade e no campo no presente, comparando-os com os do passado.", "A cidade e suas atividades", "intermediario", 4),
    ("EF03HI09", "3º ano", "História", "Espaço público e privado", "Espaços públicos", "Mapear os espaços públicos no lugar em que vive e identificar suas funções.", "A cidade e suas atividades", "fundamental", 4),
    ("EF03HI10", "3º ano", "História", "Espaço público e privado", "Diferenças de espaços", "Identificar as diferenças entre o espaço doméstico, os espaços públicos e as áreas de conservação.", "A cidade e suas atividades", "intermediario", 4),
    ("EF03HI11", "3º ano", "História", "Espaço público e privado", "Trabalho", "Identificar diferenças entre formas de trabalho realizadas na cidade e no campo.", "A cidade e suas atividades", "intermediario", 4),
    ("EF03HI12", "3º ano", "História", "Espaço público e privado", "Trabalho e lazer", "Comparar as relações de trabalho e lazer do presente com as de outros tempos e espaços.", "A cidade e suas atividades", "avancado", 4),
    
    # 4º ANO
    ("EF04HI01", "4º ano", "História", "Transformações e permanências", "Ação humana", "Reconhecer a história como resultado da ação do ser humano no tempo e no espaço.", "A ação das pessoas, grupos sociais e comunidades", "fundamental", 1),
    ("EF04HI02", "4º ano", "História", "Transformações e permanências", "Marcos da humanidade", "Identificar mudanças e permanências ao longo do tempo.", "A ação das pessoas, grupos sociais e comunidades", "intermediario", 1),
    ("EF04HI03", "4º ano", "História", "Transformações e permanências", "Transformações na cidade", "Identificar as transformações ocorridas na cidade ao longo do tempo.", "A ação das pessoas, grupos sociais e comunidades", "intermediario", 2),
    ("EF04HI04", "4º ano", "História", "Circulação de pessoas", "Nomadismo", "Identificar as relações entre os indivíduos e a natureza e discutir o significado do nomadismo.", "O passado e o presente", "intermediario", 2),
    ("EF04HI05", "4º ano", "História", "Circulação de pessoas", "Ocupação do campo", "Relacionar os processos de ocupação do campo a intervenções na natureza.", "O passado e o presente", "intermediario", 3),
    ("EF04HI06", "4º ano", "História", "Circulação de pessoas", "Deslocamentos", "Identificar as transformações ocorridas nos processos de deslocamento das pessoas e mercadorias.", "A circulação de pessoas e as transformações", "intermediario", 3),
    ("EF04HI07", "4º ano", "História", "As questões migratórias", "Rotas comerciais", "Identificar e descrever a importância dos caminhos terrestres, fluviais e marítimos.", "A invenção do comércio", "intermediario", 3),
    ("EF04HI08", "4º ano", "História", "As questões migratórias", "Meios de comunicação", "Identificar as transformações ocorridas nos meios de comunicação.", "As rotas terrestres, fluviais e marítimas", "avancado", 4),
    ("EF04HI09", "4º ano", "História", "As questões migratórias", "Migrações", "Identificar as motivações dos processos migratórios em diferentes tempos e espaços.", "O surgimento da espécie humana", "avancado", 4),
    ("EF04HI10", "4º ano", "História", "As questões migratórias", "Formação do Brasil", "Analisar diferentes fluxos populacionais e suas contribuições para a formação da sociedade brasileira.", "Os processos migratórios para a formação do Brasil", "avancado", 4),
    ("EF04HI11", "4º ano", "História", "As questões migratórias", "Mudanças e migração", "Analisar a existência ou não de mudanças associadas à migração.", "Os processos migratórios do final do século XIX", "avancado", 4),
    
    # 5º ANO
    ("EF05HI01", "5º ano", "História", "Povos e culturas", "Formação cultural", "Identificar os processos de formação das culturas e dos povos.", "O que forma um povo", "intermediario", 1),
    ("EF05HI02", "5º ano", "História", "Povos e culturas", "Organização política", "Identificar os mecanismos de organização do poder político com vistas à compreensão da ideia de Estado.", "As formas de organização social e política", "intermediario", 2),
    ("EF05HI03", "5º ano", "História", "Povos e culturas", "Culturas e religiões", "Analisar o papel das culturas e das religiões na composição identitária dos povos antigos.", "O papel das religiões e da cultura", "intermediario", 2),
    ("EF05HI04", "5º ano", "História", "Registros da história", "Cidadania", "Associar a noção de cidadania com os princípios de respeito à diversidade.", "Cidadania, diversidade cultural e respeito às diferenças", "intermediario", 3),
    ("EF05HI05", "5º ano", "História", "Registros da história", "Direitos", "Associar o conceito de cidadania à conquista de direitos dos povos e das sociedades.", "As tradições orais e a valorização da memória", "intermediario", 3),
    ("EF05HI06", "5º ano", "História", "Registros da história", "Linguagens", "Comparar o uso de diferentes linguagens e tecnologias no processo de comunicação.", "O surgimento da escrita", "intermediario", 4),
    ("EF05HI07", "5º ano", "História", "Registros da história", "Marcos de memória", "Identificar os processos de produção, hierarquização e difusão dos marcos de memória.", "Os patrimônios materiais e imateriais", "avancado", 4),
    ("EF05HI08", "5º ano", "História", "Registros da história", "Marcação do tempo", "Identificar formas de marcação da passagem do tempo em distintas sociedades.", "Os patrimônios materiais e imateriais", "avancado", 4),
    ("EF05HI09", "5º ano", "História", "Registros da história", "Pontos de vista", "Comparar pontos de vista sobre temas que impactam a vida cotidiana.", "Os patrimônios materiais e imateriais", "avancado", 4),
    ("EF05HI10", "5º ano", "História", "Registros da história", "Patrimônios", "Inventariar os patrimônios materiais e imateriais da humanidade.", "Os patrimônios materiais e imateriais", "avancado", 4),
]

# ============================================
# GEOGRAFIA - Anos Iniciais
# ============================================
BNCC_GEOGRAFIA = [
    # 1º ANO
    ("EF01GE01", "1º ano", "Geografia", "O sujeito e seu lugar no mundo", "Lugares de vivência", "Descrever características observadas de seus lugares de vivência.", "O modo de vida das crianças em diferentes lugares", "fundamental", 1),
    ("EF01GE02", "1º ano", "Geografia", "O sujeito e seu lugar no mundo", "Jogos e brincadeiras", "Identificar semelhanças e diferenças entre jogos e brincadeiras de diferentes épocas e lugares.", "Situações de convívio em diferentes lugares", "fundamental", 2),
    ("EF01GE03", "1º ano", "Geografia", "Conexões e escalas", "Espaços públicos", "Identificar e relatar semelhanças e diferenças de usos do espaço público para o lazer.", "Ciclos naturais e a vida cotidiana", "fundamental", 2),
    ("EF01GE04", "1º ano", "Geografia", "Conexões e escalas", "Regras de convívio", "Discutir e elaborar, coletivamente, regras de convívio em diferentes espaços.", "Ciclos naturais e a vida cotidiana", "fundamental", 3),
    ("EF01GE05", "1º ano", "Geografia", "Mundo do trabalho", "Ritmos naturais", "Observar e descrever ritmos naturais (dia e noite, variação de temperatura e umidade).", "Diferentes tipos de trabalho", "intermediario", 3),
    ("EF01GE06", "1º ano", "Geografia", "Mundo do trabalho", "Moradias e objetos", "Descrever e comparar diferentes tipos de moradia ou objetos de uso cotidiano.", "Diferentes tipos de trabalho", "fundamental", 3),
    ("EF01GE07", "1º ano", "Geografia", "Mundo do trabalho", "Trabalho na comunidade", "Descrever atividades de trabalho relacionadas com o dia a dia da sua comunidade.", "Diferentes tipos de trabalho", "fundamental", 4),
    ("EF01GE08", "1º ano", "Geografia", "Representação espacial", "Mapas mentais", "Criar mapas mentais e desenhos com base em itinerários.", "Pontos de referência", "fundamental", 3),
    ("EF01GE09", "1º ano", "Geografia", "Representação espacial", "Localização", "Elaborar e utilizar mapas simples para localizar elementos do local de vivência.", "Pontos de referência", "intermediario", 4),
    ("EF01GE10", "1º ano", "Geografia", "Natureza e qualidade de vida", "Ritmos da natureza", "Descrever características de seus lugares de vivência relacionadas aos ritmos da natureza.", "Condições de vida nos lugares de vivência", "fundamental", 4),
    ("EF01GE11", "1º ano", "Geografia", "Natureza e qualidade de vida", "Vestuário e alimentação", "Associar mudanças de vestuário e hábitos alimentares ao longo do ano.", "Condições de vida nos lugares de vivência", "intermediario", 4),
    
    # 2º ANO
    ("EF02GE01", "2º ano", "Geografia", "O sujeito e seu lugar no mundo", "Migrações", "Descrever a história das migrações no bairro ou comunidade em que vive.", "Convivência e interações entre pessoas na comunidade", "fundamental", 1),
    ("EF02GE02", "2º ano", "Geografia", "O sujeito e seu lugar no mundo", "Costumes e tradições", "Comparar costumes e tradições de diferentes populações inseridas no bairro.", "Riscos e cuidados nos meios de transporte", "fundamental", 2),
    ("EF02GE03", "2º ano", "Geografia", "Conexões e escalas", "Meios de transporte", "Comparar diferentes meios de transporte e de comunicação.", "Riscos e cuidados nos meios de transporte", "intermediario", 2),
    ("EF02GE04", "2º ano", "Geografia", "Conexões e escalas", "Modos de vida", "Reconhecer semelhanças e diferenças nos hábitos de pessoas em diferentes lugares.", "Experiências da comunidade", "intermediario", 3),
    ("EF02GE05", "2º ano", "Geografia", "Conexões e escalas", "Mudanças e permanências", "Analisar mudanças e permanências, comparando imagens de um mesmo lugar.", "Experiências da comunidade", "intermediario", 3),
    ("EF02GE06", "2º ano", "Geografia", "Mundo do trabalho", "Dia e noite", "Relacionar o dia e a noite a diferentes tipos de atividades sociais.", "Tipos de trabalho em lugares e tempos diferentes", "fundamental", 3),
    ("EF02GE07", "2º ano", "Geografia", "Mundo do trabalho", "Atividades extrativas", "Descrever as atividades extrativas de diferentes lugares.", "Tipos de trabalho em lugares e tempos diferentes", "intermediario", 4),
    ("EF02GE08", "2º ano", "Geografia", "Representação espacial", "Representações", "Identificar e elaborar diferentes formas de representação.", "Localização, orientação e representação espacial", "fundamental", 3),
    ("EF02GE09", "2º ano", "Geografia", "Representação espacial", "Imagens aéreas", "Identificar objetos e lugares de vivência em imagens aéreas e mapas.", "Localização, orientação e representação espacial", "intermediario", 4),
    ("EF02GE10", "2º ano", "Geografia", "Representação espacial", "Princípios de localização", "Aplicar princípios de localização e posição de objetos.", "Localização, orientação e representação espacial", "intermediario", 4),
    ("EF02GE11", "2º ano", "Geografia", "Natureza e qualidade de vida", "Solo e água", "Reconhecer a importância do solo e da água para a vida.", "Os usos dos recursos naturais", "intermediario", 4),
    
    # 3º ANO
    ("EF03GE01", "3º ano", "Geografia", "O sujeito e seu lugar no mundo", "Cidade e campo", "Identificar e comparar aspectos culturais dos grupos sociais de seus lugares de vivência.", "A cidade e o campo", "fundamental", 1),
    ("EF03GE02", "3º ano", "Geografia", "O sujeito e seu lugar no mundo", "Contribuições culturais", "Identificar, em seus lugares de vivência, marcas de contribuição cultural e econômica.", "A cidade e o campo", "intermediario", 2),
    ("EF03GE03", "3º ano", "Geografia", "O sujeito e seu lugar no mundo", "Povos tradicionais", "Reconhecer os diferentes modos de vida de povos e comunidades tradicionais.", "A cidade e o campo", "intermediario", 2),
    ("EF03GE04", "3º ano", "Geografia", "Conexões e escalas", "Paisagens", "Explicar como os processos naturais e históricos atuam na produção e na mudança das paisagens.", "Paisagens naturais e antrópicas", "intermediario", 3),
    ("EF03GE05", "3º ano", "Geografia", "Mundo do trabalho", "Produtos da natureza", "Identificar alimentos, minerais e outros produtos cultivados e extraídos da natureza.", "Matéria-prima e indústria", "fundamental", 3),
    ("EF03GE06", "3º ano", "Geografia", "Mundo do trabalho", "Áreas de produção", "Identificar e comparar alguns pontos de vista diferentes sobre as áreas de produção.", "Matéria-prima e indústria", "intermediario", 4),
    ("EF03GE07", "3º ano", "Geografia", "Representação espacial", "Legendas e símbolos", "Reconhecer e elaborar legendas com símbolos de diversos tipos de representações.", "Representações cartográficas", "intermediario", 3),
    ("EF03GE08", "3º ano", "Geografia", "Natureza e qualidade de vida", "Lixo e consumo", "Relacionar a produção de lixo doméstico aos problemas causados pelo consumo excessivo.", "Produção, circulação e consumo", "intermediario", 4),
    ("EF03GE09", "3º ano", "Geografia", "Natureza e qualidade de vida", "Recursos naturais", "Investigar os usos dos recursos naturais.", "Impactos das atividades humanas", "intermediario", 4),
    ("EF03GE10", "3º ano", "Geografia", "Natureza e qualidade de vida", "Água na agricultura", "Identificar os cuidados necessários para utilização da água na agricultura.", "Impactos das atividades humanas", "avancado", 4),
    ("EF03GE11", "3º ano", "Geografia", "Natureza e qualidade de vida", "Impactos econômicos", "Comparar impactos das atividades econômicas urbanas e rurais sobre o ambiente.", "Impactos das atividades humanas", "avancado", 4),
    
    # 4º ANO
    ("EF04GE01", "4º ano", "Geografia", "O sujeito e seu lugar no mundo", "Diversidade cultural", "Selecionar, em seus lugares de vivência, elementos de distintas culturas.", "Território e diversidade cultural", "intermediario", 1),
    ("EF04GE02", "4º ano", "Geografia", "O sujeito e seu lugar no mundo", "Processos migratórios", "Descrever processos migratórios e suas contribuições para a formação da sociedade brasileira.", "Processos migratórios no Brasil", "intermediario", 2),
    ("EF04GE03", "4º ano", "Geografia", "O sujeito e seu lugar no mundo", "Poder público", "Distinguir funções e papéis dos órgãos do poder público municipal.", "Instâncias do poder público", "intermediario", 2),
    ("EF04GE04", "4º ano", "Geografia", "Conexões e escalas", "Campo e cidade", "Reconhecer especificidades e analisar a interdependência do campo e da cidade.", "Relação campo e cidade", "intermediario", 3),
    ("EF04GE05", "4º ano", "Geografia", "Conexões e escalas", "Unidades políticas", "Distinguir unidades político-administrativas oficiais nacionais.", "Unidades político-administrativas do Brasil", "fundamental", 3),
    ("EF04GE06", "4º ano", "Geografia", "Conexões e escalas", "Territórios étnicos", "Identificar e descrever territórios étnico-culturais existentes no Brasil.", "Territórios étnico-culturais", "intermediario", 4),
    ("EF04GE07", "4º ano", "Geografia", "Mundo do trabalho", "Trabalho campo e cidade", "Comparar as características do trabalho no campo e na cidade.", "Trabalho no campo e na cidade", "fundamental", 3),
    ("EF04GE08", "4º ano", "Geografia", "Mundo do trabalho", "Processo de produção", "Descrever e discutir o processo de produção, circulação e consumo.", "Produção, circulação e consumo", "intermediario", 4),
    ("EF04GE09", "4º ano", "Geografia", "Representação espacial", "Direções cardeais", "Utilizar as direções cardeais na localização de componentes.", "Sistema de orientação", "intermediario", 3),
    ("EF04GE10", "4º ano", "Geografia", "Representação espacial", "Tipos de mapas", "Comparar tipos variados de mapas.", "Elementos constitutivos dos mapas", "intermediario", 4),
    ("EF04GE11", "4º ano", "Geografia", "Natureza e qualidade de vida", "Paisagens naturais", "Identificar as características das paisagens naturais e antrópicas.", "Conservação e degradação da natureza", "intermediario", 4),
    
    # 5º ANO
    ("EF05GE01", "5º ano", "Geografia", "O sujeito e seu lugar no mundo", "Dinâmicas populacionais", "Descrever e analisar dinâmicas populacionais na Unidade da Federação.", "Dinâmica populacional", "intermediario", 1),
    ("EF05GE02", "5º ano", "Geografia", "O sujeito e seu lugar no mundo", "Desigualdades", "Identificar diferenças étnico-raciais e desigualdades sociais entre grupos.", "Diferenças étnico-raciais e desigualdades sociais", "intermediario", 2),
    ("EF05GE03", "5º ano", "Geografia", "Conexões e escalas", "Cidades", "Identificar as formas e funções das cidades.", "Território, redes e urbanização", "intermediario", 2),
    ("EF05GE04", "5º ano", "Geografia", "Conexões e escalas", "Rede urbana", "Reconhecer as características da cidade e analisar as interações entre a cidade e o campo.", "Território, redes e urbanização", "intermediario", 3),
    ("EF05GE05", "5º ano", "Geografia", "Mundo do trabalho", "Trabalho e tecnologia", "Identificar e comparar as mudanças dos tipos de trabalho e desenvolvimento tecnológico.", "Trabalho e inovação tecnológica", "intermediario", 3),
    ("EF05GE06", "5º ano", "Geografia", "Mundo do trabalho", "Transportes e comunicação", "Identificar e comparar transformações dos meios de transporte e de comunicação.", "Trabalho e inovação tecnológica", "intermediario", 4),
    ("EF05GE07", "5º ano", "Geografia", "Mundo do trabalho", "Tipos de energia", "Identificar os diferentes tipos de energia utilizados na produção.", "Trabalho e inovação tecnológica", "avancado", 4),
    ("EF05GE08", "5º ano", "Geografia", "Representação espacial", "Transformações", "Analisar transformações de paisagens nas cidades.", "Mapas e imagens de satélite", "intermediario", 3),
    ("EF05GE09", "5º ano", "Geografia", "Representação espacial", "Hierarquia urbana", "Estabelecer conexões e hierarquias entre diferentes cidades.", "Representação das cidades", "avancado", 4),
    ("EF05GE10", "5º ano", "Geografia", "Natureza e qualidade de vida", "Qualidade ambiental", "Reconhecer e comparar atributos da qualidade ambiental.", "Qualidade ambiental", "intermediario", 4),
    ("EF05GE11", "5º ano", "Geografia", "Natureza e qualidade de vida", "Problemas ambientais", "Identificar e descrever problemas ambientais que ocorrem no entorno.", "Diferentes tipos de poluição", "intermediario", 4),
    ("EF05GE12", "5º ano", "Geografia", "Natureza e qualidade de vida", "Gestão pública", "Identificar órgãos do poder público responsáveis pela qualidade de vida.", "Gestão pública da qualidade de vida", "avancado", 4),
]

# ============================================
# ARTE - Anos Iniciais
# ============================================
BNCC_ARTE = [
    ("EF15AR01", "1º ao 5º ano", "Arte", "Artes Visuais", "Contextos e práticas", "Identificar e apreciar formas distintas das artes visuais tradicionais e contemporâneas.", "Contextos e práticas", "fundamental", 1),
    ("EF15AR02", "1º ao 5º ano", "Arte", "Artes Visuais", "Elementos da linguagem", "Explorar e reconhecer elementos constitutivos das artes visuais (ponto, linha, forma, cor, espaço, movimento).", "Elementos da linguagem", "fundamental", 1),
    ("EF15AR03", "1º ao 5º ano", "Arte", "Artes Visuais", "Matrizes estéticas", "Reconhecer e analisar a influência de distintas matrizes estéticas e culturais das artes visuais.", "Matrizes estéticas e culturais", "intermediario", 2),
    ("EF15AR04", "1º ao 5º ano", "Arte", "Artes Visuais", "Materialidades", "Experimentar diferentes formas de expressão artística.", "Materialidades", "fundamental", 2),
    ("EF15AR05", "1º ao 5º ano", "Arte", "Artes Visuais", "Processos de criação", "Experimentar a criação em artes visuais de modo individual, coletivo e colaborativo.", "Processos de criação", "intermediario", 3),
    ("EF15AR06", "1º ao 5º ano", "Arte", "Artes Visuais", "Diálogo", "Dialogar sobre a sua criação e as dos colegas.", "Sistemas da linguagem", "intermediario", 3),
    ("EF15AR07", "1º ao 5º ano", "Arte", "Artes Visuais", "Sistema das artes", "Reconhecer algumas categorias do sistema das artes visuais.", "Sistemas da linguagem", "avancado", 4),
    ("EF15AR08", "1º ao 5º ano", "Arte", "Dança", "Contextos e práticas", "Experimentar e apreciar formas distintas de manifestações da dança.", "Contextos e práticas", "fundamental", 1),
    ("EF15AR09", "1º ao 5º ano", "Arte", "Dança", "Elementos da linguagem", "Estabelecer relações entre as partes do corpo na construção do movimento dançado.", "Elementos da linguagem", "fundamental", 2),
    ("EF15AR10", "1º ao 5º ano", "Arte", "Dança", "Orientação no espaço", "Experimentar diferentes formas de orientação no espaço e ritmos de movimento.", "Elementos da linguagem", "intermediario", 2),
    ("EF15AR11", "1º ao 5º ano", "Arte", "Dança", "Criação de movimentos", "Criar e improvisar movimentos dançados de modo individual, coletivo e colaborativo.", "Processos de criação", "intermediario", 3),
    ("EF15AR12", "1º ao 5º ano", "Arte", "Dança", "Experiências em dança", "Discutir, com respeito e sem preconceito, as experiências pessoais e coletivas em dança.", "Processos de criação", "intermediario", 3),
    ("EF15AR13", "1º ao 5º ano", "Arte", "Música", "Contextos e práticas", "Identificar e apreciar criticamente diversas formas e gêneros de expressão musical.", "Contextos e práticas", "fundamental", 1),
    ("EF15AR14", "1º ao 5º ano", "Arte", "Música", "Elementos da linguagem", "Perceber e explorar os elementos constitutivos da música.", "Elementos da linguagem", "fundamental", 2),
    ("EF15AR15", "1º ao 5º ano", "Arte", "Música", "Fontes sonoras", "Explorar fontes sonoras diversas.", "Materialidades", "fundamental", 2),
    ("EF15AR16", "1º ao 5º ano", "Arte", "Música", "Notação musical", "Explorar diferentes formas de registro musical não convencional.", "Notação e registro musical", "intermediario", 3),
    ("EF15AR17", "1º ao 5º ano", "Arte", "Música", "Processos de criação", "Experimentar improvisações, composições e sonorização de histórias.", "Processos de criação", "intermediario", 3),
    ("EF15AR18", "1º ao 5º ano", "Arte", "Teatro", "Contextos e práticas", "Reconhecer e apreciar formas distintas de manifestações do teatro.", "Contextos e práticas", "fundamental", 1),
    ("EF15AR19", "1º ao 5º ano", "Arte", "Teatro", "Elementos da linguagem", "Descobrir teatralidades na vida cotidiana.", "Elementos da linguagem", "fundamental", 2),
    ("EF15AR20", "1º ao 5º ano", "Arte", "Teatro", "Trabalho colaborativo", "Experimentar o trabalho colaborativo, coletivo e autoral em improvisações teatrais.", "Processos de criação", "intermediario", 3),
    ("EF15AR21", "1º ao 5º ano", "Arte", "Teatro", "Imitação e faz de conta", "Exercitar a imitação e o faz de conta.", "Processos de criação", "intermediario", 3),
    ("EF15AR22", "1º ao 5º ano", "Arte", "Teatro", "Criação de personagem", "Experimentar possibilidades criativas de movimento e de voz na criação de um personagem.", "Processos de criação", "intermediario", 4),
    ("EF15AR23", "1º ao 5º ano", "Arte", "Artes Integradas", "Relações processuais", "Reconhecer e experimentar, em projetos temáticos, as relações processuais entre diversas linguagens artísticas.", "Processos de criação", "avancado", 4),
    ("EF15AR24", "1º ao 5º ano", "Arte", "Artes Integradas", "Matrizes estéticas", "Caracterizar e experimentar brinquedos, brincadeiras, jogos, danças, canções e histórias de diferentes matrizes estéticas.", "Matrizes estéticas e culturais", "intermediario", 3),
    ("EF15AR25", "1º ao 5º ano", "Arte", "Artes Integradas", "Patrimônio cultural", "Conhecer e valorizar o patrimônio cultural, material e imaterial, de culturas diversas.", "Patrimônio cultural", "intermediario", 4),
    ("EF15AR26", "1º ao 5º ano", "Arte", "Artes Integradas", "Arte e tecnologia", "Explorar diferentes tecnologias e recursos digitais nos processos de criação artística.", "Arte e tecnologia", "avancado", 4),
]


def importar_tudo():
    """Importa todos os dados da BNCC para o banco de dados"""
    
    print("=" * 70)
    print("📚 IMPORTAÇÃO COMPLETA DA BNCC - BASE NACIONAL COMUM CURRICULAR")
    print("=" * 70)
    
    # Todos os componentes
    COMPONENTES = [
        ("Matemática", BNCC_MATEMATICA),
        ("Língua Portuguesa", BNCC_PORTUGUES),
        ("Ciências", BNCC_CIENCIAS),
        ("História", BNCC_HISTORIA),
        ("Geografia", BNCC_GEOGRAFIA),
        ("Arte", BNCC_ARTE),
        ("Educação Física", BNCC_EDUCACAO_FISICA),
    ]
    
    with engine.connect() as conn:
        # Verificar se a tabela existe
        result = conn.execute(text("SHOW TABLES LIKE 'curriculo_nacional'"))
        if not result.fetchone():
            print("\n❌ ERRO: Tabela 'curriculo_nacional' não existe!")
            print("   Execute primeiro: python criar_tabelas_bncc.py")
            return
        
        # Verificar quantidade atual
        result = conn.execute(text("SELECT COUNT(*) FROM curriculo_nacional"))
        count_inicial = result.scalar()
        print(f"\n📊 Habilidades já existentes: {count_inicial}")
        
        total_importado = 0
        
        for nome_comp, dados in COMPONENTES:
            print(f"\n📐 Importando {nome_comp}...")
            
            count = 0
            for item in dados:
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
                    count += 1
                except Exception as e:
                    pass  # Ignorar duplicatas
            
            print(f"   ✅ {count} habilidades importadas")
            total_importado += count
        
        # Importar pré-requisitos
        print("\n🔗 Importando mapeamento de pré-requisitos...")
        count_prereqs = 0
        for item in PREREQUISITOS_EXPANDIDOS:
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
                count_prereqs += 1
            except Exception as e:
                pass
        
        print(f"   ✅ {count_prereqs} pré-requisitos importados")
        
        # Estatísticas finais
        print("\n" + "=" * 70)
        print("✅ IMPORTAÇÃO CONCLUÍDA!")
        print("=" * 70)
        
        result = conn.execute(text("SELECT COUNT(*) FROM curriculo_nacional"))
        total_final = result.scalar()
        
        result = conn.execute(text("SELECT COUNT(*) FROM mapeamento_prerequisitos"))
        total_prereqs = result.scalar()
        
        print(f"\n📚 Total de habilidades: {total_final}")
        print(f"🔗 Total de pré-requisitos: {total_prereqs}")
        print(f"➕ Novos registros: {total_importado}")
        
        # Por componente
        print("\n📊 Por componente:")
        for comp in ["Matemática", "Língua Portuguesa", "Ciências", "História", "Geografia", "Arte", "Educação Física"]:
            result = conn.execute(
                text("SELECT COUNT(*) FROM curriculo_nacional WHERE componente = :comp"),
                {"comp": comp}
            )
            count = result.scalar()
            if count > 0:
                print(f"   • {comp}: {count}")
        
        # Por ano escolar
        print("\n📊 Por ano escolar:")
        for ano in ["1º ano", "2º ano", "3º ano", "4º ano", "5º ano", "1º e 2º ano", "3º ao 5º ano", "1º ao 5º ano"]:
            result = conn.execute(
                text("SELECT COUNT(*) FROM curriculo_nacional WHERE ano_escolar = :ano"),
                {"ano": ano}
            )
            count = result.scalar()
            if count > 0:
                print(f"   • {ano}: {count}")


if __name__ == "__main__":
    importar_tudo()
