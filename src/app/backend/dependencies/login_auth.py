"""
Módulo de injeção de autenticação para rotas protegidas via JWT.
"""

from typing import Annotated

from beartype import beartype
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.dependencies.database import injeta_sessao_api
from app.core.settings import settings
from app.repositories.usuarios import UsuariosRepository
from app.schemas.login_auth import TokenDecode
from app.services.login_auth import (
    ManipuladorHashService,
    ManipuladorTokenService,
    ManipuladorUsuarioService,
    ValidadorTokenService,
)


@beartype
async def injeta_manipulador_token() -> ManipuladorTokenService:
    """
    Fornece o manipulador de tokens para criação e decodificação dos mesmos.
    """
    validador = ValidadorTokenService()
    return ManipuladorTokenService(settings, validador)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
DepToken = Annotated[ManipuladorTokenService, Depends(injeta_manipulador_token)]


@beartype
async def injeta_autenticacao_jwt(
    manipulador: DepToken,
    token: str = Depends(oauth2_scheme),
) -> TokenDecode:
    """
    Valida e decodifica o token JWT fornecido no cabeçalho Authorization.
    """
    return await manipulador.decodifica_token(token)


DepSessao = Annotated[AsyncSession, Depends(injeta_sessao_api)]


@beartype
async def injeta_manipulador_usuarios(
    sessao: DepSessao,
) -> ManipuladorUsuarioService:
    """
    Fornece o manipulador de usuários com métodos que tratam as senhas
    trasnformadas em hash.
    """
    hasher = ManipuladorHashService()
    repo = UsuariosRepository(sessao)
    return ManipuladorUsuarioService(settings, repo, hasher)
