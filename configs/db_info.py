"""Stores constants for database connections."""

from src.utils.get_env_var import get_env_value

POSTGRES_USER: str = get_env_value("POSTGRES_USER", mandatory=True)
POSTGRES_PASSWORD: str = get_env_value("POSTGRES_PASSWORD", mandatory=True)
POSTGRES_HOST: str = get_env_value("POSTGRES_HOST", mandatory=True)
POSTGRES_PORT: str = get_env_value("POSTGRES_PORT", mandatory=True)
