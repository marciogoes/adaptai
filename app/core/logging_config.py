"""
Logging estruturado central.

MOTIVACAO: antes o codigo usava print() em toda parte, o que:
- Nao tem niveis (debug/info/warning/error) - tudo aparece igual
- Nao pode ser filtrado em producao
- Nao tem timestamps padronizados
- Polui stdout sem estrutura

Uso:

    from app.core.logging_config import get_logger
    logger = get_logger(__name__)
    
    logger.info("Usuario logado", extra={"user_id": user.id})
    logger.warning("Rate limit atingido", extra={"ip": ip})
    logger.error("Falha na IA", exc_info=True)

Em desenvolvimento: formato legivel com cores.
Em producao (Railway): JSON estruturado para facilitar parsing em ferramentas como Datadog/Logtail.
"""
import logging
import os
import sys
import json
from datetime import datetime, timezone


IS_PRODUCTION = bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PRODUCTION"))


class _JsonFormatter(logging.Formatter):
    """Formata log como JSON em uma linha (ideal para producao)."""
    
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        
        # Incluir dados extras passados via extra={}
        for attr, value in record.__dict__.items():
            if attr in ("args", "asctime", "created", "exc_info", "exc_text",
                        "filename", "funcName", "levelname", "levelno", "lineno",
                        "message", "module", "msecs", "msg", "name", "pathname",
                        "process", "processName", "relativeCreated", "stack_info",
                        "thread", "threadName", "taskName"):
                continue
            try:
                json.dumps(value)  # apenas incluir se serializavel
                payload[attr] = value
            except (TypeError, ValueError):
                payload[attr] = str(value)
        
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(payload, ensure_ascii=False)


class _DevFormatter(logging.Formatter):
    """Formato legivel para desenvolvimento."""
    
    def format(self, record: logging.LogRecord) -> str:
        level = record.levelname
        ts = datetime.now().strftime("%H:%M:%S")
        name = record.name.split(".")[-1]
        msg = record.getMessage()
        
        line = f"[{ts}] [{level:<7}] [{name}] {msg}"
        
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        
        return line


_configured = False


def setup_logging(level: str = "INFO"):
    """
    Configura logging global. Chamado uma vez no startup.
    """
    global _configured
    if _configured:
        return
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Remove handlers padrao (evita duplicacao)
    root = logging.getLogger()
    for h in root.handlers[:]:
        root.removeHandler(h)
    
    handler = logging.StreamHandler(sys.stdout)
    
    if IS_PRODUCTION:
        handler.setFormatter(_JsonFormatter())
    else:
        handler.setFormatter(_DevFormatter())
    
    root.addHandler(handler)
    root.setLevel(log_level)
    
    # Silenciar libs muito verbosas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.INFO)
    
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Retorna logger com o nome especificado (tipicamente __name__).
    Garante que setup_logging ja foi chamado.
    """
    if not _configured:
        setup_logging()
    return logging.getLogger(name)
