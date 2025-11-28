"""Helpers to load SQL scripts from files used for DB setup.

The module exposes `get_content_sql_file` which reads the content of a
SQL file located under the configured `PATH_SQL_SETUP` and returns the
script as a string.
"""

from beartype import beartype

from configs.paths import PATH_SQL_QUERIES, PATH_SQL_SETUP


@beartype
def get_content_sql_file(file_name: str, setup: bool = True) -> str:
    """Returns the contents of a SQL file in the SQL setup directory.

    Args:
        file_name: Name of the SQL file to read.
        setup: If it has to get the sql from the setup folder.

    Returns:
        str: The textual SQL script read from disk.

    Raises:
        ValueError: If `file_name` is empty or the file is empty after reading.
    """
    if not file_name:
        raise ValueError("The argument for the name of the file cannot be empty.")

    if not file_name.endswith(".sql"):
        file_name = f"{file_name}.sql"

    sql_script: str = ""
    folder_path: str = PATH_SQL_SETUP if setup else PATH_SQL_QUERIES

    with open(f"{folder_path}{file_name}", "r") as file:
        sql_script = file.read()

    if not sql_script:
        raise ValueError(f"File {file_name} is empty.")

    return sql_script
