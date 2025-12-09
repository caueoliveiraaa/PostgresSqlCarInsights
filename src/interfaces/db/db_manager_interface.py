"""This module stores the Interface for database manager implementations."""

from abc import ABC, abstractmethod

from beartype.typing import Any

from src.db.db_connection import DbConnection


class IDatabaseManager(ABC):
    """Interface for database manager class.

    Defines the contract for setting up a DatabaseManager instance, for interacting
    with databases, executing queries and retriving values.
    """

    @abstractmethod
    def __init__(self, connection: DbConnection) -> None:
        """Initialze the class with a valid database connection.

        Args:
            connection (str): A configured connection ready to go.

        Attributes:
            _db_connection (DbConnection): The configured connection passed as
                an argument.
        """

    @abstractmethod
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

    @abstractmethod
    def validate_database(self, database_name: str) -> bool:
        """Validate whether the target database already exists.

        Args:
            database_name (str): The name of the database to validate.

        Returns:
            bool: True when the database exists, otherwise False.

        Raises:
            ValueError: If 'select_database' is empty or the file is empty.
        """

    @abstractmethod
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
