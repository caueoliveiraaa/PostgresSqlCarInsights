"""
Lógica para geração e validação de tokens JWT com autenticação de usuários.
"""

from datetime import UTC, datetime, timedelta
from typing import Any, cast

from beartype import beartype
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.settings import Settings
from app.interfaces.login_auth import (
    IManipuladorHashService,
    IManipuladorTokenService,
    IManipuladorUsuarioService,
    IValidadorTokenService,
)
from app.interfaces.usuarios import IUserRepository
from app.models.base_api.user_auth import UserAuth
from app.schemas.login_auth import TokenDecode, TokenEncode


class ValidadorTokenService(IValidadorTokenService):
    """
    Implementação do manipulador de tokens utilizando a biblioteca python-jose.
    """

    @beartype
    def encode(self, payload: dict[str, Any], secret: str, algorithm: str) -> str:
        """
        Codifica um dicionário em uma string de token JWT.
        """
        return str(jwt.encode(payload, secret, algorithm))

    @beartype
    def decode(
        self, token: str, secret: str, algorithms: list[str]
    ) -> dict[str, Any]:
        """
        Decodifica um token JWT e valida sua integridade.
        """
        payload = jwt.decode(token, secret, algorithms)
        return cast(dict[str, Any], payload)


class ManipuladorHashService(IManipuladorHashService):
    """
    Implementação do serviço de hash utilizando a lógica do Werkzeug.
    """

    @beartype
    def gera_hash(self, password: str) -> str:
        """
        Transforma uma senha em texto puro em um hash seguro.
        """
        return generate_password_hash(password)

    @beartype
    def valida_hash(self, hash: str, password: str) -> bool:
        """
        Verifica se uma senha corresponde ao hash salvo.
        """
        return check_password_hash(hash, password)


class ManipuladorTokenService(IManipuladorTokenService):
    """
    Classe responsável por manipular (criar e decodificar) os tokens JWT.
    """

    @beartype
    def __init__(
        self, settings: Settings, validador: IValidadorTokenService
    ) -> None:
        """
        Inicializa o manipulador de tokens com a dependência responsável por
        armazenar dados sensíveis do projeto.
        """
        self.settings = settings
        self.validador = validador

    @beartype
    async def _monta_corpo_jwt(self, sub: str) -> TokenEncode:
        """
        Monta corpo com as configurações necessárias para geração de tokens JWT.
        """
        data_atual: datetime = datetime.now(UTC)
        expira_em: datetime = data_atual + timedelta(
            minutes=self.settings.EXPIRE_MINUTES,
        )

        return TokenEncode(
            sub=sub,
            iat=data_atual,
            exp=expira_em,
        )

    @beartype
    async def cria_token_acesso(self, sub: str) -> str:
        """
        Gera um token JWT de acesso para o usuário autenticado.
        """
        payload: TokenEncode = await self._monta_corpo_jwt(sub)
        token: str = self.validador.encode(
            payload.model_dump(),
            self.settings.SECRET_KEY,
            self.settings.ALGORITHM,
        )

        return token

    @beartype
    async def decodifica_token(self, token: str) -> TokenDecode:
        """
        Decodifica e valida o token JWT.
        """
        try:
            payload_bruto: dict[str, Any] = self.validador.decode(
                token,
                self.settings.SECRET_KEY,
                [self.settings.ALGORITHM],
            )

            return TokenDecode(
                sub=str(payload_bruto["sub"]),
                iat=int(payload_bruto["iat"]),
                exp=int(payload_bruto["exp"]),
            )

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado!",
            ) from e


class ManipuladorUsuarioService(IManipuladorUsuarioService):
    """
    Classe de serviço responsável por orquestrar a lógica de autenticação
    e gerenciamento de usuários.
    """

    @beartype
    def __init__(
        self,
        settings: Settings,
        repo: IUserRepository,
        hasher: IManipuladorHashService,
    ) -> None:
        """
        Inicializa o manipulador e autenticador de usuários.
        """
        self.repo = repo
        self.hasher = hasher
        self.settings = settings

    @beartype
    async def autentica_usuario(self, form: OAuth2PasswordRequestForm) -> UserAuth:
        """
        Autentica o usuário para geração de tokens.
        """
        usuario: UserAuth | None = await self.repo.busca_por_username(
            form.username, self.settings.API_NAME
        )

        if (
            not usuario
            or not usuario.ativo
            or not self.hasher.valida_hash(usuario.password_hash, form.password)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas ou usuário inativo/inexistente",
            )

        return usuario

    @beartype
    async def autentica_usuario_admin(
        self, form: OAuth2PasswordRequestForm
    ) -> UserAuth:
        """
        Autentica usuário admin para criação de outros usuários e manipulação de
        certos endpoints.
        """
        usuario: UserAuth | None = await self.repo.busca_admin(
            self.settings.API_NAME
        )

        if (
            not usuario
            or not usuario.ativo
            or not self.hasher.valida_hash(usuario.password_hash, form.password)
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas ou usuário admin inválido/inexistente",
            )

        return usuario

    @beartype
    async def cria_novo_usuario(self, username: str, password: str) -> None:
        """
        Verifica se o usuário já existe no banco de dados. Caso o mesmo ainda não
        exista, realiza a criação.
        """
        api: str = self.settings.API_NAME
        existente: UserAuth | None = await self.repo.busca_por_username(
            username, api
        )

        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já cadastrado para esta API.",
            )

        novo = UserAuth(
            username=username,
            api_name=api,
            is_admin=False,
            ativo=True,
            password_hash=self.hasher.gera_hash(password),
        )

        await self.repo.salva_usuario(novo)

    @beartype
    async def cria_novo_usuario_admin(self) -> None:
        """
        Verifica se o usuário admin já existe no banco de dados. Caso não exista,
        cria um admin novo com os valores armazenados nas variáveis de ambiente
        já configuradas e carregadas pelo objeto 'settings'.
        """
        api: str = self.settings.API_NAME
        existente: UserAuth | None = await self.repo.busca_admin(api)

        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um admin cadastrado para a api {api}",
            )

        novo = UserAuth(
            username=self.settings.ADMIN_USERNAME,
            api_name=api,
            is_admin=True,
            ativo=True,
            password_hash=self.hasher.gera_hash(self.settings.ADMIN_PASSWORD),
        )

        await self.repo.salva_usuario(novo)
