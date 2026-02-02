"""Show base rates use case."""

from src.domain.value_objects import GameRules


class ShowBaseRatesUseCase:
    """
    Use case for displaying base rates and pity system information.
    """
    
    def __init__(self, rules: GameRules):
        """Initialize use case."""
        self.rules = rules
    
    def execute(self) -> dict:
        """
        Get base rates and pity system information.
        
        Returns:
            Dictionary with all game rules
        """
        return {
            "base_rates": {
                "6_star": self.rules.prob_6_star_base * 100,
                "5_star": self.rules.prob_5_star * 100,
                "4_star": self.rules.prob_4_star * 100,
            },
            "pity_system": {
                "5_star_guarantee": self.rules.five_star_guarantee,
                "soft_pity_start": self.rules.soft_pity_start,
                "soft_pity_increment": self.rules.soft_pity_increment * 100,
                "hard_pity": self.rules.hard_pity,
                "featured_guarantee": self.rules.featured_guarantee,
                "bonus_dupe": self.rules.bonus_dupe,
            },
            "special_rules": {
                "prob_prev_limited": self.rules.prob_prev_limited * 100,
                "prob_standard": (1 - self.rules.prob_prev_limited * 2) * 100,
                "free_pull_reward": self.rules.free_pull_reward,
            }
        }
