"""Tests for project-wide logger setup utilities."""

import logging
from logging import FileHandler, Formatter, Logger
from unittest import main
from unittest.mock import MagicMock, patch

from src.utils.logger_factory import _set_handlers, get_project_logger
from tests.base_tests.base_test_case import BaseTestCase


class TestGetProjectLogger(BaseTestCase):
    """Tests for the function 'get_project_logger'."""

    @patch("src.utils.logger_factory.makedirs")
    @patch("src.utils.logger_factory.getLogger")
    @patch("src.utils.logger_factory._set_handlers")
    def test_logger_created_successfully(
        self,
        mock_set_handlers: MagicMock,
        mock_get_logger: MagicMock,
        _mock_makedirs: MagicMock,
    ) -> None:
        """Verify that the logger is created and returned correctly."""
        mock_logger: Logger = MagicMock(spec=Logger)
        mock_get_logger.return_value = mock_logger

        result: Logger = get_project_logger()

        self.assertEqual(result, mock_logger)
        mock_set_handlers.assert_called_once()

    @patch("src.utils.logger_factory.makedirs")
    @patch("src.utils.logger_factory.getLogger")
    @patch("src.utils.logger_factory._set_handlers")
    def test_invalid_logger_raises_error(
        self,
        mock_set_handlers: MagicMock,
        mock_get_logger: MagicMock,
        _mock_makedirs: MagicMock,
    ) -> None:
        """Verify that a ValueError is raised when the logger is invalid."""
        mock_get_logger.return_value = None

        with self.assertRaises(ValueError):
            get_project_logger()


class TestSetHandlers(BaseTestCase):
    """Tests for the function '_set_handlers'."""

    @patch("src.utils.logger_factory.FileHandler")
    @patch("src.utils.logger_factory.Formatter")
    def test_handlers_are_removed_and_reconfigured(
        self,
        mock_formatter: MagicMock,
        mock_file_handler: MagicMock,
    ) -> None:
        """Verify that old handlers are removed and new ones are added."""
        mock_logger: Logger = MagicMock(spec=Logger)
        mock_handler: FileHandler = MagicMock(spec=FileHandler)
        mock_file_handler.return_value = mock_handler
        mock_formatter.return_value = MagicMock(spec=Formatter)
        mock_logger.handlers = [MagicMock(spec=FileHandler)]

        def remove_handler_side_effect(handler: FileHandler) -> None:
            """Mock removal of handlers."""
            mock_logger.handlers.remove(handler)

        mock_logger.removeHandler.side_effect = remove_handler_side_effect

        _set_handlers("fake_path.log", mock_logger)

        self.assertEqual(len(mock_logger.removeHandler.call_args_list), 1)
        self.assertEqual(len(mock_logger.addHandler.call_args_list), 1)

    @patch("src.utils.logger_factory.FileHandler")
    @patch("src.utils.logger_factory.Formatter")
    def test_handlers_are_configured_when_empty(
        self,
        mock_formatter: MagicMock,
        mock_file_handler: MagicMock,
    ) -> None:
        """Verify that handlers are configured when no existing handlers are present."""
        mock_logger: Logger = MagicMock(spec=Logger)
        mock_logger.handlers = []
        mock_handler: FileHandler = MagicMock(spec=FileHandler)
        mock_file_handler.return_value = mock_handler
        mock_formatter.return_value = MagicMock(spec=Formatter)

        _set_handlers("fake_path.log", mock_logger)

        mock_logger.setLevel.assert_called_once_with(level=logging.DEBUG)
        self.assertEqual(len(mock_logger.addHandler.call_args_list), 1)


if __name__ == "__main__":
    main()
