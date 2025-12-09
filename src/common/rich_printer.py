"""Utilities for displaying information in different ways on the terminal."""

from beartype import beartype
from beartype.typing import Any, Iterable
from rich.align import Align
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from config.rich_info import RICH_COLORS, RICH_LANGUAGES, RICH_STYLES, RICH_THEMES
from src.interfaces.common.rich_printer_interface import IRichPrinter


class RichPrinter(IRichPrinter):
    """Create an UI with many options for displaying data.
    Thsis class operates as a 'Singleton' in this project.
    """

    def __init__(self) -> None:
        """Initialize terminal printer with an instance of 'Console'."""
        self._console = Console()

    @beartype
    def _prepare_text(self, text: str, color: str, style: str) -> Text:
        """Prepare style and color of the text being printed.

        Args:
            text: Text being printed.
            color: The color of the text.
            style: The style being applied to the text.

        Returns:
            Text: Content for printing after cuztomizing it.

        Raises:
            ValueError: In case the style or the color are not valid.
        """
        if not text:
            raise ValueError("Text cannot be empty.")

        styled_text: Text = Text(text)

        if color:
            color = color.lower()
            if color not in RICH_COLORS:
                raise ValueError(f"Color {color} is invalid.")

            styled_text.stylize(color)

        if style:
            style = style.lower()
            if style not in RICH_STYLES:
                raise ValueError(f"Style {style} is invalid.")

            styled_text.stylize(style)

        return styled_text

    @beartype
    def print_rich(self, object: Any) -> None:
        """Generic method for printing different rich objects.

        Args:
            object: Object being printed.
        """
        self._console.print(object)

    @beartype
    def print_text(self, text: str, color: str = "", style: str = "") -> None:
        """Prints text with style and color set in 'attributes'.

        Args:
            text: Text being printed.
            color: The color of the text.
            style: The style being applied to the text.

        Raises:
            ValueError: In case the style or the color are not valid or if
                the content of text is empty.
        """
        self._console.print(
            Align.left(self._prepare_text(text, color, style)), end="\n"
        )

    @beartype
    def print_panel(
        self,
        text: str,
        color: str = "",
        title: str = "",
    ) -> None:
        """Print a Rich panel containing the given text.

        Args:
            text: The content to display inside the panel.
            title: Optional title displayed at the top of the panel.
            color: Optional color style applied to the text inside the panel.

        Raises:
            ValueError: If the provided 'color' is invalid or the text is empty.
        """
        if not text:
            raise ValueError("Text cannot be empty.")

        if color:
            if color not in RICH_COLORS:
                raise ValueError(f"Color {color} is invalid.")

        panel = Panel(
            Text(text, style=color) if color else text, title=title if title else None
        )

        self._console.print(Align.left(panel))

    @beartype
    def create_table(
        self, *columns: Iterable[str], header_style: str = "bold magenta"
    ) -> Table:
        """Create a Rich table with the given column headers.

        Args:
            *columns: One or more strings representing the table's column names.
            header_style: Style applied to the table header. Defaults to 'bold magenta'.

        Returns:
            Table: A Rich Table instance ready to receive rows.

        Raises:
            ValueError: If no column names are provided.
        """
        if not columns:
            raise ValueError("Columns cannot be empty.")

        table: Table = Table(show_header=True, header_style=header_style)
        for col in columns:
            table.add_column(str(col))

        return table

    @beartype
    def print_table(self, table: Table) -> None:
        """Render a Rich table to the console.

        Args:
            table: A Rich Table instance to be printed.
            None
        """
        self._console.print(Align.left(table))

    @beartype
    def print_markdown(self, md_text: str) -> None:
        """Render Markdown-formatted text using Rich.

        Args:
            md_text: A string containing Markdown content.

        Raises:
            ValueError: If the provided Markdown text is empty.
        """
        if not md_text:
            raise ValueError("Markdown text cannot be empty.")

        mark_down: Markdown = Markdown(md_text)
        self._console.print(Align.left(mark_down))

    @beartype
    def print_code(
        self, code: str, language: str = "python", theme: str = "dracula"
    ) -> None:
        """Print highlighted source code.

        Args:
            code: The code snippet to highlight.
            language: The programming language used for syntax highlighting.
            theme: The theme used for syntax highlighting.

        Raises:
            ValueError: If the provided 'code', 'theme' or 'language' are not valid.
        """
        if not code:
            raise ValueError("Content of code cannot be empty.")

        if language not in RICH_LANGUAGES:
            raise ValueError(f"Language {language} is invalid.")

        if theme not in RICH_THEMES:
            raise ValueError(f"Theme {theme} is invalid.")

        syntax = Syntax(code, language, theme=theme, line_numbers=True)
        self._console.print(Align.left(syntax))
