"""
Armazena a interface de contrato para a classe UsuariosRepository.
"""

from abc import ABC, abstractmethod

from app.models.base_api.user_auth import UserAuth


class IUserRepository(ABC):
    """
    Interface de contrato para operações de persistência de usuários no banco
    de dados para manipular usuários durante autenticações.
    """

    @abstractmethod
    async def busca_por_username(
        self, username: str, api_name: str
    ) -> UserAuth | None:
        """
        Busca um usuário pelo nome e nome da API.
        """
        pass

    @abstractmethod
    async def busca_admin(self, api_name: str) -> UserAuth | None:
        """
        Busca o usuário administrador do sistema.
        """
        pass

    @abstractmethod
    async def salva_usuario(self, usuario: UserAuth) -> None:
        """
        Persiste ou atualiza um usuário na base de dados.
        """
        pass
