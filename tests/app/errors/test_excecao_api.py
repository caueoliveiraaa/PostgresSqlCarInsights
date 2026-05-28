"""
Testes para a classe APIException.
"""

import pytest

from app.errors.excecao_api import APIException


def test_api_exception() -> None:
    """
    Garante que a exceção seja lançada com sua mensagem padrão.
    """
    mensagem = "Ocorreu um erro ao realizar uma requisição."

    with pytest.raises(APIException, match=mensagem):
        raise APIException()


def test_api_exception_com_mensagem() -> None:
    """
    Garante que a exceção seja lançada com uma mensagem personalizada.
    """
    mensagem = "Erro de timeout"

    with pytest.raises(APIException, match=mensagem):
        raise APIException(mensagem)
