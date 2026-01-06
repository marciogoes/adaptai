# ============================================
# DIAGNOSTICO COMPLETO - PLANEJAMENTO
# ============================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.db_url, echo=False)

def diagnostico():
    print("=" * 60)
    print("DIAGNOSTICO COMPLETO DO SISTEMA")
    print("=" * 60)
    
    with engine.connect() as conn:
        # 1. Verificar aluno
        print("\n1. ALUNOS NO SISTEMA:")
        print("-" * 60)
        result = conn.execute(text("""
            SELECT id, name, grade_level, turma 
            FROM students 
            ORDER BY id
        """))
        alunos = result.fetchall()
        
        for aluno in alunos:
            print(f"   ID: {aluno[0]} | Nome: {aluno[1]}")
            print(f"   Serie (grade_level): '{aluno[2] or 'NAO DEFINIDO!'}'")
            print(f"   Turma: {aluno[3] or 'N/A'}")
            print()
        
        # 2. Verificar BNCC por ano escolar
        print("\n2. HABILIDADES BNCC POR ANO ESCOLAR:")
        print("-" * 60)
        result = conn.execute(text("""
            SELECT ano_escolar, COUNT(*) as total
            FROM curriculo_nacional
            GROUP BY ano_escolar
            ORDER BY ano_escolar
        """))
        
        bncc = result.fetchall()
        if not bncc:
            print("   NENHUMA HABILIDADE BNCC ENCONTRADA!")
        else:
            for row in bncc:
                print(f"   '{row[0]}': {row[1]} habilidades")
        
        # 3. Verificar PEIs existentes
        print("\n3. PEIs EXISTENTES:")
        print("-" * 60)
        result = conn.execute(text("""
            SELECT p.id, p.student_id, s.name, p.ano_letivo, p.status, p.created_at
            FROM pei p
            JOIN students s ON p.student_id = s.id
            ORDER BY p.created_at DESC
            LIMIT 10
        """))
        
        peis = result.fetchall()
        if not peis:
            print("   NENHUM PEI ENCONTRADO!")
        else:
            for pei in peis:
                print(f"   PEI #{pei[0]} | Aluno: {pei[2]} (ID:{pei[1]})")
                print(f"   Ano: {pei[3]} | Status: {pei[4]} | Criado: {pei[5]}")
                print()
        
        # 4. Verificar objetivos PEI
        print("\n4. OBJETIVOS PEI:")
        print("-" * 60)
        result = conn.execute(text("""
            SELECT pei_id, COUNT(*) as total
            FROM pei_objetivos
            GROUP BY pei_id
        """))
        
        objetivos = result.fetchall()
        if not objetivos:
            print("   NENHUM OBJETIVO PEI ENCONTRADO!")
        else:
            for obj in objetivos:
                print(f"   PEI #{obj[0]}: {obj[1]} objetivos")
        
        # 5. Mostrar correspondencia
        print("\n" + "=" * 60)
        print("VERIFICACAO DE CORRESPONDENCIA:")
        print("=" * 60)
        
        for aluno in alunos:
            grade = aluno[2]
            if grade:
                # Verificar se existe BNCC para essa serie
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM curriculo_nacional 
                    WHERE ano_escolar = :grade
                """), {"grade": grade})
                count = result.fetchone()[0]
                
                if count > 0:
                    print(f"   Aluno '{aluno[1]}' (grade_level='{grade}'): OK - {count} habilidades encontradas")
                else:
                    print(f"   Aluno '{aluno[1]}' (grade_level='{grade}'): ERRO - Nenhuma habilidade BNCC!")
                    print(f"      Sugestao: Altere grade_level para um dos valores acima")
            else:
                print(f"   Aluno '{aluno[1]}': ERRO - grade_level nao definido!")
    
    print("\n" + "=" * 60)
    print("FIM DO DIAGNOSTICO")
    print("=" * 60)


if __name__ == "__main__":
    diagnostico()
