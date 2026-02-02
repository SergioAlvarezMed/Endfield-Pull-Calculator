"""Pity simulation domain service."""

from typing import Protocol

from ..entities import PullResult, CharacterType, PityState
from ..value_objects import GameRules


class RandomGenerator(Protocol):
    """Protocol for random number generation (dependency inversion)."""
    
    def random(self) -> float:
        """Generate random float in [0, 1)."""
        ...


class PitySimulator:
    """
    Domain service for simulating pity/gacha pulls.
    
    Uses dependency injection for random generation to enable testing.
    """
    
    def __init__(self, rules: GameRules, random_gen: RandomGenerator):
        """
        Initialize simulator.
        
        Args:
            rules: Game rules
            random_gen: Random number generator (injected for testing)
        """
        self.rules = rules
        self.random_gen = random_gen
    
    def simulate_50_50(self, won: bool) -> PullResult:
        """
        Simulate a 50/50 result.
        
        Args:
            won: Whether the player won the 50/50
        
        Returns:
            PullResult with character type
        """
        if won:
            return PullResult(
                rarity=6,
                character_type=CharacterType.FEATURED,
                won_50_50=True
            )
        
        # Lost 50/50 - determine which off-banner character
        roll = self.random_gen.random()
        
        if roll < self.rules.prob_prev_limited:
            character_type = CharacterType.PREV_LIMITED_1
        elif roll < self.rules.prob_prev_limited * 2:
            character_type = CharacterType.PREV_LIMITED_2
        else:
            character_type = CharacterType.STANDARD
        
        return PullResult(
            rarity=6,
            character_type=character_type,
            won_50_50=False
        )
    
    def is_in_50_50(self, state: PityState) -> bool:
        """
        Check if player is in a 50/50 event.
        
        Args:
            state: Current pity state
        
        Returns:
            True if at hard pity (50/50 active)
        """
        return state.is_at_hard_pity()
    
    def has_featured_guarantee(self, state: PityState) -> bool:
        """
        Check if player has featured guarantee.
        
        Args:
            state: Current pity state
        
        Returns:
            True if at 120 pulls on banner
        """
        return state.is_at_featured_guarantee()
    
    def apply_pull_result(self, state: PityState, result: PullResult) -> PityState:
        """
        Apply a pull result to the current state.
        
        Args:
            state: Current pity state
            result: Pull result to apply
        
        Returns:
            New pity state after applying result
        """
        new_state = state.increment_pull()
        
        if result.is_six_star():
            new_state = new_state.reset_6_star_pity()
        
        if result.is_five_star() or result.is_six_star():
            new_state = new_state.reset_5_star_pity()
        
        return new_state
