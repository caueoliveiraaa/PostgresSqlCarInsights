"""File responsible for creating the base test class."""

import io
import sys
from unittest import TestCase
from unittest.mock import patch

import pandas as pd
from beartype.typing import Any, Dict, Optional


class BaseTestCase(TestCase):
    """
    Base test class that sets up standard methods that can be imported
    by test classes to use the same methods.

    Thus, by simply importing the BaseTestCase, the "setUpClass"
    and "tearDownClass" methods below will be executed automatically, and elements
    like 'sleep' and 'print' will not affect the tests.
    """

    _mocks: Dict[str, Optional[Any]] = {}
    _patchers: Dict[str, Any] = {}
    _original_stderr: Any = None

    def setUp(self) -> None:
        """
        Stores attributes, variables and constants that are shared across tests.
        """
        super().setUp()

    @classmethod
    def setUpClass(cls) -> None:
        """
        Overrides methods that can influence tests when executing them.
        More methods to be overridden can be added here.

        Args:
            cls: It is a convention (like self), short for 'class'
        """
        cls._patchers = {
            "print": patch("builtins.print", return_value=None),
            "traceback": patch("traceback.print_exception", return_value=None),
            "sleep": patch("time.sleep", return_value=None),
            "logger": patch("logging.Logger._log", return_value=None),
            "df_head": patch.object(pd.DataFrame, "head", return_value=pd.DataFrame()),
            "df_tail": patch.object(pd.DataFrame, "tail", return_value=pd.DataFrame()),
            "df_info": patch.object(pd.DataFrame, "info", return_value=None),
        }

        cls._mocks = {name: patcher.start() for name, patcher in cls._patchers.items()}

        cls._original_stderr = sys.stderr
        sys.stderr = io.StringIO()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Ends the methods that were overwritten at the end of the tests.
        More methods to be overridden can be added here.

        Args:
            cls: It is a convention (like self), short for 'class'
        """
        for patcher in cls._patchers.values():
            patcher.stop()

        sys.stderr = cls._original_stderr
