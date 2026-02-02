"""Integration tests for complete flows."""

import pytest
from pathlib import Path
import tempfile
from src.domain.value_objects import GameRules
from src.domain.services import ProbabilityCalculator, CounterCalculator, PitySimulator
from src.domain.entities import PityState
from src.application.use_cases import CalculateStateUseCase, SimulatePullUseCase
from src.infrastructure.persistence.json_repository import JsonStateRepository


class TestEndToEndFlow:
    """Integration tests for complete user flows."""
    
    def test_complete_state_calculation_flow(self):
        """Test complete flow from state creation to calculation."""
        # Setup
        rules = GameRules.default()
        prob_calc = ProbabilityCalculator(rules)
        counter_calc = CounterCalculator(rules)
        use_case = CalculateStateUseCase(prob_calc, counter_calc, rules)
        
        # Create state
        state = PityState(
            pulls_without_6_star=50,
            pulls_without_5_star=5,
            banner_pulls=50,
            total_pulls=100
        )
        
        # Execute use case
        info = use_case.execute(state)
        
        # Verify results
        assert info.current_pity == 50
        assert info.pulls_to_soft_pity == 15
        assert info.pulls_to_hard_pity == 30
        assert info.in_soft_pity is False
    
    def test_persistence_flow(self):
        """Test saving and loading state."""
        # Use temporary file
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            repository = JsonStateRepository(tmp_path)
            
            # Create and save state
            state = PityState(
                pulls_without_6_star=65,
                pulls_without_5_star=5,
                banner_pulls=65,
                total_pulls=100
            )
            repository.save(state)
            
            # Load state
            loaded_state = repository.load()
            
            # Verify
            assert loaded_state is not None
            assert loaded_state.pulls_without_6_star == 65
            assert loaded_state.pulls_without_5_star == 5
            assert loaded_state.banner_pulls == 65
            assert loaded_state.total_pulls == 100
        
        finally:
            # Cleanup
            if tmp_path.exists():
                tmp_path.unlink()
    
    def test_simulation_with_persistence(self):
        """Test simulating a pull and persisting result."""
        # Setup
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            rules = GameRules.default()
            
            class MockRandom:
                def random(self):
                    return 0.5
            
            simulator = PitySimulator(rules, MockRandom())
            repository = JsonStateRepository(tmp_path)
            use_case = SimulatePullUseCase(simulator, repository, rules)
            
            # Create state at hard pity
            state = PityState(
                pulls_without_6_star=80,
                pulls_without_5_star=0,
                banner_pulls=80,
                total_pulls=80
            )
            
            # Simulate winning 50/50
            result = use_case.execute(state, won_50_50=True)
            
            # Verify result
            assert result.won is True
            assert result.new_pity == 0  # Should reset
            
            # Verify state was saved
            loaded_state = repository.load()
            assert loaded_state is not None
            assert loaded_state.pulls_without_6_star == 0
        
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
