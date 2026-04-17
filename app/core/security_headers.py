"""
Middleware que adiciona security headers conservadores nas respostas HTTP.

Por que conservador?
    AdaptAI serve tres tipos de conteudo muito diferentes:
      1. API JSON       (/api/v1/*, /, /health, /info)
      2. Storage de HTML gerado por IA (/storage/materiais/*)
      3. Docs Swagger   (/docs, /redoc, /openapi.json)

    Uma politica uniforme restritiva (tipo CSP: default-src 'none') quebraria
    os materiais adaptados gerados pela IA, que sao HTML com CSS inline,
    imagens base64, e as vezes JavaScript simples. Ela tambem quebraria o
    Swagger, que carrega CSS/JS de CDN.

    Entao este middleware SO aplica headers que sao seguros em todas as rotas:

      - X-Content-Type-Options: nosniff
      - Referrer-Policy: strict-origin-when-cross-origin
      - Permissions-Policy: restritivo para APIs
      - X-Frame-Options: DENY (so em rotas de API JSON, nao /storage)
      - Strict-Transport-Security (so em producao HTTPS)

    Nao aplicamos Content-Security-Policy globalmente por enquanto - seria
    necessario definir politicas diferentes por path, o que e complexidade
    extra sem ganho proporcional enquanto o tamanho da superficie de ataque
    e moderado. Deixado para quando o produto estabilizar.

Referencias:
    - OWASP Secure Headers Project
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


# Headers aplicados em TODA resposta - sao seguros universalmente.
_HEADERS_SEMPRE = {
    # Bloqueia o browser de "adivinhar" content-type (protege contra XSS
    # via upload malicioso que e servido com content-type errado).
    "X-Content-Type-Options": "nosniff",

    # Libera apenas origin + path na navegacao cross-site, omite query string.
    # Protege query params sensiveis (ex: tokens em URLs, embora nao usemos).
    "Referrer-Policy": "strict-origin-when-cross-origin",

    # Desabilita features sensiveis do browser. AdaptAI nao usa camera,
    # microfone, geolocalizacao nem pagamentos via web API.
    "Permissions-Policy": (
        "camera=(), microphone=(), geolocation=(), payment=(), "
        "usb=(), magnetometer=(), gyroscope=(), accelerometer=()"
    ),
}


# Paths onde NAO aplicamos X-Frame-Options: DENY porque precisam ser embutidos
# em iframes pelo frontend (materiais adaptados sao HTML renderizado em iframe
# no portal do aluno).
_PATHS_SEM_FRAME_OPTIONS = (
    "/storage/materiais/",
    "/storage/registros_diarios/",
    # Swagger e Redoc tambem - podem ser embutidos por ferramentas internas
    "/docs",
    "/redoc",
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Aplica security headers nas respostas.

    Args:
        is_production: se True, ativa HSTS (Strict-Transport-Security).
                       HSTS so faz sentido se o app SEMPRE roda em HTTPS.
                       Em dev (localhost) ativar HSTS pode quebrar navegacao
                       futura ao mesmo host se usar HTTP.
    """

    def __init__(self, app, *, is_production: bool):
        super().__init__(app)
        self.is_production = is_production

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Aplicar headers universais
        for k, v in _HEADERS_SEMPRE.items():
            # Nao sobrescrever se o endpoint ja setou (caso raro mas possivel)
            response.headers.setdefault(k, v)

        # X-Frame-Options: DENY exceto em paths que precisam ser embutidos
        path = request.url.path
        if not any(path.startswith(p) for p in _PATHS_SEM_FRAME_OPTIONS):
            response.headers.setdefault("X-Frame-Options", "DENY")

        # HSTS so em producao. 1 ano de max-age, includeSubDomains,
        # mas SEM "preload" - preload exige garantias operacionais.
        if self.is_production:
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )

        return response
