"""
Arquivo responsável por armazenar a exceção personalizada para banco de dados.
"""

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.errors.excecao_api import APIException


class DatabaseException(APIException):
    """
    Classe que representa a exceção para banco de dados.
    """

    def __init__(
        self,
        excecao_original: Exception | None = None,
        mensagem: str | None = None,
    ) -> None:
        """
        Inicializa uma exceção personalizada para erros relacionados ao banco
        de dados com mensagem padrão.
        """
        mensagem_padrao: str = "Ocorreu um problema ao consultar o banco de dados."
        self.mensagem: str = mensagem if mensagem else mensagem_padrao
        self.excecao_original = excecao_original
        if excecao_original:
            print(f"DATABASE_EXCEPTION: {str(self.excecao_original)}")

        super().__init__(
            mensagem=self.mensagem,
            codigo=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def trata_excecao(excecao: Exception) -> "DatabaseException":
        """
        Envolve exceções específicas de banco de dados em uma instância
        de DatabaseException.
        """
        if isinstance(excecao, SQLAlchemyError):
            return DatabaseException(excecao_original=excecao)

        return DatabaseException(
            excecao_original=excecao,
            mensagem=f"Erro desconhecido: {str(excecao)}",
        )
