"""Store dataclass used for displaying menus with 'rich'."""

from dataclasses import dataclass

from beartype.typing import Callable, Dict, List


@dataclass
class MenuInfo:
    """Dataclass responsible for storing the necessary information
    used by 'rich' interactive CRUD menus.

    Attributes:
        menu_name (str): Name of the menu for display.
        options (List[str]): Options representing the available operations.
        actions (Dict[str, Callable[[], None]]): Methods to be executed based
            on the selected option.
        exit_choice (str): The choice that represent the exit path.
        exit_action (Callable[[], None] | None): The method that will be
            executed when exiting the loop. Default = None.
    """

    menu_name: str
    options: List[str]
    actions: Dict[str, Callable[[], None]]
    exit_choice: str
    exit_action: Callable[[], None] | None = None
