"""
Fixtures para testes do módulo dependencies.
"""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.login_auth import ManipuladorTokenService


@pytest.fixture
async def mock_cria_db() -> AsyncGenerator[MagicMock, None]:
    """
    Simula o comportamento de um AsyncGenerator para o método cria_db.
    """

    async def gerador_async(
        *args: object, **kwargs: object
    ) -> AsyncGenerator[MagicMock, None]:
        """
        Simula o gerador que gera a sessão via 'yield'.
        """
        yield MagicMock(spec=AsyncSession)

    with patch("app.backend.dependencies.database.cria_db") as mock_patch:
        mock_patch.side_effect = gerador_async
        yield mock_patch


@pytest.fixture
def mock_manipulador_token() -> MagicMock:
    """
    Gera um mock da classe ManipuladorTokenService com o retorno do
    método decodifica_token já pré-configurado.
    """
    mock_manipulador = MagicMock(spec=ManipuladorTokenService)
    mock_manipulador.decodifica_token.return_value = {"user": "teste_user"}

    return mock_manipulador
