"""Tests for ProbabilityCalculator service."""

import pytest
from src.domain.services import ProbabilityCalculator
from src.domain.value_objects import GameRules, Probability


class TestProbabilityCalculator:
    """Test suite for ProbabilityCalculator."""
    
    def test_base_probability(self, prob_calculator):
        """Test base 6★ probability."""
        prob = prob_calculator.calculate_6_star_probability(0)
        assert float(prob) == 0.008
    
    def test_soft_pity_start(self, prob_calculator):
        """Test soft pity at pull 65."""
        # Pull 65 is index 64
        prob = prob_calculator.calculate_6_star_probability(64)
        expected = 0.008 + 0.05  # Base + 1 increment
        assert abs(float(prob) - expected) < 0.001
    
    def test_hard_pity(self, prob_calculator):
        """Test hard pity at pull 80."""
        # Pull 80 is index 79
        prob = prob_calculator.calculate_6_star_probability(79)
        assert float(prob) == 1.0
    
    def test_soft_pity_progression(self, prob_calculator):
        """Test soft pity increments correctly."""
        # Pull 66 (index 65) = base + 2 increments
        prob = prob_calculator.calculate_6_star_probability(65)
        expected = 0.008 + 0.05 * 2
        assert abs(float(prob) - expected) < 0.001
        
        # Pull 70 (index 69) = base + 6 increments
        prob = prob_calculator.calculate_6_star_probability(69)
        expected = 0.008 + 0.05 * 6
        assert abs(float(prob) - expected) < 0.001
    
    def test_calculate_pulls_for_5_star(self, prob_calculator):
        """Test 5★ guarantee calculation."""
        assert prob_calculator.calculate_pulls_for_5_star(0) == 10
        assert prob_calculator.calculate_pulls_for_5_star(5) == 5
        assert prob_calculator.calculate_pulls_for_5_star(9) == 1
        assert prob_calculator.calculate_pulls_for_5_star(10) == 10  # Resets
    
    def test_average_pulls_to_6_star(self, prob_calculator):
        """Test expected value calculation."""
        avg = prob_calculator.calculate_average_pulls_to_6_star()
        # Average should be less than hard pity
        assert 0 < avg < 80
        # Known approximation from soft pity mechanics (around 53-54 pulls)
        assert 40 < avg < 60
    
    @pytest.mark.parametrize("current_pity,num_pulls,expected_min", [
        (0, 80, 0.99),  # Should be near certain within 80 pulls
        (70, 10, 0.90),  # High probability from soft pity
        (0, 1, 0.008),  # Single pull at base rate
    ])
    def test_cumulative_probability(self, prob_calculator, current_pity, num_pulls, expected_min):
        """Test cumulative probability calculation."""
        prob = prob_calculator.calculate_cumulative_probability(current_pity, num_pulls)
        assert float(prob) >= expected_min
