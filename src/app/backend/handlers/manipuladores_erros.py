"""
Módulo de registro de manipuladores globais de erro para a aplicação FastAPI.
"""

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from app.errors.configuracao_invalida import InvalidConfigError
from app.errors.excecao_api import APIException
from app.errors.excecao_banco import DatabaseException


def registra_manipuladores_erros(app: FastAPI) -> None:
    """
    Registra os manipuladores globais de exceções na aplicação FastAPI.
    """

    @app.exception_handler(APIException)
    async def _trata_erro_api(
        _requisicao: Request, excecao: APIException
    ) -> JSONResponse:
        """
        Manipula exceções do tipo APIException, retornando uma resposta
        personalizada.
        """
        codigo: int = excecao.status_code
        return JSONResponse(
            status_code=codigo,
            content={"code": codigo, "message": excecao.detail},
        )

    @app.exception_handler(DatabaseException)
    async def _trata_erro_banco(
        _requisicao: Request, excecao: DatabaseException
    ) -> JSONResponse:
        """
        Manipula exceções relacionadas ao banco de dados.
        """
        codigo: int = excecao.status_code
        return JSONResponse(
            status_code=codigo,
            content={
                "code": codigo,
                "message": (
                    "Ocorreu uma falha interagir com o banco de dados. "
                    "Verifique a conexão ou tente novamente."
                ),
            },
        )

    @app.exception_handler(InvalidConfigError)
    async def _trata_invalid_config(
        _requisicao: Request, excecao: InvalidConfigError
    ) -> JSONResponse:
        """
        Manipula exceções relacionadas com configurações incorretas.
        """
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"detail": str(excecao)},
        )

    @app.exception_handler(ValueError)
    async def _trata_value_error(
        _requisicao: Request, excecao: ValueError
    ) -> JSONResponse:
        """
        Manipula exceções relacionadas com tratamento de valores.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(excecao)},
        )


def registra_middleware_erro(app: FastAPI) -> None:
    """
    Registra um middleware global para captura de exceções genéricas não tratadas.
    """

    @app.middleware("http")
    async def _captura_excecoes(
        requisicao: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response | JSONResponse:
        """
        Captura exceções não mapeadas.
        """
        try:
            return await call_next(requisicao)
        except Exception as exc:
            print(f"MIDDLEWARE: {str(exc)}")
            codigo: int = status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(
                status_code=codigo,
                content={"code": codigo, "message": "Erro inesperado"},
            )
