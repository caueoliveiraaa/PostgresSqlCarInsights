"""Stores paths shared across the modules."""

import os
from pathlib import Path

from dotenv import load_dotenv

_PATH_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PATH_SQL: str = os.path.join(_PATH_ROOT, "sql\\")
_PATH_CONFIG: str = os.path.join(_PATH_ROOT, "config\\")
_PATH_DOT_ENV: str = os.path.join(_PATH_CONFIG, ".env")

env_file: Path = Path(f"{_PATH_DOT_ENV}.env")
if not env_file.exists():
    print("Não encontrou arquivo .env na pasta config!")
else:
    load_dotenv()

PATH_LOGS: str = os.path.join(_PATH_ROOT, "logs\\")
PATH_SQL_CREATE: str = os.path.join(_PATH_SQL, "01_create_scripts\\")
PATH_SQL_READ: str = os.path.join(_PATH_SQL, "02_read_scripts\\")
PATH_SQL_UPDATE: str = os.path.join(_PATH_SQL, "03_update_scripts\\")
PATH_SQL_DELETE: str = os.path.join(_PATH_SQL, "04_delete_scripts\\")
PATH_SQL_ANALYSIS: str = os.path.join(_PATH_SQL, "05_analysis_scripts\\")
