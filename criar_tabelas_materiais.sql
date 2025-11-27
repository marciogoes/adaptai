-- SQL para criar tabelas de materiais manualmente
-- Execute este SQL no seu banco MySQL se preferir

-- Tabela: materiais
CREATE TABLE IF NOT EXISTS materiais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    conteudo_prompt TEXT NOT NULL,
    tipo ENUM('visual', 'mapa_mental') NOT NULL,
    materia VARCHAR(100) NOT NULL,
    serie_nivel VARCHAR(50),
    tags JSON,
    conteudo_html TEXT,
    conteudo_json JSON,
    metadados JSON,
    status ENUM('gerando', 'disponivel', 'erro') DEFAULT 'gerando',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    criado_por_id INT NOT NULL,
    INDEX idx_titulo (titulo),
    INDEX idx_criado_por (criado_por_id),
    FOREIGN KEY (criado_por_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabela: materiais_alunos
CREATE TABLE IF NOT EXISTS materiais_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    aluno_id INT NOT NULL,
    data_disponibilizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_primeira_visualizacao DATETIME,
    data_ultima_visualizacao DATETIME,
    total_visualizacoes INT DEFAULT 0,
    favorito INT DEFAULT 0,
    anotacoes_aluno TEXT,
    INDEX idx_material (material_id),
    INDEX idx_aluno (aluno_id),
    UNIQUE KEY unique_material_aluno (material_id, aluno_id),
    FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES students(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Verificar se as tabelas foram criadas
SHOW TABLES LIKE 'materiais%';

-- Ver estrutura
DESCRIBE materiais;
DESCRIBE materiais_alunos;
