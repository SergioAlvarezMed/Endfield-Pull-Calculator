"""
Counter functions for tracking pity, spark, and dupe progress.
"""

from .constants import HARD_PITY, FEATURED_GUARANTEE, BONUS_DUPE


def pity_counter(r: int) -> int:
    """P(r) = min(r, 80) - Current pity counter"""
    return min(r, HARD_PITY)


def spark_counter(r: int) -> int:
    """S(r) = min(r, 120) - Featured guarantee counter"""
    return min(r, FEATURED_GUARANTEE)


def dupe_counter(r: int) -> int:
    """D(r) = min(r, 240) - Spark Dupe counter"""
    return min(r, BONUS_DUPE)


def pity_reset(r: int) -> int:
    """PR(r) = max(0, r-80) - Pity reset when winning 50/50 with active spark"""
    return max(0, r - HARD_PITY)

