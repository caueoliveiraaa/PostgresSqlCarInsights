"""Tests database connecion factory."""

from unittest import main
from unittest.mock import MagicMock, patch

from config.db_info import CAR_DB, POSTGRES_DB
from src.domain.connection_info import ConnectionInfo
from src.utils.connection_factory import get_connection_info
from tests.base_tests.base_test_case import BaseTestCase


class TestGetConnectionInfo(BaseTestCase):
    """Tests for the function 'get_connection_info'."""

    @patch("src.utils.connection_factory.ConnectionInfo", spec=ConnectionInfo)
    def test_returns_car_db(self, mock_connection_info: MagicMock) -> None:
        """Checks if correct information is returned for 'CAR_DB'."""
        mock_instance: ConnectionInfo = mock_connection_info.return_value

        result: ConnectionInfo = get_connection_info(CAR_DB)

        self.assertEqual(result, mock_instance)

    @patch("src.utils.connection_factory.ConnectionInfo", spec=ConnectionInfo)
    def test_returns_postgres_db(self, mock_connection_info: MagicMock) -> None:
        """Checks if correct information is returned for 'POSTGRES_DB'."""

        mock_instance: ConnectionInfo = mock_connection_info.return_value
        result: ConnectionInfo = get_connection_info(POSTGRES_DB)

        self.assertEqual(result, mock_instance)

    def test_error_invalid_database(self) -> None:
        """Checks if an error is raised when the database name is invalid."""
        with self.assertRaises(ValueError):
            get_connection_info("INVALID_DB")


if __name__ == "__main__":
    main()
