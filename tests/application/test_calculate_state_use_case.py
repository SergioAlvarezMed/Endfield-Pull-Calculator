"""Tests for CalculateStateUseCase."""

import pytest
from src.application.use_cases import CalculateStateUseCase
from src.domain.entities import PityState


class TestCalculateStateUseCase:
    """Test suite for CalculateStateUseCase."""
    
    def test_initial_state_calculation(self, game_rules, prob_calculator, counter_calculator):
        """Test calculating info for initial state."""
        use_case = CalculateStateUseCase(prob_calculator, counter_calculator, game_rules)
        state = PityState.initial()
        
        info = use_case.execute(state)
        
        assert info.pulls_without_6_star == 0
        assert info.current_pity == 0
        assert info.pulls_to_soft_pity == 65
        assert info.pulls_to_hard_pity == 80
        assert info.in_soft_pity is False
        assert info.at_hard_pity is False
    
    def test_soft_pity_state_calculation(self, game_rules, prob_calculator, counter_calculator):
        """Test calculating info at soft pity."""
        use_case = CalculateStateUseCase(prob_calculator, counter_calculator, game_rules)
        state = PityState(
            pulls_without_6_star=65,
            pulls_without_5_star=5,
            banner_pulls=65,
            total_pulls=100
        )
        
        info = use_case.execute(state)
        
        assert info.current_pity == 65
        assert info.pulls_to_soft_pity == 0
        assert info.pulls_to_hard_pity == 15
        assert info.in_soft_pity is True
        assert info.at_hard_pity is False
    
    def test_hard_pity_state_calculation(self, game_rules, prob_calculator, counter_calculator):
        """Test calculating info at hard pity."""
        use_case = CalculateStateUseCase(prob_calculator, counter_calculator, game_rules)
        state = PityState(
            pulls_without_6_star=80,
            pulls_without_5_star=10,
            banner_pulls=80,
            total_pulls=150
        )
        
        info = use_case.execute(state)
        
        assert info.current_pity == 80
        assert info.pulls_to_hard_pity == 0
        assert info.at_hard_pity is True
        assert info.in_soft_pity is True
