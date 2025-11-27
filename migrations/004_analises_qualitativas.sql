"""
Migration: Adicionar tabela de análises qualitativas
"""

-- Tabela de análises qualitativas das provas
CREATE TABLE IF NOT EXISTS analises_qualitativas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prova_aluno_id INT NOT NULL,
    
    -- Análise geral
    pontos_fortes TEXT,
    pontos_fracos TEXT,
    conteudos_revisar JSON,
    recomendacoes TEXT,
    
    -- Análise por conteúdo
    analise_por_conteudo JSON,
    
    -- Métricas
    nivel_dominio VARCHAR(50),  -- 'excelente', 'bom', 'regular', 'precisa_melhorar'
    areas_prioridade JSON,
    
    -- Metadata
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (prova_aluno_id) REFERENCES provas_alunos(id) ON DELETE CASCADE,
    INDEX idx_prova_aluno (prova_aluno_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
