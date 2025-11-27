"""
Script para diagnosticar problema de visualização de materiais do aluno
"""
from app.database import SessionLocal
from app.models.material import Material, MaterialAluno, StatusMaterial
from app.models.student import Student

def diagnosticar():
    db = SessionLocal()
    
    try:
        print("\n" + "="*80)
        print("🔍 DIAGNÓSTICO - MATERIAIS DO ALUNO")
        print("="*80 + "\n")
        
        # 1. Verificar materiais disponíveis
        materiais = db.query(Material).filter(
            Material.status == StatusMaterial.DISPONIVEL
        ).all()
        
        print(f"📊 MATERIAIS DISPONÍVEIS: {len(materiais)}")
        for mat in materiais:
            print(f"\n   ID: {mat.id}")
            print(f"   Título: {mat.titulo}")
            print(f"   Tipo: {mat.tipo}")
            print(f"   Status: {mat.status}")
            print(f"   Arquivo: {mat.arquivo_path or 'NULL ❌'}")
            
            # Verificar se arquivo existe
            if mat.arquivo_path:
                import os
                from pathlib import Path
                storage_path = Path(__file__).parent / "storage" / "materiais" / mat.arquivo_path
                existe = storage_path.exists()
                print(f"   Arquivo existe? {'✅ SIM' if existe else '❌ NÃO'}")
                if existe:
                    tamanho = storage_path.stat().st_size
                    print(f"   Tamanho: {tamanho} bytes")
        
        print("\n" + "-"*80 + "\n")
        
        # 2. Verificar associações com alunos
        associacoes = db.query(MaterialAluno).all()
        print(f"🔗 ASSOCIAÇÕES MATERIAL-ALUNO: {len(associacoes)}")
        
        for assoc in associacoes:
            material = db.query(Material).get(assoc.material_id)
            aluno = db.query(Student).get(assoc.aluno_id)
            
            print(f"\n   MaterialAluno ID: {assoc.id}")
            print(f"   Material: {material.titulo if material else 'NÃO ENCONTRADO'}")
            print(f"   Status Material: {material.status if material else 'N/A'}")
            print(f"   Aluno: {aluno.name if aluno else 'NÃO ENCONTRADO'}")
            print(f"   Email Aluno: {aluno.email if aluno else 'N/A'}")
            print(f"   Visualizações: {assoc.total_visualizacoes}")
            print(f"   Favorito: {'✅' if assoc.favorito else '❌'}")
        
        print("\n" + "-"*80 + "\n")
        
        # 3. Verificar alunos
        alunos = db.query(Student).all()
        print(f"👥 ALUNOS CADASTRADOS: {len(alunos)}")
        for aluno in alunos:
            print(f"\n   ID: {aluno.id}")
            print(f"   Nome: {aluno.name}")
            print(f"   Email: {aluno.email}")
            print(f"   Ativo: {'✅' if aluno.is_active else '❌'}")
            
            # Materiais deste aluno
            meus_materiais = db.query(MaterialAluno).filter(
                MaterialAluno.aluno_id == aluno.id
            ).all()
            print(f"   Materiais: {len(meus_materiais)}")
            
            for ma in meus_materiais:
                mat = db.query(Material).get(ma.material_id)
                if mat:
                    print(f"      - {mat.titulo} ({mat.status})")
        
        print("\n" + "="*80)
        print("✅ DIAGNÓSTICO CONCLUÍDO!")
        print("="*80 + "\n")
        
        # Sugestões
        print("💡 SUGESTÕES:")
        
        materiais_disponiveis = [m for m in materiais if m.arquivo_path and m.status == StatusMaterial.DISPONIVEL]
        if not materiais_disponiveis:
            print("   ⚠️ Nenhum material disponível com arquivo!")
            print("   → Crie um novo material e aguarde a geração")
        
        if not associacoes:
            print("   ⚠️ Nenhuma associação material-aluno!")
            print("   → Ao criar material, selecione pelo menos 1 aluno")
        
        if not alunos:
            print("   ⚠️ Nenhum aluno cadastrado!")
            print("   → Cadastre alunos primeiro")
        
        print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    diagnosticar()
