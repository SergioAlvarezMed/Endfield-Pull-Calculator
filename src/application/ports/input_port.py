"""Input port for receiving user input."""

from typing import Protocol, Optional


class InputPort(Protocol):
    """
    Port for user input.
    
    This abstracts how we receive input from the user.
    """
    
    def get_integer(self, prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
        """Get integer input from user with optional validation."""
        ...
    
    def get_boolean(self, prompt: str) -> bool:
        """Get yes/no boolean input from user."""
        ...
    
    def get_choice(self, prompt: str, choices: list[str]) -> str:
        """Get a choice from a list of options."""
        ...
