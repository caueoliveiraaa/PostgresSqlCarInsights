"""
Testes para a classe InvalidConfigError.
"""

import pytest

from app.errors.configuracao_invalida import InvalidConfigError


def test_invalid_config_error() -> None:
    """
    Garante que a exceção seja lançada com sua mensagem padrão.
    """
    mensagem = "A configuração fornecida é inválida"

    with pytest.raises(InvalidConfigError, match=mensagem):
        raise InvalidConfigError()


def test_invalid_config_error_com_mensagem() -> None:
    """
    Garante que a exceção seja lançada com uma mensagem personalizada.
    """
    mensagem = "Configuração ausente"

    with pytest.raises(InvalidConfigError, match=mensagem):
        raise InvalidConfigError(mensagem)
