"""Factory helper to produce a configured DbConnection.

This module contains `fabricate_connection` which builds a
`DbConnection` instance from the application's configuration for a
named database. It keeps the creation logic centralized so callers
can request connections simply by name.
"""

from beartype import beartype
from beartype.typing import Optional

from configs.db_info import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from src.db.helpers.connection import DbConnection
from src.utils.dataclasses import ConnectionInfo


@beartype
def fabricate_connection(database_name: str) -> DbConnection:
    """Creates a `DbConnection` for a configured database name.

    Args:
        database_name: The identifier for the database configuration.

    Returns:
        DbConnection: A configured connection wrapper with a cursor ready.

    Raises:
        ValueError: If the given `database_name` is not recognized.
    """
    connection_info: Optional[ConnectionInfo] = None
    match str(database_name).lower():
        case "postgres_car_data_analysis":
            connection_info = ConnectionInfo(
                dbname="postgres_car_data_analysis",
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
            )
        case "postgres":
            connection_info = ConnectionInfo(
                dbname="postgres",
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
            )
        case _:
            raise ValueError(f"There are no settings for {database_name}.")

    connection: DbConnection = DbConnection(connection_info)
    connection.create_cursor()

    return connection
