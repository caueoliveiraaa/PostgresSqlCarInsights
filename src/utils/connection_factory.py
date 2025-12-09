"""Utilities for creating connections for different databases."""

from beartype import beartype
from beartype.typing import Optional

from config.db_info import (
    CAR_DB,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from src.domain.connection_info import ConnectionInfo


@beartype
def get_connection_info(database_name: str) -> ConnectionInfo:
    """Creates a 'DbConnection' for a configured database name.

    Args:
        database_name (str): The name of the database for the connection.

    Returns:
        ConnectionInfo: Necessary credentials for connection with databases.

    Raises:
        ValueError: If the given 'database_name' is not recognized.
    """
    connection_info: Optional[ConnectionInfo] = None
    if database_name == CAR_DB:
        connection_info = ConnectionInfo(
            dbname=CAR_DB,
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

    return connection_info
