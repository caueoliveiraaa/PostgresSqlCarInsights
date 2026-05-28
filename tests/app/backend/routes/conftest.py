"""
Fixtures para testes do módulo routes.
"""

from collections.abc import AsyncGenerator
from typing import NamedTuple
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.backend.dependencies.database import injeta_sessao_api
from app.backend.dependencies.exemplo import injeta_consultor
from app.backend.dependencies.login_auth import (
    injeta_autenticacao_jwt,
    injeta_manipulador_token,
    injeta_manipulador_usuarios,
)
from app.backend.routes.exemplo import router_exemplo
from app.backend.routes.health_check import router_health
from app.backend.routes.login_auth import router_login


class ClientExemplo(NamedTuple):
    """
    Classe mock responsável por carregar o AsyncClient e a injeção de dependência
    para o consultor de dados assíncrono.
    """

    client: AsyncClient
    mock_consultor: AsyncMock


@pytest.fixture
async def exemplo_client() -> AsyncGenerator[ClientExemplo, None]:
    """
    Gera uma instância da classe ClientExemplo com AsyncClient e mocks assíncronos.
    """
    app = FastAPI()
    app.include_router(router_exemplo)
    mock_consultor = AsyncMock()
    mock_payload = {"sub": "teste_user"}

    app.dependency_overrides[injeta_consultor] = lambda: mock_consultor
    app.dependency_overrides[injeta_autenticacao_jwt] = lambda: mock_payload

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield ClientExemplo(client=async_client, mock_consultor=mock_consultor)


@pytest.fixture
async def health_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Gera um AsyncClient configurado apenas com as rotas de debug.
    """
    app = FastAPI()
    app.include_router(router_health)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield async_client


class ClientLogin(NamedTuple):
    """
    Classe mock responsável por carregar o AsyncClient e mocks de autenticação.
    """

    client: AsyncClient
    mock_usu: AsyncMock
    mock_token: AsyncMock
    mock_sessao: AsyncMock


@pytest.fixture
async def login_client() -> AsyncGenerator[ClientLogin, None]:
    """
    Gera um AsyncClient configurado para testes de login.
    """
    app = FastAPI()
    app.include_router(router_login)
    mock_usu = AsyncMock()
    mock_token = AsyncMock()
    mock_sessao = AsyncMock()

    app.dependency_overrides[injeta_manipulador_usuarios] = lambda: mock_usu
    app.dependency_overrides[injeta_manipulador_token] = lambda: mock_token
    app.dependency_overrides[injeta_sessao_api] = lambda: mock_sessao

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_client:
        yield ClientLogin(
            client=async_client,
            mock_usu=mock_usu,
            mock_token=mock_token,
            mock_sessao=mock_sessao,
        )
