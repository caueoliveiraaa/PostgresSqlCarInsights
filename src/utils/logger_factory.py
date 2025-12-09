"""Utilities for setting up a project-wide file-based logger."""

from datetime import date
from logging import DEBUG, FileHandler, Formatter, Logger, getLogger
from os import makedirs, path

from beartype import beartype

from config.paths import PATH_LOGS


@beartype
def get_project_logger() -> Logger:
    """Create and configure a project-level Logger.

    Returns:
        Logger: Logger instance for logging in the project.
    """
    logs_path: str = f"{PATH_LOGS}{date.today()}.log"
    makedirs(path.dirname(logs_path), exist_ok=True)

    logger: Logger = getLogger(__name__)
    _set_handlers(logs_path, logger)

    if not logger:
        raise ValueError("Could not set up logger properly.")

    return logger


@beartype
def _set_handlers(logs_path: str, logger: Logger) -> None:
    """Attach a 'FileHandler' to the logger, removing any old handlers.

    Args:
        logs_path: Full path to the log file.
    """
    for handler in logger.handlers:
        logger.removeHandler(handler)

    if not logger.handlers:
        logger.setLevel(level=DEBUG)

        logger_formatter: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        file_handler: FileHandler = FileHandler(logs_path)
        formatter: Formatter = Formatter(logger_formatter)

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
