# ============================================
# DELETAR PEI ANTIGO DO MÁRCIO
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

def deletar_pei_marcio():
    print("=" * 60)
    print("DELETAR PEIs ANTIGOS DO MÁRCIO")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Listar PEIs do Márcio (student_id = 1)
        result = conn.execute(text("""
            SELECT p.id, p.ano_letivo, p.status, p.created_at,
                   (SELECT COUNT(*) FROM pei_objetivos WHERE pei_id = p.id) as total_objetivos
            FROM peis p
            WHERE p.student_id = 1
            ORDER BY p.created_at DESC
        """))
        
        peis = result.fetchall()
        
        if not peis:
            print("\nNenhum PEI encontrado para o Márcio.")
            return
        
        print("\nPEIs encontrados:")
        print("-" * 60)
        for pei in peis:
            print(f"   PEI #{pei[0]} | Ano: {pei[1]} | Status: {pei[2]}")
            print(f"   Objetivos: {pei[4]} | Criado: {pei[3]}")
            print()
        
        # Confirmar
        resposta = input("Deseja DELETAR TODOS os PEIs do Márcio? (s/n): ")
        
        if resposta.lower() == 's':
            # Deletar objetivos primeiro (por causa da FK)
            conn.execute(text("""
                DELETE FROM pei_objetivos 
                WHERE pei_id IN (SELECT id FROM peis WHERE student_id = 1)
            """))
            
            # Deletar PEIs
            result = conn.execute(text("""
                DELETE FROM peis WHERE student_id = 1
            """))
            
            conn.commit()
            
            print("\n" + "=" * 60)
            print(f"✅ {result.rowcount} PEI(s) deletado(s) com sucesso!")
            print("Agora você pode gerar um novo planejamento.")
            print("=" * 60)
        else:
            print("\nOperação cancelada.")


if __name__ == "__main__":
    deletar_pei_marcio()
