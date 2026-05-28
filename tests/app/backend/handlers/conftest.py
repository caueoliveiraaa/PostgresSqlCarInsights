"""
Fixtures para testes do módulo handlers.
"""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.backend.handlers.manipuladores_erros import (
    registra_manipuladores_erros,
    registra_middleware_erro,
)
from app.errors.configuracao_invalida import InvalidConfigError
from app.errors.excecao_api import APIException
from app.errors.excecao_banco import DatabaseException


@pytest.fixture
def test_client() -> TestClient:
    """
    Gera um TestClient com rotas pré-configuradas para lançamento de
    exceções para os testes dos manipuladores.
    """
    app = FastAPI()
    registra_manipuladores_erros(app)
    registra_middleware_erro(app)

    @app.get("/erro-api")
    def rota_api_error() -> None:
        """Lança exceção APIException."""
        raise APIException(
            codigo=status.HTTP_418_IM_A_TEAPOT, mensagem="Erro Custom"
        )

    @app.get("/erro-db")
    def rota_db_error() -> None:
        """Lança exceção DatabaseException."""
        raise DatabaseException()

    @app.get("/erro-config")
    def rota_config_error() -> None:
        """Lança exceção InvalidConfigError."""
        raise InvalidConfigError("Configuração Inválida")

    @app.get("/erro-value")
    def rota_value_error() -> None:
        """Lança exceção ValueError."""
        raise ValueError("Valor Incorreto")

    @app.get("/bug-real")
    def rota_bug() -> None:
        """Lança exceção RuntimeError."""
        raise RuntimeError("Algo quebrou no projeto")

    return TestClient(app)
