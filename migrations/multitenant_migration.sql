-- ============================================
-- MIGRATION: MULTI-TENANT AdaptAI
-- ============================================
-- Execute este SQL no MySQL para criar as tabelas
-- de multi-tenant (escolas, planos, assinaturas)
-- ============================================

-- 1. TABELA DE PLANOS
CREATE TABLE IF NOT EXISTS planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    valor DECIMAL(10,2) NOT NULL DEFAULT 0,
    valor_anual DECIMAL(10,2),
    limite_alunos INT DEFAULT 50,
    limite_professores INT DEFAULT 5,
    limite_provas_mes INT DEFAULT 100,
    limite_materiais_mes INT DEFAULT 100,
    limite_peis_mes INT DEFAULT 50,
    limite_relatorios_mes INT DEFAULT 50,
    pei_automatico BOOLEAN DEFAULT TRUE,
    materiais_adaptativos BOOLEAN DEFAULT TRUE,
    mapas_mentais BOOLEAN DEFAULT TRUE,
    relatorios_avancados BOOLEAN DEFAULT FALSE,
    api_access BOOLEAN DEFAULT FALSE,
    suporte_prioritario BOOLEAN DEFAULT FALSE,
    treinamento_incluido BOOLEAN DEFAULT FALSE,
    integracao_whatsapp BOOLEAN DEFAULT FALSE,
    integracao_google BOOLEAN DEFAULT FALSE,
    exportacao_pdf BOOLEAN DEFAULT TRUE,
    exportacao_excel BOOLEAN DEFAULT TRUE,
    ativo BOOLEAN DEFAULT TRUE,
    destaque BOOLEAN DEFAULT FALSE,
    ordem INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. TABELA DE ESCOLAS (TENANTS)
CREATE TABLE IF NOT EXISTS escolas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(18) UNIQUE,
    razao_social VARCHAR(255),
    tipo VARCHAR(50) DEFAULT 'ESCOLA',
    segmento VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    whatsapp VARCHAR(20),
    site VARCHAR(255),
    cep VARCHAR(10),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    logo VARCHAR(500),
    cor_primaria VARCHAR(7) DEFAULT '#8B5CF6',
    cor_secundaria VARCHAR(7) DEFAULT '#EC4899',
    ativa BOOLEAN DEFAULT TRUE,
    data_fundacao TIMESTAMP NULL,
    asaas_customer_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. TABELA DE ASSINATURAS
CREATE TABLE IF NOT EXISTS assinaturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    escola_id INT NOT NULL UNIQUE,
    plano_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'trial',
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP NULL,
    data_proxima_cobranca TIMESTAMP NULL,
    valor_mensal DECIMAL(10,2) NOT NULL,
    desconto_percentual DECIMAL(5,2) DEFAULT 0,
    dia_vencimento INT DEFAULT 10,
    forma_pagamento VARCHAR(50),
    alunos_ativos INT DEFAULT 0,
    professores_ativos INT DEFAULT 0,
    provas_mes_atual INT DEFAULT 0,
    materiais_mes_atual INT DEFAULT 0,
    peis_mes_atual INT DEFAULT 0,
    relatorios_mes_atual INT DEFAULT 0,
    cancelada_em TIMESTAMP NULL,
    motivo_cancelamento TEXT,
    asaas_subscription_id VARCHAR(100),
    asaas_customer_id VARCHAR(100),
    asaas_payment_link_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (escola_id) REFERENCES escolas(id) ON DELETE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. TABELA DE FATURAS
CREATE TABLE IF NOT EXISTS faturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assinatura_id INT NOT NULL,
    numero VARCHAR(50) NOT NULL UNIQUE,
    valor DECIMAL(10,2) NOT NULL,
    valor_pago DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pendente',
    data_emissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_vencimento TIMESTAMP NOT NULL,
    data_pagamento TIMESTAMP NULL,
    metodo_pagamento VARCHAR(50),
    link_pagamento VARCHAR(500),
    codigo_pix TEXT,
    linha_digitavel VARCHAR(100),
    nota_fiscal VARCHAR(255),
    observacoes TEXT,
    asaas_payment_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assinatura_id) REFERENCES assinaturas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. TABELA DE CONFIGURAÇÕES DA ESCOLA
CREATE TABLE IF NOT EXISTS configuracoes_escola (
    id INT AUTO_INCREMENT PRIMARY KEY,
    escola_id INT NOT NULL UNIQUE,
    modelo_ia_preferido VARCHAR(100) DEFAULT 'claude-3-haiku-20240307',
    quantidade_questoes_padrao INT DEFAULT 5,
    dificuldade_padrao VARCHAR(20) DEFAULT 'medio',
    notificacoes_email BOOLEAN DEFAULT TRUE,
    notificacoes_whatsapp BOOLEAN DEFAULT FALSE,
    pei_automatico_ativo BOOLEAN DEFAULT TRUE,
    materiais_adaptativos_ativo BOOLEAN DEFAULT TRUE,
    relatorios_avancados_ativo BOOLEAN DEFAULT TRUE,
    lgpd_ativo BOOLEAN DEFAULT TRUE,
    termo_aceito_em TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (escola_id) REFERENCES escolas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. ADICIONAR escola_id NA TABELA DE USUÁRIOS (SE NÃO EXISTIR)
-- Primeiro verifica se a coluna já existe
SET @exists = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
               WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'escola_id');
SET @query = IF(@exists = 0, 
    'ALTER TABLE users ADD COLUMN escola_id INT NULL, ADD FOREIGN KEY (escola_id) REFERENCES escolas(id)',
    'SELECT "Coluna escola_id já existe"');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 7. ADICIONAR escola_id NA TABELA DE ALUNOS (SE NÃO EXISTIR)
SET @exists2 = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
               WHERE TABLE_NAME = 'students' AND COLUMN_NAME = 'escola_id');
SET @query2 = IF(@exists2 = 0, 
    'ALTER TABLE students ADD COLUMN escola_id INT NULL, ADD FOREIGN KEY (escola_id) REFERENCES escolas(id)',
    'SELECT "Coluna escola_id já existe em students"');
PREPARE stmt2 FROM @query2;
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;

-- 8. INSERIR PLANOS PADRÃO
INSERT INTO planos (nome, slug, descricao, valor, valor_anual, limite_alunos, limite_professores, 
    limite_provas_mes, limite_materiais_mes, limite_peis_mes, limite_relatorios_mes,
    pei_automatico, materiais_adaptativos, mapas_mentais, relatorios_avancados,
    api_access, suporte_prioritario, treinamento_incluido, integracao_whatsapp,
    integracao_google, exportacao_pdf, exportacao_excel, ativo, destaque, ordem)
VALUES 
    ('Gratuito', 'gratuito', 'Plano gratuito para experimentar a plataforma', 
     0, 0, 5, 1, 10, 10, 5, 5, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, TRUE, FALSE, 0),
    
    ('Essencial', 'essencial', 'Plano ideal para professores e pequenas escolas', 
     79.90, 766.80, 30, 3, 50, 50, 30, 30, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, 1),
    
    ('Profissional', 'profissional', 'Para escolas e clínicas. MAIS POPULAR!', 
     159.00, 1526.40, 100, 10, 200, 200, 100, 100, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, 2),
    
    ('Institucional', 'institucional', 'Para grandes instituições', 
     399.00, 3830.40, 500, 50, 1000, 1000, 500, 500, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, 3),
    
    ('Enterprise', 'enterprise', 'Personalizado para redes de ensino', 
     999.00, 9590.40, 9999, 999, 9999, 9999, 9999, 9999, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, 4)
ON DUPLICATE KEY UPDATE 
    valor = VALUES(valor),
    valor_anual = VALUES(valor_anual),
    limite_alunos = VALUES(limite_alunos),
    limite_professores = VALUES(limite_professores);

-- 9. VERIFICAR PLANOS CRIADOS
SELECT id, nome, valor, limite_alunos, limite_professores, destaque 
FROM planos 
ORDER BY ordem;

-- ============================================
-- FIM DA MIGRATION
-- ============================================
