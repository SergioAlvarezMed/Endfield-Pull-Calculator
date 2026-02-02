"""Probability calculation domain service."""

from ..value_objects import Probability, GameRules, PullCount


class ProbabilityCalculator:
    """
    Domain service for calculating probabilities.
    
    Stateless service containing pure business logic for probability calculations.
    """
    
    def __init__(self, rules: GameRules):
        """Initialize with game rules."""
        self.rules = rules
    
    def calculate_6_star_probability(self, pulls_without_6_star: int) -> Probability:
        """
        Calculate the probability of getting a 6★ on the next pull.
        
        - Base: 0.8%
        - Soft Pity (pull 65+): +5% for each pull after 65
        - Hard Pity (pull 80): 100% guaranteed
        
        Args:
            pulls_without_6_star: Number of pulls since last 6★ (0-indexed)
        
        Returns:
            Probability of getting 6★ on next pull
        """
        # Hard pity: pull 80 (index 79) is 100% guaranteed
        if pulls_without_6_star >= self.rules.hard_pity - 1:
            return Probability.certain()
        
        # Soft pity: starts at pull 65 (index 64)
        if pulls_without_6_star >= self.rules.soft_pity_start - 1:
            pulls_in_soft = pulls_without_6_star - (self.rules.soft_pity_start - 1) + 1
            prob_value = self.rules.prob_6_star_base + (pulls_in_soft * self.rules.soft_pity_increment)
            return Probability(value=min(prob_value, 1.0))
        
        return Probability(value=self.rules.prob_6_star_base)
    
    def calculate_pulls_for_5_star(self, pulls_without_5_star: int) -> int:
        """
        Calculate how many pulls are left for the 5★ guarantee.
        
        Args:
            pulls_without_5_star: Number of pulls since last 5★
        
        Returns:
            Number of pulls remaining until 5★ guarantee
        """
        return self.rules.five_star_guarantee - (pulls_without_5_star % self.rules.five_star_guarantee)
    
    def calculate_average_pulls_to_6_star(self) -> float:
        """
        Calculate the expected average pull to get a 6★.
        
        This accounts for the soft pity mechanics.
        
        Returns:
            Expected number of pulls to get a 6★
        """
        expected_pull = 0.0
        prob_no_6_previous = 1.0
        
        for t in range(self.rules.hard_pity):
            pull_prob = float(self.calculate_6_star_probability(t))
            # Probability of getting 6★ exactly on this pull
            exact_prob = prob_no_6_previous * pull_prob
            expected_pull += (t + 1) * exact_prob
            prob_no_6_previous *= (1 - pull_prob)
        
        # If we reach hard pity without 6★
        expected_pull += self.rules.hard_pity * prob_no_6_previous
        
        return expected_pull
    
    def calculate_cumulative_probability(self, current_pity: int, num_pulls: int) -> Probability:
        """
        Calculate cumulative probability of getting at least one 6★ in the next N pulls.
        
        Args:
            current_pity: Current pity count
            num_pulls: Number of future pulls to consider
        
        Returns:
            Probability of getting at least one 6★
        """
        prob_no_6_star = 1.0
        
        for i in range(num_pulls):
            pull_index = current_pity + i
            if pull_index >= self.rules.hard_pity:
                # Guaranteed by hard pity
                return Probability.certain()
            
            prob_this_pull = float(self.calculate_6_star_probability(pull_index))
            prob_no_6_star *= (1 - prob_this_pull)
        
        return Probability(value=1.0 - prob_no_6_star)
