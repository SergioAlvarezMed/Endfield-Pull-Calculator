"""
Pity System Probability Calculator - Arknights: Endfield
=========================================================
A command-line tool to calculate probabilities and track pity counters
for the gacha system in Arknights: Endfield.

Refactored with Domain-Driven Design architecture:
- Domain layer: Business logic, entities, value objects
- Application layer: Use cases, ports
- Infrastructure layer: CLI, persistence, presentation

Usage:
    python main.py

For more information, see README.md and docs/ARCHITECTURE.md
"""

from src.domain.value_objects import GameRules
from src.domain.services import ProbabilityCalculator, CounterCalculator, PitySimulator
from src.application.use_cases import (
    CalculateStateUseCase,
    SimulatePullUseCase,
    ShowProbabilityTableUseCase,
    ShowBaseRatesUseCase,
)
from src.infrastructure.persistence.json_repository import JsonStateRepository
from src.infrastructure.persistence.random_adapter import StandardRandomGenerator
from src.infrastructure.presentation.console_presenter import ConsolePresenter
from src.infrastructure.cli.console_input import ConsoleInput
from src.infrastructure.cli.menu import PityCalculatorMenu


def main():
    """
    Main entry point - Dependency Injection Container.
    
    This function manually constructs the dependency graph:
    1. Create value objects and configurations
    2. Create infrastructure adapters (repository, random, I/O)
    3. Create domain services
    4. Create application use cases
    5. Create CLI menu and run
    """
    # 1. Configuration
    rules = GameRules.default()
    
    # 2. Infrastructure adapters
    repository = JsonStateRepository()
    random_gen = StandardRandomGenerator()
    presenter = ConsolePresenter()
    input_adapter = ConsoleInput()
    
    # 3. Domain services
    prob_calculator = ProbabilityCalculator(rules)
    counter_calculator = CounterCalculator(rules)
    simulator = PitySimulator(rules, random_gen)
    
    # 4. Application use cases
    calculate_state_uc = CalculateStateUseCase(prob_calculator, counter_calculator, rules)
    simulate_pull_uc = SimulatePullUseCase(simulator, repository, rules)
    show_prob_table_uc = ShowProbabilityTableUseCase(prob_calculator, counter_calculator, rules)
    show_base_rates_uc = ShowBaseRatesUseCase(rules)
    
    # 5. CLI Menu
    menu = PityCalculatorMenu(
        calculate_state_uc,
        simulate_pull_uc,
        show_prob_table_uc,
        show_base_rates_uc,
        repository,
        presenter,
        input_adapter,
    )
    
    # Run the application
    menu.run()


if __name__ == '__main__':
    main()
