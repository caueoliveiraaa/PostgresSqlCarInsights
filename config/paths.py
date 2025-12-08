"""Stores paths shared across the modules."""

import os
from pathlib import Path

from dotenv import load_dotenv

_PATH_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PATH_SQL: str = os.path.join(_PATH_ROOT, "sql\\")
_PATH_CONFIGS: str = os.path.join(_PATH_ROOT, "configs\\")
_PATH_DOT_ENV: str = os.path.join(_PATH_CONFIGS, ".env")
PATH_LOGS: str = os.path.join(_PATH_ROOT, "logs\\")
PATH_SQL_SETUP: str = os.path.join(_PATH_SQL, "setup\\")
PATH_SQL_QUERIES: str = os.path.join(_PATH_SQL, "queries\\")

env_file: Path = Path(f"{_PATH_DOT_ENV}.env")
if not env_file.exists():
    print("Não encontrou arquivo .env na pasta config!")
else:
    load_dotenv()
