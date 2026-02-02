"""Simulate pull use case."""

from src.domain.entities import PityState
from src.domain.services import PitySimulator
from src.domain.value_objects import GameRules
from ..dto import SimulationResultDTO
from ..ports import StateRepository


class SimulatePullUseCase:
    """
    Use case for simulating a 50/50 pull.
    
    This orchestrates the simulation and persists the result.
    """
    
    def __init__(
        self,
        simulator: PitySimulator,
        repository: StateRepository,
        rules: GameRules
    ):
        """Initialize use case."""
        self.simulator = simulator
        self.repository = repository
        self.rules = rules
    
    def execute(self, state: PityState, won_50_50: bool) -> SimulationResultDTO:
        """
        Simulate a 50/50 pull.
        
        Args:
            state: Current pity state
            won_50_50: Whether player wins the 50/50
        
        Returns:
            Simulation result as DTO
        """
        # Simulate the pull
        result = self.simulator.simulate_50_50(won_50_50)
        
        # Apply result to state
        new_state = self.simulator.apply_pull_result(state, result)
        
        # Save new state
        self.repository.save(new_state)
        
        # Generate message
        if result.won_50_50:
            message = "You won the 50/50! You got the featured banner character."
        else:
            char_type = result.character_type.value
            if char_type == "prev_limited_1":
                message = "You lost the 50/50. You got the 1st previous limited."
            elif char_type == "prev_limited_2":
                message = "You lost the 50/50. You got the 2nd previous limited."
            else:
                message = "You lost the 50/50. You got a standard 6★."
            message += "\n  ⚠ NO featured guarantee until pull 120."
        
        return SimulationResultDTO(
            won=result.won_50_50 or False,
            character_type=result.character_type.value,
            message=message,
            new_pity=new_state.pulls_without_6_star,
            banner_pulls=new_state.banner_pulls
        )
