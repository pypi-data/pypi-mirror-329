"""Decorators for Angets."""

# Built-ins
from typing import Callable
from functools import wraps

# Angets
from ._defaults import ATTEMPTS
from ._helpers import warn
from ._exceptions import AttemptsExceededError, InvalidAttemptsValueError


def loop(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        attempts: int = kwargs.get('attempts', ATTEMPTS)
        if attempts <= 0:
            raise InvalidAttemptsValueError(attempts)
        elif attempts == 1:
            return function(*args, **kwargs)
        else:
            for _ in range(attempts):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    if kwargs.get('verbose'):
                        warn(str(error))
                    continue
            else:
                raise AttemptsExceededError(attempts)

    return wrapper
