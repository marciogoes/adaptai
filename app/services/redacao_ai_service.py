"""
📝 AdaptAI - Serviço de IA para Redações ENEM
Geração de temas atuais e correção por competências
"""
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from app.core.config import settings

# Inicializar cliente Anthropic
anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
_MODELO_IA = settings.CLAUDE_MODEL or "claude-3-5-sonnet-20241022"


class RedacaoAIService:
    """
    Serviço de IA para redações no estilo ENEM
    """
    
    COMPETENCIAS_ENEM = {
        1: {
            "nome": "Domínio da Norma Culta",
            "descricao": "Demonstrar domínio da modalidade escrita formal da língua portuguesa",
            "criterios": [
                "Ortografia e acentuação",
                "Concordância verbal e nominal",
                "Regência verbal e nominal",
                "Pontuação",
                "Colocação pronominal",
                "Uso de crase"
            ]
        },
        2: {
            "nome": "Compreensão da Proposta",
            "descricao": "Compreender a proposta de redação e aplicar conceitos das várias áreas de conhecimento para desenvolver o tema, dentro dos limites estruturais do texto dissertativo-argumentativo em prosa",
            "criterios": [
                "Atendimento ao tema proposto",
                "Estrutura dissertativo-argumentativa",
                "Uso de repertório sociocultural",
                "Autoria e originalidade"
            ]
        },
        3: {
            "nome": "Argumentação",
            "descricao": "Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista",
            "criterios": [
                "Seleção de argumentos",
                "Consistência argumentativa",
                "Organização das ideias",
                "Progressão temática"
            ]
        },
        4: {
            "nome": "Coesão Textual",
            "descricao": "Demonstrar conhecimento dos mecanismos linguísticos necessários para a construção da argumentação",
            "criterios": [
                "Uso de conectivos",
                "Referenciação",
                "Articulação entre parágrafos",
                "Sequenciação lógica"
            ]
        },
        5: {
            "nome": "Proposta de Intervenção",
            "descricao": "Elaborar proposta de intervenção para o problema abordado, respeitando os direitos humanos",
            "criterios": [
                "Ação (O que fazer)",
                "Agente (Quem vai fazer)",
                "Modo/Meio (Como fazer)",
                "Efeito/Finalidade (Para que)",
                "Detalhamento de um dos elementos",
                "Respeito aos direitos humanos"
            ]
        }
    }
    
    NIVEIS_NOTA = [
        (200, "Excelente"),
        (160, "Bom"),
        (120, "Mediano"),
        (80, "Insuficiente"),
        (40, "Precário"),
        (0, "Zero")
    ]
    
    def _classificar_nivel(self, nota: int) -> str:
        """Classifica o nível baseado na nota"""
        for limite, nivel in self.NIVEIS_NOTA:
            if nota >= limite:
                return nivel
        return "Zero"
    
    def _classificar_nivel_geral(self, nota_final: int) -> str:
        """Classifica nível geral (0-1000)"""
        if nota_final >= 900:
            return "Excelente"
        elif nota_final >= 700:
            return "Muito Bom"
        elif nota_final >= 500:
            return "Bom"
        elif nota_final >= 300:
            return "Regular"
        else:
            return "Insuficiente"

    async def gerar_tema_atual(
        self,
        area_tematica: Optional[str] = None,
        nivel_dificuldade: str = "medio"
    ) -> Dict[str, Any]:
        """
        Gera um tema de redação ATUAL usando IA
        A IA escolhe um tema relevante e contemporâneo
        """
        
        areas = area_tematica or "qualquer área relevante (tecnologia, meio ambiente, sociedade, saúde, educação, cultura)"
        
        prompt = f"""Você é um especialista em elaboração de provas do ENEM. Crie um tema de redação ATUAL e RELEVANTE para o Brasil em {datetime.now().year}.

ÁREA TEMÁTICA: {areas}
NÍVEL DE DIFICULDADE: {nivel_dificuldade}

O tema deve:
1. Ser ATUAL e relevante para a sociedade brasileira
2. Permitir argumentação de diferentes perspectivas
3. Exigir proposta de intervenção social
4. Estar no formato do ENEM

Responda APENAS com um JSON válido no seguinte formato:
{{
    "titulo": "Título do tema em formato de frase (ex: 'Os desafios da educação digital no Brasil')",
    "tema": "Descrição detalhada do tema e seu contexto social",
    "proposta": "A partir da leitura dos textos motivadores e com base nos conhecimentos construídos ao longo de sua formação, redija texto dissertativo-argumentativo em modalidade escrita formal da língua portuguesa sobre o tema [TEMA], apresentando proposta de intervenção que respeite os direitos humanos. Selecione, organize e relacione, de forma coerente e coesa, argumentos e fatos para defesa de seu ponto de vista.",
    "texto_motivador_1": "Primeiro texto motivador (citação, dado estatístico ou trecho de reportagem REAL e ATUAL)",
    "texto_motivador_2": "Segundo texto motivador (perspectiva diferente sobre o tema)",
    "texto_motivador_3": "Terceiro texto motivador (pode ser um dado numérico ou infográfico descrito)",
    "texto_motivador_4": "Quarto texto motivador (opcional, pode ser null)",
    "area_tematica": "Nome da área (ex: 'Tecnologia e Sociedade')",
    "palavras_chave": ["palavra1", "palavra2", "palavra3"]
}}

IMPORTANTE: 
- Use dados e referências REAIS e ATUAIS
- O tema deve ser algo que está em discussão na sociedade brasileira AGORA
- Os textos motivadores devem parecer autênticos (com fontes citadas)
"""

        try:
            response = anthropic_client.messages.create(
                model=_MODELO_IA,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extrair JSON da resposta
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                tema_data = json.loads(json_match.group())
                tema_data["nivel_dificuldade"] = nivel_dificuldade
                return tema_data
            else:
                raise ValueError("Resposta da IA não contém JSON válido")
                
        except Exception as e:
            print(f"[ERRO] Erro ao gerar tema: {e}")
            raise

    async def corrigir_redacao_enem(
        self,
        texto_redacao: str,
        tema: Dict[str, Any],
        aluno_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Corrige redação no padrão ENEM com as 5 competências
        Retorna notas de 0-200 por competência e feedback detalhado
        """
        
        # Contar linhas e palavras
        linhas = texto_redacao.strip().split('\n')
        quantidade_linhas = len([l for l in linhas if l.strip()])
        quantidade_palavras = len(texto_redacao.split())
        
        # Verificar se está muito curta
        if quantidade_palavras < 50:
            return self._redacao_anulada("Texto muito curto (menos de 50 palavras)")
        
        # Preparar contexto do aluno
        contexto_aluno = ""
        if aluno_info:
            contexto_aluno = f"""
INFORMAÇÕES DO ALUNO:
- Nome: {aluno_info.get('nome', 'Não informado')}
- Série: {aluno_info.get('serie', 'Não informada')}
- Diagnóstico: {aluno_info.get('diagnostico', 'Nenhum')}

Considere o nível escolar e possíveis necessidades especiais ao dar feedback (seja encorajador mas honesto).
"""

        prompt = f"""Você é um corretor oficial do ENEM com vasta experiência. Corrija a redação abaixo seguindo RIGOROSAMENTE os critérios do ENEM.

{contexto_aluno}

=== TEMA DA REDAÇÃO ===
TÍTULO: {tema.get('titulo', '')}
TEMA: {tema.get('tema', '')}
PROPOSTA: {tema.get('proposta', '')}

TEXTOS MOTIVADORES:
1. {tema.get('texto_motivador_1', 'Não fornecido')}
2. {tema.get('texto_motivador_2', 'Não fornecido')}
3. {tema.get('texto_motivador_3', 'Não fornecido')}

=== REDAÇÃO DO ALUNO ===
{texto_redacao}

=== INSTRUÇÕES DE CORREÇÃO ===
Analise a redação nas 5 COMPETÊNCIAS do ENEM. Cada competência vale de 0 a 200 pontos (em múltiplos de 40: 0, 40, 80, 120, 160, 200).

COMPETÊNCIA 1 - Domínio da norma culta:
- Ortografia, acentuação, concordância, regência, pontuação

COMPETÊNCIA 2 - Compreensão da proposta:
- Atendimento ao tema, estrutura dissertativo-argumentativa, repertório sociocultural

COMPETÊNCIA 3 - Argumentação:
- Seleção de argumentos, consistência, organização, progressão

COMPETÊNCIA 4 - Coesão textual:
- Conectivos, referenciação, articulação entre parágrafos

COMPETÊNCIA 5 - Proposta de intervenção:
- Deve ter: AÇÃO + AGENTE + MODO + EFEITO + DETALHAMENTO
- Deve respeitar direitos humanos

Responda APENAS com um JSON válido:
{{
    "nota_competencia_1": <0-200>,
    "feedback_competencia_1": "Feedback detalhado da competência 1",
    "nota_competencia_2": <0-200>,
    "feedback_competencia_2": "Feedback detalhado da competência 2",
    "nota_competencia_3": <0-200>,
    "feedback_competencia_3": "Feedback detalhado da competência 3",
    "nota_competencia_4": <0-200>,
    "feedback_competencia_4": "Feedback detalhado da competência 4",
    "nota_competencia_5": <0-200>,
    "feedback_competencia_5": "Feedback detalhado da competência 5",
    "feedback_geral": "Análise geral da redação em 2-3 parágrafos",
    "pontos_fortes": ["ponto forte 1", "ponto forte 2", "ponto forte 3"],
    "pontos_melhoria": ["ponto a melhorar 1", "ponto a melhorar 2", "ponto a melhorar 3"],
    "sugestoes": ["sugestão de estudo 1", "sugestão de estudo 2"]
}}

IMPORTANTE:
- Seja JUSTO mas RIGOROSO como um corretor real do ENEM
- O feedback deve ser EDUCATIVO e CONSTRUTIVO
- Aponte erros específicos com exemplos do texto
- Dê sugestões práticas de melhoria
"""

        try:
            response = anthropic_client.messages.create(
                model=_MODELO_IA,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extrair JSON
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                correcao = json.loads(json_match.group())
                
                # Calcular nota final
                nota_final = (
                    correcao.get("nota_competencia_1", 0) +
                    correcao.get("nota_competencia_2", 0) +
                    correcao.get("nota_competencia_3", 0) +
                    correcao.get("nota_competencia_4", 0) +
                    correcao.get("nota_competencia_5", 0)
                )
                
                correcao["nota_final"] = nota_final
                correcao["quantidade_linhas"] = quantidade_linhas
                correcao["quantidade_palavras"] = quantidade_palavras
                correcao["nivel_geral"] = self._classificar_nivel_geral(nota_final)
                
                # Adicionar níveis por competência
                for i in range(1, 6):
                    nota = correcao.get(f"nota_competencia_{i}", 0)
                    correcao[f"nivel_competencia_{i}"] = self._classificar_nivel(nota)
                
                return correcao
            else:
                raise ValueError("Resposta da IA não contém JSON válido")
                
        except Exception as e:
            print(f"[ERRO] Erro ao corrigir redação: {e}")
            raise

    def _redacao_anulada(self, motivo: str) -> Dict[str, Any]:
        """Retorna estrutura de redação anulada"""
        return {
            "nota_competencia_1": 0,
            "nota_competencia_2": 0,
            "nota_competencia_3": 0,
            "nota_competencia_4": 0,
            "nota_competencia_5": 0,
            "nota_final": 0,
            "feedback_competencia_1": motivo,
            "feedback_competencia_2": motivo,
            "feedback_competencia_3": motivo,
            "feedback_competencia_4": motivo,
            "feedback_competencia_5": motivo,
            "feedback_geral": f"Redação anulada: {motivo}",
            "pontos_fortes": [],
            "pontos_melhoria": [motivo],
            "sugestoes": ["Reescreva a redação com atenção aos requisitos mínimos"],
            "nivel_geral": "Anulada",
            "anulada": True,
            "motivo_anulacao": motivo
        }


# Instância global do serviço
redacao_ai_service = RedacaoAIService()
