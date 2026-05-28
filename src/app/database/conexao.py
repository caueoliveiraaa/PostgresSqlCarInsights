"""
Lógica para conexões com as bases de dados.
"""

from collections.abc import AsyncGenerator

from beartype import beartype
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings
from app.errors.configuracao_invalida import InvalidConfigError


@beartype
def busca_engines(nome_banco: str) -> dict[str, AsyncEngine]:
    """
    Retorna um dicionário com as engines pré configuradas do projeto.
    Esta função é utilizado para a API com requisições assíncronas.
    """
    engines: dict[str, AsyncEngine] = {
        "base_nome": create_async_engine(settings.uri_assincrona_base_api),
    }

    if nome_banco not in engines:
        raise InvalidConfigError(f"Banco '{nome_banco}' não está configurado.")

    return engines


@beartype
def cria_sessao(nome_banco: str) -> async_sessionmaker[AsyncSession]:
    """
    Cria uma fábrica de sessões assíncronas do SQLAlchemy vinculada aos bancos
    configurados.
    """
    engines: dict[str, AsyncEngine] = busca_engines(nome_banco)
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engines[nome_banco],
        expire_on_commit=False,
    )


@beartype
async def cria_db(nome_banco: str) -> AsyncGenerator[AsyncSession, None]:
    """
    Gera uma sessão de banco de dados (via yield) e garante seu fechamento
    após o uso.
    """
    fabrica_sessao: async_sessionmaker[AsyncSession] = cria_sessao(nome_banco)
    async with fabrica_sessao() as sessao:
        try:
            yield sessao
        except Exception:
            await sessao.rollback()
            raise
        finally:
            await sessao.close()
