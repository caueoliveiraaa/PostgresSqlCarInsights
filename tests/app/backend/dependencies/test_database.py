"""
Testes para a dependência de banco de dados.
"""

from unittest.mock import MagicMock

import pytest

from app.backend.dependencies.database import injeta_sessao_api


@pytest.mark.asyncio
async def test_injeta_sessao_api(mock_cria_db: MagicMock) -> None:
    """
    Garante que a função retorna uma sessão válida para a base API.
    """
    qtd_sessoes_esperadas = 1

    gerador = injeta_sessao_api()
    sessoes_coletadas = []
    async for sessao in gerador:
        sessoes_coletadas.append(sessao)

    assert len(sessoes_coletadas) == qtd_sessoes_esperadas
    mock_cria_db.assert_called_once_with("base_api_auth")
