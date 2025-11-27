"""
Script para limpar materiais travados em GERANDO
"""
from app.database import SessionLocal
from app.models.material import Material, StatusMaterial

def limpar_materiais_travados():
    db = SessionLocal()
    
    try:
        # Buscar materiais travados
        materiais_gerando = db.query(Material).filter(
            Material.status == StatusMaterial.GERANDO
        ).all()
        
        if not materiais_gerando:
            print("✅ Nenhum material travado encontrado!")
            db.close()
            return
        
        print(f"🔍 Encontrados {len(materiais_gerando)} materiais travados:\n")
        
        for material in materiais_gerando:
            print(f"   ID {material.id}: {material.titulo} ({material.tipo})")
        
        print("\n" + "="*60)
        print("OPÇÕES:")
        print("="*60)
        print("1. Marcar TODOS como ERRO (rápido) ⚡")
        print("2. Re-gerar TODOS automaticamente (demora ~1 min/material) 🔄")
        print("3. Cancelar ❌")
        print("="*60)
        
        opcao = input("\nEscolha uma opção (1/2/3): ").strip()
        
        if opcao == "1":
            # Marcar como ERRO
            for material in materiais_gerando:
                material.status = StatusMaterial.ERRO
                material.metadados = {"erro": "Material travado - marcado como erro manualmente"}
            
            db.commit()
            db.close()
            print(f"\n✅ {len(materiais_gerando)} materiais marcados como ERRO!")
            print("   Você pode deletá-los no frontend e criar novos.\n")
        
        elif opcao == "2":
            # Re-gerar
            print("\n🔄 Iniciando re-geração...\n")
            print("⚠️  IMPORTANTE: Esta versão usa a NOVA lógica otimizada!")
            print("   Transação super rápida para evitar timeout MySQL.\n")
            
            db.close()  # Fechar sessão atual
            
            from app.api.routes.materiais import gerar_material_background
            
            for i, material in enumerate(materiais_gerando, 1):
                print(f"⏳ [{i}/{len(materiais_gerando)}] Gerando: {material.titulo}...")
                gerar_material_background(material.id)
            
            print(f"\n✅ Processo concluído!")
            print(f"   Verifique no frontend se ficaram DISPONÍVEL.\n")
        
        else:
            print("\n❌ Operação cancelada.\n")
            db.close()
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        db.rollback()
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🛠️  LIMPEZA DE MATERIAIS TRAVADOS")
    print("="*60 + "\n")
    limpar_materiais_travados()
