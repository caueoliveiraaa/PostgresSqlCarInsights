"""Database connection helper utilities."""

from beartype import beartype
from beartype.typing import Optional
from psycopg2 import Error, connect
from psycopg2.extensions import connection, cursor

from src.utils.base_class import BaseClass
from src.utils.dataclasses import ConnectionInfo


class DbConnection(BaseClass):
    """Lightweight wrapper around a psycopg2 database connection.

    `DbConnection` stores connection parameters and exposes methods to
    establish a new connection, create a cursor and to safely close both the
    cursor and the connection. All operations are logged using
    the class `ProjectLogger`.
    """

    @beartype
    def __init__(self, connection_info: ConnectionInfo) -> None:
        """Initializes connection helper from a `ConnectionInfo` dataclass.

        Args:
            connection_info: A dataclass that provides the database
                connection parameters (dbname, user, password, host, port).
        """
        super().__init__()
        self.dbname: str = connection_info.dbname
        self.user: str = connection_info.user
        self.password: str = connection_info.password
        self.host: str = connection_info.host
        self.port: str = connection_info.port
        self.cursor: Optional[cursor] = None
        self._connection: Optional[connection] = None

    def _create_connection(self) -> None:
        """Opens a new database connection using psycopg2.

        Raises:
            Error: If any psycopg2 error occurs.
        """
        try:
            self._connection = connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self._connection.autocommit = True

            self._logger.info("Connection created successfully.")
        except Error as e:
            self._logger.critical(f"Psycopg2 error: {e}")
            raise

    def create_cursor(self) -> None:
        """Creates a database cursor from an existing connection.

        Raises:
            Error: If any psycopg2 error occurs.
        """
        try:
            if not self._connection:
                self._create_connection()

            self.cursor = self._connection.cursor()
            self._logger.info("Cursor created successfully.")
        except Error as e:
            self._logger.critical(f"Psycopg2 error: {e}")
            raise

    def close_cursor_and_connection(self) -> None:
        """Closes cursor and connection, logging any errors encountered.

        Raises:
            Error: If any psycopg2 error occurs while closing connections.
        """
        try:
            try:
                if self.cursor:
                    self.cursor.close()
            except Error as e:
                self._logger.error(f"Psycopg2 error when closing cursor: {e}")

            if self._connection:
                self._connection.close()

            self._logger.info("Connections closed successfully.")
        except Error as e:
            self._logger.critical(f"Psycopg2 error when closing connection: {e}")
            raise
