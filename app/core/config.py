from pydantic_settings import BaseSettings
from typing import List
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AdaptAI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Database MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "adaptai"
    
    # Ou usar DATABASE_URL diretamente (para Railway)
    DATABASE_URL: str = ""
    
    @property
    def db_url(self) -> str:
        # Se DATABASE_URL estiver definido, usa ele diretamente
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # Senão, monta a URL a partir das partes
        encoded_password = quote_plus(self.MYSQL_PASSWORD) if self.MYSQL_PASSWORD else ""
        return f"mysql+pymysql://{self.MYSQL_USER}:{encoded_password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    
    # Security
    SECRET_KEY: str = "adaptai-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    # Claude API (Anthropic)
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-haiku-20240307"
    
    # CORS - Origens permitidas (separadas por vírgula)
    # Em produção, adicione o domínio do Vercel aqui
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

settings = Settings()
