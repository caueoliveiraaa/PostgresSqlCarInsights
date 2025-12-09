"""Database connection helper utilities."""

from beartype import beartype
from beartype.typing import Optional
from psycopg2 import connect
from psycopg2.extensions import connection, cursor

from src.domain.connection_info import ConnectionInfo


class DbConnection:
    """ """

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
        """Opens a new database connection using psycopg2."""
        self._connection = connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

        self._connection.autocommit = True

    def create_cursor(self) -> None:
        """Creates a database cursor from an existing connection."""
        if not self._connection:
            self._create_connection()

        self.cursor = self._connection.cursor()

    def close_cursor_and_connection(self) -> None:
        """Closes cursor and connection."""
        if self.cursor:
            self.cursor.close()

        if self._connection:
            self._connection.close()
