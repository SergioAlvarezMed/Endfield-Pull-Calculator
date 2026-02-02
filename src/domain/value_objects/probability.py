"""Probability value object."""

from pydantic import BaseModel, Field, field_validator


class Probability(BaseModel):
    """
    Represents a probability value between 0 and 1.
    
    Immutable value object with validation.
    """
    value: float = Field(ge=0.0, le=1.0, description="Probability value between 0 and 1")
    
    model_config = {"frozen": True}
    
    @field_validator("value")
    @classmethod
    def validate_probability(cls, v: float) -> float:
        """Ensure probability is in valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Probability must be between 0 and 1, got {v}")
        return v
    
    def as_percentage(self) -> float:
        """Return probability as percentage (0-100)."""
        return self.value * 100
    
    def __str__(self) -> str:
        return f"{self.as_percentage():.2f}%"
    
    def __float__(self) -> float:
        return self.value
    
    @classmethod
    def from_percentage(cls, percentage: float) -> "Probability":
        """Create from percentage value (0-100)."""
        return cls(value=percentage / 100)
    
    @classmethod
    def zero(cls) -> "Probability":
        """Return probability of 0."""
        return cls(value=0.0)
    
    @classmethod
    def certain(cls) -> "Probability":
        """Return probability of 1."""
        return cls(value=1.0)
