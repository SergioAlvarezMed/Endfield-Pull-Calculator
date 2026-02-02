"""Show probability table use case."""

from src.domain.services import ProbabilityCalculator, CounterCalculator
from src.domain.value_objects import GameRules
from ..dto import ProbabilityTableRowDTO


class ShowProbabilityTableUseCase:
    """
    Use case for generating probability tables.
    """
    
    def __init__(
        self,
        probability_calculator: ProbabilityCalculator,
        counter_calculator: CounterCalculator,
        rules: GameRules
    ):
        """Initialize use case."""
        self.prob_calc = probability_calculator
        self.counter_calc = counter_calculator
        self.rules = rules
    
    def execute(self, max_pulls: int = 80) -> list[ProbabilityTableRowDTO]:
        """
        Generate probability table for pulls 1 to max_pulls.
        
        Args:
            max_pulls: Maximum number of pulls to show
        
        Returns:
            List of table rows
        """
        rows = []
        cumulative_prob_no_6 = 1.0
        
        for pull in range(max_pulls):
            pity = self.counter_calc.calculate_pity_counter(pull)
            prob = self.prob_calc.calculate_6_star_probability(pull)
            
            # Update cumulative
            cumulative_prob_no_6 *= (1 - float(prob))
            cumulative = 1.0 - cumulative_prob_no_6
            
            rows.append(ProbabilityTableRowDTO(
                pull_number=pull + 1,
                pity=int(pity),
                probability=float(prob),
                cumulative=cumulative
            ))
        
        return rows
