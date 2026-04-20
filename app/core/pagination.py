"""
Utilitarios de paginacao para endpoints de listagem.

MOTIVACAO: antes, endpoints como GET /relatorios, GET /materiais retornavam
TODOS os registros. Com escolas crescendo, isso se torna lento e pesado.

Uso tipico:

    from fastapi import Depends
    from app.core.pagination import PaginationParams, paginated_response
    
    @router.get("/materiais")
    def listar(pagination: PaginationParams = Depends()):
        query = db.query(Material).order_by(Material.created_at.desc())
        return paginated_response(query, pagination)

Ou manual para queries mais customizadas:

    query = db.query(...).order_by(...)
    total = query.count()
    items = query.offset(pagination.offset).limit(pagination.limit).all()
    return build_page(items=items, total=total, pagination=pagination)
"""
from typing import Any, Dict, List, Optional, Annotated
from fastapi import Query


class PaginationParams:
    """
    Dependency injectavel que captura page e size das query strings.
    
    Defaults seguros:
    - page 1 (comeca em 1, nao 0 - mais natural para clientes)
    - size 20 (ok para dashboards; max 100 para evitar dump massivo)
    
    FIX: antes, `__init__` recebia `page: int = Query(1, ge=1)` direto.
    Isso funcionava quando o FastAPI resolvia via Depends(PaginationParams),
    mas quebrava na instanciacao direta (PaginationParams() -> self.page
    recebia o objeto Query, nao o int 1). Agora usa Annotated[int, Query(...)]:
    o FastAPI le a metadata via Annotated mas o default real e um int, entao
    PaginationParams() -> self.page == 1 funciona tambem em testes e codigo
    que nao e endpoint.
    """
    
    def __init__(
        self,
        page: Annotated[int, Query(ge=1, description="Pagina (comecando em 1)")] = 1,
        size: Annotated[int, Query(ge=1, le=100, description="Itens por pagina (max 100)")] = 20,
    ):
        self.page = page
        self.size = size
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size
    
    @property
    def limit(self) -> int:
        return self.size


def build_page(
    items: List[Any],
    total: int,
    pagination: PaginationParams,
) -> Dict[str, Any]:
    """
    Monta resposta paginada a partir de items ja carregados + total.
    Retorna dict para ser serializado pelo FastAPI (evita problemas de generics).
    """
    total_pages = (total + pagination.size - 1) // pagination.size if total > 0 else 0
    
    return {
        "items": items,
        "meta": {
            "page": pagination.page,
            "size": pagination.size,
            "total": total,
            "total_pages": total_pages,
            "has_next": pagination.page < total_pages,
            "has_prev": pagination.page > 1,
        },
    }


def paginated_response(
    query,
    pagination: PaginationParams,
    serializer: Optional[callable] = None,
) -> Dict[str, Any]:
    """
    Helper que recebe uma Query do SQLAlchemy ja pronta e devolve pagina.
    
    Args:
        query: SQLAlchemy Query com filtros + ordenacao ja aplicados
        pagination: parametros de paginacao (page, size)
        serializer: funcao opcional para converter cada item (ex: para dict)
    """
    total = query.count()
    items = query.offset(pagination.offset).limit(pagination.limit).all()
    
    if serializer:
        items = [serializer(item) for item in items]
    
    return build_page(items=items, total=total, pagination=pagination)
