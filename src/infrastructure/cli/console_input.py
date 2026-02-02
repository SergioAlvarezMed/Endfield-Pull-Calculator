"""Console input adapter."""

from __future__ import annotations


class ConsoleInput:
    """
    Console-based input adapter.
    
    Implements InputPort protocol.
    """
    
    def get_integer(
        self,
        prompt: str,
        min_val: int | None = None,
        max_val: int | None = None
    ) -> int:
        """Get integer input from user with validation."""
        while True:
            try:
                value = int(input(prompt))
                
                if min_val is not None and value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                
                return value
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def get_boolean(self, prompt: str) -> bool:
        """Get yes/no boolean input from user."""
        while True:
            response = input(prompt).strip().lower()
            if response in ('y', 'yes', '1', 'true'):
                return True
            elif response in ('n', 'no', '0', 'false'):
                return False
            else:
                print("❌ Please enter 'y' or 'n'.")
    
    def get_choice(self, prompt: str, choices: list[str]) -> str:
        """Get a choice from a list of options."""
        while True:
            choice = input(prompt).strip()
            if choice in choices:
                return choice
            print(f"❌ Please choose from: {', '.join(choices)}")
