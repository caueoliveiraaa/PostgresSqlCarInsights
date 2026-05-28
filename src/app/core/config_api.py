"""
Configurações públicas da API para inicialização.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigApi:
    """
    Objeto que contém as configurações públicas da API.
    """

    nome_app: str = "arquitetura_fastapi"
    versao_app: str = "1.0.0"
    import_app: str = "app.main:aplicacao"
    local_host: str = "localhost"
    local_port: int = 8001
