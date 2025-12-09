"""Database management and SQL query execution."""

from beartype import beartype
from beartype.typing import Any, Optional, Tuple

from config.paths import PATH_SQL_CUSTOM, PATH_SQL_QUERIES, PATH_SQL_SETUP
from src.db.db_connection import DbConnection
from src.interfaces.db.db_manager_interface import IDatabaseManager


class DatabaseManager(IDatabaseManager):
    """Database manager for executing different queries, retrieving, updating or
    inserting data into databases, by applying queries and logic from different
    SQL files stored in the 'sql' folder.
    """

    @beartype
    def __init__(self, connection: DbConnection) -> None:
        """Initialze the class with a valid database connection.

        Args:
            connection (str): A configured connection ready to go.

        Attributes:
            _db_connection (DbConnection): The configured connection passed as
                an argument.
        """
        self._db_connection: DbConnection = connection

    @beartype
    def _get_content_sql_file(self, file_name: str, folder_option: int = 1) -> str:
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
            ValueError: If 'file_name' is empty or the file is empty after reading.
        """
        if not file_name:
            raise ValueError("The argument for the name of the file cannot be empty.")

        if not file_name.endswith(".sql"):
            file_name = f"{file_name}.sql"

        folder_path: str = ""
        match folder_option:
            case 1:
                folder_path = PATH_SQL_SETUP
            case 2:
                folder_path = PATH_SQL_QUERIES
            case 3:
                folder_path = PATH_SQL_CUSTOM
            case _:
                raise ValueError(f"Invalid folder option: {folder_option}")

        sql_script: str = ""
        with open(f"{folder_path}{file_name}", "r") as file:
            sql_script = file.read()

        if not sql_script:
            raise ValueError(f"File {file_name} is empty.")

        return sql_script

    @beartype
    def validate_database(self, database_name: str) -> bool:
        """Validate whether the target database already exists.

        Args:
            database_name (str): The name of the database to validate.

        Returns:
            bool: True when the database exists, otherwise False.

        Raises:
            ValueError: If 'select_database' is empty or the file is empty.
        """
        with self._db_connection.create_cursor() as cursor:
            cursor.execute(
                self._get_content_sql_file("select_database.sql", folder_option=2),
                (database_name,),
            )

            result: Optional[Tuple[Any, Any]] = cursor.fetchone()
            return bool(result)

        return False

    @beartype
    def run_setup_sql(
        self, sql_file_name: str, folder_option: int = 1, return_value: bool = False
    ) -> Any:
        """Runs SQL queries from 'sql' folder and return values if 'return_value'
        is ever True.

        Args:
            sql_file_name (str): Name of the SQL file to execute.
            folder_option (int): Which folder to select for retriving SQL queries.
                1. Setup sql files (Default).
                2. Queries sql files
                3. Custom sql files.
            return_value (bool): If the querie should return a value.

        Returns:
            Any: Possible returns from queries.

        Raises:
            ValueError: If 'file_name' is empty or the file is empty after reading.
        """

        # TODO:  make other functions for returning values and etc

        if not sql_file_name.endswith(".sql"):
            sql_file_name = f"{sql_file_name}.sql"

        sql_script: str = self._get_content_sql_file(sql_file_name, folder_option)
        with self._db_connection.create_cursor() as cursor:
            cursor.execute(sql_script)
