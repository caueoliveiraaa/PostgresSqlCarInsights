"""Main entry point for the PostgreSQL Car Insights application.

This module can contain application bootstrapping and CLI orchestration
logic. When executed it should configure logging, set up any required
resources and delegate control flow to submodules that run analysis and
reporting tasks.
"""

import os

from psycopg2 import Error

from src.cli.crud_menu import CrudMenu


def main() -> None:
    """Application entry point.

    This function serves as a minimal CLI launcher for the CRUD menu. It
    clears the console, instantiates `CrudMenu`, and
    runs the interactive menu. Errors are caught and printed as user-facing
    messages while the details are logged by the application logger.
    """
    try:
        os.system("cls")
        crud: CrudMenu = CrudMenu()
        crud.run_crud()
    except ValueError:
        print("A value error has stopped the program. Check logs.")
    except Error:
        print("A database error has stopped the program. Check logs.")


if __name__ == "__main__":
    main()
