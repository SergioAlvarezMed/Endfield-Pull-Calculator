"""Pull result entity."""

from enum import Enum
from pydantic import BaseModel, Field


class CharacterType(str, Enum):
    """Type of character obtained from a pull."""
    FEATURED = "featured"
    PREV_LIMITED_1 = "prev_limited_1"
    PREV_LIMITED_2 = "prev_limited_2"
    STANDARD = "standard"
    FIVE_STAR = "five_star"
    FOUR_STAR = "four_star"


class PullResult(BaseModel):
    """
    Represents the result of a single pull.
    
    This is an entity representing a gacha pull event.
    """
    rarity: int = Field(ge=4, le=6, description="Character rarity (4, 5, or 6 stars)")
    character_type: CharacterType = Field(description="Type of character obtained")
    won_50_50: bool | None = Field(default=None, description="Whether won 50/50 (None if not applicable)")
    
    model_config = {"frozen": True}
    
    def is_six_star(self) -> bool:
        """Check if this is a 6★ pull."""
        return self.rarity == 6
    
    def is_five_star(self) -> bool:
        """Check if this is a 5★ pull."""
        return self.rarity == 5
    
    def is_featured(self) -> bool:
        """Check if this is the featured character."""
        return self.character_type == CharacterType.FEATURED
    
    def __str__(self) -> str:
        stars = "★" * self.rarity
        type_str = self.character_type.value.replace("_", " ").title()
        result = f"{self.rarity}{stars} - {type_str}"
        if self.won_50_50 is not None:
            result += f" ({'Won' if self.won_50_50 else 'Lost'} 50/50)"
        return result
