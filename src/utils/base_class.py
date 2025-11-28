"""Base utilities for common helper behaviour.

This module exposes `BaseClass`, a small helper class that provides a
pre-configured project logger to any subclass that needs standardized logging
functionality. Classes extending `BaseClass` can rely on `self._logger` being
available after initialization.
"""

from logging import Logger

from beartype.typing import Optional

from src.utils.logger import ProjectLogger


class BaseClass:
    """Simple base class to provide a configured `logging.Logger`.

    `BaseClass` creates and stores a `logging.Logger` instance using
    `ProjectLogger`. Subclasses may reference `self._logger` to log
    messages according to the application's centralized logging configuration.
    """

    def __init__(self) -> None:
        """Initialize the base class and attach a configured logger."""
        self._logger: Optional[Logger] = None
        self._set_logger()

    def _set_logger(self) -> None:
        """Instantiate a `ProjectLogger` and attach the configured logger.

        Raises:
            ValueError: If the logger could not be created.
        """
        project_logger: ProjectLogger = ProjectLogger()
        self._logger: Logger = project_logger.get_logger()
        del project_logger
        if not self._logger:
            raise ValueError("Could not set up logger.")
