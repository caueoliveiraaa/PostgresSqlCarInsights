"""
Testes para o método main que roda a API.
"""

from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI

from app.core.config_api import ConfigApi
from app.main import cria_aplicacao, descarta_engines


@pytest.mark.asyncio
async def test_descarta_engines(
    mock_busca_engines: MagicMock,
) -> None:
    """
    Garante que o lifespan descarta as engines corretamente usando a fixture.
    """
    mock_app = MagicMock(spec=FastAPI)
    engines_retornadas = mock_busca_engines.return_value

    async with descarta_engines(mock_app):
        for engine in engines_retornadas.values():
            engine.dispose.assert_not_called()

    mock_busca_engines.assert_called_once_with("base_api_auth")
    for engine in engines_retornadas.values():
        engine.dispose.assert_called_once()


def test_cria_aplicacao(
    mock_config_api: ConfigApi,
    mock_registra_manipuladores: MagicMock,
    mock_registra_middleware: MagicMock,
) -> None:
    """
    Garante que a fábrica da aplicação inicialize o FastAPI com as
    configurações corretas e registre todos os componentes.
    """
    config = ConfigApi()

    app = cria_aplicacao(mock_config_api)

    assert isinstance(app, FastAPI)
    assert app.title == config.nome_app
    assert app.version == config.versao_app
    mock_registra_manipuladores.assert_called_once_with(app)
    mock_registra_middleware.assert_called_once_with(app)


def test_cria_aplicacao_rotas_incluidas(
    mock_config_api: ConfigApi, mock_include_router: MagicMock
) -> None:
    """
    Garante que os roteadores específicos foram registrados na aplicação
    sem violar as regras do beartype.
    """
    qtd_routers = 3

    cria_aplicacao(mock_config_api)

    assert mock_include_router.call_count == qtd_routers
