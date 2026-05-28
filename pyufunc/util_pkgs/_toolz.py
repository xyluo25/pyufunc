"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around toolz.
# Source: https://github.com/pytoolz/toolz

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from pyufunc.util_magic import requires


@requires("toolz")
def toolz_groupby_key(key: Callable[[Any], Any] | str, sequence: Iterable[Any]) -> dict[Any, list[Any]]:
    """Group items by a key function or mapping key.

    Args:
        key: Callable or key name used by ``toolz.groupby``.
        sequence: Items to group.

    Note:
        - Source package: ``toolz``.
        - Source repository: https://github.com/pytoolz/toolz
        - Source document: https://toolz.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> toolz_groupby_key(lambda x: x % 2, [1, 2, 3])
        {1: [1, 3], 0: [2]}

    Returns:
        dict[Any, list[Any]]: Grouped items.
    """
    from toolz import groupby

    return groupby(key, sequence)


@requires("toolz")
def toolz_merge_dicts(*dicts: Mapping[Any, Any], **kwargs: Any) -> dict[Any, Any]:
    """Merge dictionaries with later values taking precedence.

    Args:
        *dicts: Dictionaries to merge.
        **kwargs: Extra key-value pairs merged last.

    Note:
        - Source package: ``toolz``.
        - Source repository: https://github.com/pytoolz/toolz
        - Source document: https://toolz.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> toolz_merge_dicts({"a": 1}, {"b": 2})
        {'a': 1, 'b': 2}

    Returns:
        dict[Any, Any]: Merged dictionary.
    """
    from toolz import merge

    return merge(*dicts, **kwargs)


@requires("toolz")
def toolz_sliding_window(window_size: int, sequence: Iterable[Any]) -> Iterable[tuple[Any, ...]]:
    """Return a sliding window over a sequence.

    Args:
        window_size: Number of items per window.
        sequence: Items to scan.

    Note:
        - Source package: ``toolz``.
        - Source repository: https://github.com/pytoolz/toolz
        - Source document: https://toolz.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> list(toolz_sliding_window(2, [1, 2, 3]))
        [(1, 2), (2, 3)]

    Returns:
        Iterable[tuple[Any, ...]]: Sliding windows.
    """
    from toolz import sliding_window

    return sliding_window(window_size, sequence)


@requires("toolz")
def toolz_pipe_call(value: Any, *functions: Callable[[Any], Any]) -> Any:
    """Pipe a value through a sequence of functions.

    Args:
        value: Initial value.
        *functions: Functions applied in order.

    Note:
        - Source package: ``toolz``.
        - Source repository: https://github.com/pytoolz/toolz
        - Source document: https://toolz.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> toolz_pipe_call(2, lambda x: x + 1, lambda x: x * 2)
        6

    Returns:
        Any: Final result.
    """
    from toolz import pipe

    return pipe(value, *functions)


@requires("toolz")
def toolz_count_frequencies(sequence: Iterable[Any]) -> dict[Any, int]:
    """Count item frequencies in a sequence.

    Args:
        sequence: Items to count.

    Note:
        - Source package: ``toolz``.
        - Source repository: https://github.com/pytoolz/toolz
        - Source document: https://toolz.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> toolz_count_frequencies(["a", "a", "b"])
        {'a': 2, 'b': 1}

    Returns:
        dict[Any, int]: Frequency mapping.
    """
    from toolz import frequencies

    return frequencies(sequence)
