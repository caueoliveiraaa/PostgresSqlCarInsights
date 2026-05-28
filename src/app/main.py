"""
Módulo principal da API. Define o ponto de entrada da aplicação e os
endpoints de teste de funcionamento.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beartype import beartype
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from app.backend.handlers.manipuladores_erros import (
    registra_manipuladores_erros,
    registra_middleware_erro,
)
from app.backend.routes.exemplo import router_exemplo
from app.backend.routes.health_check import router_health
from app.backend.routes.login_auth import router_login
from app.core.config_api import ConfigApi
from app.database.conexao import busca_engines


@asynccontextmanager
async def descarta_engines(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gerencia o ciclo de vida da aplicação, garantindo que as conexões com o
    banco de dados sejam encerradas corretamente no desligamento.
    """
    yield
    engines: dict[str, AsyncEngine] = busca_engines("base_api_auth")
    for engine in engines.values():
        await engine.dispose()


@beartype
def cria_aplicacao(dados_api: ConfigApi) -> FastAPI:
    """
    Atua como uma fábrica da aplicação, reunindo todos os componentes essenciais
    para inicializar as instâncias de aplicações FastAPI.
    """
    app = FastAPI(title=dados_api.nome_app, version=dados_api.versao_app)
    app.include_router(router_exemplo)
    app.include_router(router_login)
    app.include_router(router_health)

    registra_manipuladores_erros(app)
    registra_middleware_erro(app)

    return app


dados_api = ConfigApi()
aplicacao: FastAPI = cria_aplicacao(dados_api)
descarta_engines(aplicacao)
