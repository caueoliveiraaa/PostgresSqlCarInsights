"""
Este módulo inicializa a aplicação FastAPI.
"""

from beartype import beartype
from uvicorn import run

from app.core.config_api import ConfigApi
from app.core.settings import settings


@beartype
def inicia_api(dados_api: ConfigApi, depuracao: bool = False) -> None:
    """
    Inicializa a aplicação FastAPI em ambiente de produção ou local.
    """
    run(
        dados_api.import_app,
        reload=depuracao,
        host=dados_api.local_host if depuracao else settings.APP_HOST,
        port=dados_api.local_port if depuracao else settings.APP_PORT,
    )


if __name__ == "__main__":
    dados_api = ConfigApi()
    inicia_api(dados_api, depuracao=True)
