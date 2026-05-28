"""
Testes assíncronos para as rotas de exemplo.
"""

import pytest
from fastapi import status

from app.schemas.exemplo import ConsultaExemplo
from tests.app.backend.routes.conftest import ClientExemplo

pytestmark = pytest.mark.asyncio


async def test_busca_dados_protegidos(exemplo_client: ClientExemplo) -> None:
    """
    Garante que a rota protegida retorna dados e valida o payload.
    """
    id_alvo = 1
    dados_mock = ConsultaExemplo(id=id_alvo, descricao="desc", ativo=True)
    exemplo_client.mock_consultor.consulta_dados_mock.return_value = dados_mock

    response = await exemplo_client.client.get("/exemplo-protegido")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == id_alvo
    exemplo_client.mock_consultor.consulta_dados_mock.assert_called_once()


async def test_busca_dados_mock(exemplo_client: ClientExemplo) -> None:
    """
    Garante o funcionamento do GET público.
    """
    id_alvo = 2
    dados_mock = ConsultaExemplo(id=id_alvo, descricao="desc", ativo=True)
    exemplo_client.mock_consultor.consulta_dados_mock.return_value = dados_mock

    response = await exemplo_client.client.get("/exemplo")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == id_alvo


async def test_cria_exemplo(exemplo_client: ClientExemplo) -> None:
    """
    Garante que o POST envia dados e retorna o objeto criado.
    """
    id_alvo = 3
    dados_retorno = ConsultaExemplo(id=id_alvo, descricao="desc", ativo=True)
    dados_envio = {"id": id_alvo, "descricao": "desc", "ativo": True}
    exemplo_client.mock_consultor.gera_dados_mock.return_value = dados_retorno

    response = await exemplo_client.client.post("/exemplo", json=dados_envio)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == id_alvo
    exemplo_client.mock_consultor.gera_dados_mock.assert_called_once()


async def test_altera_exemplo(exemplo_client: ClientExemplo) -> None:
    """
    Garante que o PATCH atualiza o recurso corretamente.
    """
    id_alvo = 4
    dados_patch = {"id": id_alvo, "descricao": "desc", "ativo": True}
    dados_finais = ConsultaExemplo(id=id_alvo, descricao="desc", ativo=True)
    exemplo_client.mock_consultor.modifica_dados_mock.return_value = dados_finais

    response = await exemplo_client.client.patch(
        f"/exemplo/{id_alvo}", json=dados_patch
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == id_alvo


async def test_deleta_exemplo(exemplo_client: ClientExemplo) -> None:
    """
    Garante que o DELETE remove o recurso e retorna os dados excluídos.
    """
    id_alvo = 5
    dados_excluidos = ConsultaExemplo(id=5, descricao="desc", ativo=True)
    exemplo_client.mock_consultor.remove_dados_mock.return_value = dados_excluidos

    response = await exemplo_client.client.delete(f"/exemplo/{id_alvo}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == id_alvo
    exemplo_client.mock_consultor.remove_dados_mock.assert_called_once_with(id_alvo)
