"""This module stores the Interface for rich implementations."""

from abc import ABC, abstractmethod

from beartype.typing import Any, Iterable
from rich.table import Table
from rich.text import Text


class IRichPrinter(ABC):
    """Interface for rich printing class.

    Defines the contract for setting up a rich instance, for priting custimized
    menus, panels and colored messages with different styles.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initialize terminal printer with an instance of 'Console'."""

    @abstractmethod
    def _prepare_text(self, text: str, color: str, style: str) -> Text:
        """Prepare style and color of the text being printed.

        This is a private method used to set up all the styles and attributes
        of the text being printed.

        Args:
            text: Text being printed.
            color: The color of the text.
            style: The style being applied to the text.

        Returns:
            Text: Content for printing after cuztomizing it.

        Raises:
            ValueError: In case the style or the color are not valid.
        """

    @abstractmethod
    def print_rich(self, object: Any) -> None:
        """Generic method for printing different 'rich' objects.

        Print any object accepted by the 'rich' library.

        Args:
            object: Object being printed.
        """

    @abstractmethod
    def print_text(self, text: str, color: str = "", style: str = "") -> None:
        """Prints text with style and color set in 'attributes'.

        Args:
            text: Text being printed.
            color: The color of the text. Defaults to "".
            style: The style being applied to the text. Defaults to "".

        Raises:
            ValueError: In case the style or the color are not valid or if
                the content of text is empty.
        """

    @abstractmethod
    def print_panel(
        self,
        text: str,
        color: str = "",
        title: str = "",
    ) -> None:
        """Print a Rich panel containing the given text after validation the values
        being passed to set up the output.

        Args:
            text: The content to display inside the panel.
            title: Optional title displayed at the top of the panel.
            color: Optional color style applied to the text inside the panel.

        Raises:
            ValueError: If the provided 'color' is invalid or the text is empty.
        """

    @abstractmethod
    def create_table(
        self, *columns: Iterable[str], header_style: str = "bold magenta"
    ) -> Table:
        """Create a Rich table with the given column headers.

        Only create the table so that it returns a 'Table' object for setting up
        its data and columns later on.

        Args:
            *columns: One or more strings representing the table's column names.
            header_style: Style applied to the table header. Defaults to 'bold magenta'.

        Returns:
            Table: A Rich Table instance ready to receive rows.

        Raises:
            ValueError: If no column names are provided.
        """

    @abstractmethod
    def print_table(self, table: Table) -> None:
        """Render a Rich table to the console.

        Args:
            table: A Rich Table instance to be printed.
            None
        """

    @abstractmethod
    def print_markdown(self, md_text: str) -> None:
        """Render Markdown-formatted text using Rich.

        Args:
            md_text: A string containing Markdown content.

        Raises:
            ValueError: If the provided Markdown text is empty.
        """

    @abstractmethod
    def print_code(
        self, code: str, language: str = "sql", theme: str = "material"
    ) -> None:
        """Print highlighted source code.

        Args:
            code: The code snippet to highlight.
            language: The programming language used for syntax highlighting.
                Default = sql.
            theme: The theme used for syntax highlighting. Default = material.

        Raises:
            ValueError: If the provided 'code', 'theme' or 'language' are not valid.
        """

    @abstractmethod
    def get_input(
        self, text: str, color: str = "bright_green", style: str = "bold"
    ) -> str:
        """Read input from user via terminal.

        Args:
            text: Text for the prompt.
            color: The color of the text.
            style: The style being applied to the text.

        Returns:
            Text: The choice that has been input.

        Raises:
            ValueError: In case the style or the color are not valid.
        """
