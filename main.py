"""
Pity System Probability Calculator - Arknights: Endfield
=========================================================
A command-line tool to calculate probabilities and track pity counters
for the gacha system in Arknights: Endfield.

Usage:
    python main.py

For more information, see README.md
"""

from src.cli import (
    show_menu,
    option_base_rates,
    option_current_state,
    option_6_star_probability,
    option_simulate_50_50,
    option_featured_guarantee,
    option_soft_pity_table,
    option_featured_table,
    option_featured_graph
)


def main():
    """Main function"""
    print("\nWelcome to the Arknights: Endfield Pity Calculator!")

    while True:
        show_menu()
        option = input("\nSelect an option: ").strip()

        if option == "1":
            option_base_rates()
        elif option == "2":
            option_current_state()
        elif option == "3":
            option_6_star_probability()
        elif option == "4":
            option_simulate_50_50()
        elif option == "5":
            option_featured_guarantee()
        elif option == "6":
            option_soft_pity_table()
        elif option == "7":
            option_featured_table()
        elif option == "8":
            option_featured_graph()
        elif option == "9":
            print("\nGoodbye! Good luck on your pulls.")
            break
        else:
            print("\nInvalid option. Please try again.")


if __name__ == '__main__':
    main()
