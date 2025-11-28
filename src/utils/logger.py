"""Utilities for setting up a project-wide file-based logger."""

import os
from datetime import date
from logging import DEBUG, FileHandler, Formatter, Logger, getLogger

from beartype import beartype
from beartype.typing import Optional

from configs.paths import PATH_LOGS


class ProjectLogger:
    """Create and configure a project-level Logger.

    The `ProjectLogger` class centralizes the creation of a `logging.Logger`
    instance and makes sure that a file handler with a consistent formatter
    is attached. It allows creation of log files under a configurable
    path and names logs using today's date so a new file is used each day.
    """

    @beartype
    def __init__(self, name: str = "PostgreSQL", path: str = PATH_LOGS) -> None:
        """Initialize the logger helper.

        Args:
            name: A name for the logging process.
            path: Path prefix for log files. The file name will append the
                current date and the `.log` extension.
        """
        self._name: str = name
        self._path: str = path
        self._logger: Optional[Logger] = None
        self._logger_formatter: str = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    @beartype
    def get_logger(self) -> Logger:
        """Ensures the logger is created and configured and then returns
        its instance.

        Returns:
            Logger: A configured `logging.Logger` instance.

        Raises:
            ValueError: If the logger could not be created.
        """
        self._setup_logger()
        if not self._logger:
            raise ValueError("Could not set up logger properly.")

        return self._logger

    @beartype
    def _setup_logger(self) -> None:
        """Prepare the logger and attach handlers."""
        full_path: str = f"{self._path}{date.today()}.log"
        os.makedirs(os.path.dirname(self._path), exist_ok=True)

        self._logger = getLogger(self._name)
        self._set_handlers(full_path)

    @beartype
    def _set_handlers(self, full_path: str) -> None:
        """Attach a `FileHandler` to the logger, removing any old handlers.

        Args:
            full_path: Full path to the log file (including file name).
        """
        for handler in self._logger.handlers:
            self._logger.removeHandler(handler)

        if not self._logger.handlers:
            self._logger.setLevel(level=DEBUG)
            file_handler: FileHandler = FileHandler(full_path)
            formatter: Formatter = Formatter(self._logger_formatter)

            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
