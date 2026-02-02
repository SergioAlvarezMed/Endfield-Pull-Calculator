"""Pytest configuration and shared fixtures."""

import pytest
from src.domain.value_objects import GameRules
from src.domain.entities import PityState
from src.domain.services import ProbabilityCalculator, CounterCalculator, PitySimulator


@pytest.fixture
def game_rules():
    """Provide default game rules."""
    return GameRules.default()


@pytest.fixture
def prob_calculator(game_rules):
    """Provide probability calculator."""
    return ProbabilityCalculator(game_rules)


@pytest.fixture
def counter_calculator(game_rules):
    """Provide counter calculator."""
    return CounterCalculator(game_rules)


@pytest.fixture
def mock_random():
    """Provide mock random generator."""
    class MockRandom:
        def __init__(self, value=0.5):
            self.value = value
        
        def random(self):
            return self.value
    
    return MockRandom()


@pytest.fixture
def pity_simulator(game_rules, mock_random):
    """Provide pity simulator with mock random."""
    return PitySimulator(game_rules, mock_random)


@pytest.fixture
def initial_state():
    """Provide initial pity state."""
    return PityState.initial()


@pytest.fixture
def soft_pity_state():
    """Provide state at soft pity."""
    return PityState(
        pulls_without_6_star=65,
        pulls_without_5_star=0,
        banner_pulls=65,
        total_pulls=65
    )


@pytest.fixture
def hard_pity_state():
    """Provide state at hard pity."""
    return PityState(
        pulls_without_6_star=80,
        pulls_without_5_star=0,
        banner_pulls=80,
        total_pulls=80
    )
