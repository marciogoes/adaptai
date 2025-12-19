-- ============================================================================
-- MIGRATION: Sistema Completo de PEI, Laudos e Avaliações Diagnósticas
-- AdaptAI - Plataforma de Educação Inclusiva
-- ============================================================================

-- ============================================================================
-- 1. FOTOS DE ESTUDANTES
-- ============================================================================

ALTER TABLE students 
ADD COLUMN foto_url VARCHAR(500) NULL AFTER email,
ADD COLUMN foto_upload_date TIMESTAMP NULL,
ADD COLUMN foto_uploaded_by INT NULL,
ADD COLUMN foto_consentimento BOOLEAN DEFAULT FALSE,
ADD COLUMN foto_consentimento_data TIMESTAMP NULL,
ADD COLUMN foto_consentimento_responsavel VARCHAR(255) NULL;

CREATE INDEX idx_students_foto ON students(foto_url);

ALTER TABLE students 
ADD CONSTRAINT fk_foto_uploaded_by 
FOREIGN KEY (foto_uploaded_by) REFERENCES users(id);

-- Histórico de fotos
CREATE TABLE student_photos_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    foto_url VARCHAR(500),
    uploaded_by INT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo_alteracao VARCHAR(255),
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    INDEX idx_student_photos (student_id, uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. SISTEMA DE LAUDOS
-- ============================================================================

CREATE TABLE laudos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    uploaded_by INT NOT NULL,
    
    -- Arquivo
    arquivo_nome VARCHAR(255),
    arquivo_path VARCHAR(500),
    arquivo_size INT,
    arquivo_hash VARCHAR(64),
    
    -- Identificação automática pela IA
    tipo_laudo ENUM(
        'neuropsicologico',
        'psicopedagogico',
        'fonoaudiologico',
        'terapia_ocupacional',
        'psiquiatrico',
        'neurologico',
        'psicologico',
        'outro'
    ),
    tipo_confianca DECIMAL(3,2),
    
    -- Dados extraídos pela IA
    profissional_nome VARCHAR(255),
    profissional_especialidade VARCHAR(255),
    profissional_crp_crm VARCHAR(50),
    data_avaliacao DATE,
    data_emissao DATE,
    
    -- Diagnósticos identificados
    diagnosticos JSON,
    
    -- Conteúdo extraído e estruturado
    texto_completo TEXT,
    resumo_ia TEXT,
    pontos_fortes JSON,
    dificuldades JSON,
    recomendacoes JSON,
    observacoes_relevantes TEXT,
    
    -- Análise da IA
    ia_analise_completa JSON,
    ia_areas_prioritarias JSON,
    ia_sugestoes_pei JSON,
    
    -- Processamento
    status_processamento ENUM('pendente', 'processando', 'concluido', 'erro') DEFAULT 'pendente',
    erro_processamento TEXT,
    processado_em TIMESTAMP NULL,
    
    -- Visibilidade
    visivel_para_pais BOOLEAN DEFAULT FALSE,
    compartilhado_com JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id),
    
    INDEX idx_student (student_id),
    INDEX idx_tipo (tipo_laudo),
    INDEX idx_data_avaliacao (data_avaliacao),
    INDEX idx_status (status_processamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Recomendações dos laudos
CREATE TABLE laudo_recomendacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    laudo_id INT NOT NULL,
    
    categoria ENUM('academica', 'terapeutica', 'familiar', 'adaptacao', 'outra'),
    texto_original TEXT,
    texto_normalizado TEXT,
    
    prioridade ENUM('alta', 'media', 'baixa'),
    area_foco VARCHAR(100),
    
    -- Implementação
    status_implementacao ENUM(
        'nao_implementada',
        'em_planejamento',
        'parcialmente_implementada',
        'implementada',
        'nao_aplicavel'
    ) DEFAULT 'nao_implementada',
    
    objetivo_pei_id INT NULL,
    data_implementacao DATE NULL,
    observacoes_implementacao TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (laudo_id) REFERENCES laudos(id) ON DELETE CASCADE,
    
    INDEX idx_status (status_implementacao),
    INDEX idx_prioridade (prioridade)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Evolução entre laudos
CREATE TABLE laudo_evolucao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    
    laudo_anterior_id INT NULL,
    laudo_atual_id INT NOT NULL,
    
    tipo_mudanca ENUM('melhora', 'estavel', 'regressao', 'novo_diagnostico'),
    area_mudanca VARCHAR(100),
    descricao_mudanca TEXT,
    
    ia_analise_comparativa JSON,
    pontos_atencao JSON,
    sugestoes_ajuste_pei JSON,
    
    analisado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (laudo_anterior_id) REFERENCES laudos(id) ON DELETE SET NULL,
    FOREIGN KEY (laudo_atual_id) REFERENCES laudos(id) ON DELETE CASCADE,
    
    INDEX idx_student (student_id),
    INDEX idx_tipo_mudanca (tipo_mudanca)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. CURRÍCULO E PRÉ-REQUISITOS
-- ============================================================================

CREATE TABLE curriculo_nacional (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    codigo_bncc VARCHAR(20) UNIQUE,
    ano_escolar VARCHAR(10),
    componente VARCHAR(50),
    
    campo_experiencia VARCHAR(100),
    eixo_tematico VARCHAR(100),
    
    habilidade_codigo VARCHAR(20),
    habilidade_descricao TEXT,
    objeto_conhecimento TEXT,
    
    exemplos_atividades JSON,
    prerequisitos JSON,
    
    dificuldade ENUM('fundamental', 'intermediario', 'avancado'),
    trimestre_sugerido INT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_ano_componente (ano_escolar, componente),
    INDEX idx_codigo_bncc (codigo_bncc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE curriculo_escola (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    curriculo_nacional_id INT NULL,
    
    ano_escolar VARCHAR(10),
    disciplina VARCHAR(50),
    unidade_tematica VARCHAR(100),
    
    titulo VARCHAR(255),
    descricao TEXT,
    objetivos_aprendizagem JSON,
    
    periodo ENUM('bimestre_1', 'bimestre_2', 'bimestre_3', 'bimestre_4'),
    carga_horaria_estimada INT,
    
    materiais_necessarios JSON,
    avaliacoes_sugeridas JSON,
    
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (curriculo_nacional_id) REFERENCES curriculo_nacional(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE mapeamento_prerequisitos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    
    habilidade_codigo VARCHAR(20),
    habilidade_titulo VARCHAR(255),
    ano_escolar VARCHAR(10),
    
    prerequisito_codigo VARCHAR(20),
    prerequisito_titulo VARCHAR(255),
    ano_prerequisito VARCHAR(10),
    
    essencial BOOLEAN DEFAULT TRUE,
    peso DECIMAL(3,2) DEFAULT 1.0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_habilidade (habilidade_codigo),
    INDEX idx_prerequisito (prerequisito_codigo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. AVALIAÇÕES DIAGNÓSTICAS
-- ============================================================================

CREATE TABLE avaliacoes_diagnosticas_rapidas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    
    ano_escolar_aluno VARCHAR(10),
    avalia_ciclos JSON,
    
    gerada_por_ia BOOLEAN DEFAULT TRUE,
    gerada_por INT,
    gerada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    status ENUM('rascunho', 'pronta', 'em_andamento', 'concluida', 'cancelada') DEFAULT 'rascunho',
    iniciada_em TIMESTAMP NULL,
    concluida_em TIMESTAMP NULL,
    tempo_total_minutos INT,
    
    adaptativa BOOLEAN DEFAULT TRUE,
    tempo_limite_minutos INT DEFAULT 30,
    
    adaptacoes_aplicadas JSON,
    resultado_geral JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (gerada_por) REFERENCES users(id),
    
    INDEX idx_student (student_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE questoes_diagnosticas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    avaliacao_id INT NOT NULL,
    
    ordem INT,
    
    area VARCHAR(50),
    subarea VARCHAR(100),
    habilidade_bncc VARCHAR(20),
    ano_referencia VARCHAR(10),
    
    tipo_questao ENUM('multipla_escolha', 'verdadeiro_falso', 'ordenacao', 'associacao', 'resposta_curta'),
    enunciado TEXT,
    contexto_visual TEXT,
    
    opcoes JSON,
    resposta_correta JSON,
    
    dificuldade ENUM('basico', 'intermediario', 'avancado'),
    adaptacoes_visuais JSON,
    
    gerada_por_ia BOOLEAN DEFAULT TRUE,
    prompt_geracao TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (avaliacao_id) REFERENCES avaliacoes_diagnosticas_rapidas(id) ON DELETE CASCADE,
    INDEX idx_avaliacao (avaliacao_id),
    INDEX idx_area (area)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE respostas_diagnosticas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    avaliacao_id INT NOT NULL,
    questao_id INT NOT NULL,
    student_id INT NOT NULL,
    
    resposta_dada JSON,
    correta BOOLEAN,
    tempo_resposta_segundos INT,
    
    tentativas INT DEFAULT 1,
    ajuda_solicitada BOOLEAN DEFAULT FALSE,
    
    respondida_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (avaliacao_id) REFERENCES avaliacoes_diagnosticas_rapidas(id) ON DELETE CASCADE,
    FOREIGN KEY (questao_id) REFERENCES questoes_diagnosticas(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    
    INDEX idx_avaliacao (avaliacao_id),
    INDEX idx_student (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 5. SISTEMA DE PEI
-- ============================================================================

CREATE TABLE peis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    created_by INT NOT NULL,
    
    ano_letivo VARCHAR(10),
    tipo_periodo ENUM('anual', 'semestral') DEFAULT 'anual',
    semestre INT NULL,
    
    data_inicio DATE,
    data_fim DATE,
    data_proxima_revisao DATE,
    
    -- Dados consolidados do perfil
    diagnosticos JSON,
    pontos_fortes JSON,
    desafios JSON,
    estilo_aprendizagem JSON,
    desempenho_atual JSON,
    adaptacoes_atuais JSON,
    contexto_familiar TEXT,
    
    -- Vinculação com avaliação diagnóstica
    avaliacao_diagnostica_id INT NULL,
    baseline_estabelecido BOOLEAN DEFAULT FALSE,
    
    -- Sugestões originais da IA
    ia_sugestoes_originais JSON,
    
    status ENUM('rascunho', 'ativo', 'em_revisao', 'concluido', 'arquivado') DEFAULT 'rascunho',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (avaliacao_diagnostica_id) REFERENCES avaliacoes_diagnosticas_rapidas(id),
    
    INDEX idx_student (student_id),
    INDEX idx_ano (ano_letivo),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE pei_objetivos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pei_id INT NOT NULL,
    
    area ENUM('matematica', 'portugues', 'ciencias', 'historia', 'geografia', 'socioemocional', 'autonomia', 'outro'),
    
    -- Conteúdo curricular vinculado
    curriculo_nacional_id INT NULL,
    codigo_bncc VARCHAR(20),
    
    titulo VARCHAR(255),
    descricao TEXT,
    
    meta_especifica TEXT,
    criterio_medicao VARCHAR(255),
    valor_alvo DECIMAL(5,2),
    prazo DATE,
    trimestre INT,
    
    adaptacoes JSON,
    estrategias JSON,
    materiais_recursos JSON,
    criterios_avaliacao JSON,
    
    -- Progresso
    valor_atual DECIMAL(5,2) DEFAULT 0,
    status ENUM('nao_iniciado', 'em_progresso', 'atingido', 'parcialmente_atingido', 'nao_atingido', 'cancelado') DEFAULT 'nao_iniciado',
    
    -- Origem
    origem ENUM('ia_sugestao', 'professor_manual', 'ia_ajustado', 'diagnostico') DEFAULT 'ia_sugestao',
    ia_sugestao_original JSON,
    
    -- Justificativa
    justificativa JSON,
    
    ultima_atualizacao TIMESTAMP,
    observacoes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (pei_id) REFERENCES peis(id) ON DELETE CASCADE,
    FOREIGN KEY (curriculo_nacional_id) REFERENCES curriculo_nacional(id),
    
    INDEX idx_pei (pei_id),
    INDEX idx_area (area),
    INDEX idx_status (status),
    INDEX idx_trimestre (trimestre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vincular recomendações de laudos aos objetivos do PEI
ALTER TABLE laudo_recomendacoes 
ADD CONSTRAINT fk_objetivo_pei 
FOREIGN KEY (objetivo_pei_id) REFERENCES pei_objetivos(id) ON DELETE SET NULL;

CREATE TABLE pei_progress_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    goal_id INT NOT NULL,
    assessment_id INT NULL,
    
    observation TEXT,
    progress_value DECIMAL(5,2),
    
    ai_analysis TEXT,
    ai_suggestions JSON,
    
    recorded_by INT NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (goal_id) REFERENCES pei_objetivos(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES applications(id) ON DELETE SET NULL,
    FOREIGN KEY (recorded_by) REFERENCES users(id),
    
    INDEX idx_goal (goal_id),
    INDEX idx_recorded_at (recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE pei_adjustments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pei_id INT NOT NULL,
    
    adjustment_type ENUM('goal_added', 'goal_modified', 'goal_removed', 'adaptation_changed', 'timeline_adjusted'),
    description TEXT,
    reason TEXT,
    
    old_value JSON,
    new_value JSON,
    
    adjusted_by INT NOT NULL,
    adjusted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (pei_id) REFERENCES peis(id) ON DELETE CASCADE,
    FOREIGN KEY (adjusted_by) REFERENCES users(id),
    
    INDEX idx_pei (pei_id),
    INDEX idx_type (adjustment_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 6. DADOS INICIAIS (BNCC - Exemplos)
-- ============================================================================

-- Alguns exemplos do 5º ano de matemática
INSERT INTO curriculo_nacional (codigo_bncc, ano_escolar, componente, campo_experiencia, eixo_tematico, habilidade_codigo, habilidade_descricao, objeto_conhecimento, dificuldade, trimestre_sugerido) VALUES
('EF05MA08', '5º ano', 'Matemática', 'Números e Álgebra', 'Operações', 'EF05MA08', 'Resolver e elaborar problemas de adição e subtração com números racionais cuja representação decimal seja finita, utilizando estratégias diversas.', 'Frações - Adição e Subtração', 'intermediario', 2),
('EF05MA09', '5º ano', 'Matemática', 'Números e Álgebra', 'Operações', 'EF05MA09', 'Resolver e elaborar problemas simples de contagem envolvendo o princípio multiplicativo.', 'Multiplicação e Divisão', 'intermediario', 2),
('EF05MA17', '5º ano', 'Matemática', 'Geometria', 'Formas Geométricas', 'EF05MA17', 'Reconhecer, nomear e comparar polígonos, considerando lados, vértices e ângulos.', 'Polígonos', 'basico', 1);

-- Alguns exemplos de pré-requisitos
INSERT INTO mapeamento_prerequisitos (habilidade_codigo, habilidade_titulo, ano_escolar, prerequisito_codigo, prerequisito_titulo, ano_prerequisito, essencial, peso) VALUES
('EF05MA08', 'Frações - Adição e Subtração', '5º ano', 'EF04MA09', 'Reconhecer frações', '4º ano', TRUE, 1.0),
('EF05MA08', 'Frações - Adição e Subtração', '5º ano', 'EF04MA10', 'Representar frações', '4º ano', TRUE, 1.0),
('EF05MA08', 'Frações - Adição e Subtração', '5º ano', 'EF03MA09', 'Noção de fração', '3º ano', TRUE, 0.8);

-- ============================================================================
-- FIM DA MIGRATION
-- ============================================================================
