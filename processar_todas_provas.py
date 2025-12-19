"""
Script para processar TODAS as provas corrigidas em lote
Gera análise qualitativa + prova de reforço para cada uma
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# IMPORTAR TODOS OS MODELOS NECESSÁRIOS
from app.models.user import User
from app.models.student import Student
from app.models.question import QuestionSet, Question
from app.models.application import Application
from app.models.performance import PerformanceAnalysis
from app.models.material import Material, MaterialAluno
from app.models.prova import Prova, QuestaoGerada, ProvaAluno, RespostaAluno, StatusProvaAluno
from app.models.analise_qualitativa import AnaliseQualitativa

# Importar services
from app.services.analise_qualitativa_service import analise_service
from app.services.prova_adaptativa_service import prova_adaptativa_service
import time

def processar_todas_provas():
    print("\n" + "="*80)
    print("🚀 PROCESSAMENTO EM LOTE - ANÁLISES E PROVAS DE REFORÇO")
    print("="*80 + "\n")
    
    # Conectar ao banco
    engine = create_engine(settings.db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Buscar todas as provas corrigidas
        print("📊 Buscando provas corrigidas...\n")
        
        provas_corrigidas = db.query(ProvaAluno).filter(
            ProvaAluno.status.in_([StatusProvaAluno.CORRIGIDA, StatusProvaAluno.CONCLUIDA])
        ).all()
        
        if not provas_corrigidas:
            print("❌ Nenhuma prova corrigida encontrada!")
            return
        
        print(f"✅ Encontradas {len(provas_corrigidas)} prova(s) corrigida(s)!\n")
        print("="*80)
        
        # Estatísticas
        total_processadas = 0
        total_analises_geradas = 0
        total_provas_reforco = 0
        total_erros = 0
        
        # 2. Processar cada prova
        for idx, prova_aluno in enumerate(provas_corrigidas, 1):
            aluno = prova_aluno.aluno
            prova = prova_aluno.prova
            
            print(f"\n[{idx}/{len(provas_corrigidas)}] " + "="*70)
            print(f"📝 Prova: {prova.titulo}")
            print(f"👤 Aluno: {aluno.name}")
            print(f"📊 Nota: {prova_aluno.nota_final}/10")
            print(f"📅 ProvaAluno ID: {prova_aluno.id}")
            print("-"*70)
            
            try:
                # 2.1. Verificar se já tem análise
                analise_existente = db.query(AnaliseQualitativa).filter(
                    AnaliseQualitativa.prova_aluno_id == prova_aluno.id
                ).first()
                
                if analise_existente:
                    print("ℹ️  Análise já existe, pulando...")
                    analise = analise_existente
                else:
                    # 2.2. Gerar análise qualitativa
                    print("🤖 Gerando análise qualitativa com IA...")
                    analise_ia = analise_service.gerar_analise(prova_aluno)
                    
                    # Salvar análise
                    nova_analise = AnaliseQualitativa(
                        prova_aluno_id=prova_aluno.id,
                        pontos_fortes=analise_ia.get('pontos_fortes', ''),
                        pontos_fracos=analise_ia.get('pontos_fracos', ''),
                        conteudos_revisar=analise_ia.get('conteudos_revisar', []),
                        recomendacoes=analise_ia.get('recomendacoes', ''),
                        analise_por_conteudo=analise_ia.get('analise_por_conteudo', {}),
                        nivel_dominio=analise_ia.get('nivel_dominio', 'regular'),
                        areas_prioridade=analise_ia.get('areas_prioridade', [])
                    )
                    
                    db.add(nova_analise)
                    db.commit()
                    db.refresh(nova_analise)
                    
                    analise = nova_analise
                    total_analises_geradas += 1
                    print(f"   ✅ Análise gerada! ID: {analise.id}")
                    print(f"   📊 Nível: {analise.nivel_dominio}")
                    print(f"   📚 Conteúdos a revisar: {len(analise.conteudos_revisar)}")
                
                # 2.3. Verificar se precisa de prova de reforço
                if analise.conteudos_revisar and len(analise.conteudos_revisar) > 0 and prova_aluno.nota_final < 7.0:
                    print(f"\n🎯 Gerando prova de reforço...")
                    print(f"   Conteúdos focados: {', '.join(analise.conteudos_revisar[:3])}")
                    
                    try:
                        # Verificar se já existe prova de reforço
                        provas_reforco_existentes = db.query(ProvaAluno, Prova).join(
                            Prova, ProvaAluno.prova_id == Prova.id
                        ).filter(
                            ProvaAluno.aluno_id == prova_aluno.aluno_id,
                            Prova.titulo.like(f'🎯 Reforço:%'),
                            Prova.criado_por_id == prova.criado_por_id
                        ).all()
                        
                        # Verificar se já existe para esta prova específica
                        ja_existe = False
                        for pa_reforco, prova_reforco in provas_reforco_existentes:
                            if prova.titulo in prova_reforco.descricao:
                                ja_existe = True
                                break
                        
                        if ja_existe:
                            print("   ℹ️  Prova de reforço já existe para esta prova, pulando...")
                        else:
                            # Gerar prova de reforço
                            prova_reforco = prova_adaptativa_service.gerar_prova_reforco(
                                db=db,
                                prova_aluno_id=prova_aluno.id,
                                analise_id=analise.id
                            )
                            
                            # Associar ao aluno
                            prova_aluno_reforco = prova_adaptativa_service.associar_prova_ao_aluno(
                                db=db,
                                prova_id=prova_reforco.id,
                                aluno_id=prova_aluno.aluno_id
                            )
                            
                            total_provas_reforco += 1
                            print(f"   ✅ Prova de reforço criada! ID: {prova_reforco.id}")
                            print(f"   ✅ Associada ao aluno! ProvaAluno ID: {prova_aluno_reforco.id}")
                            print(f"   📝 {prova_reforco.quantidade_questoes} questões geradas")
                        
                    except Exception as e:
                        print(f"   ❌ Erro ao gerar prova de reforço: {str(e)[:150]}")
                        total_erros += 1
                        # IMPORTANTE: Fazer rollback da sessão
                        db.rollback()
                        print("   🔄 Sessão resetada, continuando...")
                else:
                    if prova_aluno.nota_final >= 7.0:
                        print(f"\n✅ Nota >= 7.0, prova de reforço não necessária")
                    else:
                        print(f"\nℹ️  Sem conteúdos específicos para revisar")
                
                total_processadas += 1
                print(f"\n{'='*70}")
                
                # Aguardar 2 segundos entre provas para não sobrecarregar a API
                if idx < len(provas_corrigidas):
                    print("\n⏳ Aguardando 2 segundos...")
                    time.sleep(2)
                
            except Exception as e:
                print(f"\n❌ ERRO ao processar esta prova: {str(e)[:200]}")
                total_erros += 1
                # Fazer rollback para limpar o estado
                try:
                    db.rollback()
                    print("🔄 Sessão resetada")
                except:
                    pass
                import traceback
                print("\n[DETALHES DO ERRO - primeiras 10 linhas]:")
                traceback.print_exc(limit=10)
        
        # 3. Resumo final
        print("\n" + "="*80)
        print("📊 RESUMO DO PROCESSAMENTO")
        print("="*80)
        print(f"\n✅ Total de provas processadas: {total_processadas}/{len(provas_corrigidas)}")
        print(f"🤖 Análises geradas: {total_analises_geradas}")
        print(f"🎯 Provas de reforço geradas: {total_provas_reforco}")
        print(f"❌ Erros: {total_erros}")
        print(f"\n{'='*80}")
        print("🎉 PROCESSAMENTO CONCLUÍDO!")
        print("="*80 + "\n")
        
        if total_provas_reforco > 0:
            print(f"💡 {total_provas_reforco} aluno(s) agora têm provas de reforço disponíveis!")
            print("   Os alunos podem ver as provas no dashboard deles.\n")
        
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()
        engine.dispose()
        print("🔌 Conexão fechada\n")


if __name__ == "__main__":
    print("\n" + "🚀"*40)
    print("INICIANDO PROCESSAMENTO EM LOTE")
    print("🚀"*40 + "\n")
    
    input("⚠️  Este script vai processar TODAS as provas corrigidas.\n"
          "   Isso pode demorar alguns minutos dependendo da quantidade.\n"
          "   Pressione ENTER para continuar ou Ctrl+C para cancelar...\n")
    
    processar_todas_provas()
    
    print("\n" + "✅"*40)
    print("SCRIPT FINALIZADO")
    print("✅"*40 + "\n")
    
    input("Pressione ENTER para sair...")
