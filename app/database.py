from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Criar engine do MySQL com configurações AGRESSIVAS para DBaaS
engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,  # CRÍTICO: Testa conexão antes de usar
    pool_size=10,  # AUMENTADO: Mais conexões disponíveis
    max_overflow=20,  # AUMENTADO: Mais overflow
    pool_recycle=180,  # REDUZIDO: Reconecta a cada 3 minutos (DBaaS agressivo)
    pool_timeout=60,  # AUMENTADO: 1 minuto para pegar conexão
    connect_args={
        "connect_timeout": 60,   # 1 minuto para conectar
        "read_timeout": 60,      # 1 minuto de leitura
        "write_timeout": 60,     # 1 minuto de escrita
        "charset": "utf8mb4"     # Suporte completo UTF-8
    },
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
