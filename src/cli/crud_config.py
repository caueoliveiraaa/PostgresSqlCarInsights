"""This file stores values used in `crud_menu`."""

from beartype.typing import List

MAIN_TITLE: str = "\n[bold yellow]--- CRUD Options ---[/]"
CREATE_TITLE: str = "\n[bold yellow]--- Menu Create ---[/]"

INVALID_OPTION: str = "[bold red]--- Invalid option: {option} ---[/]"
DATABASE_CREATED: str = "[bold green]--- Database {database} created ---[/]"
END_OF_PROGRAM: str = "[bold green]--- Program has stopped ---[/]"
START_OF_PROGRAM: str = "[bold green]--- Program has started ---[/]"

MAIN_OPTIONS: List[str] = [
    "1. Create",
    "2. Read",
    "3. Update",
    "4. Delete",
    "5. Clean",
    "6. Exit",
]

OPTIONS_CREATE: List[str] = [
    "1. Create database",
    "2. Create tables",
    "3. Insert lines",
    "4. Insert columns",
    "5. Return to CRUD Options",
]

OPTIONS_READ: List[str] = [
    "1. Read entire table",
    "2. Read entire column",
    "3. Read entire row",
    "4. Return to CRUD Options",
]

OPTIONS_UPDATE: List[str] = [
    "1. Alter column",
    "2. Return to CRUD Options",
]

OPTIONS_DELETE: List[str] = [
    "1. Drop database",
    "2. Drop tables",
    "3. Delete lines",
    "3. Delete column",
    "4. Return to CRUD Options",
]
