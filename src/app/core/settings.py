"""
Configurações do projeto, como JWT e conexões com o banco de dados.
"""

from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Extrai variáveis do arquivo .env e as armazena nos atributos da classe.
    """

    EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "hs000"
    SECRET_KEY: str = "secret"
    TOKEN_TYPE: str = "type"

    APP_HOST: str = "localhost"
    APP_PORT: int = 0000
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin_pass"
    API_NAME: str = "projeto"

    DRIVER: str = "driver"
    TRUST: str = "trust"
    ENCRYPT: str = "encrypt"

    LOCAL_HOST: str = "localhost"
    LOCAL_PORTA: str = "222"
    LOCAL_USUARIO: str = "user"
    LOCAL_SENHA: str = "pass"
    API_BASE: str = "base"

    @property
    def codifica_usuario_local(self) -> str:
        """
        Codifica o nome de usuário do banco local para uso seguro na
        URI de conexão.
        """
        return quote_plus(self.LOCAL_USUARIO)

    @property
    def codifica_senha_local(self) -> str:
        """
        Codifica a senha do banco local para uso seguro na URI de conexão.
        """
        return quote_plus(self.LOCAL_SENHA)

    @property
    def cria_base_uri(self) -> str:
        """
        Gera a URI de conexão SQLAlchemy para a base API com
        credenciais codificadas.
        """
        return (
            f"{self.codifica_usuario_local}"
            f":{self.codifica_senha_local}"
            f"@{self.LOCAL_HOST}"
            f",{self.LOCAL_PORTA}"
            f"/{self.API_BASE}"
            f"?{self.DRIVER}"
            f"&{self.TRUST}"
            f"&{self.ENCRYPT}"
        )

    @property
    def uri_assincrona_base_api(self) -> str:
        """
        URI para uso na API (Async).
        """
        return f"mssql+aioodbc://{self.cria_base_uri}"

    @property
    def uri_sincrona_base_api(self) -> str:
        """
        URI para uso em scripts/utilitários (Sync).
        """
        return f"mssql+pyodbc://{self.cria_base_uri}"

    class ConfigDict:
        arquivo_env = str(Path(__file__).parent / ".env")


settings = Settings()
