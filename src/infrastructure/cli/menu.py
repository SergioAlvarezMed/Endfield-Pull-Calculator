"""CLI Menu for the pity calculator."""

from __future__ import annotations

from src.domain.entities import PityState
from src.application.use_cases import (
    CalculateStateUseCase,
    SimulatePullUseCase,
    ShowProbabilityTableUseCase,
    ShowBaseRatesUseCase,
)
from src.infrastructure.presentation.console_presenter import ConsolePresenter
from src.infrastructure.cli.console_input import ConsoleInput
from src.application.ports import StateRepository


class PityCalculatorMenu:
    """
    Main CLI menu for the pity calculator.
    
    Orchestrates use cases and user interaction.
    """
    
    def __init__(
        self,
        calculate_state_uc: CalculateStateUseCase,
        simulate_pull_uc: SimulatePullUseCase,
        show_prob_table_uc: ShowProbabilityTableUseCase,
        show_base_rates_uc: ShowBaseRatesUseCase,
        repository: StateRepository,
        presenter: ConsolePresenter,
        input_adapter: ConsoleInput,
    ):
        """Initialize menu with use cases and adapters."""
        self.calculate_state_uc = calculate_state_uc
        self.simulate_pull_uc = simulate_pull_uc
        self.show_prob_table_uc = show_prob_table_uc
        self.show_base_rates_uc = show_base_rates_uc
        self.repository = repository
        self.presenter = presenter
        self.input_adapter = input_adapter
        self.current_state: PityState | None = None
    
    def show_menu(self) -> None:
        """Display the main menu."""
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
        print("8. Load/Save state")
        print("9. Exit")
        print("=" * 60)
    
    def run(self) -> None:
        """Run the main menu loop."""
        self.presenter.show_message("\nWelcome to the Arknights: Endfield Pity Calculator!")
        
        # Try to load saved state
        saved_state = self.repository.load()
        if saved_state:
            self.current_state = saved_state
            self.presenter.show_message("✓ Loaded saved state from previous session")
        
        while True:
            self.show_menu()
            choice = input("\nChoose an option (1-9): ").strip()
            
            try:
                if choice == "1":
                    self.option_base_rates()
                elif choice == "2":
                    self.option_current_state()
                elif choice == "3":
                    self.option_6_star_probability()
                elif choice == "4":
                    self.option_simulate_50_50()
                elif choice == "5":
                    self.option_featured_guarantee()
                elif choice == "6":
                    self.option_soft_pity_table()
                elif choice == "7":
                    self.option_featured_table()
                elif choice == "8":
                    self.option_load_save()
                elif choice == "9":
                    self.presenter.show_message("\nThank you for using the Pity Calculator!")
                    break
                else:
                    self.presenter.show_error("Invalid option. Please choose 1-9.")
            except Exception as e:
                self.presenter.show_error(f"An error occurred: {e}")
    
    def option_base_rates(self) -> None:
        """Show base rates and pity system."""
        rates_info = self.show_base_rates_uc.execute()
        self.presenter.show_base_rates(rates_info)
    
    def option_current_state(self) -> None:
        """Calculate and show current state."""
        print("\n--- ENTER YOUR CURRENT STATE ---")
        
        pulls_without_6 = self.input_adapter.get_integer(
            "How many pulls without 6★? ",
            min_val=0,
            max_val=80
        )
        banner_pulls = self.input_adapter.get_integer(
            "How many pulls on this banner? ",
            min_val=0
        )
        total_pulls = self.input_adapter.get_integer(
            "How many total pulls (for Spark Dupe)? ",
            min_val=banner_pulls
        )
        pulls_without_5 = self.input_adapter.get_integer(
            "How many pulls without 5★? (0-10): ",
            min_val=0,
            max_val=10
        )
        
        # Create state
        self.current_state = PityState(
            pulls_without_6_star=pulls_without_6,
            pulls_without_5_star=pulls_without_5,
            banner_pulls=banner_pulls,
            total_pulls=total_pulls
        )
        
        # Calculate and show info
        info = self.calculate_state_uc.execute(self.current_state)
        self.presenter.show_state_info(info)
        
        # Auto-save
        self.repository.save(self.current_state)
        self.presenter.show_message("\n✓ State auto-saved")
    
    def option_6_star_probability(self) -> None:
        """Calculate 6★ probability for upcoming pulls."""
        if self.current_state is None:
            self.presenter.show_error("Please calculate your current state first (option 2)")
            return
        
        num_pulls = self.input_adapter.get_integer(
            "\nHow many upcoming pulls to calculate? ",
            min_val=1,
            max_val=80
        )
        
        rows = self.show_prob_table_uc.execute(num_pulls)
        # Show only from current position
        relevant_rows = [r for r in rows if r.pull_number > self.current_state.pulls_without_6_star]
        
        if relevant_rows:
            self.presenter.show_probability_table(
                relevant_rows[:num_pulls],
                "UPCOMING PULLS PROBABILITY"
            )
        else:
            self.presenter.show_message("\nYou are already at or past the specified pulls.")
    
    def option_simulate_50_50(self) -> None:
        """Simulate 50/50 result."""
        if self.current_state is None:
            self.presenter.show_error("Please calculate your current state first (option 2)")
            return
        
        if not self.current_state.is_at_hard_pity():
            self.presenter.show_error("You are not at hard pity (80 pulls). 50/50 only triggers at pull 80.")
            return
        
        won = self.input_adapter.get_boolean("\nDid you win the 50/50? (y/n): ")
        
        result = self.simulate_pull_uc.execute(self.current_state, won)
        self.presenter.show_simulation_result(result)
        
        # Update current state
        self.current_state = self.repository.load()
    
    def option_featured_guarantee(self) -> None:
        """Calculate pulls for featured guarantee."""
        if self.current_state is None:
            self.presenter.show_error("Please calculate your current state first (option 2)")
            return
        
        info = self.calculate_state_uc.execute(self.current_state)
        
        print("\n" + "=" * 60)
        print("  FEATURED GUARANTEE CALCULATOR")
        print("=" * 60)
        print(f"\nCurrent banner pulls: {info.banner_pulls}")
        print(f"Pulls to featured guarantee: {info.pulls_to_featured}")
        
        if info.at_featured_guarantee:
            print("\n⭐ YOU HAVE FEATURED GUARANTEE!")
            print("   Your next 6★ will be the featured character 100%")
        else:
            print(f"\nYou need {info.pulls_to_featured} more pulls on this banner")
            print("to guarantee the featured character.")
    
    def option_soft_pity_table(self) -> None:
        """Show soft pity table."""
        rows = self.show_prob_table_uc.execute(80)
        self.presenter.show_probability_table(rows, "SOFT PITY TABLE - 6★ PROBABILITY")
    
    def option_featured_table(self) -> None:
        """Show featured 6★ probability table."""
        # Simplified version - show first 120 pulls
        rows = self.show_prob_table_uc.execute(120)
        self.presenter.show_probability_table(rows[:80], "FEATURED 6★ PROBABILITY TABLE (Phase 1)")
    
    def option_load_save(self) -> None:
        """Load or save state."""
        print("\n" + "=" * 60)
        print("  LOAD/SAVE STATE")
        print("=" * 60)
        print("1. Load state")
        print("2. Save current state")
        print("3. Delete saved state")
        print("4. Back")
        
        choice = input("\nChoose an option: ").strip()
        
        if choice == "1":
            state = self.repository.load()
            if state:
                self.current_state = state
                info = self.calculate_state_uc.execute(state)
                self.presenter.show_message("\n✓ State loaded successfully")
                self.presenter.show_state_info(info)
            else:
                self.presenter.show_message("\nNo saved state found.")
        
        elif choice == "2":
            if self.current_state:
                self.repository.save(self.current_state)
                self.presenter.show_message("\n✓ State saved successfully")
            else:
                self.presenter.show_error("No state to save. Calculate your state first (option 2).")
        
        elif choice == "3":
            if self.input_adapter.get_boolean("Are you sure you want to delete saved state? (y/n): "):
                self.repository.delete()
                self.presenter.show_message("\n✓ Saved state deleted")
        
        elif choice == "4":
            return
        else:
            self.presenter.show_error("Invalid option")
