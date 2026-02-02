"""Console output presenter."""

from typing import Any
from src.application.dto import StateInfoDTO, SimulationResultDTO, ProbabilityTableRowDTO


class ConsolePresenter:
    """
    Console-based output presenter.
    
    Implements OutputPort protocol.
    """
    
    def show_message(self, message: str) -> None:
        """Display a message."""
        print(message)
    
    def show_error(self, error: str) -> None:
        """Display an error message."""
        print(f"❌ Error: {error}")
    
    def show_data(self, data: dict[str, Any]) -> None:
        """Display structured data."""
        for key, value in data.items():
            print(f"{key}: {value}")
    
    def show_table(self, headers: list[str], rows: list[list[Any]]) -> None:
        """Display a simple table."""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print headers
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print("\n" + header_line)
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            print(row_line)
    
    def show_state_info(self, info: StateInfoDTO) -> None:
        """Display formatted state information."""
        print("\n" + "=" * 60)
        print("  YOUR CURRENT STATE")
        print("=" * 60)
        
        print(f"\n--- CURRENT COUNTERS ---")
        print(f"  Pity (P):          {info.current_pity}/80")
        print(f"  Banner Pulls (S):  {info.banner_counter}/120")
        print(f"  Spark Dupe (D):    {info.dupe_counter}/240")
        print(f"  5★ Guarantee:      {info.pulls_without_5_star}/10")
        
        print(f"\n--- PULLS TO NEXT MILESTONE ---")
        print(f"  To 5★ Guarantee:   {info.pulls_to_5_star} pulls")
        print(f"  To Soft Pity:      {info.pulls_to_soft_pity} pulls")
        print(f"  To Hard Pity:      {info.pulls_to_hard_pity} pulls")
        print(f"  To Featured:       {info.pulls_to_featured} pulls")
        print(f"  To Bonus Dupe:     {info.pulls_to_bonus_dupe} pulls")
        print(f"  To Free 10-pull:   {info.pulls_to_free_pull} pulls")
        
        print(f"\n--- STATUS ---")
        if info.at_hard_pity:
            print("  ⚡ HARD PITY ACTIVE - Next 6★ GUARANTEED (50/50)")
        elif info.in_soft_pity:
            print("  🔥 SOFT PITY ACTIVE - Increased rates")
        else:
            print("  📊 Base rates active")
        
        if info.at_featured_guarantee:
            print("  ⭐ FEATURED GUARANTEE - Next 6★ is featured 100%")
    
    def show_simulation_result(self, result: SimulationResultDTO) -> None:
        """Display simulation result."""
        print("\n" + "=" * 60)
        print("  SIMULATION RESULT")
        print("=" * 60)
        print(f"\n{result.message}")
        print(f"\nNew pity: {result.new_pity}")
        print(f"Banner pulls: {result.banner_pulls}")
    
    def show_base_rates(self, rates_info: dict) -> None:
        """Display base rates and pity system information."""
        print("\n" + "=" * 60)
        print("  GACHA SYSTEM - ARKNIGHTS: ENDFIELD")
        print("=" * 60)
        
        base = rates_info["base_rates"]
        print("\n--- BASE RATES ---")
        print(f"  6★: {base['6_star']}%")
        print(f"  5★: {base['5_star']}%")
        print(f"  4★: {base['4_star']}%")
        
        pity = rates_info["pity_system"]
        print("\n--- PITY SYSTEM ---")
        print(f"  • 5★ Guarantee: Every {pity['5_star_guarantee']} pulls (50% featured)")
        print(f"  • Soft Pity: Pull {pity['soft_pity_start']}+ → +{pity['soft_pity_increment']:.0f}% per pull")
        print(f"  • Hard Pity: Pull {pity['hard_pity']} → 6★ guaranteed (50/50)")
        print(f"  • Featured Guarantee: Pull {pity['featured_guarantee']} → Featured 100%")
        print(f"  • Bonus Dupe: Pull {pity['bonus_dupe']} → Extra copy (repeats)")
        
        special = rates_info["special_rules"]
        print("\n--- SPECIAL RULES ---")
        print("  • When losing 50/50:")
        print(f"    - {special['prob_prev_limited']:.2f}% for each previous limited (x2)")
        print(f"    - {special['prob_standard']:.2f}% for standard 6★")
        print("  • ⚠ NO featured guarantee after losing 50/50 until pull 120")
        print(f"  • After {special['free_pull_reward']} pulls: Free 10-pull (next banner)")
        
        print("\n--- CARRY OVER ---")
        print("  ✓ 6★ Pity (soft/hard): Carries over between banners")
        print("  ✓ 5★ Guarantee: Carries over between banners")
        print("  ✓ Bonus Dupe: Carries over between banners")
        print("  ✗ Featured Guarantee (120): Does NOT carry over")
    
    def show_probability_table(self, rows: list[ProbabilityTableRowDTO], title: str = "PROBABILITY TABLE") -> None:
        """Display probability table with formatting."""
        print("\n" + "=" * 95)
        print(f"  {title}")
        print("=" * 95)
        print("\n  Pull   | Pity |  Prob. 6★  |  Cumulative Prob.")
        print("  " + "-" * 85)
        
        for row in rows:
            marker = ""
            if row.pull_number == 65:
                marker = " <- Soft Pity Start"
            elif row.pull_number == 80:
                marker = " <- Hard Pity (GUARANTEED)"
            
            if row.cumulative >= 0.999 and row.pull_number < 80:
                print(f"    {row.pull_number:3d}  |  {row.pity:2d}  |    {row.probability * 100:5.1f}%   |     {row.cumulative * 100:6.3f}%{marker}")
            else:
                print(f"    {row.pull_number:3d}  |  {row.pity:2d}  |    {row.probability * 100:5.1f}%   |      {row.cumulative * 100:5.1f}%{marker}")
