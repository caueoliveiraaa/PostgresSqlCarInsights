"""
Configurações globais de teste e fixtures para todos os testes.
"""

from collections.abc import Generator
from unittest.mock import MagicMock, mock_open, patch

import pytest


@pytest.fixture(autouse=True)
def mock_sleep() -> Generator[MagicMock, None, None]:
    """
    Desativa o time.sleep por um mock que não faz nada para performance.
    """
    with patch("time.sleep", return_value=None) as _mocked:
        yield _mocked


@pytest.fixture(autouse=True)
def mock_print() -> Generator[MagicMock, None, None]:
    """
    Desativa prints em todos os testes para performance.
    """
    with patch("builtins.print") as _mocked:
        yield _mocked


@pytest.fixture
def mock_open_file() -> Generator[MagicMock, None, None]:
    """
    Gera um mock do builtins.open globalmente para o teste.
    """
    _mocked = mock_open()
    with patch("builtins.open", _mocked):
        yield _mocked
