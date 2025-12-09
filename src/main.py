"""Main entry point for the PostgreSQL Car Insights application.

This module can contain application bootstrapping and CLI orchestration
logic. When executed it should configure logging, set up any required
resources and delegate control flow to submodules that run analysis and
reporting tasks.
"""

from logging import Logger

from src.cli.crud_menu import CrudMenu
from src.utils.logger_factory import get_project_logger

logger: Logger = get_project_logger()


def main() -> None:
    """Application entry point."""
    crud: CrudMenu = CrudMenu()
    crud.run_crud()


if __name__ == "__main__":
    main()
