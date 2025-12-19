"""
Script para aumentar max_allowed_packet do MySQL
Resolve problema de "Lost connection" em queries grandes
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def aumentar_max_packet():
    print("\n" + "="*80)
    print("🔧 AUMENTAR MAX_ALLOWED_PACKET DO MYSQL")
    print("="*80 + "\n")
    
    print("📊 Conectando ao banco de dados...")
    
    # Adicionar parâmetros de conexão para aumentar timeouts
    db_url_modificada = settings.db_url
    if "?" in db_url_modificada:
        db_url_modificada += "&connect_timeout=60&read_timeout=60&write_timeout=60"
    else:
        db_url_modificada += "?connect_timeout=60&read_timeout=60&write_timeout=60"
    
    engine = create_engine(db_url_modificada, pool_pre_ping=True)
    
    try:
        with engine.connect() as conn:
            print("✅ Conectado!\n")
            
            print("🔍 Verificando configuração atual...\n")
            
            # Ver valor atual
            result = conn.execute(text("SHOW VARIABLES LIKE 'max_allowed_packet'"))
            row = result.fetchone()
            valor_atual = int(row[1]) if row else 0
            valor_atual_mb = valor_atual / (1024 * 1024)
            
            print(f"   Valor atual: {valor_atual_mb:.2f} MB")
            
            # Aumentar para 64MB
            novo_valor = 64 * 1024 * 1024  # 64MB
            novo_valor_mb = 64
            
            print(f"   Novo valor: {novo_valor_mb} MB\n")
            
            if valor_atual >= novo_valor:
                print("✅ Valor já está adequado!")
            else:
                print("🔄 Aumentando max_allowed_packet...")
                
                try:
                    # Tentar aumentar globalmente (requer privilégios)
                    conn.execute(text(f"SET GLOBAL max_allowed_packet={novo_valor}"))
                    conn.commit()
                    print(f"   ✅ GLOBAL: Definido para {novo_valor_mb} MB")
                except Exception as e:
                    print(f"   ⚠️  GLOBAL: Sem permissão ({str(e)[:50]})")
                
                try:
                    # Aumentar para a sessão atual (sempre funciona)
                    conn.execute(text(f"SET SESSION max_allowed_packet={novo_valor}"))
                    conn.commit()
                    print(f"   ✅ SESSION: Definido para {novo_valor_mb} MB")
                except Exception as e:
                    print(f"   ❌ SESSION: Erro ({str(e)[:50]})")
            
            print("\n" + "="*80)
            print("📝 RECOMENDAÇÕES")
            print("="*80 + "\n")
            print("1. Se não conseguiu definir GLOBAL, peça ao administrador do banco")
            print("2. Ou adicione no arquivo de configuração do MySQL (my.cnf ou my.ini):")
            print("   ")
            print("   [mysqld]")
            print(f"   max_allowed_packet = {novo_valor_mb}M")
            print("   ")
            print("3. Reinicie o MySQL após modificar o arquivo")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
    
    finally:
        engine.dispose()
        print("🔌 Conexão fechada\n")


if __name__ == "__main__":
    print("\n" + "🔧"*40)
    print("AUMENTAR MAX_ALLOWED_PACKET")
    print("🔧"*40 + "\n")
    
    input("⚠️  Este script vai tentar aumentar o max_allowed_packet do MySQL.\n"
          "   Isso resolve problemas de 'Lost connection' em queries grandes.\n"
          "   Pressione ENTER para continuar...\n")
    
    aumentar_max_packet()
    
    print("\n" + "✅"*40)
    print("SCRIPT FINALIZADO")
    print("✅"*40 + "\n")
    
    input("Pressione ENTER para sair...")
