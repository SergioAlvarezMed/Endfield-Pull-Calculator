"""
State management and simulation functions.
"""

import random

from .constants import (
    HARD_PITY,
    FEATURED_GUARANTEE,
    SOFT_PITY_START,
    FREE_PULL_REWARD,
    BONUS_DUPE,
    PROB_PREV_LIMITED
)
from .counters import pity_counter, spark_counter, dupe_counter


def is_in_50_50(pity: int, banner_pulls: int) -> tuple[bool, str]:
    """
    Checks if the player is in a 50/50 event.
    Returns (is_in_50_50, reason)
    """
    if pity >= HARD_PITY:
        return True, "Hard Pity reached (80 pulls)"
    return False, ""


def is_in_featured_guarantee(banner_pulls: int) -> tuple[bool, str]:
    """
    Checks if the player has the featured guarantee.
    Returns (has_guarantee, reason)
    """
    if banner_pulls >= FEATURED_GUARANTEE:
        return True, "Featured Guarantee reached (120 pulls)"
    return False, ""


def calculate_expected_pulls(pulls_without_6_star: int, banner_pulls: int, total_pulls: int = None) -> dict:
    """
    Calculates expected pull statistics from the current position.
    total_pulls: accumulated pulls for Spark Dupe counter (carries over between banners)
    """
    if total_pulls is None:
        total_pulls = banner_pulls  # Default to banner pulls

    return {
        "pulls_without_6_star": pulls_without_6_star,
        "banner_pulls": banner_pulls,
        "total_pulls": total_pulls,
        "current_pity": pity_counter(pulls_without_6_star),
        "banner_counter": spark_counter(banner_pulls),
        "dupe_counter": dupe_counter(total_pulls),
        "pulls_to_soft_pity": max(0, SOFT_PITY_START - pulls_without_6_star),
        "pulls_to_hard_pity": max(0, HARD_PITY - pulls_without_6_star),
        "pulls_to_featured": max(0, FEATURED_GUARANTEE - banner_pulls),
        "pulls_to_bonus_dupe": max(0, BONUS_DUPE - total_pulls),
        "pulls_to_free_pull": max(0, FREE_PULL_REWARD - banner_pulls),
        "in_soft_pity": pulls_without_6_star >= SOFT_PITY_START
    }


def simulate_50_50(win: bool, current_pity: int, banner_pulls: int) -> dict:
    """
    Simulates the 50/50 result and calculates new counters.

    The 50/50 triggers when:
    - Hard Pity (pity = 80): Guarantees a 6★, 50% chance of being the banner character

    If WIN the 50/50:
        - Gets the featured banner character
        - Pity resets to 0
        - Banner counter continues

    If LOSE the 50/50:
        - Gets an off-banner 6★
        - 28.56% total chance of getting a previous limited (14.28% each)
        - Pity resets to 0
        - Banner counter continues (until 120 for featured guarantee)
    """
    if win:
        new_pity = 0
        message = "You won the 50/50! You got the featured banner character."
        result_detail = "featured"
    else:
        new_pity = 0
        # Determine which character was obtained
        roll = random.random()
        if roll < PROB_PREV_LIMITED:
            message = "You lost the 50/50. You got the 1st previous limited."
            result_detail = "prev_limited_1"
        elif roll < PROB_PREV_LIMITED * 2:
            message = "You lost the 50/50. You got the 2nd previous limited."
            result_detail = "prev_limited_2"
        else:
            message = "You lost the 50/50. You got a standard 6★."
            result_detail = "standard"

        message += f"\n  ⚠ NO featured guarantee until pull 120."

    return {
        "result": message,
        "won": win,
        "new_pity": new_pity,
        "banner_pulls": banner_pulls,  # Does not reset
        "result_detail": result_detail
    }

