"""Main entry point for the PostgreSQL Car Insights application.

This module can contain a CLI orchestration logic. When executed it should configure
logging, set up any required resources and delegate control flow to submodules that
run analysis and reporting tasks via terminal.

The 'LOGGER' and 'RICH' constants operate as a Singletons for the project.
"""

from logging import Logger
from os import name as os_name
from os import system

from config.db_info import CAR_DB
from src.cli.crud_menu import CrudMenu
from src.common.rich_printer import RichPrinter
from src.db.db_connection import DbConnection
from src.db.db_manager import DatabaseManager
from src.utils.connection_factory import get_connection_info
from src.utils.logger_factory import get_project_logger

system("cls" if os_name == "nt" else "clear")
LOGGER: Logger = get_project_logger()
RICH: RichPrinter = RichPrinter()


def main() -> None:
    """Application entry point.

    Organizes the instances and calls necessary to execute the program.
    """
    connection: DbConnection = DbConnection(get_connection_info(CAR_DB))
    db_manager: DatabaseManager = DatabaseManager(connection)
    crud: CrudMenu = CrudMenu(LOGGER, RICH, db_manager)

    crud.run_crud_main_menu()


if __name__ == "__main__":
    main()
