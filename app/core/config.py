from pydantic_settings import BaseSettings
from typing import List, Optional
from urllib.parse import quote_plus
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AdaptAI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database MySQL - Opcional se DATABASE_URL estiver definido
    # Railway/produção pode usar DATABASE_URL OU variáveis separadas
    MYSQL_HOST: Optional[str] = None
    MYSQL_PORT: int = 3306
    MYSQL_USER: Optional[str] = None
    MYSQL_PASSWORD: Optional[str] = None
    MYSQL_DATABASE: Optional[str] = None
    
    # Ou usar DATABASE_URL diretamente (para Railway)
    DATABASE_URL: Optional[str] = None
    
    @property
    def db_url(self) -> str:
        """
        Constrói URL do banco de dados.
        Prioridade: DATABASE_URL > variáveis separadas
        """
        # Se DATABASE_URL estiver definido, usa ele diretamente
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Senão, monta a URL a partir das partes
        # Valida que todas as variáveis necessárias estão presentes
        if not all([self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_DATABASE]):
            raise ValueError(
                "❌ ERRO: DATABASE_URL não definido e variáveis MYSQL_* incompletas.\n"
                "Defina DATABASE_URL OU todas as variáveis: MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE"
            )
        
        encoded_password = quote_plus(self.MYSQL_PASSWORD) if self.MYSQL_PASSWORD else ""
        
        db_url = f"mysql+pymysql://{self.MYSQL_USER}:{encoded_password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        
        # Log para debug (sem mostrar senha completa)
        if self.DEBUG:
            safe_url = f"mysql+pymysql://{self.MYSQL_USER}:***@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            print(f"[CONFIG] Database URL: {safe_url}")
        
        return db_url
    
    # Security
    SECRET_KEY: str = "adaptai-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    # Claude API (Anthropic)
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-haiku-20240307"
    
    # CORS - Origens permitidas (separadas por vírgula)
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,https://*.vercel.app"
    
    @property
    def cors_origins(self) -> List[str]:
        """Converte a string de CORS em lista"""
        origins = [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        # Em produção, permite qualquer subdomínio vercel.app
        if self.ENVIRONMENT == "production":
            origins.append("https://*.vercel.app")
        return origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"
        
        # Permite ler variáveis de ambiente mesmo sem .env
        # Importante para Railway/Docker
        env_file_encoding = 'utf-8'

# Instancia as configurações
settings = Settings()

# Debug: mostra quais variáveis foram carregadas (apenas em produção para debug)
if settings.ENVIRONMENT == "production":
    import os
    print(f"[DEBUG] DATABASE_URL presente: {bool(settings.DATABASE_URL)}")
    print(f"[DEBUG] DATABASE_URL valor (primeiros 20 chars): {str(settings.DATABASE_URL)[:20] if settings.DATABASE_URL else 'None'}")
    print(f"[DEBUG] MYSQL_HOST: {bool(settings.MYSQL_HOST)}")
    print(f"[DEBUG] MYSQL_USER: {bool(settings.MYSQL_USER)}")
    print(f"[DEBUG] Env vars disponíveis: {', '.join([k for k in os.environ.keys() if 'MYSQL' in k or 'DATABASE' in k])}")

# Validação adicional em produção
if settings.ENVIRONMENT == "production":
    # Verifica DATABASE_URL OU variáveis MYSQL separadas
    # Trata strings vazias como None
    has_database_url = bool(settings.DATABASE_URL and settings.DATABASE_URL.strip())
    has_mysql_vars = all([
        settings.MYSQL_HOST and settings.MYSQL_HOST.strip(),
        settings.MYSQL_USER and settings.MYSQL_USER.strip(),
        settings.MYSQL_PASSWORD and settings.MYSQL_PASSWORD.strip(),
        settings.MYSQL_DATABASE and settings.MYSQL_DATABASE.strip()
    ])
    
    if not has_database_url and not has_mysql_vars:
        raise ValueError(
            "❌ ERRO: Configure DATABASE_URL OU todas as variáveis MYSQL_* (HOST, USER, PASSWORD, DATABASE)\n"
            "Configure no Railway/Render/Docker antes de fazer deploy!"
        )
    
    # Verifica SECRET_KEY
    if not settings.SECRET_KEY or settings.SECRET_KEY == "adaptai-secret-key-change-in-production-2024":
        print("⚠️  WARNING: Configure SECRET_KEY única em produção!")
