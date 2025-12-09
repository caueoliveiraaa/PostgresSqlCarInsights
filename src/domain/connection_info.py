"""Hosts dataclasses used for database connections."""

from dataclasses import dataclass


@dataclass
class ConnectionInfo:
    """Dataclass responsible for storing the necessary credentials
    for connection with databases.

    Attributes:
        dbname: The database name.
        user: The database user for login.
        password: The password user for login.
        host: The server where the database is.
        port: The port for the server.
    """

    dbname: str
    user: str
    password: str
    host: str
    port: str
