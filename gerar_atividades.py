# Gerar atividades para o PEI do Márcio
import asyncio
import sys
import os

# Configurar ambiente
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

# Carregar .env
from dotenv import load_dotenv
load_dotenv()

async def main():
    from app.database import SessionLocal
    from app.services.calendario_atividades_service import CalendarioAtividadesService
    
    db = SessionLocal()
    
    try:
        service = CalendarioAtividadesService(db)
        
        print("🚀 Gerando atividades para o PEI do Márcio (ID: 3)...")
        print("=" * 60)
        
        resultado = await service.gerar_calendario_completo(
            pei_id=3,
            user_id=1  # Admin
        )
        
        print(f"\n✅ SUCESSO!")
        print(f"📊 Resumo:")
        print(f"   - Aluno: {resultado['student_name']}")
        print(f"   - Total de objetivos: {resultado['total_objetivos']}")
        print(f"   - Atividades geradas: {resultado['atividades_geradas']}")
        print(f"   - Materiais criados: {resultado['materiais_gerados']}")
        print(f"   - Provas criadas: {resultado['provas_geradas']}")
        
        print(f"\n📅 Calendário:")
        for ativ in resultado['calendario'][:10]:  # Mostrar primeiras 10
            print(f"   {ativ['data']} - [{ativ['tipo']}] {ativ['titulo'][:50]}...")
        
        if len(resultado['calendario']) > 10:
            print(f"   ... e mais {len(resultado['calendario']) - 10} atividades")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
