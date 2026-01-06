# ============================================
# IMPORTAR HABILIDADES BNCC - ENSINO FUNDAMENTAL II
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

# BNCC Ensino Fundamental II (6º ao 9º ano)
HABILIDADES_EF2 = [
    # ============================================
    # MATEMATICA - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06MA01", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Numeros naturais",
     "habilidade_descricao": "Comparar, ordenar, ler e escrever numeros naturais e numeros racionais cuja representacao decimal e finita."},
    
    {"codigo_bncc": "EF06MA02", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Operacoes com naturais",
     "habilidade_descricao": "Reconhecer o sistema de numeracao decimal como o que prevaleceu no mundo ocidental e destacar semelancas e diferencas com outros sistemas."},
    
    {"codigo_bncc": "EF06MA03", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Divisibilidade",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam calculos com numeros naturais, envolvendo as quatro operacoes."},
    
    {"codigo_bncc": "EF06MA04", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Fracoes",
     "habilidade_descricao": "Construir algoritmo em linguagem natural e representa-lo por fluxograma que indique a resolucao de um problema simples."},
    
    {"codigo_bncc": "EF06MA05", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Operacoes com fracoes",
     "habilidade_descricao": "Classificar numeros naturais em primos e compostos, estabelecer relacoes entre numeros."},
    
    {"codigo_bncc": "EF06MA06", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Numeros decimais",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam as ideias de multiplo e de divisor."},
    
    {"codigo_bncc": "EF06MA07", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Porcentagem",
     "habilidade_descricao": "Compreender, comparar e ordenar fracoes associadas as ideias de partes de inteiros e resultado de divisao."},
    
    {"codigo_bncc": "EF06MA08", "componente": "Matematica", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Geometria plana",
     "habilidade_descricao": "Reconhecer que os numeros racionais positivos podem ser expressos nas formas fracionaria e decimal."},

    # ============================================
    # MATEMATICA - 7º ANO
    # ============================================
    {"codigo_bncc": "EF07MA01", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Numeros inteiros",
     "habilidade_descricao": "Resolver e elaborar problemas com numeros naturais, envolvendo as nocoes de divisor e de multiplo."},
    
    {"codigo_bncc": "EF07MA02", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Operacoes com inteiros",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam porcentagens, como os que lidam com acrescimos e decrescimos simples."},
    
    {"codigo_bncc": "EF07MA03", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Numeros racionais",
     "habilidade_descricao": "Comparar e ordenar numeros inteiros em diferentes contextos, incluindo o historico."},
    
    {"codigo_bncc": "EF07MA04", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Equacoes",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam operacoes com numeros inteiros."},
    
    {"codigo_bncc": "EF07MA05", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Razao e proporcao",
     "habilidade_descricao": "Resolver um mesmo problema utilizando diferentes algoritmos."},
    
    {"codigo_bncc": "EF07MA06", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Regra de tres",
     "habilidade_descricao": "Reconhecer que as resolucoes de um grupo de problemas que tem a mesma estrutura podem ser obtidas utilizando os mesmos procedimentos."},
    
    {"codigo_bncc": "EF07MA07", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Angulos",
     "habilidade_descricao": "Representar por meio de um fluxograma os passos utilizados para resolver um grupo de problemas."},
    
    {"codigo_bncc": "EF07MA08", "componente": "Matematica", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Triangulos",
     "habilidade_descricao": "Comparar e ordenar fracoes associadas as ideias de partes de inteiros, resultado da divisao, razao e operador."},

    # ============================================
    # MATEMATICA - 8º ANO
    # ============================================
    {"codigo_bncc": "EF08MA01", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Numeros reais",
     "habilidade_descricao": "Efetuar calculos com potencias de expoentes inteiros e aplicar esse conhecimento na representacao de numeros em notacao cientifica."},
    
    {"codigo_bncc": "EF08MA02", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Notacao cientifica",
     "habilidade_descricao": "Resolver e elaborar problemas usando a relacao entre potenciacao e radiciacao."},
    
    {"codigo_bncc": "EF08MA03", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Expressoes algebricas",
     "habilidade_descricao": "Resolver e elaborar problemas de contagem cuja resolucao envolva a aplicacao do principio multiplicativo."},
    
    {"codigo_bncc": "EF08MA04", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Produtos notaveis",
     "habilidade_descricao": "Resolver e elaborar problemas, envolvendo calculo de porcentagens, incluindo o uso de tecnologias digitais."},
    
    {"codigo_bncc": "EF08MA05", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Fatoracao",
     "habilidade_descricao": "Reconhecer e utilizar procedimentos para a obtencao de uma fracao geratriz para uma dizima periodica."},
    
    {"codigo_bncc": "EF08MA06", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Sistemas de equacoes",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam calculos de porcentagem e calculo de juros."},
    
    {"codigo_bncc": "EF08MA07", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Teorema de Pitagoras",
     "habilidade_descricao": "Associar uma equacao linear de 1o grau com duas incognitas a uma reta no plano cartesiano."},
    
    {"codigo_bncc": "EF08MA08", "componente": "Matematica", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Semelhanca de triangulos",
     "habilidade_descricao": "Resolver e elaborar problemas relacionados ao volume de prisma e de cilindro retos."},

    # ============================================
    # MATEMATICA - 9º ANO
    # ============================================
    {"codigo_bncc": "EF09MA01", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Numeros reais e radicais",
     "habilidade_descricao": "Reconhecer que, uma vez fixada uma unidade de comprimento, existem segmentos de reta cujo comprimento nao e expresso por numero racional."},
    
    {"codigo_bncc": "EF09MA02", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Potencias e radicais",
     "habilidade_descricao": "Reconhecer um numero irracional como um numero real cuja representacao decimal e infinita e nao periodica."},
    
    {"codigo_bncc": "EF09MA03", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Funcoes",
     "habilidade_descricao": "Efetuar calculos com numeros reais, inclusive potencias com expoentes fracionarios."},
    
    {"codigo_bncc": "EF09MA04", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Funcao afim",
     "habilidade_descricao": "Resolver e elaborar problemas com numeros reais, inclusive em notacao cientifica."},
    
    {"codigo_bncc": "EF09MA05", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Funcao quadratica",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam porcentagens, com a ideia de aplicacao de percentuais sucessivos."},
    
    {"codigo_bncc": "EF09MA06", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Equacoes do 2o grau",
     "habilidade_descricao": "Compreender as funcoes como relacoes de dependencia univalente entre duas variaveis."},
    
    {"codigo_bncc": "EF09MA07", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Estatistica",
     "habilidade_descricao": "Resolver problemas que envolvam a razao entre duas grandezas de especies diferentes."},
    
    {"codigo_bncc": "EF09MA08", "componente": "Matematica", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Probabilidade",
     "habilidade_descricao": "Resolver e elaborar problemas que envolvam relacoes de proporcionalidade direta e inversa entre duas ou mais grandezas."},

    # ============================================
    # LINGUA PORTUGUESA - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06LP01", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Leitura e interpretacao",
     "habilidade_descricao": "Reconhecer a impossibilidade de uma neutralidade absoluta no relato de fatos e identificar diferentes graus de parcialidade."},
    
    {"codigo_bncc": "EF06LP02", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Generos textuais",
     "habilidade_descricao": "Estabelecer relacao entre os diferentes generos jornalisticos, compreendendo a centralidade da noticia."},
    
    {"codigo_bncc": "EF06LP03", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Producao de textos",
     "habilidade_descricao": "Analisar diferencas de sentido entre palavras de uma serie sinonima."},
    
    {"codigo_bncc": "EF06LP04", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Ortografia",
     "habilidade_descricao": "Analisar a funcao e as flexoes de substantivos e adjetivos e de verbos nos modos Indicativo, Subjuntivo e Imperativo."},
    
    {"codigo_bncc": "EF06LP05", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Gramatica",
     "habilidade_descricao": "Identificar os efeitos de sentido dos modos verbais, considerando o genero textual e a intencao comunicativa."},
    
    {"codigo_bncc": "EF06LP06", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Pontuacao",
     "habilidade_descricao": "Empregar, adequadamente, as regras de concordancia nominal e verbal."},
    
    {"codigo_bncc": "EF06LP07", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Narrativa",
     "habilidade_descricao": "Identificar, em textos, periodos compostos por coordenacao, subordinacao e suas funcoes."},
    
    {"codigo_bncc": "EF06LP08", "componente": "Lingua Portuguesa", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Literatura",
     "habilidade_descricao": "Identificar, em texto narrativo ficcional, a estrutura da narrativa: apresentacao, desenvolvimento, climax e desfecho."},

    # ============================================
    # LINGUA PORTUGUESA - 7º ANO
    # ============================================
    {"codigo_bncc": "EF07LP01", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Leitura critica",
     "habilidade_descricao": "Distinguir diferentes propositos da leitura de textos noticiosos e identificar diferentes formas de tratar uma informacao."},
    
    {"codigo_bncc": "EF07LP02", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Generos argumentativos",
     "habilidade_descricao": "Comparar noticias e reportagens sobre um mesmo fato divulgadas em diferentes midias."},
    
    {"codigo_bncc": "EF07LP03", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Coesao textual",
     "habilidade_descricao": "Formar, com base em palavras primitivas, palavras derivadas com os prefixos e sufixos mais produtivos no portugues."},
    
    {"codigo_bncc": "EF07LP04", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Coerencia textual",
     "habilidade_descricao": "Reconhecer, em textos, o verbo como o nucleo das oracoes."},
    
    {"codigo_bncc": "EF07LP05", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Figuras de linguagem",
     "habilidade_descricao": "Identificar, em textos lidos ou de producao propria, adverbios e locucoes adverbiais."},
    
    {"codigo_bncc": "EF07LP06", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Variacoes linguisticas",
     "habilidade_descricao": "Empregar as regras basicas de concordancia nominal e verbal em situacoes comunicativas."},
    
    {"codigo_bncc": "EF07LP07", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Cronica",
     "habilidade_descricao": "Identificar, em textos lidos e em producoes proprias, a estrutura basica da oracao."},
    
    {"codigo_bncc": "EF07LP08", "componente": "Lingua Portuguesa", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Poesia",
     "habilidade_descricao": "Identificar, em textos lidos, os elementos estruturais da poesia: verso, estrofe e rima."},

    # ============================================
    # LINGUA PORTUGUESA - 8º ANO
    # ============================================
    {"codigo_bncc": "EF08LP01", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Argumentacao",
     "habilidade_descricao": "Identificar e comparar as varias edicoes de uma obra literaria ou de um texto."},
    
    {"codigo_bncc": "EF08LP02", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Debate",
     "habilidade_descricao": "Justificar diferencas ou semelancas de tratamento dado a uma mesma informacao veiculada em textos diferentes."},
    
    {"codigo_bncc": "EF08LP03", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Texto dissertativo",
     "habilidade_descricao": "Produzir artigos de opiniao, tendo em vista o contexto de producao dado."},
    
    {"codigo_bncc": "EF08LP04", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Analise sintatica",
     "habilidade_descricao": "Utilizar, ao produzir texto, conhecimentos linguisticos e gramaticais."},
    
    {"codigo_bncc": "EF08LP05", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Vozes verbais",
     "habilidade_descricao": "Analisar processos de formacao de palavras por composicao e derivacao."},
    
    {"codigo_bncc": "EF08LP06", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Regencia verbal",
     "habilidade_descricao": "Identificar, em textos lidos, oracao subordinada com funcao de adverbio."},
    
    {"codigo_bncc": "EF08LP07", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Romance",
     "habilidade_descricao": "Diferenciar, em textos lidos, os efeitos de sentido decorrentes do uso de mecanismos de intertextualidade."},
    
    {"codigo_bncc": "EF08LP08", "componente": "Lingua Portuguesa", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Teatro",
     "habilidade_descricao": "Identificar, em texto dramatico, a funcao das rubricas e sua relacao com a encenacao."},

    # ============================================
    # LINGUA PORTUGUESA - 9º ANO
    # ============================================
    {"codigo_bncc": "EF09LP01", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Leitura critica avancada",
     "habilidade_descricao": "Analisar o fenomeno da disseminacao de noticias falsas nas redes sociais e desenvolver estrategias para reconhece-las."},
    
    {"codigo_bncc": "EF09LP02", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Texto cientifico",
     "habilidade_descricao": "Analisar e comparar propostas politicas e de solucao de problemas apresentadas em diferentes midias."},
    
    {"codigo_bncc": "EF09LP03", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Resenha critica",
     "habilidade_descricao": "Produzir artigos de opiniao, textos de apresentacao e apreciacao de obras artistica e textos expositivos."},
    
    {"codigo_bncc": "EF09LP04", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Periodo composto",
     "habilidade_descricao": "Analisar os efeitos de sentido decorrentes do uso de recursos linguisticos e multissemioticos em textos."},
    
    {"codigo_bncc": "EF09LP05", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Oracoes subordinadas",
     "habilidade_descricao": "Identificar, em textos lidos, recursos de coesao referencial, recategoricao e sequencial."},
    
    {"codigo_bncc": "EF09LP06", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Crase e concordancia",
     "habilidade_descricao": "Empregar, adequadamente, as regras de colocacao pronominal."},
    
    {"codigo_bncc": "EF09LP07", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Literatura brasileira",
     "habilidade_descricao": "Analisar, em textos literarios, como a escolha de genero, as situacoes de producao e recepca influenciam na construcao do sentido."},
    
    {"codigo_bncc": "EF09LP08", "componente": "Lingua Portuguesa", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Producao literaria",
     "habilidade_descricao": "Criar contos ou cronicas, explorando os recursos de linguagem literaria e desenvolvendo estilo proprio."},

    # ============================================
    # CIENCIAS - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06CI01", "componente": "Ciencias", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Materia e energia",
     "habilidade_descricao": "Classificar como homogenea ou heterogenea a mistura de dois ou mais materiais."},
    
    {"codigo_bncc": "EF06CI02", "componente": "Ciencias", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Transformacoes quimicas",
     "habilidade_descricao": "Identificar evidencias de transformacoes quimicas a partir do resultado de misturas de materiais."},
    
    {"codigo_bncc": "EF06CI03", "componente": "Ciencias", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Celula",
     "habilidade_descricao": "Selecionar metodos mais adequados para a separacao de diferentes sistemas heterogeneos."},
    
    {"codigo_bncc": "EF06CI04", "componente": "Ciencias", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Sistema Solar",
     "habilidade_descricao": "Associar a producao de medicamentos e outros materiais sinteticos ao desenvolvimento cientifico e tecnologico."},

    # ============================================
    # CIENCIAS - 7º ANO
    # ============================================
    {"codigo_bncc": "EF07CI01", "componente": "Ciencias", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Maquinas simples",
     "habilidade_descricao": "Discutir a aplicacao, ao longo da historia, das maquinas simples e propor solucoes tecnologicas."},
    
    {"codigo_bncc": "EF07CI02", "componente": "Ciencias", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Calor e temperatura",
     "habilidade_descricao": "Diferenciar temperatura, calor e sensacao termica nas diferentes situacoes de equilibrio termodinamico cotidianas."},
    
    {"codigo_bncc": "EF07CI03", "componente": "Ciencias", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Ecossistemas",
     "habilidade_descricao": "Utilizar o conhecimento das formas de propagacao do calor para justificar a utilizacao de determinados materiais."},
    
    {"codigo_bncc": "EF07CI04", "componente": "Ciencias", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Reproducao",
     "habilidade_descricao": "Avaliar o papel do equilibrio termodinamico para a manutencao da vida na Terra."},

    # ============================================
    # CIENCIAS - 8º ANO
    # ============================================
    {"codigo_bncc": "EF08CI01", "componente": "Ciencias", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Fontes de energia",
     "habilidade_descricao": "Identificar e classificar diferentes fontes de energia e discutir o impacto ambiental de cada uma."},
    
    {"codigo_bncc": "EF08CI02", "componente": "Ciencias", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Sistema nervoso",
     "habilidade_descricao": "Construir circuitos eletricos com pilha/bateria, fios e lampada e reconhecer seu uso domestico."},
    
    {"codigo_bncc": "EF08CI03", "componente": "Ciencias", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Sistema endocrino",
     "habilidade_descricao": "Classificar equipamentos eletricos de uso domestico de acordo com tipo e uso."},
    
    {"codigo_bncc": "EF08CI04", "componente": "Ciencias", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Reproducao humana",
     "habilidade_descricao": "Calcular o consumo de eletrodomesticos a partir de dados de potencia e tempo medio de uso."},

    # ============================================
    # CIENCIAS - 9º ANO
    # ============================================
    {"codigo_bncc": "EF09CI01", "componente": "Ciencias", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Estrutura da materia",
     "habilidade_descricao": "Investigar as mudancas de estado fisico da materia e explicar essas transformacoes com base no modelo de constituicao submicroscopica."},
    
    {"codigo_bncc": "EF09CI02", "componente": "Ciencias", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Radiacao",
     "habilidade_descricao": "Comparar quantidades de reagentes e produtos envolvidos em transformacoes quimicas, estabelecendo a proporcao entre as suas massas."},
    
    {"codigo_bncc": "EF09CI03", "componente": "Ciencias", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Genetica",
     "habilidade_descricao": "Identificar modelos que descrevem a estrutura da materia e reconhecer sua evolucao historica."},
    
    {"codigo_bncc": "EF09CI04", "componente": "Ciencias", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Evolucao",
     "habilidade_descricao": "Planejar e executar experimentos que evidenciem que todas as cores de luz podem ser formadas pela composicao das tres cores primarias."},

    # ============================================
    # HISTORIA - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06HI01", "componente": "Historia", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Tempo e historia",
     "habilidade_descricao": "Identificar diferentes formas de compreensao da nocao de tempo e de periodizacao dos processos historicos."},
    
    {"codigo_bncc": "EF06HI02", "componente": "Historia", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Civilizacoes antigas",
     "habilidade_descricao": "Identificar a genesis da producao do saber historico e analisar o significado das fontes que originaram determinadas formas de registro."},
    
    {"codigo_bncc": "EF06HI03", "componente": "Historia", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Grecia antiga",
     "habilidade_descricao": "Identificar as hipoteses cientificas sobre o surgimento da especie humana e sua historicidade."},
    
    {"codigo_bncc": "EF06HI04", "componente": "Historia", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Roma antiga",
     "habilidade_descricao": "Conhecer as teorias sobre a origem do homem americano."},

    # ============================================
    # HISTORIA - 7º ANO
    # ============================================
    {"codigo_bncc": "EF07HI01", "componente": "Historia", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Idade Media",
     "habilidade_descricao": "Explicar o significado de 'modernidade' e suas logicas de inclusao e exclusao, com base em uma concepcao europeia."},
    
    {"codigo_bncc": "EF07HI02", "componente": "Historia", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Feudalismo",
     "habilidade_descricao": "Identificar conexoes e interacoes entre as sociedades do Novo Mundo, da Europa, da Africa e da Asia."},
    
    {"codigo_bncc": "EF07HI03", "componente": "Historia", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Grandes navegacoes",
     "habilidade_descricao": "Identificar aspectos e processos especificos das sociedades africanas e americanas antes da chegada dos europeus."},
    
    {"codigo_bncc": "EF07HI04", "componente": "Historia", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Colonizacao",
     "habilidade_descricao": "Identificar e relacionar as teorias religiosas e cientificas que embasaram as navegacoes europeias."},

    # ============================================
    # HISTORIA - 8º ANO
    # ============================================
    {"codigo_bncc": "EF08HI01", "componente": "Historia", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Revolucoes",
     "habilidade_descricao": "Identificar os principais aspectos conceituais do iluminismo e do liberalismo e discutir a relacao entre eles."},
    
    {"codigo_bncc": "EF08HI02", "componente": "Historia", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Independencias",
     "habilidade_descricao": "Identificar as particularidades politico-sociais da Inglaterra do seculo XVII e analisar os desdobramentos da Revolucao Inglesa."},
    
    {"codigo_bncc": "EF08HI03", "componente": "Historia", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Brasil Imperio",
     "habilidade_descricao": "Analisar os impactos da Revolucao Industrial na producao e circulacao de povos, produtos e culturas."},
    
    {"codigo_bncc": "EF08HI04", "componente": "Historia", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Abolicionismo",
     "habilidade_descricao": "Identificar e relacionar os processos da Revolucao Francesa e seus desdobramentos na Europa e no mundo."},

    # ============================================
    # HISTORIA - 9º ANO
    # ============================================
    {"codigo_bncc": "EF09HI01", "componente": "Historia", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Primeira Republica",
     "habilidade_descricao": "Descrever e contextualizar os principais aspectos sociais, culturais, economicos e politicos da emergencia da Republica no Brasil."},
    
    {"codigo_bncc": "EF09HI02", "componente": "Historia", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Era Vargas",
     "habilidade_descricao": "Caracterizar e compreender os ciclos da historia republicana, identificando particularidades da historia local e regional."},
    
    {"codigo_bncc": "EF09HI03", "componente": "Historia", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Ditadura militar",
     "habilidade_descricao": "Identificar os mecanismos de insercao dos negros na sociedade brasileira pos-abolicao e avaliar os seus resultados."},
    
    {"codigo_bncc": "EF09HI04", "componente": "Historia", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Redemocratizacao",
     "habilidade_descricao": "Discutir a importancia da participacao da populacao brasileira na Constituicao de 1988."},

    # ============================================
    # GEOGRAFIA - 6º ANO
    # ============================================
    {"codigo_bncc": "EF06GE01", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Orientacao e localizacao",
     "habilidade_descricao": "Comparar modificacoes das paisagens nos lugares de vivencia e os usos desses lugares em diferentes tempos."},
    
    {"codigo_bncc": "EF06GE02", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Cartografia",
     "habilidade_descricao": "Analisar modificacoes de paisagens por diferentes tipos de sociedade, com destaque para os povos originarios."},
    
    {"codigo_bncc": "EF06GE03", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Paisagem",
     "habilidade_descricao": "Descrever os movimentos do planeta e sua relacao com a circulacao geral da atmosfera."},
    
    {"codigo_bncc": "EF06GE04", "componente": "Geografia", "ano_escolar": "6 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Clima",
     "habilidade_descricao": "Identificar as caracteristicas das paisagens transformadas pelo trabalho humano a partir do desenvolvimento da agropecuaria."},

    # ============================================
    # GEOGRAFIA - 7º ANO
    # ============================================
    {"codigo_bncc": "EF07GE01", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 1, "dificuldade": "media",
     "objeto_conhecimento": "Brasil: territorio",
     "habilidade_descricao": "Avaliar, por meio de exemplos extraidos dos meios de comunicacao, ideias e estereotipos acerca das paisagens e da formacao territorial do Brasil."},
    
    {"codigo_bncc": "EF07GE02", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 2, "dificuldade": "media",
     "objeto_conhecimento": "Regioes brasileiras",
     "habilidade_descricao": "Analisar a influencia dos fluxos economicos e populacionais na formacao socioeconômica e territorial do Brasil."},
    
    {"codigo_bncc": "EF07GE03", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 3, "dificuldade": "media",
     "objeto_conhecimento": "Populacao brasileira",
     "habilidade_descricao": "Selecionar argumentos que reconhecam as territorilidades dos povos indigenas originarios, das comunidades quilombolas, tradicionais."},
    
    {"codigo_bncc": "EF07GE04", "componente": "Geografia", "ano_escolar": "7 ano", "trimestre_sugerido": 4, "dificuldade": "media",
     "objeto_conhecimento": "Urbanizacao brasileira",
     "habilidade_descricao": "Analisar a distribuicao territorial da populacao brasileira, considerando a diversidade etnico-cultural."},

    # ============================================
    # GEOGRAFIA - 8º ANO
    # ============================================
    {"codigo_bncc": "EF08GE01", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "America",
     "habilidade_descricao": "Descrever as rotas de dispersao da populacao humana pelo planeta e os principais fluxos migratorios em diferentes periodos da historia."},
    
    {"codigo_bncc": "EF08GE02", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Africa",
     "habilidade_descricao": "Relacionar fatos e situacoes representativas da historia das familias do Municipio em que se localiza a escola."},
    
    {"codigo_bncc": "EF08GE03", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Europa",
     "habilidade_descricao": "Analisar aspectos representativos da dinamica demografica, produtiva e urbano-industrial."},
    
    {"codigo_bncc": "EF08GE04", "componente": "Geografia", "ano_escolar": "8 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Asia",
     "habilidade_descricao": "Compreender os fluxos de migracao na America Latina e as principais politicas migratorias."},

    # ============================================
    # GEOGRAFIA - 9º ANO
    # ============================================
    {"codigo_bncc": "EF09GE01", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 1, "dificuldade": "alta",
     "objeto_conhecimento": "Globalizacao",
     "habilidade_descricao": "Analisar criticamente de que forma a hegemonia europeia foi exercida em varias regioes do planeta."},
    
    {"codigo_bncc": "EF09GE02", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 2, "dificuldade": "alta",
     "objeto_conhecimento": "Geopolitica mundial",
     "habilidade_descricao": "Analisar a atuacao das corporacoes internacionais e das organizacoes economicas mundiais na vida da populacao."},
    
    {"codigo_bncc": "EF09GE03", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 3, "dificuldade": "alta",
     "objeto_conhecimento": "Conflitos mundiais",
     "habilidade_descricao": "Identificar diferentes manifestacoes culturais de minorias etnicas como forma de compreender a multiplicidade cultural na escala mundial."},
    
    {"codigo_bncc": "EF09GE04", "componente": "Geografia", "ano_escolar": "9 ano", "trimestre_sugerido": 4, "dificuldade": "alta",
     "objeto_conhecimento": "Meio ambiente",
     "habilidade_descricao": "Relacionar diferenças de paisagens aos modos de viver de diferentes povos na Europa, Asia e Oceania."},
]


def importar_bncc_ef2():
    print("=" * 60)
    print("IMPORTANDO BNCC - ENSINO FUNDAMENTAL II (6 ao 9 ano)")
    print("=" * 60)
    
    with engine.connect() as conn:
        importados = 0
        atualizados = 0
        
        for hab in HABILIDADES_EF2:
            # Verificar se ja existe
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
        
        print(f"\nImportados: {importados}")
        print(f"Atualizados: {atualizados}")
        
        # Mostrar resumo
        print("\n" + "=" * 60)
        print("RESUMO POR ANO E COMPONENTE:")
        print("-" * 60)
        
        result = conn.execute(text("""
            SELECT ano_escolar, componente, COUNT(*) as total
            FROM curriculo_nacional
            WHERE ano_escolar LIKE '%ano%' AND ano_escolar NOT LIKE '%EM%'
            GROUP BY ano_escolar, componente
            ORDER BY ano_escolar, componente
        """))
        
        for row in result.fetchall():
            print(f"   {row[0]} - {row[1]}: {row[2]} habilidades")
    
    print("\n" + "=" * 60)
    print("IMPORTACAO CONCLUIDA!")
    print("=" * 60)


if __name__ == "__main__":
    importar_bncc_ef2()
