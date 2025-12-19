"""
Script de diagnóstico completo - Análise Qualitativa
"""
from sqlalchemy import create_engine, text
from app.core.config import settings
import os

def diagnosticar():
    print("\n" + "="*80)
    print("🔍 DIAGNÓSTICO COMPLETO - ANÁLISE QUALITATIVA")
    print("="*80 + "\n")
    
    # 1. Verificar se tabela existe
    print("1️⃣  Verificando tabela no banco...")
    try:
        engine = create_engine(settings.db_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'analises_qualitativas'
            """), (settings.MYSQL_DATABASE,))
            
            tabela_existe = result.fetchone()[0] > 0
            
            if tabela_existe:
                print("   ✅ Tabela 'analises_qualitativas' existe!")
            else:
                print("   ❌ Tabela 'analises_qualitativas' NÃO existe!")
                print("   💡 Execute: APLICAR_MIGRACAO_ANALISE.bat")
                return
        
        # 2. Verificar provas
        print("\n2️⃣  Verificando provas no sistema...")
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    pa.id as prova_aluno_id,
                    pa.status,
                    pa.nota_final,
                    p.titulo as prova_titulo,
                    s.name as aluno_nome,
                    s.email as aluno_email
                FROM provas_alunos pa
                JOIN provas p ON pa.prova_id = p.id
                JOIN students s ON pa.aluno_id = s.id
                ORDER BY pa.id DESC
            """))
            
            provas = result.fetchall()
            
            if not provas:
                print("   ❌ Nenhuma prova encontrada!")
                print("\n   💡 Você precisa:")
                print("      1. Criar uma prova")
                print("      2. Associar a um aluno")
                print("      3. Aluno fazer a prova")
                print("      4. Corrigir a prova")
                return
            
            print(f"   ✅ Total de provas: {len(provas)}")
            
            # Contar por status
            status_count = {}
            for p in provas:
                status = p.status
                status_count[status] = status_count.get(status, 0) + 1
            
            print("\n   📊 Provas por status:")
            for status, count in status_count.items():
                print(f"      • {status}: {count}")
            
            # Verificar corrigidas
            corrigidas = [p for p in provas if p.status == 'corrigida']
            
            if not corrigidas:
                print("\n   ⚠️  PROBLEMA: Nenhuma prova CORRIGIDA!")
                print("\n   💡 Para testar a análise IA, você precisa:")
                print("      1. Ir em 'Analytics de Provas'")
                print("      2. Escolher um aluno")
                print("      3. Encontrar prova com status diferente de 'corrigida'")
                print("      4. Corrigir a prova primeiro")
                return
            
            print(f"\n   ✅ {len(corrigidas)} prova(s) CORRIGIDA(S) encontrada(s)!")
            print("\n   🎯 Provas corrigidas:")
            
            for prova in corrigidas:
                print(f"\n      📝 Prova Aluno ID: {prova.prova_aluno_id}")
                print(f"         Título: {prova.prova_titulo}")
                print(f"         Aluno: {prova.aluno_nome}")
                print(f"         Nota: {prova.nota_final}/10")
                print(f"         Status: ✅ CORRIGIDA")
        
        # 3. Verificar arquivos frontend
        print("\n3️⃣  Verificando arquivos do frontend...")
        
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src")
        
        # Verificar AnaliseQualitativaPage.jsx
        analise_page = os.path.join(frontend_path, "pages", "AnaliseQualitativaPage.jsx")
        if os.path.exists(analise_page):
            print("   ✅ AnaliseQualitativaPage.jsx existe")
        else:
            print("   ❌ AnaliseQualitativaPage.jsx NÃO existe!")
            print(f"   Caminho esperado: {analise_page}")
        
        # Verificar App.jsx
        app_jsx = os.path.join(frontend_path, "App.jsx")
        if os.path.exists(app_jsx):
            with open(app_jsx, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'AnaliseQualitativaPage' in content:
                    print("   ✅ AnaliseQualitativaPage importada no App.jsx")
                else:
                    print("   ❌ AnaliseQualitativaPage NÃO está importada no App.jsx!")
                
                if '/provas/analytics/analise/:provaAlunoId' in content:
                    print("   ✅ Rota /provas/analytics/analise/:provaAlunoId existe")
                else:
                    print("   ❌ Rota /provas/analytics/analise/:provaAlunoId NÃO existe!")
        else:
            print("   ❌ App.jsx não encontrado!")
        
        # Verificar ProvaRealizadaDetalhes.jsx
        detalhes_page = os.path.join(frontend_path, "pages", "ProvaRealizadaDetalhes.jsx")
        if os.path.exists(detalhes_page):
            with open(detalhes_page, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Ver Análise Qualitativa IA' in content:
                    print("   ✅ Botão 'Ver Análise Qualitativa IA' existe em ProvaRealizadaDetalhes.jsx")
                else:
                    print("   ❌ Botão 'Ver Análise Qualitativa IA' NÃO encontrado!")
                
                if "dados.resultado.status === 'corrigida'" in content:
                    print("   ✅ Condição de status 'corrigida' verificada")
                else:
                    print("   ⚠️  Condição de status pode estar incorreta")
        else:
            print("   ❌ ProvaRealizadaDetalhes.jsx não encontrado!")
        
        # 4. Instruções finais
        print("\n" + "="*80)
        print("📋 RESUMO E INSTRUÇÕES")
        print("="*80 + "\n")
        
        if corrigidas:
            primeira_corrigida = corrigidas[0]
            print("✅ Tudo configurado! Para acessar a análise:")
            print(f"\n1. Acesse: http://localhost:5173")
            print(f"2. Login como professor")
            print(f"3. Menu → 'Analytics de Provas'")
            print(f"4. Click no aluno: {primeira_corrigida.aluno_nome}")
            print(f"5. Procure a prova: '{primeira_corrigida.prova_titulo}'")
            print(f"6. Click em 'Ver Detalhes'")
            print(f"7. NO TOPO DA PÁGINA → Botão roxo/azul 'Ver Análise Qualitativa IA'")
            print(f"\n💡 Se não aparecer:")
            print(f"   • Aperte F12 → Console → Veja se há erros")
            print(f"   • Aperte Ctrl+Shift+R para forçar reload")
            print(f"   • Verifique se frontend está rodando em http://localhost:5173")
        
        engine.dispose()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    diagnosticar()
