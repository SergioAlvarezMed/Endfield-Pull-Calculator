"""Tests for Probability value object."""

import pytest
from pydantic import ValidationError
from src.domain.value_objects import Probability


class TestProbability:
    """Test suite for Probability value object."""
    
    def test_valid_probability(self):
        """Test creating valid probability."""
        prob = Probability(value=0.5)
        assert prob.value == 0.5
        assert float(prob) == 0.5
    
    def test_probability_bounds(self):
        """Test probability boundaries."""
        # Valid boundaries
        Probability(value=0.0)
        Probability(value=1.0)
        
        # Invalid values
        with pytest.raises(ValidationError):
            Probability(value=-0.1)
        
        with pytest.raises(ValidationError):
            Probability(value=1.1)
    
    def test_as_percentage(self):
        """Test conversion to percentage."""
        prob = Probability(value=0.5)
        assert prob.as_percentage() == 50.0
        
        prob = Probability(value=0.008)
        assert prob.as_percentage() == 0.8
    
    def test_from_percentage(self):
        """Test creating from percentage."""
        prob = Probability.from_percentage(50.0)
        assert prob.value == 0.5
        
        prob = Probability.from_percentage(0.8)
        assert prob.value == 0.008
    
    def test_zero_and_certain(self):
        """Test factory methods."""
        zero = Probability.zero()
        assert zero.value == 0.0
        
        certain = Probability.certain()
        assert certain.value == 1.0
    
    def test_immutability(self):
        """Test that probability is immutable."""
        prob = Probability(value=0.5)
        with pytest.raises(ValidationError):
            prob.value = 0.6
    
    def test_string_representation(self):
        """Test string formatting."""
        prob = Probability(value=0.5)
        assert str(prob) == "50.00%"
