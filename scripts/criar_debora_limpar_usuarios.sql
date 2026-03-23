-- ===========================================================================
-- SCRIPT SQL: Criar Debora Santana e Limpar Usuários em Caixa Baixa
-- ===========================================================================
-- Database: teamarcionovo
-- Data: Janeiro 2026
-- ===========================================================================

-- Passo 1: Listar usuários atuais (para verificação)
SELECT 'ANTES DA LIMPEZA - Lista de usuários:' AS info;
SELECT id, name, email, role, is_active FROM users ORDER BY name;

-- ===========================================================================
-- PASSO 2: Remover usuários 'marcio' e 'cassio' em CAIXA BAIXA
-- ===========================================================================
-- BINARY faz comparação case-sensitive no MySQL

SELECT 'Usuários em caixa baixa que serão removidos:' AS info;
SELECT id, name, email FROM users 
WHERE BINARY name = 'marcio' OR BINARY name = 'cassio';

-- Executar a remoção
DELETE FROM users 
WHERE BINARY name = 'marcio' OR BINARY name = 'cassio';

SELECT CONCAT('Usuários removidos: ', ROW_COUNT()) AS resultado;

-- ===========================================================================
-- PASSO 3: Verificar usuários em caixa alta (serão mantidos)
-- ===========================================================================
SELECT 'Usuários em caixa alta mantidos:' AS info;
SELECT id, name, email FROM users 
WHERE BINARY name LIKE 'Marcio%' OR BINARY name LIKE 'Cassio%';

-- ===========================================================================
-- PASSO 4: Criar usuária Debora Santana (professora)
-- ===========================================================================
-- Verificar se já existe
SELECT 'Verificando se Debora Santana já existe:' AS info;
SELECT id, name, email FROM users 
WHERE email = 'debora.santana@adaptai.com' OR name = 'Debora Santana';

-- Inserir apenas se não existir
INSERT INTO users (name, email, hashed_password, role, is_active, created_at)
SELECT 
    'Debora Santana',
    'debora.santana@adaptai.com',
    '$2b$12$rltGrlJBVEYuGXzbHIP3TOHr.gt8T2T8Xj84.NdEbVCxIRFMdW.0O', -- Senha: Prof@2024
    'teacher',
    1,
    NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users 
    WHERE email = 'debora.santana@adaptai.com'
);

SELECT CONCAT('Usuária criada: ', IF(ROW_COUNT() > 0, 'SIM', 'NÃO (já existia)')) AS resultado;

-- ===========================================================================
-- RESULTADO FINAL
-- ===========================================================================
SELECT 'DEPOIS DA OPERAÇÃO - Lista de usuários atualizada:' AS info;
SELECT id, name, email, role, is_active FROM users ORDER BY name;

-- ===========================================================================
-- CREDENCIAIS DA NOVA USUÁRIA
-- ===========================================================================
-- Nome: Debora Santana
-- Email: debora.santana@adaptai.com  
-- Senha: Prof@2024
-- Role: teacher (professora)
-- ===========================================================================
