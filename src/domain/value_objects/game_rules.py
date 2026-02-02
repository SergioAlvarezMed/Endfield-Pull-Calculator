"""Game rules configuration value object."""

from pydantic import BaseModel, Field


class GameRules(BaseModel):
    """
    Immutable game rules configuration for Arknights: Endfield pity system.
    
    This encapsulates all the constants that define the game mechanics.
    """
    # Base probabilities
    prob_6_star_base: float = Field(default=0.008, description="Base 6★ probability (0.8%)")
    prob_5_star: float = Field(default=0.08, description="5★ probability (8%)")
    prob_4_star: float = Field(default=0.912, description="4★ probability (91.2%)")
    prob_50_50: float = Field(default=0.5, description="50/50 probability")
    prob_prev_limited: float = Field(default=0.1428, description="Previous limited probability (14.28%)")
    
    # Pity thresholds
    five_star_guarantee: int = Field(default=10, description="5★ guarantee every N pulls")
    soft_pity_start: int = Field(default=65, description="Soft pity starts at pull N")
    soft_pity_increment: float = Field(default=0.05, description="Soft pity increment per pull (+5%)")
    hard_pity: int = Field(default=80, description="Hard pity at pull N (guaranteed 6★)")
    featured_guarantee: int = Field(default=120, description="Featured guarantee at pull N")
    bonus_dupe: int = Field(default=240, description="Bonus dupe at pull N")
    free_pull_reward: int = Field(default=60, description="Free 10-pull reward at pull N")
    
    model_config = {"frozen": True}
    
    @classmethod
    def default(cls) -> "GameRules":
        """Get default game rules."""
        return cls()
