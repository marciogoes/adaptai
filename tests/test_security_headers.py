"""
Testes do SecurityHeadersMiddleware.

Cobre:
    - Headers aplicados em rotas API JSON (X-Content-Type-Options, etc)
    - X-Frame-Options: DENY em API, ausente em /storage/materiais e /docs
    - HSTS so em producao
    - Headers nao sobrescrevem valores ja setados pelo endpoint
"""
import pytest
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.testclient import TestClient

from app.core.security_headers import SecurityHeadersMiddleware


def _make_app(is_production: bool) -> FastAPI:
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware, is_production=is_production)

    @app.get("/api/v1/coisa")
    def rota_api():
        return {"ok": True}

    @app.get("/storage/materiais/123")
    def rota_storage():
        return Response(content="<html></html>", media_type="text/html")

    @app.get("/docs")
    def rota_docs():
        return {"docs": True}

    @app.get("/com-header-custom")
    def rota_custom():
        r = Response(content="{}", media_type="application/json")
        r.headers["X-Frame-Options"] = "SAMEORIGIN"  # Endpoint tem preferencia
        return r

    return app


class TestHeadersUniversais:
    def test_api_recebe_headers_basicos(self):
        client = TestClient(_make_app(is_production=False))
        r = client.get("/api/v1/coisa")
        assert r.status_code == 200
        assert r.headers["X-Content-Type-Options"] == "nosniff"
        assert r.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
        assert "camera=()" in r.headers["Permissions-Policy"]

    def test_storage_tambem_recebe_headers_basicos(self):
        client = TestClient(_make_app(is_production=False))
        r = client.get("/storage/materiais/123")
        assert r.headers["X-Content-Type-Options"] == "nosniff"
        assert r.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


class TestXFrameOptions:
    def test_api_tem_x_frame_options_deny(self):
        client = TestClient(_make_app(is_production=False))
        r = client.get("/api/v1/coisa")
        assert r.headers.get("X-Frame-Options") == "DENY"

    def test_storage_materiais_nao_tem_x_frame_options(self):
        """Materiais sao renderizados em iframe pelo portal do aluno."""
        client = TestClient(_make_app(is_production=False))
        r = client.get("/storage/materiais/123")
        assert "X-Frame-Options" not in r.headers

    def test_docs_nao_tem_x_frame_options(self):
        client = TestClient(_make_app(is_production=False))
        r = client.get("/docs")
        assert "X-Frame-Options" not in r.headers


class TestHSTS:
    def test_dev_nao_tem_hsts(self):
        """Dev usa HTTP local - HSTS aqui quebra navegacao futura."""
        client = TestClient(_make_app(is_production=False))
        r = client.get("/api/v1/coisa")
        assert "Strict-Transport-Security" not in r.headers

    def test_producao_tem_hsts(self):
        client = TestClient(_make_app(is_production=True))
        r = client.get("/api/v1/coisa")
        hsts = r.headers.get("Strict-Transport-Security")
        assert hsts is not None
        assert "max-age=31536000" in hsts
        assert "includeSubDomains" in hsts


class TestNaoSobrescreve:
    def test_endpoint_pode_setar_x_frame_options_proprio(self):
        """Middleware usa setdefault - nao pisa em headers setados pelo endpoint."""
        client = TestClient(_make_app(is_production=False))
        r = client.get("/com-header-custom")
        assert r.headers["X-Frame-Options"] == "SAMEORIGIN"  # nao foi trocado para DENY
