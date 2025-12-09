"""This file stores values used in `crud_menu`."""

from beartype.typing import List

MAIN_TITLE: str = "\n[bold yellow]--- CRUD Options ---[/]"
CREATE_TITLE: str = "\n[bold yellow]--- Menu Create ---[/]"
DROP_TITLE: str = "\n[bold yellow]--- Drop Create ---[/]"

INVALID_OPTION: str = "[bold red]--- Invalid option: {option} ---[/]"
DATABASE_CREATED: str = "[bold green]--- Database {database} created ---[/]"
TABLES_CREATED: str = "[bold green]--- Pre-defined tables created ---[/]"
END_OF_PROGRAM: str = "[bold green]--- Program has stopped ---[/]"
START_OF_PROGRAM: str = "[bold green]--- Program has started ---[/]"
INVALID_OPETATION: str = "[bold red]--- Invalid operation. Check logs. ---[/]"

MAIN_OPTIONS: List[str] = [
    "1. Add",
    "2. Read",
    "3. Update",
    "4. Delete",
    "5. Clean",
    "6. Exit",
]

OPTIONS_CREATE: List[str] = [
    "1. Create local database",
    "2. Create pre-defined tables",
    "3. Create new table",
    "4. Insert pre-defined lines",
    "5. Insert new line",
    "6. Return to CRUD Options",
]

OPTIONS_READ: List[str] = [
    "1. Show entire table",
    "2. Show entire column",
    "3. Show entire row",
    "4. Return to CRUD Options",
]

OPTIONS_UPDATE: List[str] = [
    "1. Alter column",
    "2. Return to CRUD Options",
]

OPTIONS_DELETE: List[str] = [
    "1. Drop database",
    "2. Drop pre-defined tables",
    "3. Drop other tables",
    "4. Delete lines",
    "5. Delete columns",
    "6. Return to CRUD Options",
]
