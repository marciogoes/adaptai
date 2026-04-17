"""
Testes do helper de paginacao.
"""
from app.core.pagination import PaginationParams, build_page


class TestPaginationParams:
    def test_defaults(self):
        p = PaginationParams()
        assert p.page == 1
        assert p.size == 20
        assert p.offset == 0
        assert p.limit == 20
    
    def test_offset_calculado_corretamente(self):
        p = PaginationParams(page=3, size=10)
        assert p.offset == 20  # (3-1)*10
        assert p.limit == 10


class TestBuildPage:
    def test_primeira_pagina(self):
        p = PaginationParams(page=1, size=10)
        result = build_page(items=["a", "b", "c"], total=25, pagination=p)
        
        assert result["items"] == ["a", "b", "c"]
        assert result["meta"]["page"] == 1
        assert result["meta"]["size"] == 10
        assert result["meta"]["total"] == 25
        assert result["meta"]["total_pages"] == 3
        assert result["meta"]["has_next"] is True
        assert result["meta"]["has_prev"] is False
    
    def test_ultima_pagina(self):
        p = PaginationParams(page=3, size=10)
        result = build_page(items=["y", "z"], total=22, pagination=p)
        
        assert result["meta"]["total_pages"] == 3  # ceil(22/10)
        assert result["meta"]["has_next"] is False
        assert result["meta"]["has_prev"] is True
    
    def test_total_zero(self):
        p = PaginationParams()
        result = build_page(items=[], total=0, pagination=p)
        assert result["meta"]["total_pages"] == 0
        assert result["meta"]["has_next"] is False
        assert result["meta"]["has_prev"] is False
    
    def test_exata_divisao(self):
        """Quando total e multiplo exato de size, nao deve criar pagina extra."""
        p = PaginationParams(page=1, size=10)
        result = build_page(items=[], total=30, pagination=p)
        assert result["meta"]["total_pages"] == 3
