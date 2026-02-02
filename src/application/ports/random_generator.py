"""Random generator port."""

from typing import Protocol


class RandomGeneratorPort(Protocol):
    """
    Port for random number generation.
    
    This allows us to inject different random generators for testing.
    """
    
    def random(self) -> float:
        """Generate random float in [0, 1)."""
        ...
