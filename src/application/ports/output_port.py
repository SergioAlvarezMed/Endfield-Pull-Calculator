"""Output port for presenting results."""

from typing import Protocol, Any


class OutputPort(Protocol):
    """
    Port for output/presentation.
    
    This abstracts how results are presented to the user.
    """
    
    def show_message(self, message: str) -> None:
        """Display a message."""
        ...
    
    def show_error(self, error: str) -> None:
        """Display an error message."""
        ...
    
    def show_data(self, data: dict[str, Any]) -> None:
        """Display structured data."""
        ...
    
    def show_table(self, headers: list[str], rows: list[list[Any]]) -> None:
        """Display a table."""
        ...
