"""
Rotas para endpoint de login e geração de token JWT.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm

from app.backend.dependencies.login_auth import (
    injeta_manipulador_token,
    injeta_manipulador_usuarios,
)
from app.models.base_api.user_auth import UserAuth
from app.schemas.login_auth import JwtTokenResponse, UsuarioResponse
from app.services.login_auth import (
    ManipuladorTokenService,
    ManipuladorUsuarioService,
)

router_login = APIRouter(prefix="/login", tags=["Login"])

DepFormOAuth = Annotated[OAuth2PasswordRequestForm, Depends()]
DepToken = Annotated[ManipuladorTokenService, Depends(injeta_manipulador_token)]
DepUsuario = Annotated[
    ManipuladorUsuarioService, Depends(injeta_manipulador_usuarios)
]


@router_login.post(
    "/token",
    response_model=JwtTokenResponse,
    status_code=status.HTTP_200_OK,
)
async def realiza_login_para_token(
    dados_form: DepFormOAuth,
    manipulador_usu: DepUsuario,
    manipulador_token: DepToken,
) -> JwtTokenResponse:
    """
    Autentica o usuário e gera token JWT de acesso.
    """
    user_auth: UserAuth = await manipulador_usu.autentica_usuario(dados_form)
    token: str = await manipulador_token.cria_token_acesso(str(user_auth.id))
    token_type: str = manipulador_token.settings.TOKEN_TYPE
    return JwtTokenResponse(access_token=token, token_type=token_type)


@router_login.post(
    "/novo_usuario",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registra_novo_usuario(
    dados_form: DepFormOAuth,
    manipulador_usu: DepUsuario,
    nome_novo_usuario: str = Form(...),
    senha_novo_usuario: str = Form(...),
) -> UsuarioResponse:
    """
    Cria um novo usuário não-administrador no sistema.
    """
    await manipulador_usu.autentica_usuario_admin(dados_form)
    await manipulador_usu.cria_novo_usuario(nome_novo_usuario, senha_novo_usuario)
    return UsuarioResponse(
        message=f"Usuário {nome_novo_usuario} registrado com sucesso"
    )


@router_login.post(
    "/novo_admin",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registra_usuario_admin(manipulador_usu: DepUsuario) -> UsuarioResponse:
    """
    Cria um novo usuário administrador no sistema.
    """
    await manipulador_usu.cria_novo_usuario_admin()
    return UsuarioResponse(message="Usuário administrador criado com sucesso")
