"""
Display functions for tables and graphs.
"""

from .constants import (
    HARD_PITY,
    FEATURED_GUARANTEE,
    BONUS_DUPE,
    SOFT_PITY_START,
    PROB_50_50
)
from .counters import pity_counter, spark_counter, dupe_counter
from .probability import calculate_6_star_probability, calculate_average_pull


def show_soft_pity_table(max_pulls: int = None):
    """Shows the complete soft pity probability table with all counters"""
    if max_pulls is None:
        max_pulls = HARD_PITY

    max_pulls = min(max(1, max_pulls), HARD_PITY)  # Clamp between 1 and 80

    print("\n" + "=" * 95)
    print("  SOFT PITY TABLE - 6★ PROBABILITY")
    print("=" * 95)
    print("\n  Pull   | P(r) | S(r) | D(r) |  Prob. 6★  |  Cumulative Prob.")
    print("         | Pity | Spark| Dupe |            |")
    print("  " + "-" * 85)

    prob_no_6_cumulative = 1.0

    # Show pulls from 1 to max_pulls
    for pull in range(1, max_pulls + 1):
        pity = pity_counter(pull)
        spark = spark_counter(pull)
        dupe = dupe_counter(pull)

        prob = calculate_6_star_probability(pull - 1)
        prob_no_6_cumulative *= (1 - prob)
        prob_cum = 1 - prob_no_6_cumulative

        marker = ""
        if pull == SOFT_PITY_START:
            marker = " <- Soft Pity Start"
        elif pull == HARD_PITY:
            marker = " <- Hard Pity (GUARANTEED)"

        # Show more decimals for values close to 100%
        if prob_cum >= 0.999 and pull < HARD_PITY:
            print(f"    {pull:3d}  |  {pity:2d}  |  {spark:3d} |  {dupe:3d} |    {prob * 100:5.1f}%   |     {prob_cum * 100:6.3f}%{marker}")
        else:
            print(f"    {pull:3d}  |  {pity:2d}  |  {spark:3d} |  {dupe:3d} |    {prob * 100:5.1f}%   |      {prob_cum * 100:5.1f}%{marker}")

    print(f"\n  📊 Counter Formulas:")
    print(f"     P(r) = min(r, {HARD_PITY}) -> Pity counter")
    print(f"     S(r) = min(r, {FEATURED_GUARANTEE}) -> Spark counter")
    print(f"     D(r) = min(r, {BONUS_DUPE}) -> Dupe counter")
    print(f"\n  📊 Statistics:")
    print(f"     Average pull for 6★: ~{calculate_average_pull():.1f}")
    print(f"\n  ⚠ NOTE: Only pull 80 is 100% GUARANTEED.")
    print(f"     Previous pulls with ~99.9% are very likely,")
    print(f"     but NOT guaranteed.")


def show_featured_table(phase1_pulls: int = None, phase2_pulls: int = None):
    """Shows the cumulative probability table of getting the featured 6★."""
    if phase1_pulls is None:
        phase1_pulls = HARD_PITY
    if phase2_pulls is None:
        phase2_pulls = FEATURED_GUARANTEE - HARD_PITY

    phase1_pulls = min(max(1, phase1_pulls), HARD_PITY)
    phase2_pulls = min(max(0, phase2_pulls), FEATURED_GUARANTEE - HARD_PITY)

    print("\n" + "=" * 100)
    print("  FEATURED 6★ PROBABILITY TABLE")
    print("=" * 100)

    # ==================== PART 1: Pulls 1-80 ====================
    print("\n  +----------------------------------------------------------------------------------------------------+")
    print(f"  |                          PHASE 1: PATH TO HARD PITY (Pulls 1-{phase1_pulls})                                  |")
    print("  +----------------------------------------------------------------------------------------------------+")
    print("\n  Pull   | P(r) | S(r) | D(r) |  Prob. 6★  |  Cumul. 6★ Prob.  |  Featured Prob.")
    print("         | Pity | Spark| Dupe |            |                   |     (50/50)")
    print("  " + "-" * 90)

    prob_no_6_cumulative = 1.0

    for pull in range(1, phase1_pulls + 1):
        pity = pity_counter(pull)
        spark = spark_counter(pull)
        dupe = dupe_counter(pull)

        prob_6_this_pull = calculate_6_star_probability(pull - 1)
        prob_no_6_cumulative *= (1 - prob_6_this_pull)
        prob_6_cumulative = 1 - prob_no_6_cumulative

        marker = ""
        if pull == SOFT_PITY_START:
            marker = " <- Soft Pity"
        elif pull == HARD_PITY:
            marker = " <- Hard Pity (50/50)"

        prob_featured = prob_6_cumulative * PROB_50_50

        if prob_6_cumulative >= 0.999 and pull < HARD_PITY:
            print(f"    {pull:3d}  |  {pity:2d}  |  {spark:3d} |  {dupe:3d} |    {prob_6_this_pull * 100:5.1f}%   |     {prob_6_cumulative * 100:6.3f}%      |     {prob_featured * 100:6.3f}%{marker}")
        else:
            print(f"    {pull:3d}  |  {pity:2d}  |  {spark:3d} |  {dupe:3d} |    {prob_6_this_pull * 100:5.1f}%   |      {prob_6_cumulative * 100:5.1f}%       |      {prob_featured * 100:5.1f}%{marker}")

    print(f"\n  📊 At pull 80:")
    print(f"     • Probability of having pulled 6★: 100% (guaranteed)")
    print(f"     • Probability of being featured: 50% (50/50)")

    # ==================== PART 2: Simulation losing 50/50 ====================
    if phase2_pulls > 0:
        print("\n" + "=" * 100)
        print("  +----------------------------------------------------------------------------------------------------+")
        print("  |                PHASE 2: SIMULATION - YOU LOSE THE 50/50 AT HARD PITY                              |")
        print("  |                      (Pity resets to 0, banner counter continues)                                 |")
        print("  +----------------------------------------------------------------------------------------------------+")
        print("\n  ⚠ ASSUMPTION: You lost the 50/50 at pull 80")
        print("    -> Your pity resets to 0")
        print("    -> Your banner counter (Spark) stays at 80")
        print("    -> Your Dupe counter stays at 80")
        print("    -> You need to reach 120 for featured guarantee\n")

        print("  Pull   | P(r) | S(r) | D(r) |  Prob. 6★  |  Cumul. 6★ Prob.  |  Featured Prob.")
        print("         | Pity | Spark| Dupe |            |                   |")
        print("  " + "-" * 90)

        prob_no_6_post = 1.0
        end_pull = HARD_PITY + phase2_pulls

        for banner_pull in range(HARD_PITY + 1, end_pull + 1):
            current_pity = banner_pull - HARD_PITY
            spark = spark_counter(banner_pull)
            dupe = dupe_counter(banner_pull)

            prob_6_this_pull = calculate_6_star_probability(current_pity - 1)
            prob_no_6_post *= (1 - prob_6_this_pull)
            prob_6_cum_post = 1 - prob_no_6_post

            marker = ""
            if banner_pull == FEATURED_GUARANTEE:
                marker = " <- FEATURED GUARANTEED"
                prob_featured = 1.0
            else:
                prob_featured = prob_6_cum_post * PROB_50_50

            print(f"    {banner_pull:3d}  |  {current_pity:2d}  |  {spark:3d} |  {dupe:3d} |    {prob_6_this_pull * 100:5.1f}%   |      {prob_6_cum_post * 100:5.1f}%       |      {prob_featured * 100:5.1f}%{marker}")

        print(f"\n  📊 Phase 2 Summary (if you lose 50/50):")
        print(f"     • Pulls 81-119: If you pull another 6★, 50% featured")
        print(f"     • Pull 120: Featured GUARANTEED (100%)")
        print(f"     • Worst case: 120 total pulls for featured")

    # ==================== FINAL SUMMARY ====================
    print("\n" + "=" * 100)
    print("  FINAL SUMMARY")
    print("=" * 100)
    print(f"\n  📊 Counter Formulas:")
    print(f"     P(r) = min(r, {HARD_PITY}) -> Pity counter (resets when pulling 6★)")
    print(f"     S(r) = min(r, {FEATURED_GUARANTEE}) -> Spark counter (does NOT reset on banner)")
    print(f"     D(r) = min(r, {BONUS_DUPE}) -> Dupe counter (carries over between banners)")
    print(f"\n  🎯 POSSIBLE SCENARIOS:")
    print(f"     • Best case: Pull featured 6★ before pull 80")
    print(f"     • Normal case: Win 50/50 at pull 80 -> Featured in ~80 pulls")
    print(f"     • Worst case: Lose 50/50 -> Featured guaranteed at pull 120")
    print(f"\n  📈 TOTAL PROBABILITIES:")
    print(f"     • Prob. of featured in <=80 pulls: 50%")
    print(f"     • Prob. of featured in <=120 pulls: 100%")
    print(f"     • Expected average pulls: ~{0.5 * 80 + 0.5 * 120:.0f}")


def show_featured_graph():
    """Shows an ASCII graph of the cumulative probability of getting the featured 6★."""
    print("\n" + "=" * 75)
    print("  GRAPH: PROBABILITY OF GETTING FEATURED 6★")
    print("=" * 75)

    prob_featured_cum = []

    # PHASE 1: Pulls 1-80
    prob_no_6 = 1.0
    for pull in range(1, HARD_PITY + 1):
        prob_6 = calculate_6_star_probability(pull - 1)
        prob_no_6 *= (1 - prob_6)
        prob_6_cum = 1 - prob_no_6
        prob_featured = prob_6_cum * PROB_50_50 * 100
        prob_featured_cum.append(min(prob_featured, 50.0))

    # PHASE 2: Pulls 81-120 (AFTER LOSING 50/50)
    prob_no_6_post = 1.0
    for banner_pull in range(HARD_PITY + 1, FEATURED_GUARANTEE + 1):
        current_pity = banner_pull - HARD_PITY
        prob_6 = calculate_6_star_probability(current_pity - 1)
        prob_no_6_post *= (1 - prob_6)
        prob_6_cum_post = 1 - prob_no_6_post

        if banner_pull == FEATURED_GUARANTEE:
            prob_featured_cum.append(100.0)
        else:
            prob_featured = prob_6_cum_post * PROB_50_50 * 100
            prob_featured_cum.append(prob_featured)

    # Create ASCII graph
    print("\n  Cumulative probability of getting the featured 6★:\n")
    print("  (Assuming you LOSE the 50/50 at pull 80)\n")

    height = 25
    width = 120

    for row in range(height, -1, -1):
        y_value = (row / height) * 100

        if row == height:
            print("  100% |", end="")
        elif row == height // 2:
            print("   50% |", end="")
        elif row == 0:
            print("    0% +", end="")
        else:
            print("       |", end="")

        for col in range(width):
            pull_idx = col
            if pull_idx >= len(prob_featured_cum):
                print(" ", end="")
                continue

            prob = prob_featured_cum[pull_idx]
            real_pull = pull_idx + 1

            row_top = (row / height) * 100
            row_bottom = ((row - 1) / height) * 100 if row > 0 else -5

            if row_bottom < prob <= row_top:
                if real_pull == 120:
                    print("*", end="")
                elif real_pull == 80:
                    print("@", end="")
                elif real_pull == 81:
                    print("!", end="")
                elif real_pull == 65:
                    print("#", end="")
                else:
                    print(".", end="")
            else:
                print(" ", end="")

        print()

    print("       +" + "-" * width)
    print("        1" + " " * 18 + "20" + " " * 18 + "40" + " " * 18 + "60" + " " * 17 + "80" + " " * 17 + "100" + " " * 15 + "120")
    print("  " + " " * 50 + "Pulls")

    print(f"\n  LEGEND:")
    print(f"    . = Probability curve")
    print(f"    # = Soft Pity start (pull 65)")
    print(f"    @ = Hard Pity (pull 80) - 50/50 point")
    print(f"    ! = Pity reset (pull 81) - after losing 50/50")
    print(f"    * = Featured GUARANTEED (pull 120)")

    print(f"\n  📍 KEY POINTS:")
    print(f"     • Pull 1: {prob_featured_cum[0]:.1f}%")
    print(f"     • Pull 50: {prob_featured_cum[49]:.1f}%")
    print(f"     • Pull 65 (Soft Pity): {prob_featured_cum[64]:.1f}%")
    print(f"     • Pull 80 (Hard Pity): {prob_featured_cum[79]:.1f}% <- 50/50 here")
    print(f"     • Pull 81 (After losing): {prob_featured_cum[80]:.1f}% <- Pity resets!")
    print(f"     • Pull 100: {prob_featured_cum[99]:.1f}%")
    print(f"     • Pull 120 (Guaranteed): {prob_featured_cum[119]:.1f}%")

    print(f"\n  📊 INTERPRETATION:")
    print(f"     • Pulls 1-80: Probability rises to 50% (6★ guaranteed, but 50/50)")
    print(f"     • Pull 81: Probability DROPS (pity resets after losing 50/50)")
    print(f"     • Pulls 81-119: Probability builds up again from ~0%")
    print(f"     • Pull 120: 100% guaranteed featured")

