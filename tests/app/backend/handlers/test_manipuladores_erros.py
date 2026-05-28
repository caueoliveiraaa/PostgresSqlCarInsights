"""
Testes para o registro de manipuladores globais de erro.
"""

from fastapi import status
from fastapi.testclient import TestClient


def test_exception_handler_erro_api(test_client: TestClient) -> None:
    """
    Garante que o erro APIException é lançado e tratado.
    """
    codigo_esperado = status.HTTP_418_IM_A_TEAPOT

    response = test_client.get("/erro-api")

    assert response.status_code == codigo_esperado
    assert response.json() == {"code": codigo_esperado, "message": "Erro Custom"}


def test_exception_handler_erro_banco(test_client: TestClient) -> None:
    """
    Garante que o erro DatabaseException é lançado e tratado.
    """
    codigo_esperado = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = test_client.get("/erro-db")

    assert response.status_code == codigo_esperado
    assert "falha interagir com o banco de dados" in response.json()["message"]


def test_exception_handler_erro_config(test_client: TestClient) -> None:
    """
    Garante que o erro InvalidConfigError é lançado e tratado.
    """
    codigo_esperado = status.HTTP_406_NOT_ACCEPTABLE

    response = test_client.get("/erro-config")

    assert response.status_code == codigo_esperado
    assert response.json()["detail"] == "Configuração Inválida"


def test_exception_handler_erro_value(test_client: TestClient) -> None:
    """
    Garante que o erro ValueError é lançado e tratado.
    """
    codigo_esperado = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = test_client.get("/erro-value")

    assert response.status_code == codigo_esperado
    assert response.json()["detail"] == "Valor Incorreto"


def test_middleware_erro_inesperado(test_client: TestClient) -> None:
    """
    Garante que erros genéricos sejam capturados pelo middleware.
    """
    codigo_esperado = status.HTTP_500_INTERNAL_SERVER_ERROR

    response = test_client.get("/bug-real")

    assert response.status_code == codigo_esperado
    assert response.json() == {"code": codigo_esperado, "message": "Erro inesperado"}
