"""
Lógica para autenticação de usuários via banco de dados.
"""

from beartype import beartype
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.usuarios import IUserRepository
from app.models.base_api.user_auth import UserAuth


class UsuariosRepository(IUserRepository):
    """
    Implementação do repositório que manipula usuários para autenticações.
    """

    @beartype
    def __init__(self, sessao: AsyncSession) -> None:
        """
        Inicializa o manipulador de usuários do banco de dados.
        """
        self.sessao = sessao

    @beartype
    async def busca_por_username(
        self, username: str, api_name: str
    ) -> UserAuth | None:
        """
        Busca um usuário pelo nome do usuário e da API.
        """
        instrucao: Select[tuple[UserAuth]] = select(UserAuth).where(
            UserAuth.username == username, UserAuth.api_name == api_name
        )
        resultado: Result[tuple[UserAuth]] = await self.sessao.execute(instrucao)
        return resultado.scalars().first()

    @beartype
    async def busca_admin(self, api_name: str) -> UserAuth | None:
        """
        Busca um usuário admin pelo campo 'is_admin'.
        """
        instrucao: Select[tuple[UserAuth]] = select(UserAuth).filter_by(
            is_admin=True, api_name=api_name
        )
        resultado: Result[tuple[UserAuth]] = await self.sessao.execute(instrucao)
        return resultado.scalars().first()

    @beartype
    async def salva_usuario(self, usuario: UserAuth) -> None:
        """
        Salva a instância atual do usuário no banco de dados.
        """
        self.sessao.add(usuario)
        await self.sessao.commit()
        await self.sessao.refresh(usuario)
