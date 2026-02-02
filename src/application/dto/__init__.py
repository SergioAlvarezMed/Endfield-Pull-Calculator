"""Data Transfer Objects for application layer."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StateInfoDTO:
    """DTO for current state information."""
    pulls_without_6_star: int
    pulls_without_5_star: int
    banner_pulls: int
    total_pulls: int
    current_pity: int
    banner_counter: int
    dupe_counter: int
    pulls_to_soft_pity: int
    pulls_to_hard_pity: int
    pulls_to_featured: int
    pulls_to_bonus_dupe: int
    pulls_to_free_pull: int
    pulls_to_5_star: int
    in_soft_pity: bool
    at_hard_pity: bool
    at_featured_guarantee: bool


@dataclass(frozen=True)
class SimulationResultDTO:
    """DTO for 50/50 simulation result."""
    won: bool
    character_type: str
    message: str
    new_pity: int
    banner_pulls: int


@dataclass(frozen=True)
class ProbabilityTableRowDTO:
    """DTO for a single row in probability table."""
    pull_number: int
    pity: int
    probability: float
    cumulative: float
