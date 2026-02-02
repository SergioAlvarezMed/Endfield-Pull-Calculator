# Arknights: Endfield Pity Calculator

A command-line tool to calculate probabilities and track pity counters for the gacha system in **Arknights: Endfield**.

## ✨ Features (v0.2.0 - Refactored with DDD Architecture)

- 📊 **View base rates** and pity system explanation
- 🎯 **Calculate your current pity state** (all counters)
- 📈 **Calculate 6★ probability** for upcoming pulls
- 🎲 **Simulate 50/50 results**
- 💾 **Auto-save state** (persists between sessions)
- 📋 **View detailed probability tables**
- 🧪 **Well-tested** (>80% coverage, 32 tests)
- 🏗️ **Clean Architecture** (Domain-Driven Design)

## 🏗️ New Architecture (v0.2.0)

Completely refactored using **Domain-Driven Design** principles:

```
src/
├── domain/         # Business logic (entities, value objects, services)
├── application/    # Use cases and ports
└── infrastructure/ # CLI, persistence, presentation
```

**See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed documentation with diagrams.**
- 💎 Calculate pulls needed for featured guarantee
- 📋 View detailed soft pity probability table
- 📋 View featured 6★ probability table (phases 1 & 2)
- 📉 View ASCII graph of featured probability vs pulls

## Gacha System Overview

### Base Rates
| Rarity | Rate |
|--------|------|
| 6★ | 0.8% |
| 5★ | 8% |
| 4★ | 91.2% |

### Pity System

| Mechanic | Pulls | Description | Carries Over? |
|----------|-------|-------------|---------------|
| **5★ Guarantee** | 10 | At least one 5★ (50% featured) | ✓ Yes |
| **Soft Pity** | 65+ | +5% per pull after 65 | ✓ Yes |
| **Hard Pity (50/50)** | 80 | 6★ guaranteed (50% featured) | ✓ Yes |
| **Featured Guarantee** | 120 | 100% featured character | ✗ No |
| **Bonus Dupe** | 240 | Extra copy (repeats) | ✓ Yes |

### Counter Formulas

```
P(r) = min(r, 80)   → Pity counter (resets when pulling 6★)
S(r) = min(r, 120)  → Spark counter (does NOT reset on banner)
D(r) = min(r, 240)  → Dupe counter (carries over between banners)
```

### Special Rules

- **When losing 50/50:**
  - 14.28% chance for each of the 2 previous limited characters
  - 71.44% chance for standard 6★
- ⚠️ **NO featured guarantee after losing 50/50 until pull 120**
- After 60 pulls: Free 10-pull for the NEXT banner (expires if not used)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/endfield-pity-system.git
cd endfield-pity-system
```

2. Run the calculator:
```bash
python main.py
```

No external dependencies required! 🎉

## Usage

Run the program and select an option from the menu:

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
8. View featured probability graph
9. Exit
============================================================
```

### Example: Viewing Soft Pity Table

```
  Pull   | P(r) | S(r) | D(r) |  Prob. 6★  |  Cumulative Prob.
         | Pity | Spark| Dupe |            |
  -------------------------------------------------------------------------
      1  |   1  |    1 |    1 |      0.8%   |        0.8%
      ...
     65  |  65  |   65 |   65 |      5.8%   |       43.7% <- Soft Pity Start
     66  |  66  |   66 |   66 |     10.8%   |       49.7%
     ...
     80  |  80  |   80 |   80 |    100.0%   |      100.0% <- Hard Pity (GUARANTEED)
```

### Example: Featured Probability Graph

```
  100% |                                                            *
       |                                                         ...
   50% |                                    @.........................
       |                               .....
       |                          .....
       |                     .....
       |                .....
       |           .....
       |      .....
    0% +.....
       +------------------------------------------------------------
        1              30              60              90          120
                                    Pulls

  LEGEND:
    . = Probability
    # = Soft Pity (pull 65)
    @ = Hard Pity (pull 80)
    * = Featured Guaranteed (pull 120)
```

## Statistics

- **Average pull for 6★:** ~62 pulls
- **Probability of featured in ≤80 pulls:** 50%
- **Probability of featured in ≤120 pulls:** 100%
- **Expected average pulls for featured:** ~100

## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## License

MIT License - feel free to use and modify as needed.

## Disclaimer

This calculator is based on community-gathered information about Arknights: Endfield's gacha system. Actual rates and mechanics may vary. Use at your own discretion.

---

Made with ❤️ for the Arknights: Endfield community

