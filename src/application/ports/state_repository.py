"""State repository port."""

from typing import Protocol, Optional
from src.domain.entities import PityState


class StateRepository(Protocol):
    """
    Port for state persistence.
    
    This is an abstract interface that infrastructure will implement.
    """
    
    def save(self, state: PityState) -> None:
        """Save pity state."""
        ...
    
    def load(self) -> Optional[PityState]:
        """Load pity state. Returns None if no state exists."""
        ...
    
    def exists(self) -> bool:
        """Check if saved state exists."""
        ...
    
    def delete(self) -> None:
        """Delete saved state."""
        ...
