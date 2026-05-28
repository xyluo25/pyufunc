"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around humanize.
# Source: https://github.com/python-humanize/humanize

from datetime import timedelta
from typing import Any

from pyufunc.util_magic import requires


@requires("humanize")
def human_file_size(value: int | float, *, binary: bool = False, gnu: bool = False, format_str: str = "%.1f") -> str:
    """Format a byte count as a human-readable file size.

    Args:
        value: Byte count.
        binary: If True, use binary prefixes.
        gnu: If True, use GNU-style prefixes.
        format_str: Numeric format string used by humanize.

    Note:
        - Source package: ``humanize``.
        - Source repository: https://github.com/python-humanize/humanize
        - Source document: https://humanize.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> human_file_size(1536)
        '1.5 kB'

    Returns:
        str: Human-readable file size.
    """
    from humanize import naturalsize

    return naturalsize(value, binary=binary, gnu=gnu, format=format_str)


@requires("humanize")
def human_time_delta(value: timedelta | int | float, **kwargs: Any) -> str:
    """Format a duration as human-readable text.

    Args:
        value: A ``datetime.timedelta`` or number of seconds.
        **kwargs: Keyword arguments passed to ``humanize.naturaldelta``.

    Note:
        - Source package: ``humanize``.
        - Source repository: https://github.com/python-humanize/humanize
        - Source document: https://humanize.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> human_time_delta(3600)
        'an hour'

    Returns:
        str: Human-readable duration.
    """
    from humanize import naturaldelta

    return naturaldelta(value, **kwargs)


@requires("humanize")
def human_number(value: int | float, *, format_str: str = "%.1f") -> str:
    """Format a large number as human-readable text.

    Args:
        value: Numeric value.
        format_str: Numeric format string used by humanize.

    Note:
        - Source package: ``humanize``.
        - Source repository: https://github.com/python-humanize/humanize
        - Source document: https://humanize.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> human_number(1200000)
        '1.2 million'

    Returns:
        str: Human-readable number.
    """
    from humanize import intword

    return intword(value, format=format_str)


@requires("humanize")
def human_intcomma(value: int | float | str, ndigits: int | None = None) -> str:
    """Format a number with comma separators.

    Args:
        value: Numeric value or numeric string.
        ndigits: Optional number of decimal digits.

    Note:
        - Source package: ``humanize``.
        - Source repository: https://github.com/python-humanize/humanize
        - Source document: https://humanize.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> human_intcomma(1200000)
        '1,200,000'

    Returns:
        str: Number formatted with comma separators.
    """
    from humanize import intcomma

    return intcomma(value, ndigits=ndigits)
