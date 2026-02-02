"""Standard Python random generator adapter."""

import random


class StandardRandomGenerator:
    """
    Adapter for Python's standard random module.
    
    Implements RandomGeneratorPort protocol.
    """
    
    def random(self) -> float:
        """Generate random float in [0, 1)."""
        return random.random()
