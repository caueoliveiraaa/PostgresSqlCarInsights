"""
Fixtures para testes do módulo services.
"""

from unittest.mock import MagicMock

import pytest

from app.core.settings import Settings
from app.repositories.usuarios import UsuariosRepository
from app.services.exemplo import ConsultorDados
from app.services.login_auth import (
    ManipuladorHashService,
    ManipuladorTokenService,
    ManipuladorUsuarioService,
    ValidadorTokenService,
)


@pytest.fixture
def consultor_dados() -> ConsultorDados:
    """
    Gera uma instância real do ConsultorDados para testes unitários.
    """
    return ConsultorDados()


@pytest.fixture
def mock_settings() -> Settings:
    """
    Gera o mock das configurações da aplicação.
    """
    settings = MagicMock(spec=Settings)
    settings.SECRET_KEY = "test_secret"
    settings.ALGORITHM = "HS256"
    settings.EXPIRE_MINUTES = 30
    settings.API_NAME = "api_teste"
    settings.ADMIN_USERNAME = "admin"
    settings.ADMIN_PASSWORD = "password"

    return settings


@pytest.fixture
def mock_hasher() -> MagicMock:
    """
    Gera uma instância mocada do manipulador de hashes e senhas.
    """
    mock_hasher = MagicMock(spec=ManipuladorHashService)
    mock_hasher.gera_hash = MagicMock()
    mock_hasher.valida_hash = MagicMock()
    mock_hasher.gera_hash.side_effect = lambda x: f"hash_{x}"
    mock_hasher.valida_hash.side_effect = lambda h, p: h == f"hash_{p}"
    return MagicMock(spec=ManipuladorHashService)


@pytest.fixture
def mock_repo_usuarios() -> MagicMock:
    """
    Gera uma instância mocada do repositório de usuários.
    """
    return MagicMock(spec=UsuariosRepository)


@pytest.fixture
def manipulador_token(
    mock_settings: Settings, validador_token: ValidadorTokenService
) -> ManipuladorTokenService:
    """
    Gera uma instância mocada do manipulador de tokens.
    """
    return ManipuladorTokenService(mock_settings, validador_token)


@pytest.fixture
def manipulador_usuario(
    mock_settings: Settings, mock_repo_usuarios: MagicMock, mock_hasher: MagicMock
) -> ManipuladorUsuarioService:
    """
    Gera uma instância mocada do manipulador de usuários.
    """
    return ManipuladorUsuarioService(mock_settings, mock_repo_usuarios, mock_hasher)


@pytest.fixture
def validador_token() -> ValidadorTokenService:
    """
    Gera uma instância mocada do validador de tokens.
    """
    return ValidadorTokenService()


@pytest.fixture
def manipulador_hash() -> ManipuladorHashService:
    """
    Gera uma instância mocada do validador de hashes e senhas.
    """
    return ManipuladorHashService()
