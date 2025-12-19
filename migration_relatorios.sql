-- ============================================
-- MIGRATION: Corrigir tabela relatorios
-- ============================================

-- 1. Adicionar coluna arquivo_path
ALTER TABLE relatorios 
ADD COLUMN arquivo_path VARCHAR(500) NULL
AFTER arquivo_tipo;

-- 2. Permitir NULL em arquivo_base64
ALTER TABLE relatorios 
MODIFY COLUMN arquivo_base64 LONGTEXT NULL;

-- 3. Verificar estrutura
DESCRIBE relatorios;

-- ============================================
-- RESULTADO ESPERADO:
-- arquivo_path: varchar(500), NULL
-- arquivo_base64: longtext, NULL
-- ============================================
