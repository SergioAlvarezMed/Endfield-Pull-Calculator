"""Domain exceptions."""


class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class InvalidPityStateError(DomainException):
    """Raised when pity state is invalid."""
    pass


class PityLimitExceededError(DomainException):
    """Raised when pity counter exceeds limits."""
    pass


class InvalidProbabilityError(DomainException):
    """Raised when probability value is invalid."""
    pass
