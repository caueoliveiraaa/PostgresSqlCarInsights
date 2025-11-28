"""Stores the method that gets and validates env variables."""

import os

from beartype import beartype


@beartype
def get_env_value(key: str, mandatory: bool = True) -> str:
    """Get the env variables, making sure the they exist and carry values.

    Args:
        key: The key of the value.
        obrigatoria: Whether it's mandatory or not.

    Returns:
        str: The value of the variable.

    Raises:
        ValueError: If it doest not find the mandatory key/value.
    """
    value = os.environ.get(key, "").strip()
    if mandatory and not value:
        raise ValueError(f"Key '{key}' undefined or empty.")

    return value
