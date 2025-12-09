"""This module stores the Interface for database connection implementations."""

from abc import ABC, abstractmethod

from beartype.typing import Any
from psycopg2.extensions import connection, cursor

from src.domain.connection_info import ConnectionInfo


class IDbConnection(ABC):
    """Interface for database connection class.

    Defines the contract for setting up a DbConnection instance, for storing
    database credentials and connection logic.
    """

    @abstractmethod
    def __init__(self, connection_info: ConnectionInfo) -> None:
        """Initializes connection helper from a 'ConnectionInfo' dataclass.

        Args:
            connection_info: A dataclass that provides the database
                connection parameters (dbname, user, password, host, port).

        Attributes:
            dbname (str): The name of the database.
            user (str): The name of the database user.
            password (str): The database password.
            host (str): The database host/server.
            port (str): The database connection port.
            cursor (Optional[cursor]): The cursor for queries.
            _connection (Optional[connection]): The connection for cursors.
        """

    @abstractmethod
    def __exit__(self, *args: Any) -> None:
        """Close connection and cursor once they have been used.

        Args:
            *args: Any arguments passed at exit time.
        """

    @abstractmethod
    def _create_connection(self) -> connection:
        """Opens a new database connection using psycopg2.

        Returns:
            connection: A new 'psycopg2' connection.
        """

    @abstractmethod
    def create_cursor(self) -> cursor:
        """Creates a database cursor from an existing connection.

        Returns:
            connection: A new 'psycopg2' cursor.
        """
