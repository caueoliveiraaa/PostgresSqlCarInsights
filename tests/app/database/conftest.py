"""
Fixtures para testes do módulo database.
"""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


@pytest.fixture
def mock_engine() -> MagicMock:
    """
    Mock para a Engine do SQLAlchemy.
    """
    return MagicMock(spec=Engine)


@pytest.fixture
def mock_async_engine() -> MagicMock:
    """
    Mock para a AsyncEngine do SQLAlchemy.
    """
    return MagicMock(spec=AsyncEngine)


@pytest.fixture
def mock_async_session() -> AsyncMock:
    """
    Mock para a AsyncSession do SQLAlchemy.
    """
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_create_async_engine(
    mock_async_engine: MagicMock,
) -> Generator[MagicMock, None, None]:
    """
    Gera um mock da função responsável pela criação das Engines assíncronas.
    """
    with patch("app.database.conexao.create_async_engine") as mocked:
        mocked.return_value = mock_async_engine
        yield mocked


@pytest.fixture
def mock_create_engine(
    mock_engine: MagicMock,
) -> Generator[MagicMock, None, None]:
    """
    Gera um mock da função responsável pela criação das Engines síncronas.
    """
    with patch("app.database.conexao.create_engine") as mocked:
        mocked.return_value = mock_engine
        yield mocked


@pytest.fixture
def mock_async_sessionmaker(
    mock_async_session: AsyncMock,
) -> Generator[MagicMock, None, None]:
    """
    Gera um mock para async_sessionmaker que retorna um gerenciador de
    contexto assíncrono.
    """
    with patch("app.database.conexao.async_sessionmaker") as mocked:
        mock_factory = MagicMock(spec=async_sessionmaker)
        mock_factory.return_value.__aenter__.return_value = mock_async_session
        mocked.return_value = mock_factory
        yield mocked
