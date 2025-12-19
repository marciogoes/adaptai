-- ============================================================
-- SCRIPT PARA CORRIGIR COLLATION DO BANCO DE DADOS
-- Converte TODAS as tabelas e colunas para utf8mb4_unicode_ci
-- ============================================================

USE teamarcionovo;

-- 1. Converter banco de dados
ALTER DATABASE teamarcionovo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. Converter tabela users
ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. Converter tabela students
ALTER TABLE students CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 4. Converter tabela question_sets
ALTER TABLE question_sets CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 5. Converter tabela questions
ALTER TABLE questions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 6. Converter tabela applications
ALTER TABLE applications CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 7. Converter tabela student_answers
ALTER TABLE student_answers CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 8. Converter tabela performance_analyses
ALTER TABLE performance_analyses CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 9. Converter tabela provas
ALTER TABLE provas CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 10. Converter tabela questoes_geradas
ALTER TABLE questoes_geradas CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 11. Converter tabela provas_alunos (PLURAL!)
ALTER TABLE provas_alunos CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 12. Converter tabela respostas_alunos (PLURAL!)
ALTER TABLE respostas_alunos CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 13. Converter tabela analises_qualitativas
ALTER TABLE analises_qualitativas CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 14. Converter tabela materiais
ALTER TABLE materiais CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 15. Converter tabela materiais_alunos (PLURAL!)
ALTER TABLE materiais_alunos CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ============================================================
-- FIM DO SCRIPT
-- ============================================================

SELECT 'Collation corrigida com sucesso!' AS status;
