"""
Dependências de banco de dados para injeção de dependências nas rotas que
se comunicam com bases de dados.
"""

from collections.abc import AsyncGenerator

from beartype import beartype
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.conexao import cria_db


@beartype
async def injeta_sessao_api() -> AsyncGenerator[AsyncSession, None]:
    """
    Retorna uma sessão assíncrona do banco de dados vinculada à base API.
    """
    base: str = "base_api_auth"
    async for sessao in cria_db(base):
        yield sessao
