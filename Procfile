# AdaptAI - Procfile
#
# MODO DE ESCALA:
# - Sem REDIS_URL: FORCE --workers 1 (rate_limit em memoria e singleton por processo).
# - Com REDIS_URL: pode aumentar --workers com seguranca (rate_limit distribuido).
#
# O cliente Anthropic (app/core/anthropic_client.py) tambem e singleton por processo,
# mas isso nao impede multi-worker - cada processo abre seu proprio pool HTTP,
# o que e comportamento normal para apps FastAPI multi-worker.
#
# Para escalar:
#   1. Adicionar plugin Redis no Railway
#   2. Setar REDIS_URL na env var do app
#   3. Trocar "--workers 1" por "--workers 2" (ou 4, dependendo da CPU)
#   4. Verificar em /health que rate_limit_backend == "redis"
web: python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
