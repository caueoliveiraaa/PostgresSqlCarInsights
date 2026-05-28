"""
Testes para o módulo de conexão com o banco de dados.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.database.conexao import (
    busca_engines,
    cria_db,
    cria_sessao,
)
from app.errors.configuracao_invalida import InvalidConfigError


def test_busca_engines(mock_create_async_engine: MagicMock) -> None:
    """
    Garante que retorna a engine assíncrona correta para um banco configurado.
    """
    base = "base_nome"
    engines = busca_engines(base)

    assert base in engines
    mock_create_async_engine.assert_called_once()


def test_busca_engines_erro(mock_create_async_engine: MagicMock) -> None:
    """
    Garante que lança InvalidConfigError para bancos assíncronos inexistentes.
    """
    with pytest.raises(InvalidConfigError) as erro:
        busca_engines("inexistente")

    assert "não está configurado" in str(erro.value)


def test_cria_sessao_configuracao(
    mock_create_async_engine: MagicMock, mock_async_sessionmaker: MagicMock
) -> None:
    """
    Garante que o async_sessionmaker é configurado com os parâmetros corretos.
    """
    cria_sessao("base_nome")

    mock_async_sessionmaker.assert_called_once_with(
        autocommit=False,
        autoflush=False,
        bind=mock_create_async_engine.return_value,
        expire_on_commit=False,
    )


@pytest.mark.asyncio
async def test_cria_db_generator_ciclo_vida(
    mock_create_async_engine: MagicMock,
    mock_async_sessionmaker: MagicMock,
) -> None:
    """
    Garante que a sessão assíncrona é aberta, cedida (yield) e fechada corretamente.
    """
    mock_session = AsyncMock()
    context_manager_mock = mock_async_sessionmaker.return_value.return_value
    context_manager_mock.__aenter__.return_value = mock_session

    gerador = cria_db("base_nome")
    db = await gerador.__anext__()

    assert db == mock_session

    with pytest.raises(StopAsyncIteration):
        await gerador.__anext__()

    mock_session.rollback.assert_not_called()
    context_manager_mock.__aexit__.assert_called_once()
    mock_session.close.assert_called_once()


@pytest.mark.asyncio
async def test_cria_db_rollback_em_caso_de_erro(
    mock_create_async_engine: MagicMock,
    mock_async_sessionmaker: MagicMock,
) -> None:
    """
    Garante que se uma exceção ocorrer durante o uso da sessão,
    o rollback é executado antes de fechar.
    """
    mock_session = AsyncMock()
    context_manager_mock = mock_async_sessionmaker.return_value.return_value
    context_manager_mock.__aenter__.return_value = mock_session

    gerador = cria_db("base_nome")
    db = await gerador.__anext__()

    assert db == mock_session
    with pytest.raises(RuntimeError, match="Erro na Rota"):
        await gerador.athrow(RuntimeError("Erro na Rota"))

    mock_session.rollback.assert_called_once()
    mock_session.close.assert_called_once()
    context_manager_mock.__aexit__.assert_called_once()
