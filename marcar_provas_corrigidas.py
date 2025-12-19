"""
Script para marcar provas concluídas como corrigidas
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def corrigir_provas():
    print("\n" + "="*80)
    print("🔧 CORRIGIR PROVAS AUTOMATICAMENTE")
    print("="*80 + "\n")
    
    try:
        engine = create_engine(settings.db_url)
        
        # 1. Listar provas concluídas
        print("1️⃣  Buscando provas CONCLUÍDAS...\n")
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    pa.id as prova_aluno_id,
                    pa.status,
                    pa.nota_final,
                    p.titulo as prova_titulo,
                    s.name as aluno_nome
                FROM provas_alunos pa
                JOIN provas p ON pa.prova_id = p.id
                JOIN students s ON pa.aluno_id = s.id
                WHERE pa.status = 'concluida'
                ORDER BY pa.id DESC
            """))
            
            provas_concluidas = result.fetchall()
            
            if not provas_concluidas:
                print("   ℹ️  Nenhuma prova CONCLUÍDA encontrada.")
                print("   Todas as provas já estão corrigidas ou não foram finalizadas.\n")
                return
            
            print(f"   ✅ Encontradas {len(provas_concluidas)} prova(s) CONCLUÍDA(S):\n")
            
            for prova in provas_concluidas:
                print(f"   📝 ID: {prova.prova_aluno_id} - {prova.prova_titulo}")
                print(f"      Aluno: {prova.aluno_nome}")
                print(f"      Nota: {prova.nota_final}/10")
                print()
        
        # 2. Confirmar ação
        print("="*80)
        resposta = input("\n⚠️  Deseja marcar TODAS essas provas como CORRIGIDAS? (s/n): ")
        
        if resposta.lower() != 's':
            print("\n❌ Operação cancelada pelo usuário.\n")
            return
        
        # 3. Atualizar status
        print("\n2️⃣  Atualizando status para CORRIGIDA...\n")
        
        with engine.begin() as conn:
            result = conn.execute(text("""
                UPDATE provas_alunos 
                SET status = 'corrigida',
                    data_correcao = NOW()
                WHERE status = 'concluida'
            """))
            
            provas_atualizadas = result.rowcount
        
        print(f"   ✅ {provas_atualizadas} prova(s) marcada(s) como CORRIGIDA!")
        
        # 4. Verificar resultado
        print("\n3️⃣  Verificando provas corrigidas...\n")
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    pa.id as prova_aluno_id,
                    p.titulo as prova_titulo,
                    s.name as aluno_nome,
                    pa.nota_final
                FROM provas_alunos pa
                JOIN provas p ON pa.prova_id = p.id
                JOIN students s ON pa.aluno_id = s.id
                WHERE pa.status = 'corrigida'
                ORDER BY pa.id DESC
            """))
            
            provas_corrigidas = result.fetchall()
            
            print(f"   ✅ Total de provas CORRIGIDAS agora: {len(provas_corrigidas)}\n")
            
            for prova in provas_corrigidas:
                print(f"   📝 {prova.prova_titulo} - {prova.aluno_nome} ({prova.nota_final}/10)")
        
        print("\n" + "="*80)
        print("✅ CONCLUÍDO COM SUCESSO!")
        print("="*80)
        print("\n💡 Agora você pode:")
        print("   1. Acessar http://localhost:5173")
        print("   2. Login como professor")
        print("   3. Analytics de Provas → Escolher aluno")
        print("   4. Click em 'Ver Detalhes' de qualquer prova")
        print("   5. Verá o botão 'Ver Análise Qualitativa IA' no topo! 🤖\n")
        
        engine.dispose()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    corrigir_provas()
