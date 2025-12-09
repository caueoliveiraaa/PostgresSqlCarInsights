"""Error handling decorator for consistent logging and styled console output."""

from functools import wraps
from typing import Callable

from beartype.typing import Any, Optional
from psycopg2 import DatabaseError
from rich.errors import ConsoleError, StyleError

from config.pg_errors_map import ERROR_MAP


def general_cli_error_handler(
    method: Callable[..., Any],
) -> Callable[..., Optional[Any]]:
    """Decorator for instance methods that handles errors using self._logger and
    self._rich.

    This decorator assumes the decorated method belongs to a class that has
    '_logger' and '_rich' attributes. It centralizes error handling so you
    don't need to repeat try/except blocks in every method.

    Args:
        method: The method the decorator is capturing.

    Returns:
        Callable[..., Optional[Any]]: A wrapped function that executes the
            original method and automatically catches errors.
    """

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Optional[Any]:
        """Execute the wrapped method with error handling.

        Args:
            self: The instance of the class (must have '_logger' and '_rich').
            *args: Positional arguments for the wrapped method.
            **kwargs: Keyword arguments for the wrapped method.

        Returns:
            Any: The result of the wrapped method if successful,
            otherwise None if an error occurs.
        """
        try:
            return method(self, *args, **kwargs)

        except (OSError, ModuleNotFoundError) as e:
            self._logger.error(f"[Operational Error] {method.__name__}: {e}")
            self._rich.print_panel(
                "An operational error occurred while processing your request.\n"
                "Please check the logs for more details.",
                title="ERROR",
                color="red",
            )
            return None

        except (ValueError, TypeError) as e:
            self._logger.error(f"[Data Error] {method.__name__}: {e}")
            self._rich.print_panel(
                "An error occurred while processing data.\n"
                "Please check the logs for more details.",
                title="ERROR",
                color="red",
            )
            return None

        except (KeyError, AttributeError) as e:
            self._logger.error(f"[Data Access Error] {method.__name__}: {e}")
            self._rich.print_panel(
                "An error occurred while trying to access data.\n"
                "Please check the logs for more details.",
                title="ERROR",
                color="red",
            )
            return None

        except (ConsoleError, StyleError) as e:
            self._logger.error(f"[Rich Console Error] {method.__name__}: {e}")
            self._rich.print_panel(
                "A console rendering error occurred while using Rich.\n"
                "Please check the logs for technical details.",
                title="RICH ERROR",
                color="red",
            )
            return None

        except (KeyboardInterrupt, EOFError):
            print("\n")
            self._rich.print_panel(
                "Program interrupted by user.\nExiting gracefully...",
                title="EXIT",
                color="yellow",
            )
            exit()

    return wrapper


def db_error_handler(method: Callable[..., Any]) -> Callable[..., Optional[Any]]:
    """Decorator for instance methods that handles errors using self._logger and
    self._rich, focused on database errors when utilizing 'psycopg2' to interact
    with databases.

    This decorator assumes the decorated method belongs to a class that has
    '_logger' and '_rich' attributes. It centralizes error handling so you
    don't need to repeat try/except blocks in every method that handles SQL
    queries.

    Args:
        method: The method the decorator is capturing.

    Returns:
        Callable[..., Optional[Any]]: A wrapped function that executes the
            original method and automatically catches psycopg2-related errors.
    """

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Optional[Any]:
        """Execute the wrapped method with error handling.

        Args:
            self: The instance of the class (must have '_logger' and '_rich').
            *args: Positional arguments for the wrapped method.
            **kwargs: Keyword arguments for the wrapped method.

        Returns:
            Any: The result of the wrapped method if successful,
            otherwise None if an error occurs.
        """
        try:
            return method(self, *args, **kwargs)

        except DatabaseError as e:
            if str(e.pgcode) in ERROR_MAP:
                self._logger.error(f"{ERROR_MAP[str(e.pgcode)]} {method.__name__}: {e}")
                self._rich.print_panel(
                    ERROR_MAP[str(e.pgcode)],
                    title="ERROR",
                    color="red",
                )
            else:
                self._logger.error(f"[DatabaseError Error] {method.__name__}: {e}")
                self._rich.print_panel(
                    "A database error occurred while processing your request.\n"
                    "Please check the logs for more details.",
                    title="CRITICAL",
                    color="red",
                )

            return None

    return wrapper
