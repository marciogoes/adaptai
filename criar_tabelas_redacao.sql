-- =============================================
-- MIGRAÇÃO: Tabelas de Redação ENEM
-- =============================================

-- Tabela de Temas de Redação
CREATE TABLE IF NOT EXISTS temas_redacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(300) NOT NULL,
    tema TEXT NOT NULL,
    proposta TEXT NOT NULL,
    
    -- Textos motivadores (até 4)
    texto_motivador_1 TEXT NULL,
    texto_motivador_2 TEXT NULL,
    texto_motivador_3 TEXT NULL,
    texto_motivador_4 TEXT NULL,
    
    -- Metadados
    area_tematica VARCHAR(100) NULL,
    palavras_chave JSON NULL,
    nivel_dificuldade VARCHAR(20) DEFAULT 'medio',
    
    -- Controle
    ativo BOOLEAN DEFAULT TRUE,
    criado_por_id INT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- FK
    FOREIGN KEY (criado_por_id) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_tema_area (area_tematica),
    INDEX idx_tema_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Tabela de Redações dos Alunos
CREATE TABLE IF NOT EXISTS redacoes_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Vínculos
    tema_id INT NOT NULL,
    aluno_id INT NOT NULL,
    
    -- Texto da redação
    titulo_redacao VARCHAR(200) NULL,
    texto TEXT NULL,
    quantidade_linhas INT DEFAULT 0,
    quantidade_palavras INT DEFAULT 0,
    
    -- Status: 'rascunho', 'submetida', 'corrigida', 'anulada'
    status ENUM('rascunho', 'submetida', 'corrigida', 'anulada') DEFAULT 'rascunho',
    
    -- Datas
    iniciado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submetido_em TIMESTAMP NULL,
    corrigido_em TIMESTAMP NULL,
    
    -- ========================================
    -- CORREÇÃO POR COMPETÊNCIAS (ENEM)
    -- Cada competência vale de 0 a 200 pontos
    -- ========================================
    
    -- Competência 1: Domínio da norma culta
    nota_competencia_1 INT NULL,
    feedback_competencia_1 TEXT NULL,
    
    -- Competência 2: Compreensão da proposta
    nota_competencia_2 INT NULL,
    feedback_competencia_2 TEXT NULL,
    
    -- Competência 3: Argumentação
    nota_competencia_3 INT NULL,
    feedback_competencia_3 TEXT NULL,
    
    -- Competência 4: Coesão textual
    nota_competencia_4 INT NULL,
    feedback_competencia_4 TEXT NULL,
    
    -- Competência 5: Proposta de intervenção
    nota_competencia_5 INT NULL,
    feedback_competencia_5 TEXT NULL,
    
    -- Nota final (0-1000)
    nota_final INT NULL,
    
    -- Feedback geral da IA
    feedback_geral TEXT NULL,
    pontos_fortes JSON NULL,
    pontos_melhoria JSON NULL,
    sugestoes JSON NULL,
    
    -- Análise detalhada
    analise_detalhada JSON NULL,
    
    -- FKs
    FOREIGN KEY (tema_id) REFERENCES temas_redacao(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES students(id) ON DELETE CASCADE,
    
    -- Índices
    INDEX idx_redacao_aluno (aluno_id),
    INDEX idx_redacao_tema (tema_id),
    INDEX idx_redacao_status (status),
    INDEX idx_redacao_nota (nota_final),
    
    -- Unique: cada aluno só pode ter uma redação por tema
    UNIQUE KEY uk_aluno_tema (aluno_id, tema_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- VERIFICAR CRIAÇÃO
-- =============================================
SELECT 'Tabelas de Redação ENEM criadas com sucesso!' AS status;

SHOW TABLES LIKE '%redac%';
