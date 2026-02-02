"""Tests for PityState entity."""

import pytest
from pydantic import ValidationError
from src.domain.entities import PityState


class TestPityState:
    """Test suite for PityState entity."""
    
    def test_initial_state(self):
        """Test creating initial state."""
        state = PityState.initial()
        assert state.pulls_without_6_star == 0
        assert state.pulls_without_5_star == 0
        assert state.banner_pulls == 0
        assert state.total_pulls == 0
    
    def test_valid_state(self):
        """Test creating valid state."""
        state = PityState(
            pulls_without_6_star=50,
            pulls_without_5_star=5,
            banner_pulls=50,
            total_pulls=100
        )
        assert state.pulls_without_6_star == 50
        assert state.banner_pulls == 50
        assert state.total_pulls == 100
    
    def test_pity_limit_validation(self):
        """Test that pity cannot exceed 80."""
        with pytest.raises(ValidationError):
            PityState(
                pulls_without_6_star=81,
                pulls_without_5_star=0,
                banner_pulls=81,
                total_pulls=81
            )
    
    def test_5_star_pity_limit(self):
        """Test that 5★ pity cannot exceed 10."""
        with pytest.raises(ValidationError):
            PityState(
                pulls_without_6_star=50,
                pulls_without_5_star=11,
                banner_pulls=50,
                total_pulls=50
            )
    
    def test_total_pulls_validation(self):
        """Test that total_pulls >= banner_pulls."""
        with pytest.raises(ValidationError):
            PityState(
                pulls_without_6_star=50,
                pulls_without_5_star=0,
                banner_pulls=100,
                total_pulls=50  # Invalid: less than banner_pulls
            )
    
    def test_is_at_hard_pity(self):
        """Test hard pity check."""
        state = PityState(
            pulls_without_6_star=80,
            pulls_without_5_star=0,
            banner_pulls=80,
            total_pulls=80
        )
        assert state.is_at_hard_pity() is True
        
        state2 = PityState.initial()
        assert state2.is_at_hard_pity() is False
    
    def test_is_in_soft_pity(self):
        """Test soft pity check."""
        state = PityState(
            pulls_without_6_star=65,
            pulls_without_5_star=0,
            banner_pulls=65,
            total_pulls=65
        )
        assert state.is_in_soft_pity() is True
        
        state2 = PityState(
            pulls_without_6_star=64,
            pulls_without_5_star=0,
            banner_pulls=64,
            total_pulls=64
        )
        assert state2.is_in_soft_pity() is False
    
    def test_increment_pull(self):
        """Test incrementing pull counters."""
        state = PityState.initial()
        new_state = state.increment_pull()
        
        assert new_state.pulls_without_6_star == 1
        assert new_state.pulls_without_5_star == 1
        assert new_state.banner_pulls == 1
        assert new_state.total_pulls == 1
        
        # Original state unchanged (immutability)
        assert state.pulls_without_6_star == 0
    
    def test_reset_6_star_pity(self):
        """Test resetting 6★ pity."""
        state = PityState(
            pulls_without_6_star=50,
            pulls_without_5_star=5,
            banner_pulls=50,
            total_pulls=100
        )
        new_state = state.reset_6_star_pity()
        
        assert new_state.pulls_without_6_star == 0
        assert new_state.pulls_without_5_star == 5  # Unchanged
        assert new_state.banner_pulls == 50  # Unchanged
    
    def test_reset_5_star_pity(self):
        """Test resetting 5★ pity."""
        state = PityState(
            pulls_without_6_star=50,
            pulls_without_5_star=5,
            banner_pulls=50,
            total_pulls=100
        )
        new_state = state.reset_5_star_pity()
        
        assert new_state.pulls_without_5_star == 0
        assert new_state.pulls_without_6_star == 50  # Unchanged
