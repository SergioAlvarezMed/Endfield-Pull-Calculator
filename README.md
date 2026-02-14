# Arknights: Endfield Pity Calculator

A command-line probability calculator and pity tracking system for the gacha mechanics in **Arknights: Endfield**. Built with Python 3.13+ using Clean Architecture and Domain-Driven Design.

---

## Table of Contents

- [Features](#features)
- [Gacha System Overview](#gacha-system-overview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Architecture](#project-architecture)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| Feature | Description |
|---------|-------------|
| **View Base Rates** | Display 6★/5★/4★ pull rates and full pity system explanation |
| **Calculate Pity State** | Input your current counters and get a complete status report with all milestones |
| **6★ Probability Calculator** | Cumulative probability for N upcoming pulls with soft pity factored in |
| **50/50 Simulator** | Simulate winning or losing the 50/50 with off-banner character breakdown |
| **Featured Guarantee Tracker** | Calculate remaining pulls until the 120-pull featured guarantee |
| **Soft Pity Table** | Full probability table (pulls 1-80) with individual and cumulative odds |
| **Featured 6★ Table** | Phase 1 & Phase 2 rate breakdown for featured characters |
| **Persistent State** | Auto-save your pity progress between sessions with backup protection |

---

## Gacha System Overview

### Base Rates

| Rarity | Rate |
|--------|------|
| 6★ | 0.8% |
| 5★ | 8.0% |
| 4★ | 91.2% |

### Pity Mechanics

| Mechanic | Pulls | Description | Carries Over? |
|----------|-------|-------------|:-------------:|
| 5★ Guarantee | 10 | Guaranteed 5★ (50% featured) | Yes |
| Soft Pity | 65+ | +5% per pull after 65 | Yes |
| Hard Pity (50/50) | 80 | Guaranteed 6★ (50% featured) | Yes |
| Featured Guarantee | 120 | 100% featured character | No |
| Bonus Dupe | 240 | Extra copy of featured (repeats every 240) | Yes |
| Free 10-Pull | 60 | Reward for next banner (expires if unused) | No |

### Counter Formulas

```
P(r) = min(r, 80)   -- Pity counter (resets when pulling a 6★)
S(r) = min(r, 120)  -- Spark counter (does NOT carry over between banners)
D(r) = min(r, 240)  -- Dupe counter (carries over between banners)
```

### 50/50 Loss Breakdown

When you lose the 50/50, the off-banner character is selected as follows:

- **14.28%** — Previous limited character #1
- **14.28%** — Previous limited character #2
- **71.44%** — Standard pool 6★

> **Note:** After losing the 50/50, you do NOT get a featured guarantee until pull 120. Also, after 60 pulls on a banner you receive a free 10-pull ticket for the **next** banner (expires if not used on that banner).

---

## Getting Started

### Prerequisites

- **Python 3.13** or higher
- **pip** (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/SergioAlvarezMed/Endfield-Pull-Calculator.git
cd Endfield-Pull-Calculator

# Install dependencies
make install
```

Or install manually:

```bash
pip install -e .
```

### Quick Start

```bash
python main.py
```

On Windows you can also double-click `pity_calculator.bat`.

---

## Usage

When you launch the application you will see the main menu:

```
============================================================
  PITY CALCULATOR - ARKNIGHTS: ENDFIELD
============================================================
1. View rates and pity system
2. Calculate current state
3. Calculate 6★ probability for upcoming pulls
4. Simulate 50/50 result
5. Calculate pulls for featured guarantee
6. View soft pity table
7. View featured 6★ probability table
8. Load/Save state
9. Exit
============================================================
```

### Example: Soft Pity Table

Option **6** displays a full probability table showing how soft pity ramps up your chances:

```
  Pull  | P(r) | S(r) | D(r) |  Prob. 6★  |  Cumulative Prob.
        | Pity | Spark| Dupe |            |
  -------------------------------------------------------------------------
     1  |   1  |    1 |    1 |      0.8%  |        0.8%
    ...
    64  |  64  |   64 |   64 |      0.8%  |       40.4%
    65  |  65  |   65 |   65 |      5.8%  |       43.7%  <- Soft Pity Start
    66  |  66  |   66 |   66 |     10.8%  |       49.7%
    67  |  67  |   67 |   67 |     15.8%  |       57.6%
    ...
    80  |  80  |   80 |   80 |    100.0%  |      100.0%  <- Hard Pity
```

### Example: Calculating Your Pity State

Option **2** lets you input your current counters and shows a detailed status:

```
Current State:
  Pulls without 6★ : 52
  Pulls without 5★ : 3
  Banner pulls      : 52
  Total pulls       : 52

  Pity Zone   : Base rates (not yet in soft pity)
  Next 6★ prob: 0.8%
  Pulls to soft pity     : 13
  Pulls to hard pity     : 28
  Pulls to featured (120): 68
```

### State Persistence

Your pity state is automatically saved to `~/.endfield_pity_state.json` after every calculation. You can also manually manage it via option **8** (Load/Save/Delete).

---

## Project Architecture

The project follows **Clean Architecture** with **Domain-Driven Design** principles, organized in three layers:

```
src/
├── domain/              # Core business logic (no external dependencies)
│   ├── entities/        #   PityState, PullResult
│   ├── value_objects/   #   Probability, PityCount, GameRules
│   ├── services/        #   ProbabilityCalculator, CounterCalculator, PitySimulator
│   └── exceptions/
├── application/         # Use cases and port interfaces
│   ├── use_cases/       #   CalculateState, SimulatePull, ShowProbabilityTable, ShowBaseRates
│   ├── ports/           #   StateRepository, OutputPort, InputPort, RandomGenerator
│   └── dto/             #   StateInfoDTO, SimulationResultDTO, ProbabilityTableRowDTO
└── infrastructure/      # Adapters for external systems
    ├── cli/             #   PityCalculatorMenu, ConsoleInput
    ├── persistence/     #   JsonStateRepository, StandardRandomGenerator
    └── presentation/    #   ConsolePresenter
```

**Dependency flow:** Infrastructure → Application → Domain

Key design decisions:

- **Pydantic v2** for validated, immutable domain models
- **Protocol-based ports** for dependency inversion (no ABC overhead)
- **Manual dependency injection** in `main.py` for explicit wiring
- **Repository pattern** for swappable persistence (JSON today, SQLite tomorrow)

For a deep dive with Mermaid diagrams and sequence flows, see **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

---

## Development

### Requirements

Production:
- `pydantic >= 2.6.0`

Development (optional):
- `pytest >= 8.0.0`
- `pytest-cov >= 4.1.0`
- `pytest-mock >= 3.12.0`
- `hypothesis >= 6.98.0`

### Available Commands

```bash
make install    # Install all dependencies (production + dev)
make run        # Run the application
make test       # Run the test suite
make coverage   # Run tests with coverage report (HTML output in htmlcov/)
make lint       # Run code quality checks
make clean      # Remove cache and build artifacts
make help       # Show all available commands
```

### Testing

The project has **32 tests** with **81% coverage**:

| Layer | Coverage | Test Type |
|-------|:--------:|-----------|
| Domain | ~90% | Pure unit tests (no mocks needed) |
| Application | ~80% | Use case tests with mocked ports |
| Infrastructure | ~64% | Adapter tests with real dependencies |
| Integration | -- | End-to-end flows with temporary files |

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run a specific test file
pytest tests/domain/test_probability_calculator.py -v
```

### Key Statistics

- **Average pulls to 6★:** ~62
- **Probability of featured in 80 pulls:** 50%
- **Probability of featured in 120 pulls:** 100%
- **Expected average pulls for featured:** ~100

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, new features, or documentation improvements.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes and add tests
4. Run the test suite (`make test`)
5. Commit and push your branch
6. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Disclaimer

This calculator is based on community-gathered information about Arknights: Endfield's gacha system. Actual in-game rates and mechanics may differ. Use at your own discretion.
