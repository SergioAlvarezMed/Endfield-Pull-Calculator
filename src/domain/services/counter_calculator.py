"""Counter calculation domain service."""

from ..value_objects import PityCount, PullCount, GameRules


class CounterCalculator:
    """
    Domain service for calculating pity counters.
    
    Stateless service for counter transformations.
    """
    
    def __init__(self, rules: GameRules):
        """Initialize with game rules."""
        self.rules = rules
    
    def calculate_pity_counter(self, pulls_without_6_star: int) -> PityCount:
        """
        Calculate P(r) = min(r, 80) - Current pity counter.
        
        Args:
            pulls_without_6_star: Number of pulls without 6★
        
        Returns:
            Current pity count
        """
        return PityCount(value=min(pulls_without_6_star, self.rules.hard_pity))
    
    def calculate_spark_counter(self, banner_pulls: int) -> int:
        """
        Calculate S(r) = min(r, 120) - Featured guarantee counter.
        
        Args:
            banner_pulls: Number of pulls on current banner
        
        Returns:
            Current spark counter value
        """
        return min(banner_pulls, self.rules.featured_guarantee)
    
    def calculate_dupe_counter(self, total_pulls: int) -> int:
        """
        Calculate D(r) = min(r, 240) - Spark Dupe counter.
        
        Args:
            total_pulls: Total accumulated pulls
        
        Returns:
            Current dupe counter value
        """
        return min(total_pulls, self.rules.bonus_dupe)
    
    def calculate_pity_reset(self, banner_pulls: int) -> int:
        """
        Calculate PR(r) = max(0, r-80) - Pity reset when winning 50/50 with active spark.
        
        Args:
            banner_pulls: Number of pulls on banner
        
        Returns:
            Pity value after reset
        """
        return max(0, banner_pulls - self.rules.hard_pity)
    
    def calculate_pulls_to_soft_pity(self, current_pity: int) -> int:
        """Calculate pulls remaining until soft pity starts."""
        return max(0, self.rules.soft_pity_start - current_pity)
    
    def calculate_pulls_to_hard_pity(self, current_pity: int) -> int:
        """Calculate pulls remaining until hard pity."""
        return max(0, self.rules.hard_pity - current_pity)
    
    def calculate_pulls_to_featured(self, banner_pulls: int) -> int:
        """Calculate pulls remaining until featured guarantee."""
        return max(0, self.rules.featured_guarantee - banner_pulls)
    
    def calculate_pulls_to_bonus_dupe(self, total_pulls: int) -> int:
        """Calculate pulls remaining until bonus dupe."""
        return max(0, self.rules.bonus_dupe - total_pulls)
    
    def calculate_pulls_to_free_pull(self, banner_pulls: int) -> int:
        """Calculate pulls remaining until free 10-pull reward."""
        return max(0, self.rules.free_pull_reward - banner_pulls)
