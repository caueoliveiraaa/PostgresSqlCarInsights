"""
Testes para dependências de autenticação e manipulação de usuários.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.dependencies.login_auth import (
    injeta_autenticacao_jwt,
    injeta_manipulador_token,
    injeta_manipulador_usuarios,
)
from app.schemas.login_auth import TokenDecode
from app.services.login_auth import (
    ManipuladorTokenService,
    ManipuladorUsuarioService,
)


@pytest.mark.asyncio
async def test_injeta_manipulador_token() -> None:
    """
    Garante que retorna um ManipuladorToken.
    """
    token = await injeta_manipulador_token()

    assert isinstance(token, ManipuladorTokenService)


@pytest.mark.asyncio
async def test_injeta_autenticacao_jwt(mock_manipulador_token: MagicMock) -> None:
    """
    Garante que a função utiliza o manipulador para decodificar o token de
    forma assíncrona.
    """
    token_fake = "jwt_token_abc"
    payload_esperado = TokenDecode(sub="user", iat=111, exp=222)
    mock_manipulador_token.decodifica_token = AsyncMock(
        return_value=payload_esperado
    )

    resultado = await injeta_autenticacao_jwt(
        manipulador=mock_manipulador_token, token=token_fake
    )

    assert resultado == payload_esperado
    mock_manipulador_token.decodifica_token.assert_called_once_with(token_fake)


@pytest.mark.asyncio
async def test_injeta_manipulador_usuarios() -> None:
    """
    Garante que retorna um ManipuladorUsuario.
    """
    mock_sessao = AsyncMock(spec=AsyncSession)

    usuario = await injeta_manipulador_usuarios(mock_sessao)

    assert isinstance(usuario, ManipuladorUsuarioService)
