"""
Testes para as rotas de login e autenticação.
"""

from unittest.mock import MagicMock

import pytest
from fastapi import status

from app.models.base_api.user_auth import UserAuth
from tests.app.backend.routes.conftest import ClientLogin


@pytest.mark.asyncio
async def test_realiza_login(login_client: ClientLogin) -> None:
    """
    Garante que o login retorna um token válido quando as credenciais estão corretas.
    """
    mock_user = MagicMock(spec=UserAuth)
    mock_user.id = 123

    login_client.mock_usu.autentica_usuario.return_value = mock_user
    login_client.mock_token.cria_token_acesso.return_value = "token_gerado"
    login_client.mock_token.settings.TOKEN_TYPE = "token_tipo"

    dados_login = {"username": "usuario", "password": "senha123"}
    response = await login_client.client.post("/login/token", data=dados_login)

    login_client.mock_usu.autentica_usuario.assert_called_once()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "access_token": "token_gerado",
        "token_type": "token_tipo",
    }


@pytest.mark.asyncio
async def test_registra_novo_usuario(login_client: ClientLogin) -> None:
    """
    Garante que um admin pode registrar um novo usuário comum.
    """
    novo_nome = "novo_usuario"
    payload = {
        "username": "admin_logado",
        "password": "senha_admin",
        "nome_novo_usuario": novo_nome,
        "senha_novo_usuario": "senha_segura",
    }

    response = await login_client.client.post("/login/novo_usuario", data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert (
        response.json()["message"] == f"Usuário {novo_nome} registrado com sucesso"
    )
    login_client.mock_usu.autentica_usuario_admin.assert_called_once()
    login_client.mock_usu.cria_novo_usuario.assert_called_once_with(
        novo_nome, "senha_segura"
    )


@pytest.mark.asyncio
async def test_registra_usuario_admin(login_client: ClientLogin) -> None:
    """
    Garante a criação de um administrador via endpoint dedicado.
    """
    response = await login_client.client.post("/login/novo_admin")

    assert response.status_code == status.HTTP_201_CREATED
    assert "administrador criado com sucesso" in response.json()["message"]
    login_client.mock_usu.cria_novo_usuario_admin.assert_called_once_with()
