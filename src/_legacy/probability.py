"""
Probability calculation functions.
"""

from .constants import (
    PROB_6_STAR_BASE,
    SOFT_PITY_START,
    SOFT_PITY_INCREMENT,
    HARD_PITY,
    FIVE_STAR_GUARANTEE
)


def calculate_6_star_probability(pulls_without_6_star: int) -> float:
    """
    Calculates the probability of getting a 6★ on the next pull.

    - Base: 0.8%
    - Soft Pity (pull 65+): +5% for each pull after 65
    - Hard Pity (pull 80): 100% guaranteed

    Parameter pulls_without_6_star is 0-indexed:
    - 0 = first pull
    - 79 = pull 80 (hard pity)

    Soft pity formula: P(r) = 0.008 + max(0, r - 64) * 0.05
    """
    # Hard pity: pull 80 (index 79) is 100% guaranteed
    if pulls_without_6_star >= HARD_PITY - 1:
        return 1.0

    # Soft pity: starts at pull 65 (index 64)
    if pulls_without_6_star >= SOFT_PITY_START - 1:
        pulls_in_soft = pulls_without_6_star - (SOFT_PITY_START - 1) + 1
        prob = PROB_6_STAR_BASE + (pulls_in_soft * SOFT_PITY_INCREMENT)
        return min(prob, 1.0)

    return PROB_6_STAR_BASE


def calculate_pulls_for_5_star(pulls_without_5_star: int) -> int:
    """Calculates how many pulls are left for the 5★ guarantee"""
    return FIVE_STAR_GUARANTEE - (pulls_without_5_star % FIVE_STAR_GUARANTEE)


def calculate_average_pull() -> float:
    """Calculates the expected average pull to get a 6★"""
    expected_pull = 0.0
    prob_no_6_previous = 1.0

    for t in range(HARD_PITY):
        pull_prob = calculate_6_star_probability(t)
        # Probability of getting 6★ exactly on this pull
        exact_prob = prob_no_6_previous * pull_prob
        expected_pull += (t + 1) * exact_prob
        prob_no_6_previous *= (1 - pull_prob)

    # If we reach hard pity without 6★
    expected_pull += HARD_PITY * prob_no_6_previous

    return expected_pull

