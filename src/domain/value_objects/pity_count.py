"""Pity counter value objects."""

from __future__ import annotations
from pydantic import BaseModel, Field, field_validator


class PullCount(BaseModel):
    """
    Represents a count of pulls.
    
    Immutable value object.
    """
    value: int = Field(ge=0, description="Number of pulls")
    
    model_config = {"frozen": True}
    
    def __int__(self) -> int:
        return self.value
    
    def __add__(self, other: int | "PullCount") -> "PullCount":
        if isinstance(other, PullCount):
            return PullCount(value=self.value + other.value)
        return PullCount(value=self.value + other)
    
    def __sub__(self, other: int | "PullCount") -> "PullCount":
        if isinstance(other, PullCount):
            result = self.value - other.value
        else:
            result = self.value - other
        return PullCount(value=max(0, result))
    
    def __str__(self) -> str:
        return str(self.value)
    
    @classmethod
    def zero(cls) -> "PullCount":
        """Return count of 0."""
        return cls(value=0)


class PityCount(BaseModel):
    """
    Represents a pity counter value.
    
    Domain invariant: Pity count cannot exceed hard pity limit.
    Immutable value object.
    """
    value: int = Field(ge=0, le=80, description="Pity counter value (0-80)")
    
    model_config = {"frozen": True}
    
    @field_validator("value")
    @classmethod
    def validate_pity_limit(cls, v: int) -> int:
        """Ensure pity doesn't exceed hard pity."""
        if v > 80:
            raise ValueError(f"Pity count cannot exceed 80, got {v}")
        return v
    
    def __int__(self) -> int:
        return self.value
    
    def __str__(self) -> str:
        return f"{self.value}/80"
    
    def is_soft_pity(self) -> bool:
        """Check if in soft pity range (65+)."""
        return self.value >= 65
    
    def is_hard_pity(self) -> bool:
        """Check if at hard pity (80)."""
        return self.value >= 80
    
    @classmethod
    def zero(cls) -> "PityCount":
        """Return pity count of 0."""
        return cls(value=0)
