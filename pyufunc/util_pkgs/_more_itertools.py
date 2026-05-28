"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around more-itertools.
# Source: https://github.com/more-itertools/more-itertools

from collections.abc import Callable, Iterable
from typing import Any

from pyufunc.util_magic import requires


@requires(("more-itertools", "more_itertools"))
def iter_chunked(iterable: Iterable[Any], chunk_size: int, *, strict: bool = False) -> Iterable[list[Any]]:
    """Split an iterable into fixed-size chunks.

    Args:
        iterable: Iterable to split.
        chunk_size: Number of items per chunk.
        strict: If True, require every chunk to have exactly ``chunk_size`` items.

    Note:
        - Source package: ``more-itertools``.
        - Source repository: https://github.com/more-itertools/more-itertools
        - Source document: https://more-itertools.readthedocs.io/en/stable/
        - Source license: MIT License.

    Example:
        >>> list(iter_chunked([1, 2, 3], 2))
        [[1, 2], [3]]

    Returns:
        Iterable[list[Any]]: Chunks from ``more_itertools.chunked``.
    """
    from more_itertools import chunked

    return chunked(iterable, chunk_size, strict=strict)


@requires(("more-itertools", "more_itertools"))
def iter_windowed(
    iterable: Iterable[Any], window_size: int, *, fillvalue: Any = None, step: int = 1
) -> Iterable[tuple]:
    """Return sliding windows over an iterable.

    Args:
        iterable: Iterable to scan.
        window_size: Number of items per window.
        fillvalue: Value used for incomplete windows.
        step: Number of items to move between windows.

    Note:
        - Source package: ``more-itertools``.
        - Source repository: https://github.com/more-itertools/more-itertools
        - Source document: https://more-itertools.readthedocs.io/en/stable/
        - Source license: MIT License.

    Example:
        >>> list(iter_windowed([1, 2, 3], 2))
        [(1, 2), (2, 3)]

    Returns:
        Iterable[tuple]: Windows from ``more_itertools.windowed``.
    """
    from more_itertools import windowed

    return windowed(iterable, window_size, fillvalue=fillvalue, step=step)


@requires(("more-itertools", "more_itertools"))
def iter_unique(iterable: Iterable[Any], key: Callable[[Any], Any] | None = None) -> Iterable[Any]:
    """Yield unique items while preserving first-seen order.

    Args:
        iterable: Iterable to de-duplicate.
        key: Optional key function used for uniqueness.

    Note:
        - Source package: ``more-itertools``.
        - Source repository: https://github.com/more-itertools/more-itertools
        - Source document: https://more-itertools.readthedocs.io/en/stable/
        - Source license: MIT License.

    Example:
        >>> list(iter_unique([1, 1, 2]))
        [1, 2]

    Returns:
        Iterable[Any]: Unique items from ``more_itertools.unique_everseen``.
    """
    from more_itertools import unique_everseen

    return unique_everseen(iterable, key=key)


@requires(("more-itertools", "more_itertools"))
def iter_flatten(iterable: Iterable[Any], *, base_type: type | tuple[type, ...] | None = None) -> Iterable[Any]:
    """Flatten nested iterables.

    Args:
        iterable: Nested iterable to flatten.
        base_type: Optional type or tuple of types that should not be flattened.

    Note:
        - Source package: ``more-itertools``.
        - Source repository: https://github.com/more-itertools/more-itertools
        - Source document: https://more-itertools.readthedocs.io/en/stable/
        - Source license: MIT License.

    Example:
        >>> list(iter_flatten([[1], [2, [3]]]))
        [1, 2, 3]

    Returns:
        Iterable[Any]: Flattened items from ``more_itertools.collapse``.
    """
    from more_itertools import collapse

    return collapse(iterable, base_type=base_type)


@requires(("more-itertools", "more_itertools"))
def iter_split_when(
    iterable: Iterable[Any],
    predicate: Callable[[Any, Any], bool],
    *,
    maxsplit: int = -1,
) -> Iterable[list[Any]]:
    """Split an iterable when a pair-wise predicate is true.

    Args:
        iterable: Iterable to split.
        predicate: Function called with adjacent items.
        maxsplit: Maximum number of splits. Use ``-1`` for no limit.

    Note:
        - Source package: ``more-itertools``.
        - Source repository: https://github.com/more-itertools/more-itertools
        - Source document: https://more-itertools.readthedocs.io/en/stable/
        - Source license: MIT License.

    Example:
        >>> list(iter_split_when([1, 2, 5], lambda a, b: b - a > 1))
        [[1, 2], [5]]

    Returns:
        Iterable[list[Any]]: Split groups from ``more_itertools.split_when``.
    """
    from more_itertools import split_when

    return split_when(iterable, predicate, maxsplit=maxsplit)
