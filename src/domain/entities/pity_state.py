"""Pity state entity."""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Self

from ..value_objects import PullCount, PityCount


class PityState(BaseModel):
    """
    Represents the current pity state of a player.
    
    This is the main entity that tracks all pity counters.
    Domain invariants:
    - pulls_without_6_star <= 80 (hard pity)
    - pulls_without_5_star <= 10 (5★ guarantee)
    - banner_pulls >= 0
    - total_pulls >= banner_pulls (total accumulates across banners)
    """
    pulls_without_6_star: int = Field(ge=0, le=80, description="Pulls since last 6★")
    pulls_without_5_star: int = Field(ge=0, le=10, default=0, description="Pulls since last 5★")
    banner_pulls: int = Field(ge=0, description="Pulls on current banner")
    total_pulls: int = Field(ge=0, description="Total accumulated pulls (for dupe counter)")
    
    @field_validator("pulls_without_6_star")
    @classmethod
    def validate_6_star_pity(cls, v: int) -> int:
        """Ensure 6★ pity doesn't exceed hard pity."""
        if v > 80:
            raise ValueError("6★ pity cannot exceed 80 (hard pity)")
        return v
    
    @field_validator("pulls_without_5_star")
    @classmethod
    def validate_5_star_pity(cls, v: int) -> int:
        """Ensure 5★ pity doesn't exceed guarantee."""
        if v > 10:
            raise ValueError("5★ pity cannot exceed 10 (guarantee)")
        return v
    
    @model_validator(mode="after")
    def validate_total_pulls(self) -> Self:
        """Ensure total pulls >= banner pulls."""
        if self.total_pulls < self.banner_pulls:
            raise ValueError(
                f"Total pulls ({self.total_pulls}) cannot be less than banner pulls ({self.banner_pulls})"
            )
        return self
    
    def get_pity_count(self) -> PityCount:
        """Get current pity count (min of pulls_without_6_star and 80)."""
        return PityCount(value=min(self.pulls_without_6_star, 80))
    
    def get_banner_count(self) -> PullCount:
        """Get current banner pull count."""
        return PullCount(value=self.banner_pulls)
    
    def get_total_count(self) -> PullCount:
        """Get total pull count."""
        return PullCount(value=self.total_pulls)
    
    def is_at_hard_pity(self) -> bool:
        """Check if at hard pity (guaranteed 6★)."""
        return self.pulls_without_6_star >= 80
    
    def is_in_soft_pity(self) -> bool:
        """Check if in soft pity range."""
        return self.pulls_without_6_star >= 65
    
    def is_at_featured_guarantee(self) -> bool:
        """Check if at featured guarantee."""
        return self.banner_pulls >= 120
    
    def is_at_5_star_guarantee(self) -> bool:
        """Check if at 5★ guarantee."""
        return self.pulls_without_5_star >= 10
    
    def increment_pull(self) -> "PityState":
        """
        Increment all counters by 1 (for a pull that didn't hit any pity).
        Returns new state.
        """
        return PityState(
            pulls_without_6_star=min(self.pulls_without_6_star + 1, 80),
            pulls_without_5_star=min(self.pulls_without_5_star + 1, 10),
            banner_pulls=self.banner_pulls + 1,
            total_pulls=self.total_pulls + 1
        )
    
    def reset_6_star_pity(self) -> "PityState":
        """
        Reset 6★ pity to 0.
        Returns new state.
        """
        return PityState(
            pulls_without_6_star=0,
            pulls_without_5_star=self.pulls_without_5_star,
            banner_pulls=self.banner_pulls,
            total_pulls=self.total_pulls
        )
    
    def reset_5_star_pity(self) -> "PityState":
        """
        Reset 5★ pity to 0.
        Returns new state.
        """
        return PityState(
            pulls_without_6_star=self.pulls_without_6_star,
            pulls_without_5_star=0,
            banner_pulls=self.banner_pulls,
            total_pulls=self.total_pulls
        )
    
    @classmethod
    def initial(cls) -> "PityState":
        """Create initial state (all counters at 0)."""
        return cls(
            pulls_without_6_star=0,
            pulls_without_5_star=0,
            banner_pulls=0,
            total_pulls=0
        )
