"""Database setup helper to create a new project database.

This module exposes `DatabaseCreator`, a helper class that can create a
database using the SQL setup script files and connection factory helpers.
It interacts with the factory module to get connection objects and
executes the SQL required to initialize the schema for the project.
"""

from beartype import beartype
from beartype.typing import Any, Optional, Tuple
from psycopg2 import Error

from configs.db_info import POSTGRES_DB
from src.db.factory.get_connection import fabricate_connection
from src.db.factory.get_sql import get_content_sql_file
from src.db.helpers.connection import DbConnection
from src.utils.base_class import BaseClass


class DatabaseCreator(BaseClass):
    """Helper that encapsulates the database creation workflow.

    `DatabaseCreator` takes a database name and exposes methods to create the
    database schema using SQL scripts found in the project's SQL setup
    directory. Errors are logged through the base class' logger.
    """

    @beartype
    def __init__(self, database_name: str) -> None:
        """Initializes the class with the target database name.

        Args:
            database_name: Name of the database to create or initialize.
        """
        super().__init__()
        self._db_connection: Optional[DbConnection] = None
        self._database_creator: str = POSTGRES_DB
        self._database_name: str = database_name

    def _get_connection(self) -> None:
        """Obtains a `DbConnection` instance from the connection factory."""
        self._db_connection = fabricate_connection(self._database_creator)

    def _validate_database(self) -> bool:
        """Validate whether the target database already exists.

        Returns:
            bool: True when the database exists, otherwise False.
        """
        self._db_connection.cursor.execute(
            get_content_sql_file("select_database.sql", setup=False),
            (self._database_name,),
        )

        exists: Optional[Tuple[Any, Any]] = self._db_connection.cursor.fetchone()

        return bool(exists)

    def create_database(self) -> None:
        """Creates the target database using the project's SQL.

        The method reads the `database_setup.sql` script from the SQL setup
        directory and executes it through the connection cursor. Errors are
        logged and connections are closed during the `finally` step.
        """
        try:
            self._get_connection()
            if not self._db_connection:
                raise ValueError(
                    f"Could not create connection for {self._database_creator}."
                )

            if not self._validate_database():
                sql_script: str = get_content_sql_file("database_setup.sql")
                self._db_connection.cursor.execute(sql_script)
                self._logger.info(f"Database {self._database_name} created.")
            else:
                self._logger.info(f"Database {self._database_name} already exists.")

        except ValueError as e:
            self._logger.error(f"Error creating database: {e}")
        except Error as e:
            self._logger.critical(f"Error with psycopg2: {e}")

        finally:
            if self._db_connection:
                self._db_connection.close_cursor_and_connection()
