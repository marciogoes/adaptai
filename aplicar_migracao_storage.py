"""
Script para aplicar migração de storage
Adiciona coluna arquivo_path na tabela materiais
"""
import pymysql
import sys
from app.core.config import settings


def executar_migracao():
    """Executa SQL de migração"""
    
    print("="*60)
    print("🔧 MIGRAÇÃO: Sistema de Storage para Materiais")
    print("="*60)
    
    try:
        # Conectar ao banco
        print("\n📡 Conectando ao MySQL DBaaS...")
        connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE,
            port=settings.MYSQL_PORT,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        print("✅ Conectado com sucesso!")
        
        # Executar migração
        print("\n🔄 Aplicando migração...")
        
        # Passo 1: Verificar se coluna já existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'materiais' 
            AND COLUMN_NAME = 'arquivo_path'
        """, (settings.MYSQL_DATABASE,))
        
        coluna_existe = cursor.fetchone()[0] > 0
        
        if coluna_existe:
            print("⚠️ Coluna 'arquivo_path' já existe, pulando...")
        else:
            # Adicionar coluna arquivo_path
            sql_add_column = """
            ALTER TABLE materiais 
            ADD COLUMN arquivo_path VARCHAR(255) DEFAULT NULL
            COMMENT 'Caminho do arquivo no storage (ex: 123_visual.html)'
            """
            
            cursor.execute(sql_add_column)
            print("✅ Coluna 'arquivo_path' adicionada")
        
        # Passo 2: Adicionar índice
        try:
            sql_add_index = """
            CREATE INDEX idx_materiais_arquivo_path ON materiais(arquivo_path)
            """
            cursor.execute(sql_add_index)
            print("✅ Índice 'idx_materiais_arquivo_path' criado")
        except pymysql.err.OperationalError as e:
            if "Duplicate key name" in str(e):
                print("⚠️ Índice já existe, pulando...")
            else:
                raise
        
        # Commit
        connection.commit()
        print("\n✅ Migração aplicada com sucesso!")
        
        # Verificar estrutura
        print("\n📊 Estrutura da tabela 'materiais':")
        cursor.execute("DESCRIBE materiais")
        colunas = cursor.fetchall()
        
        for coluna in colunas:
            print(f"  - {coluna[0]}: {coluna[1]}")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("\n⚠️ OBSERVAÇÕES IMPORTANTES:")
        print("1. Campos conteudo_html e conteudo_json NÃO foram removidos")
        print("2. Eles serão removidos manualmente após confirmar que tudo funciona")
        print("3. Por enquanto, o sistema usará apenas arquivo_path")
        print("\n💡 Para remover as colunas antigas manualmente:")
        print("   ALTER TABLE materiais DROP COLUMN conteudo_html;")
        print("   ALTER TABLE materiais DROP COLUMN conteudo_json;")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERRO ao aplicar migração: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    executar_migracao()
