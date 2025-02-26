"""Utility functions for Angets."""

# Built-ins
from unicodedata import normalize
from re import sub

# Angets
from ._exceptions import NonIntegerError


def warn(warning: str) -> None:
    """Prints the warning message the stream, if there is one."""
    if warning:
        print(warning)


def convert_float_to_int(float_number: float, warning: str | None = None) -> int:
    """Return a float as an integer if said float can be converted into an integer without loss of data.

    :raise NonIntegerError: If float is not an integer.
    """
    if float_number.is_integer():
        return int(float_number)
    else:
        raise NonIntegerError(warning)


def normalize_to_ascii(non_ascii_string: str) -> str:
    """Convert a Japanese full-width number to half-width."""
    return sub('[ー－―—‐]', '-', normalize('NFKC', non_ascii_string))
