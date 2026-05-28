"""
Fixtures para testes do módulo services.
"""

from unittest.mock import MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.usuarios import UsuariosRepository


@pytest.fixture
def mock_sessao() -> MagicMock:
    """
    Gera uma instância mocada de uma sessão assíncrona.
    """
    return MagicMock(spec=AsyncSession)


@pytest.fixture
def usuarios_repository(mock_sessao: MagicMock) -> UsuariosRepository:
    """
    Gera uma instância mocada do repositório de usuários.
    """
    return UsuariosRepository(mock_sessao)
