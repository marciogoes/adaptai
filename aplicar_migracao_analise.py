"""
Script para aplicar migração de análises qualitativas
Usa SQLAlchemy que já está instalado
"""
from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def aplicar_migracao():
    print("\n" + "="*80)
    print("🔄 APLICANDO MIGRAÇÃO - ANÁLISES QUALITATIVAS")
    print("="*80 + "\n")
    
    try:
        # Usar a propriedade db_url que já faz o encoding correto da senha
        database_url = settings.db_url
        engine = create_engine(database_url)
        
        print("✅ Conectado ao banco de dados")
        print(f"   Host: {settings.MYSQL_HOST}")
        print(f"   Database: {settings.MYSQL_DATABASE}\n")
        
        # Verificar se tabela já existe
        inspector = inspect(engine)
        tabela_existe = 'analises_qualitativas' in inspector.get_table_names()
        
        if tabela_existe:
            print("⚠️  Tabela 'analises_qualitativas' já existe!")
            resposta = input("   Deseja recriar a tabela? (s/n): ")
            if resposta.lower() != 's':
                print("\n❌ Migração cancelada pelo usuário")
                return
            
            print("   Dropando tabela antiga...")
            with engine.connect() as conn:
                conn.execute(text("DROP TABLE analises_qualitativas"))
                conn.commit()
            print("   ✅ Tabela antiga removida")
        
        # Criar tabela
        print("\n📝 Criando tabela 'analises_qualitativas'...")
        
        sql_create = """
        CREATE TABLE analises_qualitativas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            prova_aluno_id INT NOT NULL,
            
            pontos_fortes TEXT,
            pontos_fracos TEXT,
            conteudos_revisar JSON,
            recomendacoes TEXT,
            
            analise_por_conteudo JSON,
            
            nivel_dominio VARCHAR(50),
            areas_prioridade JSON,
            
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            FOREIGN KEY (prova_aluno_id) REFERENCES provas_alunos(id) ON DELETE CASCADE,
            INDEX idx_prova_aluno (prova_aluno_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        with engine.connect() as conn:
            conn.execute(text(sql_create))
            conn.commit()
        
        print("✅ Tabela 'analises_qualitativas' criada com sucesso!")
        
        # Verificar estrutura
        with engine.connect() as conn:
            result = conn.execute(text("DESCRIBE analises_qualitativas"))
            colunas = result.fetchall()
        
        print("\n📋 Estrutura da tabela:")
        for coluna in colunas:
            print(f"   • {coluna[0]} ({coluna[1]})")
        
        print("\n" + "="*80)
        print("✅ MIGRAÇÃO APLICADA COM SUCESSO!")
        print("="*80)
        print("\n💡 Próximos passos:")
        print("   1. Reinicie o backend (REINICIAR_BACKEND.bat)")
        print("   2. Acesse uma prova corrigida")
        print("   3. Click em 'Ver Análise Qualitativa IA' 🤖")
        print("   4. Click em 'Gerar Análise com IA' ✨")
        print("   5. Veja os insights sobre o aluno!\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao aplicar migração: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'engine' in locals():
            engine.dispose()
            print("🔌 Conexão fechada\n")


if __name__ == "__main__":
    aplicar_migracao()
