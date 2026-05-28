"""
Arquivo responsável por armazenar a exceção base para todas as exceções da API
que lidam com requisições.
"""

from fastapi import HTTPException, status


class APIException(HTTPException):
    """
    Exceção base para todas as exceções da API.
    """

    def __init__(
        self,
        mensagem: str = "Ocorreu um erro ao realizar uma requisição.",
        codigo: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        """
        Inicializa uma instância da exceção personalizada `APIException`.

        Essa exceção serve como base para todos os erros tratados pela API,
        permitindo o retorno de mensagens padronizadas e códigos HTTP específicos.
        """
        super().__init__(status_code=codigo, detail=mensagem)
