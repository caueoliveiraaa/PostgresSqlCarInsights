"""Logic for extracting content from SQL files to execute them."""

from beartype import beartype

from config.paths import (
    PATH_SQL_ANALYSIS,
    PATH_SQL_CREATE,
    PATH_SQL_DELETE,
    PATH_SQL_READ,
    PATH_SQL_UPDATE,
)


@beartype
def set_up_paths(folder_option: int) -> str:
    """Set up the correct path in the 'sql' folder, according to the option
    selected by 'folder_option'.

    Options available:
        1. PATH_SQL_CREATE -> '01_create_scripts/'
        2. PATH_SQL_READ -> '02_read_scripts/'
        3. PATH_SQL_UPDATE -> '03_update_scripts/'
        4. PATH_SQL_DELETE -> '04_delete_scripts/'
        5. PATH_SQL_ANALYSIS -> '05_delete_analysis/'

    Args:
        folder_option: The option representing the chosen folder.

    Returns:
        str: The path selected.

    Raises:
        ValueError: In case the 'folder_option' is not valid.
    """
    folder_path: str = ""
    match folder_option:
        case 1:
            folder_path = PATH_SQL_CREATE
        case 2:
            folder_path = PATH_SQL_READ
        case 3:
            folder_path = PATH_SQL_UPDATE
        case 4:
            folder_path = PATH_SQL_DELETE
        case 5:
            folder_path = PATH_SQL_ANALYSIS
        case _:
            raise ValueError(f"Invalid folder option: {folder_option}")

    return folder_path


@beartype
def get_content_of_sql_file(file_name: str, folder_option: int = 1) -> str:
    """Returns the contents of a SQL file in the SQL setup directory.

    Args:
        file_name (str): Name of the SQL file to read.
        folder_option (int): Which folder to select for retriving SQL queries.
            1. Setup sql files (Default).
            2. Queries sql files
            3. Custom sql files.

    Returns:
        str: The textual SQL script read from disk.

    Raises:
        ValueError:
            If 'file_name' is empty or the file is empty after reading.
            In case the 'folder_option' is not valid (via 'set_up_paths()').
    """
    if not file_name:
        raise ValueError("The argument for the name of the file cannot be empty.")

    if not file_name.endswith(".sql"):
        file_name = f"{file_name}.sql"

    sql_script: str = ""
    folder_path: str = set_up_paths(folder_option)

    with open(f"{folder_path}{file_name}", "r") as file:
        sql_script = file.read()

    if not sql_script:
        raise ValueError(f"File {file_name} is empty.")

    return sql_script
