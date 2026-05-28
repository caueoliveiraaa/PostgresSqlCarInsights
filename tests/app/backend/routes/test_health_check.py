"""
Testes para as rotas de health check.
"""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(health_client: AsyncClient) -> None:
    """
    Garante que o endpoint raiz retorna a mensagem correta.
    """
    response = await health_client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Raiz funcionando!"}


@pytest.mark.asyncio
async def test_get_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste GET.
    """
    response = await health_client.get("/test-get")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["method"] == "GET"


@pytest.mark.asyncio
async def test_post_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste POST enviando o esquema HealthCheck.
    """
    payload = {"texto_teste": "online", "inteiro_teste": 1}

    response = await health_client.post("/test-post", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["method"] == "POST"
    assert response.json()["dados_recebidos"] == payload


@pytest.mark.asyncio
async def test_put_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste PUT.
    """
    payload = {"texto_teste": "updated", "inteiro_teste": 1}

    response = await health_client.put("/test-put", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["method"] == "PUT"
    assert response.json()["dados_recebidos"] == payload


@pytest.mark.asyncio
async def test_patch_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste PATCH.
    """
    payload = {"texto_teste": "partial_update", "inteiro_teste": 1}

    response = await health_client.patch("/test-patch", json=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["method"] == "PATCH"
    assert response.json()["dados_recebidos"] == payload


@pytest.mark.asyncio
async def test_delete_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste DELETE.
    """
    response = await health_client.delete("/test-delete")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["method"] == "DELETE"


@pytest.mark.asyncio
async def test_head_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste HEAD (não retorna corpo, apenas status).
    """
    response = await health_client.head("/test-head")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == ""


@pytest.mark.asyncio
async def test_options_debug(health_client: AsyncClient) -> None:
    """
    Valida o endpoint de teste OPTIONS e os headers permitidos.
    """
    response = await health_client.options("/test-options")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "Allow" in response.headers
    assert "GET" in response.headers["Allow"]
