"""Factory helper to produce a configured DbConnection.

This module contains `fabricate_connection` which builds a
`DbConnection` instance from the application's configuration for a
named database. It keeps the creation logic centralized so callers
can request connections simply by name.
"""

from beartype import beartype
from beartype.typing import Optional

from configs.db_info import (
    CAR_DATA_ANALYSIS_DB,
    POSTGRES_DB,
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
    if database_name == CAR_DATA_ANALYSIS_DB:
        connection_info = ConnectionInfo(
            dbname=CAR_DATA_ANALYSIS_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
    elif database_name == POSTGRES_DB:
        connection_info = ConnectionInfo(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
    else:
        raise ValueError(f"There are no settings for {database_name}.")

    connection: DbConnection = DbConnection(connection_info)
    connection.create_cursor()

    return connection
