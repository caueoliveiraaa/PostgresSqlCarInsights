"""Tests for sql files reading utilities (unit tests)."""

from unittest import main
from unittest.mock import MagicMock, mock_open, patch

from beartype.typing import Dict

from config.paths import (
    PATH_SQL_ANALYSIS,
    PATH_SQL_CREATE,
    PATH_SQL_DELETE,
    PATH_SQL_READ,
    PATH_SQL_UPDATE,
)
from src.utils.sql_reader import get_content_of_sql_file, set_up_paths
from tests.base_tests.base_test_case import BaseTestCase


class TestSqlReaderSetUpPaths(BaseTestCase):
    """Test method 'set_up_paths' as a unit."""

    def test_all_folder_options(self) -> None:
        """Test all valid options for 'folder_option'."""
        valid_options: Dict[int, str] = {
            1: PATH_SQL_CREATE,
            2: PATH_SQL_READ,
            3: PATH_SQL_UPDATE,
            4: PATH_SQL_DELETE,
            5: PATH_SQL_ANALYSIS,
        }

        for option, path in valid_options.items():
            result: str = set_up_paths(folder_option=option)

            self.assertIsInstance(result, str)
            self.assertEqual(result, path)

    def test_invalid_folder_option(self) -> None:
        """Test invalid option with ValueError being raised."""
        with self.assertRaises(ValueError) as error:
            set_up_paths(folder_option=6)

        self.assertIn("Invalid folder option", str(error.exception))


class TestSqlReaderGetContentOfSqlFile(BaseTestCase):
    """Test method 'get_content_of_sql_file' as a unit."""

    def test_valid_script_with_dot_sql(self) -> None:
        """Test valid return of script whose file name is sent with '.sql'."""
        result: str = get_content_of_sql_file("01_database_setup.sql", folder_option=1)

        self.assertIsInstance(result, str)
        self.assertTrue(len(result))
        self.assertIn("create database", result)

    def test_all_valid_options(self) -> None:
        """Test all valid options for 'folder_option'."""
        valid_options: Dict[int, Dict[str, str]] = {
            1: {"01_database_setup": "create database"},
            2: {"01_select_database": "select 1"},
            3: {"01_update_table_name": "alter table"},
            4: {"01_database_drop": "drop database"},
            5: {"01_sum_of_car_prices": "select sum(price)"},
        }

        for option, dict_validation in valid_options.items():
            for file_name, validation_words in dict_validation.items():
                result: str = get_content_of_sql_file(file_name, folder_option=option)

                self.assertIsInstance(result, str)
                self.assertTrue(len(result))
                self.assertIn(validation_words, result)

    def test_invalid_folder_option(self) -> None:
        """Test invalid option with ValueError being raised."""
        with self.assertRaises(ValueError) as error:
            get_content_of_sql_file("01_database_setup", folder_option=6)

        self.assertIn(
            "Invalid folder option",
            str(error.exception),
        )

    def test_error_while_opening_file(self) -> None:
        """Test error from trying to access a file that does not exist."""
        with self.assertRaises(ValueError) as error:
            get_content_of_sql_file("invalid_name", folder_option=1)

        self.assertIn(
            "Could not open 'invalid_name.sql'",
            str(error.exception),
        )

    def test_file_name_empty(self) -> None:
        """Test parameter 'file_name' empty and raising a ValueError exception."""
        with self.assertRaises(ValueError) as error:
            get_content_of_sql_file("")

        self.assertIn(
            "The argument for the name of the file cannot be empty.",
            str(error.exception),
        )

    @patch(
        "src.utils.sql_reader.open",
        new_callable=mock_open,
        read_data="",
    )
    def test_empty_sql_script(self, _mock_open: MagicMock) -> None:
        """Test raise ValueError when the content of a file is empty."""
        with self.assertRaises(ValueError) as error:
            get_content_of_sql_file("01_database_setup")

        self.assertIn(
            "File '01_database_setup.sql' is empty.",
            str(error.exception),
        )


if __name__ == "__main__":
    main()
