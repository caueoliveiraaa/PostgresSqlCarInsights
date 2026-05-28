"""
Caminhos compartilhados pelos módulos da API.
"""

from collections.abc import Sequence
from pathlib import Path

DIRS_RAIZ: Sequence[Path] = Path(__file__).resolve().parents
INDICE_DIR_APP: int = 1
DIR_MODELS: Path = DIRS_RAIZ[INDICE_DIR_APP] / "models"
