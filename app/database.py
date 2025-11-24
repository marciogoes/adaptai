from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Criar engine do MySQL com configurações robustas para produção
engine = create_engine(
    settings.db_url,  # Usa a propriedade que decide entre DATABASE_URL ou partes
    pool_pre_ping=True,  # Testa conexão antes de usar
    pool_size=5,  # Reduzido para economizar recursos em produção
    max_overflow=10,
    pool_recycle=1800,  # Reconecta a cada 30 minutos
    pool_timeout=30,  # Timeout de 30s para pegar conexão
    connect_args={
        "connect_timeout": 60  # Timeout de conexão MySQL
    },
    echo=settings.DEBUG  # Só mostra SQL se DEBUG=True
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
