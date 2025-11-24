"""
🎓 AdaptAI - Models de Prova
Sistema de geração de provas com IA
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class StatusProva(str, enum.Enum):
    """Status da prova"""
    RASCUNHO = "rascunho"  # Prova sendo criada
    ATIVA = "ativa"  # Prova disponível para uso
    ARQUIVADA = "arquivada"  # Prova arquivada


class DificuldadeQuestao(str, enum.Enum):
    """Nível de dificuldade da questão"""
    FACIL = "facil"
    MEDIO = "medio"
    DIFICIL = "dificil"
    MUITO_DIFICIL = "muito_dificil"


class TipoQuestao(str, enum.Enum):
    """Tipo da questão"""
    MULTIPLA_ESCOLHA = "multipla_escolha"
    VERDADEIRO_FALSO = "verdadeiro_falso"
    DISSERTATIVA = "dissertativa"
    LACUNAS = "lacunas"


class StatusProvaAluno(str, enum.Enum):
    """Status da prova do aluno"""
    PENDENTE = "pendente"  # Ainda não iniciou
    EM_ANDAMENTO = "em_andamento"  # Começou mas não terminou
    CONCLUIDA = "concluida"  # Terminou
    CORRIGIDA = "corrigida"  # Já foi corrigida


class Prova(Base):
    """
    📝 Modelo de Prova
    Prova criada pelo administrador com ajuda da IA
    """
    __tablename__ = "provas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False, index=True)
    descricao = Column(Text)
    
    # Configuração da geração
    conteudo_prompt = Column(Text, nullable=False)  # Prompt usado para gerar as questões
    materia = Column(String(100), nullable=False)
    serie_nivel = Column(String(50))
    quantidade_questoes = Column(Integer, nullable=False, default=20)
    
    # Tipo e dificuldade
    tipo_questao = Column(SQLEnum(TipoQuestao), default=TipoQuestao.MULTIPLA_ESCOLHA)
    dificuldade = Column(SQLEnum(DificuldadeQuestao), default=DificuldadeQuestao.MEDIO)
    
    # Configurações da prova
    tempo_limite_minutos = Column(Integer)  # Tempo limite em minutos (opcional)
    pontuacao_total = Column(Float, default=10.0)
    nota_minima_aprovacao = Column(Float, default=6.0)
    
    # Status e datas
    status = Column(SQLEnum(StatusProva), default=StatusProva.RASCUNHO)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Quem criou
    criado_por_id = Column(Integer, ForeignKey('users.id'))
    criado_por = relationship("User", back_populates="provas_criadas")
    
    # Relacionamentos
    questoes = relationship("QuestaoGerada", back_populates="prova", cascade="all, delete-orphan")
    provas_alunos = relationship("ProvaAluno", back_populates="prova", cascade="all, delete-orphan")


class QuestaoGerada(Base):
    """
    ❓ Modelo de Questão Gerada pela IA
    Questões criadas automaticamente pela Claude API
    """
    __tablename__ = "questoes_geradas"

    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey('provas.id'), nullable=False)
    
    # Dados da questão
    numero = Column(Integer, nullable=False)  # Número da questão (1, 2, 3...)
    enunciado = Column(Text, nullable=False)
    tipo = Column(SQLEnum(TipoQuestao), nullable=False)
    dificuldade = Column(SQLEnum(DificuldadeQuestao))
    
    # Para múltipla escolha / verdadeiro-falso
    opcoes = Column(JSON)  # Lista de opções: ["A) ...", "B) ...", "C) ...", "D) ..."]
    resposta_correta = Column(String(500))  # Resposta correta
    
    # Para questões dissertativas
    criterios_avaliacao = Column(JSON)  # Critérios de correção
    
    # Metadados
    pontuacao = Column(Float, default=0.5)  # Pontos que vale a questão
    explicacao = Column(Text)  # Explicação da resposta correta
    tags = Column(JSON)  # Tags/tópicos abordados
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    prova = relationship("Prova", back_populates="questoes")
    respostas = relationship("RespostaAluno", back_populates="questao", cascade="all, delete-orphan")


class ProvaAluno(Base):
    """
    👨‍🎓 Modelo de Associação Prova-Aluno
    Quando o admin associa uma prova a um aluno
    """
    __tablename__ = "provas_alunos"

    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey('provas.id'), nullable=False)
    aluno_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    
    # Status e datas
    status = Column(SQLEnum(StatusProvaAluno), default=StatusProvaAluno.PENDENTE)
    data_atribuicao = Column(DateTime, default=datetime.utcnow)
    data_inicio = Column(DateTime)  # Quando o aluno começou
    data_conclusao = Column(DateTime)  # Quando o aluno terminou
    data_correcao = Column(DateTime)  # Quando foi corrigida
    
    # Pontuação
    pontuacao_obtida = Column(Float)
    pontuacao_maxima = Column(Float)
    nota_final = Column(Float)  # Nota de 0 a 10
    aprovado = Column(Boolean)
    
    # Tempo gasto
    tempo_gasto_minutos = Column(Integer)
    
    # Análise da IA
    analise_ia = Column(JSON)  # Análise do desempenho gerada pela IA
    feedback_ia = Column(Text)  # Feedback personalizado
    
    # Relacionamentos
    prova = relationship("Prova", back_populates="provas_alunos")
    aluno = relationship("Student", back_populates="provas")
    respostas = relationship("RespostaAluno", back_populates="prova_aluno", cascade="all, delete-orphan")


class RespostaAluno(Base):
    """
    ✍️ Modelo de Resposta do Aluno
    Respostas dadas pelo aluno em cada questão
    """
    __tablename__ = "respostas_alunos"

    id = Column(Integer, primary_key=True, index=True)
    prova_aluno_id = Column(Integer, ForeignKey('provas_alunos.id'), nullable=False)
    questao_id = Column(Integer, ForeignKey('questoes_geradas.id'), nullable=False)
    
    # Resposta
    resposta_aluno = Column(Text)  # Resposta dada pelo aluno
    esta_correta = Column(Boolean)  # Se está correta ou não
    
    # Pontuação
    pontuacao_obtida = Column(Float)  # Pontos obtidos nesta questão
    pontuacao_maxima = Column(Float)  # Pontos máximos possíveis
    
    # Feedback
    feedback = Column(Text)  # Feedback específico da questão
    
    # Tempo
    tempo_resposta_segundos = Column(Integer)  # Tempo que levou para responder
    respondido_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    prova_aluno = relationship("ProvaAluno", back_populates="respostas")
    questao = relationship("QuestaoGerada", back_populates="respostas")
