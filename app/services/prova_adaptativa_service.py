"""
Service de Geração de Provas Adaptativas (Reforço)
Gera provas focadas nos pontos fracos identificados pela análise qualitativa
"""
import anthropic
from typing import Dict, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.prova import Prova, QuestaoGerada, ProvaAluno, TipoQuestao, DificuldadeQuestao, StatusProva
from app.models.analise_qualitativa import AnaliseQualitativa
import json


class ProvaAdaptativaService:
    """
    Service para gerar provas de reforço baseadas em análise qualitativa
    """
    
    def __init__(self):
        self._client = None
        self.model = "claude-3-haiku-20240307"
    
    @property
    def client(self):
        """Lazy initialization do cliente Anthropic"""
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client
    
    def gerar_prova_reforco(
        self, 
        db: Session,
        prova_aluno_id: int,
        analise_id: int
    ) -> Prova:
        """
        Gera prova de reforço baseada na análise qualitativa
        
        Args:
            db: Sessão do banco
            prova_aluno_id: ID da prova original do aluno
            analise_id: ID da análise qualitativa
            
        Returns:
            Prova de reforço criada
        """
        
        # Buscar dados
        prova_aluno = db.query(ProvaAluno).filter(ProvaAluno.id == prova_aluno_id).first()
        if not prova_aluno:
            raise ValueError("Prova do aluno não encontrada")
        
        prova_original = prova_aluno.prova
        analise = db.query(AnaliseQualitativa).filter(AnaliseQualitativa.id == analise_id).first()
        if not analise:
            raise ValueError("Análise não encontrada")
        
        # Preparar prompt para IA
        prompt = self._criar_prompt_prova_reforco(prova_original, analise, prova_aluno)
        
        # Gerar questões com IA
        questoes_json = self._chamar_claude_api(prompt)
        
        # Criar prova de reforço
        prova_reforco = self._criar_prova_banco(
            db=db,
            prova_original=prova_original,
            analise=analise,
            questoes_json=questoes_json,
            criado_por_id=prova_original.criado_por_id
        )
        
        return prova_reforco
    
    def _criar_prompt_prova_reforco(
        self, 
        prova_original: Prova, 
        analise: AnaliseQualitativa,
        prova_aluno: ProvaAluno
    ) -> str:
        """Cria prompt para gerar prova de reforço"""
        
        conteudos_revisar = ", ".join(analise.conteudos_revisar) if analise.conteudos_revisar else "conteúdos gerais"
        
        prompt = f"""Você é um professor especialista criando uma PROVA DE REFORÇO personalizada.

**CONTEXTO:**
O aluno acabou de fazer uma prova de {prova_original.materia} e teve dificuldades específicas.
A análise da IA identificou os seguintes pontos fracos que precisam de reforço:

**CONTEÚDOS QUE O ALUNO PRECISA MELHORAR:**
{chr(10).join([f"• {conteudo}" for conteudo in analise.conteudos_revisar])}

**PONTOS FRACOS IDENTIFICADOS:**
{analise.pontos_fracos}

**NÍVEL DE DOMÍNIO:** {analise.nivel_dominio}

**ÁREAS PRIORITÁRIAS:**
{chr(10).join([f"• {area}" for area in analise.areas_prioridade])}

---

**SUA MISSÃO:**
Crie uma PROVA DE REFORÇO com EXATAMENTE {prova_original.quantidade_questoes} questões focadas ESPECIFICAMENTE nos conteúdos que o aluno precisa melhorar.

**REQUISITOS OBRIGATÓRIOS:**
1. Todas as questões devem ser de múltipla escolha (A, B, C, D)
2. Total de questões: EXATAMENTE {prova_original.quantidade_questoes}
3. Focar APENAS nos conteúdos listados acima
4. Dificuldade: Começar FÁCIL para dar confiança, depois aumentar gradualmente
5. Cada questão deve ter explicação pedagógica clara
6. Série/Nível: {prova_original.serie_nivel}

**DISTRIBUIÇÃO DE DIFICULDADE:**
- 40% Fácil (para dar confiança)
- 40% Médio (consolidar conhecimento)
- 20% Difícil (desafiar o aluno)

**FORMATO DE SAÍDA:**
Responda APENAS com JSON válido (sem markdown, sem ```json):

{{
  "questoes": [
    {{
      "numero": 1,
      "enunciado": "Texto da questão focada no conteúdo fraco",
      "opcoes": [
        "A) Opção 1",
        "B) Opção 2", 
        "C) Opção 3",
        "D) Opção 4"
      ],
      "resposta_correta": "A",
      "dificuldade": "facil",
      "explicacao": "Explicação pedagógica da resposta",
      "tags": ["Conteúdo 1", "Conceito específico"]
    }},
    ... (repetir para todas as {prova_original.quantidade_questoes} questões)
  ]
}}

**IMPORTANTE:**
- Use linguagem clara e pedagógica
- Cada questão deve reforçar os conteúdos fracos identificados
- As tags devem indicar exatamente qual conteúdo está sendo trabalhado
- A explicação deve ajudar o aluno a entender o conceito
- Distribua as questões entre os diferentes conteúdos fracos
- NUNCA use caracteres especiais ou quebras de linha dentro das strings JSON

Gere a prova de reforço agora:
"""
        
        return prompt
    
    def _chamar_claude_api(self, prompt: str) -> str:
        """Chama Claude API para gerar questões"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            raise Exception(f"Erro ao chamar Claude API: {str(e)}")
    
    def _criar_prova_banco(
        self,
        db: Session,
        prova_original: Prova,
        analise: AnaliseQualitativa,
        questoes_json: str,
        criado_por_id: int
    ) -> Prova:
        """Cria prova de reforço no banco de dados - OTIMIZADO com commits incrementais"""
        
        # Parse JSON
        try:
            # Limpar resposta
            questoes_json_limpo = questoes_json.strip()
            if questoes_json_limpo.startswith('```json'):
                questoes_json_limpo = questoes_json_limpo[7:]
            if questoes_json_limpo.startswith('```'):
                questoes_json_limpo = questoes_json_limpo[3:]
            if questoes_json_limpo.endswith('```'):
                questoes_json_limpo = questoes_json_limpo[:-3]
            questoes_json_limpo = questoes_json_limpo.strip()
            
            dados = json.loads(questoes_json_limpo)
            questoes = dados.get('questoes', [])
            
            if not questoes:
                raise ValueError("Nenhuma questão foi gerada")
            
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao processar JSON da IA: {str(e)}\nResposta: {questoes_json[:500]}")
        
        # Criar título da prova
        conteudos_str = ", ".join(analise.conteudos_revisar[:3]) if analise.conteudos_revisar else "Conteúdos Gerais"
        if len(conteudos_str) > 80:
            conteudos_str = conteudos_str[:77] + "..."
        
        titulo = f"🎯 Reforço: {conteudos_str}"
        
        # OTIMIZAÇÃO 1: Criar prova PRIMEIRO e fazer commit
        nova_prova = Prova(
            titulo=titulo,
            descricao=f"Prova de reforço gerada automaticamente para melhorar nos conteúdos: {', '.join(analise.conteudos_revisar)}. Baseada na análise da prova '{prova_original.titulo}'.",
            conteudo_prompt=f"Prova de reforço focada em: {', '.join(analise.conteudos_revisar)}",
            materia=prova_original.materia,
            serie_nivel=prova_original.serie_nivel,
            quantidade_questoes=len(questoes),
            tipo_questao=TipoQuestao.MULTIPLA_ESCOLHA,
            dificuldade=DificuldadeQuestao.MEDIO,
            tempo_limite_minutos=prova_original.tempo_limite_minutos,
            pontuacao_total=float(len(questoes) * 0.5),  # 0.5 pontos por questão
            nota_minima_aprovacao=prova_original.nota_minima_aprovacao,
            status=StatusProva.ATIVA,
            criado_por_id=criado_por_id
        )
        
        db.add(nova_prova)
        db.commit()  # COMMIT 1: Salva a prova primeiro
        db.refresh(nova_prova)
        
        # OTIMIZAÇÃO 2: Criar questões em LOTES PEQUENOS com commits incrementais
        dificuldade_map = {
            'facil': DificuldadeQuestao.FACIL,
            'medio': DificuldadeQuestao.MEDIO,
            'dificil': DificuldadeQuestao.DIFICIL,
            'muito_dificil': DificuldadeQuestao.MUITO_DIFICIL
        }
        
        lote_tamanho = 2  # Inserir 2 questões por vez
        
        for i in range(0, len(questoes), lote_tamanho):
            lote = questoes[i:i+lote_tamanho]
            
            for q_data in lote:
                questao = QuestaoGerada(
                    prova_id=nova_prova.id,
                    numero=q_data.get('numero'),
                    enunciado=q_data.get('enunciado'),
                    tipo=TipoQuestao.MULTIPLA_ESCOLHA,
                    dificuldade=dificuldade_map.get(q_data.get('dificuldade', 'medio'), DificuldadeQuestao.MEDIO),
                    opcoes=q_data.get('opcoes', []),
                    resposta_correta=q_data.get('resposta_correta'),
                    explicacao=q_data.get('explicacao'),
                    tags=q_data.get('tags', []),
                    pontuacao=0.5
                )
                
                db.add(questao)
            
            # COMMIT após cada lote de 2 questões
            db.commit()
        
        db.refresh(nova_prova)
        
        return nova_prova
    
    def associar_prova_ao_aluno(
        self,
        db: Session,
        prova_id: int,
        aluno_id: int
    ) -> ProvaAluno:
        """Associa prova de reforço ao aluno"""
        
        from app.models.prova import StatusProvaAluno
        from datetime import datetime
        
        prova_aluno = ProvaAluno(
            prova_id=prova_id,
            aluno_id=aluno_id,
            status=StatusProvaAluno.PENDENTE,
            data_atribuicao=datetime.utcnow()
        )
        
        db.add(prova_aluno)
        db.commit()
        db.refresh(prova_aluno)
        
        return prova_aluno


# Instância global
prova_adaptativa_service = ProvaAdaptativaService()
