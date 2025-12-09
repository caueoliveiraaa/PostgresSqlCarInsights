"""Tests for method that retrieves data from env variables."""

from os import environ
from unittest import main
from unittest.mock import patch

from src.utils.env_validation import get_env_value
from tests.base_tests.base_test_case import BaseTestCase


class TestGetEnvValue(BaseTestCase):
    """Tests for the function 'get_env_value'."""

    @patch.dict(environ, {"MY_KEY": "my_value"}, clear=True)
    def test_returns_value_when_key_exists(self) -> None:
        """
        Checks that it returns the correct value when the key exists and has a value.
        """
        result: str = get_env_value("MY_KEY")
        self.assertEqual(result, "my_value")

    @patch.dict(environ, {"EMPTY_KEY": ""}, clear=True)
    def test_raises_error_when_key_empty_and_mandatory(self) -> None:
        """
        Checks that it raises ValueError when the key exists but is empty
        and mandatory=True.
        """
        with self.assertRaises(ValueError):
            _ = get_env_value("EMPTY_KEY", mandatory=True)

    @patch.dict(environ, {"EMPTY_KEY": ""}, clear=True)
    def test_returns_empty_when_key_empty_and_not_mandatory(self) -> None:
        """
        Checks that it returns an empty string when the key exists but is empty
        and mandatory=False.
        """
        result: str = get_env_value("EMPTY_KEY", mandatory=False)
        self.assertEqual(result, "")

    @patch.dict(environ, {}, clear=True)
    def test_raises_error_when_key_missing_and_mandatory(self) -> None:
        """
        Checks that it raises ValueError when the key is missing and mandatory=True.
        """
        with self.assertRaises(ValueError):
            _ = get_env_value("MISSING_KEY", mandatory=True)

    @patch.dict(environ, {}, clear=True)
    def test_returns_empty_when_key_missing_and_not_mandatory(self) -> None:
        """
        Checks that it returns an empty string when the key is missing
        and mandatory=False.
        """
        result: str = get_env_value("MISSING_KEY", mandatory=False)
        self.assertEqual(result, "")


if __name__ == "__main__":
    main()
