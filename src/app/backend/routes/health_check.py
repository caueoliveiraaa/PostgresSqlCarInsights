"""
Define os endpoints de teste de funcionamento.
"""

from fastapi import APIRouter, Response, status

from app.schemas.health_check import HealthCheck

router_health = APIRouter(prefix="", tags=["Debug"])


@router_health.get("/", status_code=status.HTTP_200_OK)
async def root() -> dict[str, str]:
    """
    Endpoint raiz da API.
    """
    return {
        "message": "Raiz funcionando!",
    }


@router_health.get("/test-get", status_code=status.HTTP_200_OK)
async def test_get() -> dict[str, str]:
    """
    Endpoint de teste para requisições GET.
    """
    return {
        "method": "GET",
        "message": "GET funcionando!",
    }


@router_health.post("/test-post", status_code=status.HTTP_201_CREATED)
async def test_post(dados: HealthCheck) -> dict[str, str | HealthCheck]:
    """
    Endpoint de teste para requisições POST.
    """
    return {
        "method": "POST",
        "message": "POST funcionando!",
        "dados_recebidos": dados,
    }


@router_health.put("/test-put", status_code=status.HTTP_200_OK)
async def test_put(dados: HealthCheck) -> dict[str, str | HealthCheck]:
    """
    Endpoint de teste para requisições PUT.
    """
    return {
        "method": "PUT",
        "message": "PUT funcionando!",
        "dados_recebidos": dados,
    }


@router_health.patch("/test-patch", status_code=status.HTTP_200_OK)
async def test_patch(dados: HealthCheck) -> dict[str, str | HealthCheck]:
    """
    Endpoint de teste para requisições PATCH.
    """
    return {
        "method": "PATCH",
        "message": "PATCH funcionando!",
        "dados_recebidos": dados,
    }


@router_health.delete("/test-delete", status_code=status.HTTP_200_OK)
async def test_delete() -> dict[str, str]:
    """
    Endpoint de teste para requisições DELETE.
    """
    return {
        "method": "DELETE",
        "message": "DELETE funcionando!",
    }


@router_health.head("/test-head", status_code=status.HTTP_200_OK)
async def test_head() -> Response:
    """
    Endpoint de teste para requisições HEAD.
    """
    return Response(status_code=status.HTTP_200_OK)


@router_health.options("/test-options", status_code=status.HTTP_204_NO_CONTENT)
async def test_options() -> Response:
    """
    Endpoint de teste para requisições OPTIONS.
    """
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
        headers={
            "Allow": "GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS",
        },
    )
