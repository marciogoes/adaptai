-- ============================================
-- MIGRAÇÃO: Sistema de Storage para Materiais
-- Data: 2024-11-27
-- Descrição: Remove campos conteudo_html e conteudo_json,
--            mantém apenas arquivo_path para sistema de storage
-- ============================================

-- PASSO 1: Adicionar coluna arquivo_path se não existir
ALTER TABLE materiais 
ADD COLUMN IF NOT EXISTS arquivo_path VARCHAR(255) DEFAULT NULL
COMMENT 'Caminho do arquivo no storage (ex: 123_visual.html)';

-- PASSO 2: Adicionar índice para performance
CREATE INDEX IF NOT EXISTS idx_materiais_arquivo_path ON materiais(arquivo_path);

-- PASSO 3: Remover colunas antigas (CUIDADO: dados serão perdidos!)
-- ATENÇÃO: Execute apenas após confirmar que todos materiais foram migrados para storage
-- ALTER TABLE materiais DROP COLUMN IF EXISTS conteudo_html;
-- ALTER TABLE materiais DROP COLUMN IF EXISTS conteudo_json;

-- ============================================
-- OBSERVAÇÕES IMPORTANTES:
-- ============================================
-- 1. Os comandos DROP estão comentados por segurança
-- 2. Execute-os manualmente apenas após confirmar que:
--    - Todos materiais existentes foram migrados para storage
--    - Backups foram realizados
--    - Sistema foi testado com sucesso
-- 
-- 3. Para reverter (se necessário):
--    ALTER TABLE materiais ADD COLUMN conteudo_html TEXT DEFAULT NULL;
--    ALTER TABLE materiais ADD COLUMN conteudo_json JSON DEFAULT NULL;
-- ============================================
