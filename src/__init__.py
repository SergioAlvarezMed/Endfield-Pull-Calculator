"""
Arknights: Endfield Pity Calculator
===================================
A tool to calculate probabilities and track pity counters for the gacha system.

Refactored with Domain-Driven Design architecture.
"""

__version__ = "0.2.0"

# Main layers
from . import domain
from . import application
from . import infrastructure

__all__ = ["domain", "application", "infrastructure"]


