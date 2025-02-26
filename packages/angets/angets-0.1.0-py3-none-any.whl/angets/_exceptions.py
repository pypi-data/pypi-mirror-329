"""Custom exceptions for Angets."""
from typing import Optional


class InvalidAttemptsValueError(ValueError):
    """Invalid number of attempts."""

    def __init__(self, attempts: int) -> None:
        """Create and return a new InvalidAttemptsValueError object."""
        super(InvalidAttemptsValueError, self).__init__(f'{attempts} is not a valid number of attempts.')


class AttemptsExceededError(Exception):
    """Given attempts exceeded."""

    def __init__(self, attempts: int) -> None:
        """Create and return a new AttemptsExceededError object."""
        super(AttemptsExceededError, self).__init__(f'Attempts exceeded, Total attempts: {attempts}')


class InvalidISOFormatError(ValueError):
    """Invalid ISO format."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new InvalidISOFormatError object."""
        if warning is None:
            warning = 'Invalid ISO format. Example: (1970-01-01)'

        super(InvalidISOFormatError, self).__init__(warning)


class InvalidConfirmationError(ValueError):
    """Invalid confirmation string."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new InvalidConfirmationError object."""
        if warning is None:
            warning = 'Invalid confirmation string.'

        super(InvalidConfirmationError, self).__init__(warning)


class InvalidIntervalError(Exception):
    """Invalid interval."""

    def __init__(self, valid_intervals: list[str], invalid_interval: str) -> None:
        """Create and return a new InvalidIntervalError object."""
        super(InvalidIntervalError, self).__init__(
            f'Invalid interval: {invalid_interval}\nValid intervals: {" or ".join(valid_intervals)}')


class OutOfBoundsError(ValueError):
    """Value not within bounds."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new OutOfBoundsError object."""
        if warning is None:
            warning = 'Value not within bounds.'

        super(OutOfBoundsError, self).__init__(warning)


class EmptyStringError(ValueError):
    """Empty string."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new EmptyStringError object."""
        if warning is None:
            warning = 'Input is empty. Please input a valid string.'

        super(EmptyStringError, self).__init__(warning)


class NonFloatingPointError(ValueError):
    """Non-floating-point number."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new NonFloatingPointError object."""
        if warning is None:
            warning = 'Not a floating-point number. Please input a valid floating-point number.'

        super(NonFloatingPointError, self).__init__(warning)


class NonIntegerError(ValueError):
    """Non-integer number."""

    def __init__(self, warning: Optional[str]) -> None:
        """Create and return a new NonIntegerError object."""
        if warning is None:
            warning = 'Not an integer. Please input a valid integer number.'

        super(NonIntegerError, self).__init__(warning)
