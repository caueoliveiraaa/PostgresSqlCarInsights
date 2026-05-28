"""
Fixtures para os testes do main da aplicação.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.config_api import ConfigApi


@pytest.fixture
def mock_config_api() -> ConfigApi:
    """
    Gera uma instância real de ConfigApi para testes.
    """
    return ConfigApi()


@pytest.fixture
def mock_fastapi_app() -> MagicMock:
    """
    Mock para a instância do FastAPI.
    """
    return MagicMock(spec=FastAPI)


@pytest.fixture
def mock_registra_manipuladores() -> Generator[MagicMock, None, None]:
    """
    Mock para a função registra_manipuladores_erros.
    """
    with patch("app.main.registra_manipuladores_erros") as mocked:
        yield mocked


@pytest.fixture
def mock_registra_middleware() -> Generator[MagicMock, None, None]:
    """
    Mock para a função registra_middleware_erro.
    """
    with patch("app.main.registra_middleware_erro") as mocked:
        yield mocked


@pytest.fixture
def mock_include_router() -> Generator[MagicMock, None, None]:
    """
    Mock para o método include_router da classe FastAPI.
    """
    with patch("fastapi.FastAPI.include_router") as mocked:
        yield mocked


@pytest.fixture
def mock_busca_engines() -> Generator[MagicMock, None, None]:
    """
    Mocka a função busca_engines para retornar um dicionário de engines fictícias.
    """
    mock_engine_1 = AsyncMock(spec=AsyncEngine)
    mock_engine_2 = AsyncMock(spec=AsyncEngine)
    mock_engines_dict = {"db1": mock_engine_1, "db2": mock_engine_2}

    with patch("app.main.busca_engines") as mocked:
        mocked.return_value = mock_engines_dict
        yield mocked
