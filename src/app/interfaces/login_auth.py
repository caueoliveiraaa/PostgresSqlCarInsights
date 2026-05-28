"""
Armazena a interface de contrato para a lógica de autenticação (JWT).
"""

from abc import ABC, abstractmethod
from typing import Any

from fastapi.security import OAuth2PasswordRequestForm

from app.models.base_api.user_auth import UserAuth
from app.schemas.login_auth import TokenDecode


class IValidadorTokenService(ABC):
    """
    Interface de contrato para o motor de geração e decodificação de tokens JWT.
    """

    @abstractmethod
    def encode(self, payload: dict[str, Any], secret: str, algorithm: str) -> str:
        """
        Codifica um dicionário em uma string de token JWT.
        """
        pass

    @abstractmethod
    def decode(
        self, token: str, secret: str, algorithms: list[str]
    ) -> dict[str, Any]:
        """
        Decodifica um token JWT e valida sua integridade.
        """
        pass


class IManipuladorHashService(ABC):
    """
    Interface de contrato para serviços de criptografia e validação de senhas.
    """

    @abstractmethod
    def gera_hash(self, password: str) -> str:
        """
        Transforma uma senha em texto plano em um hash seguro.
        """
        pass

    @abstractmethod
    def valida_hash(self, hash: str, password: str) -> bool:
        """
        Verifica se uma senha corresponde ao hash salvo.
        """
        pass


class IManipuladorTokenService(ABC):
    """
    Interface de contrato para manipulação de tokens.
    """

    @abstractmethod
    async def cria_token_acesso(self, sub: str) -> str:
        """
        Gera uma string de token para um sujeito.
        """
        pass

    @abstractmethod
    async def decodifica_token(self, token: str) -> TokenDecode:
        """
        Valida o token e retorna o payload.
        """
        pass


class IManipuladorUsuarioService(ABC):
    """
    Interface de contrato para o serviço de gerenciamento de usuários.
    Define a lógica de orquestração para autenticação e persistência de contas.
    """

    @abstractmethod
    async def autentica_usuario(self, form: OAuth2PasswordRequestForm) -> UserAuth:
        """
        Realiza a autenticação de um usuário comum.
        """
        pass

    @abstractmethod
    async def autentica_usuario_admin(
        self, form: OAuth2PasswordRequestForm
    ) -> UserAuth:
        """
        Realiza a autenticação restrita a usuários com privilégios de administrador.
        """
        pass

    @abstractmethod
    async def cria_novo_usuario(self, username: str, password: str) -> None:
        """
        Registra um novo usuário comum no sistema após validar duplicidade.
        """
        pass

    @abstractmethod
    async def cria_novo_usuario_admin(self) -> None:
        """
        Cria o usuário administrador inicial baseado nas configurações de ambiente.
        """
        pass
