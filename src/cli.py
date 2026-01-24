"""
Command-line interface menu and options.
"""

from .constants import (
    PROB_6_STAR_BASE,
    PROB_5_STAR,
    PROB_4_STAR,
    PROB_PREV_LIMITED,
    FIVE_STAR_GUARANTEE,
    SOFT_PITY_START,
    SOFT_PITY_INCREMENT,
    HARD_PITY,
    FEATURED_GUARANTEE,
    BONUS_DUPE,
    FREE_PULL_REWARD
)
from .probability import calculate_6_star_probability, calculate_pulls_for_5_star
from .state import calculate_expected_pulls, simulate_50_50
from .display import show_soft_pity_table, show_featured_table, show_featured_graph


def show_menu():
    """Shows the main menu"""
    print("\n" + "=" * 60)
    print("  PITY CALCULATOR - ARKNIGHTS: ENDFIELD")
    print("=" * 60)
    print("1. View rates and pity system")
    print("2. Calculate current state")
    print("3. Calculate 6★ probability for upcoming pulls")
    print("4. Simulate 50/50 result")
    print("5. Calculate pulls for featured guarantee")
    print("6. View soft pity table")
    print("7. View featured 6★ probability table")
    print("8. View featured probability graph")
    print("9. Exit")
    print("=" * 60)


def option_base_rates():
    """Shows base rates and pity system"""
    print("\n" + "=" * 60)
    print("  GACHA SYSTEM - ARKNIGHTS: ENDFIELD")
    print("=" * 60)

    print("\n--- BASE RATES ---")
    print(f"  6★: {PROB_6_STAR_BASE * 100}%")
    print(f"  5★: {PROB_5_STAR * 100}%")
    print(f"  4★: {PROB_4_STAR * 100}%")

    print("\n--- PITY SYSTEM ---")
    print(f"  • 5★ Guarantee: Every {FIVE_STAR_GUARANTEE} pulls (50% featured)")
    print(f"  • Soft Pity: Pull {SOFT_PITY_START}+ → +{SOFT_PITY_INCREMENT*100:.0f}% per pull")
    print(f"  • Hard Pity: Pull {HARD_PITY} → 6★ guaranteed (50/50)")
    print(f"  • Featured Guarantee: Pull {FEATURED_GUARANTEE} → Featured 100%")
    print(f"  • Bonus Dupe: Pull {BONUS_DUPE} → Extra copy (repeats)")

    print("\n--- SPECIAL RULES ---")
    print("  • When losing 50/50:")
    print(f"    - {PROB_PREV_LIMITED*100:.2f}% for each previous limited (x2)")
    print(f"    - {(1-PROB_PREV_LIMITED*2)*100:.2f}% for standard 6★")
    print("  • ⚠ NO featured guarantee after losing 50/50 until pull 120")
    print(f"  • After {FREE_PULL_REWARD} pulls: Free 10-pull (next banner)")

    print("\n--- CARRY OVER ---")
    print("  ✓ 6★ Pity (soft/hard): Carries over between banners")
    print("  ✓ 5★ Guarantee: Carries over between banners")
    print("  ✓ Bonus Dupe: Carries over between banners")
    print("  ✗ Featured Guarantee (120): Does NOT carry over")


def option_current_state():
    """Calculates and shows current counter state"""
    try:
        print("\n--- ENTER YOUR CURRENT STATE ---")
        pulls_without_6 = int(input("How many pulls without 6★? "))
        banner_pulls = int(input("How many pulls on this banner? "))
        total_pulls = int(input("How many total pulls (for Spark Dupe)? "))
        pulls_without_5 = int(input("How many pulls without 5★? (0-9): "))

        state = calculate_expected_pulls(pulls_without_6, banner_pulls, total_pulls)
        current_prob = calculate_6_star_probability(pulls_without_6)

        print("\n" + "=" * 50)
        print("  YOUR CURRENT STATE")
        print("=" * 50)

        # 6★ Pity
        print(f"\n📊 6★ PITY: {pulls_without_6}/{HARD_PITY}")
        if state['in_soft_pity']:
            print(f"   ⚡ You're in SOFT PITY!")
            print(f"   Current probability: {current_prob * 100:.1f}%")
        else:
            print(f"   Pulls to soft pity: {state['pulls_to_soft_pity']}")
        print(f"   Pulls to hard pity: {state['pulls_to_hard_pity']}")

        # Featured guarantee
        print(f"\n🎯 BANNER (Featured Guarantee): {banner_pulls}/{FEATURED_GUARANTEE}")
        print(f"   Pulls to featured guarantee: {state['pulls_to_featured']}")

        # Spark Dupe counter
        print(f"\n💎 SPARK DUPE: D(r) = {state['dupe_counter']}/{BONUS_DUPE}")
        print(f"   Total accumulated pulls: {total_pulls}")
        print(f"   Pulls to bonus dupe: {state['pulls_to_bonus_dupe']}")

        # 5★ guarantee
        pulls_to_5 = calculate_pulls_for_5_star(pulls_without_5)
        print(f"\n⭐ 5★ GUARANTEE: {pulls_without_5 % FIVE_STAR_GUARANTEE}/{FIVE_STAR_GUARANTEE}")
        print(f"   Pulls to 5★: {pulls_to_5}")

        # Free pull reward
        if banner_pulls < FREE_PULL_REWARD:
            print(f"\n🎫 FREE 10-PULL: {banner_pulls}/{FREE_PULL_REWARD}")
            print(f"   Pulls remaining: {state['pulls_to_free_pull']}")
        else:
            print(f"\n🎫 FREE 10-PULL: ✓ Unlocked (for next banner)")

    except ValueError:
        print("Error: Please enter a valid number.")


def option_6_star_probability():
    """Calculates 6★ probability for upcoming pulls"""
    try:
        pulls_without_6 = int(input("\nHow many pulls without 6★? "))
        pulls_to_do = int(input("How many pulls do you plan to do? "))

        print("\n" + "=" * 50)
        print("  6★ PROBABILITY")
        print("=" * 50)

        prob_not_getting = 1.0

        for i in range(pulls_to_do):
            current_pull = pulls_without_6 + i
            pull_prob = calculate_6_star_probability(current_pull)
            prob_not_getting *= (1 - pull_prob)

            if current_pull >= HARD_PITY - 1:
                prob_not_getting = 0
                break

        prob_getting = 1 - prob_not_getting

        print(f"\nFrom pull {pulls_without_6} doing {pulls_to_do} pulls:")
        print(f"  Probability of getting at least one 6★: {prob_getting * 100:.2f}%")

        if pulls_without_6 + pulls_to_do >= HARD_PITY:
            print(f"  ✓ You'll reach hard pity! 6★ guaranteed.")
        elif pulls_without_6 + pulls_to_do >= SOFT_PITY_START:
            print(f"  ⚡ You'll enter soft pity (increased rates)")

        if pulls_without_6 < SOFT_PITY_START <= pulls_without_6 + pulls_to_do:
            print(f"\n  Probability progression:")
            for i in range(max(0, SOFT_PITY_START - pulls_without_6 - 2), min(pulls_to_do, HARD_PITY - pulls_without_6)):
                t = pulls_without_6 + i
                p = calculate_6_star_probability(t)
                if t >= SOFT_PITY_START - 1 or t >= HARD_PITY - 1:
                    print(f"    Pull {t + 1}: {p * 100:.1f}%")

    except ValueError:
        print("Error: Please enter a valid number.")


def option_simulate_50_50():
    """Simulates the 50/50 result"""
    try:
        pulls_without_6 = int(input("\nHow many pulls without 6★? "))
        banner_pulls = int(input("How many pulls on this banner? "))

        if pulls_without_6 < HARD_PITY:
            print(f"\n⚠ You're not at hard pity yet.")
            print(f"  Pulls to hard pity (50/50): {HARD_PITY - pulls_without_6}")
            print(f"  Pulls to featured guarantee: {max(0, FEATURED_GUARANTEE - banner_pulls)}")
            return

        if banner_pulls >= FEATURED_GUARANTEE:
            print(f"\n✓ You have Featured Guarantee!")
            print(f"  You'll get the featured banner character 100%.")
            return

        result = input("Did you win the 50/50? (y/n): ").lower().strip()
        won = result == 'y'

        sim = simulate_50_50(won, pulls_without_6, banner_pulls)

        print(f"\n" + "=" * 50)
        print("  50/50 RESULT")
        print("=" * 50)
        print(f"\n{sim['result']}")
        print(f"\nNew pity: {sim['new_pity']}")
        print(f"Banner pulls: {sim['banner_pulls']}")

        if not won:
            pulls_to_guarantee = FEATURED_GUARANTEE - banner_pulls
            print(f"\n📍 Pulls to featured guarantee: {pulls_to_guarantee}")

    except ValueError:
        print("Error: Please enter a valid number.")


def option_featured_guarantee():
    """Calculates pulls needed to guarantee featured character"""
    try:
        pulls_without_6 = int(input("\nHow many pulls without 6★? "))
        banner_pulls = int(input("How many pulls on this banner? "))

        print("\n" + "=" * 50)
        print("  PATH TO FEATURED GUARANTEE")
        print("=" * 50)

        pulls_to_featured = max(0, FEATURED_GUARANTEE - banner_pulls)
        pulls_to_hard_pity = max(0, HARD_PITY - pulls_without_6)

        print(f"\n📊 Current state:")
        print(f"   6★ Pity: {pulls_without_6}/{HARD_PITY}")
        print(f"   Banner: {banner_pulls}/{FEATURED_GUARANTEE}")

        print(f"\n🎲 SCENARIO: Win 50/50 at Hard Pity")
        print(f"   Pulls needed: {pulls_to_hard_pity}")
        print(f"   Probability: 50%")

        print(f"\n💎 SCENARIO: Featured Guarantee (worst case)")
        print(f"   Pulls needed: {pulls_to_featured}")
        print(f"   Probability: 100% (guaranteed)")

        expected_pulls = 0.5 * pulls_to_hard_pity + 0.5 * pulls_to_featured
        print(f"\n📈 EXPECTED VALUE:")
        print(f"   Average pulls: ~{expected_pulls:.0f}")

        pulls_to_bonus = max(0, BONUS_DUPE - banner_pulls)
        if pulls_to_bonus > 0:
            print(f"\n🎁 BONUS DUPE (extra copy):")
            print(f"   Pulls needed: {pulls_to_bonus}")

    except ValueError:
        print("Error: Please enter a valid number.")


def option_soft_pity_table():
    """Shows soft pity table with user-specified number of pulls"""
    try:
        print("\n--- SOFT PITY TABLE OPTIONS ---")
        max_pulls = int(input(f"How many pulls to show? (1-{HARD_PITY}, default {HARD_PITY}): ") or HARD_PITY)
        show_soft_pity_table(max_pulls)
    except ValueError:
        print("Error: Please enter a valid number.")


def option_featured_table():
    """Shows featured probability table with user-specified number of pulls"""
    try:
        print("\n--- FEATURED 6★ PROBABILITY TABLE OPTIONS ---")
        print(f"Phase 1: Pulls 1-{HARD_PITY} (path to hard pity)")
        print(f"Phase 2: Pulls {HARD_PITY + 1}-{FEATURED_GUARANTEE} (after losing 50/50)")

        phase1_pulls = int(input(f"\nHow many pulls to show in Phase 1? (1-{HARD_PITY}, default {HARD_PITY}): ") or HARD_PITY)
        phase2_pulls = int(input(f"How many pulls to show in Phase 2? (0-{FEATURED_GUARANTEE - HARD_PITY}, default {FEATURED_GUARANTEE - HARD_PITY}): ") or (FEATURED_GUARANTEE - HARD_PITY))

        show_featured_table(phase1_pulls, phase2_pulls)
    except ValueError:
        print("Error: Please enter a valid number.")


def option_featured_graph():
    """Shows featured probability graph"""
    show_featured_graph()

