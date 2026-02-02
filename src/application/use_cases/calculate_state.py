"""Calculate current state use case."""

from src.domain.entities import PityState
from src.domain.services import ProbabilityCalculator, CounterCalculator
from src.domain.value_objects import GameRules
from ..dto import StateInfoDTO


class CalculateStateUseCase:
    """
    Use case for calculating current pity state information.
    
    This orchestrates domain services to calculate all state information.
    """
    
    def __init__(
        self,
        probability_calculator: ProbabilityCalculator,
        counter_calculator: CounterCalculator,
        rules: GameRules
    ):
        """Initialize use case with domain services."""
        self.prob_calc = probability_calculator
        self.counter_calc = counter_calculator
        self.rules = rules
    
    def execute(self, state: PityState) -> StateInfoDTO:
        """
        Calculate comprehensive state information.
        
        Args:
            state: Current pity state
        
        Returns:
            Complete state information as DTO
        """
        pity_count = self.counter_calc.calculate_pity_counter(state.pulls_without_6_star)
        spark_count = self.counter_calc.calculate_spark_counter(state.banner_pulls)
        dupe_count = self.counter_calc.calculate_dupe_counter(state.total_pulls)
        
        pulls_to_5_star = self.prob_calc.calculate_pulls_for_5_star(state.pulls_without_5_star)
        
        return StateInfoDTO(
            pulls_without_6_star=state.pulls_without_6_star,
            pulls_without_5_star=state.pulls_without_5_star,
            banner_pulls=state.banner_pulls,
            total_pulls=state.total_pulls,
            current_pity=int(pity_count),
            banner_counter=spark_count,
            dupe_counter=dupe_count,
            pulls_to_soft_pity=self.counter_calc.calculate_pulls_to_soft_pity(state.pulls_without_6_star),
            pulls_to_hard_pity=self.counter_calc.calculate_pulls_to_hard_pity(state.pulls_without_6_star),
            pulls_to_featured=self.counter_calc.calculate_pulls_to_featured(state.banner_pulls),
            pulls_to_bonus_dupe=self.counter_calc.calculate_pulls_to_bonus_dupe(state.total_pulls),
            pulls_to_free_pull=self.counter_calc.calculate_pulls_to_free_pull(state.banner_pulls),
            pulls_to_5_star=pulls_to_5_star,
            in_soft_pity=state.is_in_soft_pity(),
            at_hard_pity=state.is_at_hard_pity(),
            at_featured_guarantee=state.is_at_featured_guarantee()
        )
