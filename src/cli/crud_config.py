"""This file stores values used in 'CrudMenu'."""

from beartype.typing import List

MAIN_OPTIONS: List[str] = [
    "CREATE",
    "READ",
    "UPDATE",
    "DELETE",
    "ANALYZE",
    "EXIT",
]

OPTIONS_CREATE: List[str] = [
    "Create pre-defined database",
    "Create pre-defined tables",
    "Create new tables",
    "Insert pre-defined lines",
    "Insert new line",
    "Add new column",
    "Return to CRUD Options",
]

OPTIONS_READ: List[str] = [
    "Show entire table",
    "Show entire column",
    "Show entire row",
    "Return to CRUD Options",
]

OPTIONS_UPDATE: List[str] = [
    "Alter column",
    "Return to CRUD Options",
]

OPTIONS_DELETE: List[str] = [
    "Drop pre-defined database",
    "Drop pre-defined tables",
    "Drop other tables",
    "Delete pre-defined lines",
    "Delete lines",
    "Delete columns",
    "Return to CRUD Options",
]

OPTIONS_ANALYSIS: List[str] = [
    "Drop pre-defined database",
    "Return to CRUD Options",
]
