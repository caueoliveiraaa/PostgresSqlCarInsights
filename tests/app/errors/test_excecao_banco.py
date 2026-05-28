"""
Testes para a classe DatabaseException.
"""

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.errors.excecao_banco import DatabaseException


def test_database_exception() -> None:
    """
    Garante que a exceção seja lançada com sua mensagem padrão.
    """
    mensagem = "Ocorreu um problema ao consultar o banco de dados."

    with pytest.raises(DatabaseException, match=mensagem):
        raise DatabaseException()


def test_database_exception_com_mensagem() -> None:
    """
    Garante que a exceção seja lançada com uma mensagem personalizada.
    """
    mensagem = "Erro de timeout"

    with pytest.raises(DatabaseException, match=mensagem):
        raise DatabaseException(mensagem=mensagem)


def test_database_exception_com_excecao_original() -> None:
    """
    Garante que a exceção original seja armazenada e printada no console.
    """
    excecao_base = ValueError("Falha crítica")

    erro = DatabaseException(excecao_original=excecao_base)

    assert erro.excecao_original == excecao_base


def test_trata_excecao_sqlalchemy() -> None:
    """
    Testa se o método trata_excecao identifica corretamente erros do SQLAlchemy.
    """
    erro_sql = SQLAlchemyError("Erro no banco")

    resultado = DatabaseException.trata_excecao(erro_sql)

    assert isinstance(resultado, DatabaseException)
    assert resultado.excecao_original == erro_sql
    assert "Ocorreu um problema ao consultar o banco de dados." in resultado.mensagem


def test_trata_excecao_desconhecida() -> None:
    """
    Testa o caminho 'else' do trata_excecao para erros não previstos.
    """
    erro_generico = RuntimeError("Algo quebrou")

    resultado = DatabaseException.trata_excecao(erro_generico)

    assert isinstance(resultado, DatabaseException)
    assert "Erro desconhecido: Algo quebrou" in resultado.mensagem
