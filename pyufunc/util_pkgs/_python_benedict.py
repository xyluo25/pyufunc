"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around python-benedict.
# Source: https://github.com/fabiocaccamo/python-benedict

from collections.abc import Mapping
from typing import Any

from pyufunc.util_magic import requires


@requires(("python-benedict", "benedict"))
def dict_get_by_path(mapping: Mapping[str, Any], key_path: str, default: Any = None, *, separator: str = ".") -> Any:
    """Get a nested dictionary value by key path.

    Args:
        mapping: Source mapping.
        key_path: Key path to read.
        default: Value returned when the path is missing.
        separator: Key path separator.

    Note:
        - Source package: ``python-benedict``.
        - Source repository: https://github.com/fabiocaccamo/python-benedict
        - Source document: https://github.com/fabiocaccamo/python-benedict#readme
        - Source license: MIT License.

    Example:
        >>> dict_get_by_path({"a": {"b": 1}}, "a.b")
        1

    Returns:
        Any: Value at ``key_path`` or ``default``.
    """
    from benedict import benedict

    return benedict(mapping, keypath_separator=separator).get(key_path, default)


@requires(("python-benedict", "benedict"))
def dict_set_by_path(
    mapping: Mapping[str, Any],
    key_path: str,
    value: Any,
    *,
    separator: str = ".",
) -> dict[str, Any]:
    """Set a nested dictionary value by key path.

    Args:
        mapping: Source mapping.
        key_path: Key path to set.
        value: Value to assign.
        separator: Key path separator.

    Note:
        - Source package: ``python-benedict``.
        - Source repository: https://github.com/fabiocaccamo/python-benedict
        - Source document: https://github.com/fabiocaccamo/python-benedict#readme
        - Source license: MIT License.

    Example:
        >>> dict_set_by_path({}, "a.b", 1)
        {'a': {'b': 1}}

    Returns:
        dict[str, Any]: Updated dictionary copy.
    """
    from benedict import benedict

    data = benedict(dict(mapping), keypath_separator=separator)
    data[key_path] = value
    return dict(data)


@requires(("python-benedict", "benedict"))
def dict_flatten(mapping: Mapping[str, Any], *, separator: str = "_", indexes: bool = False) -> dict[str, Any]:
    """Flatten a nested dictionary.

    Args:
        mapping: Source mapping.
        separator: Separator inserted between nested keys.
        indexes: If True, include list indexes in flattened keys.

    Note:
        - Source package: ``python-benedict``.
        - Source repository: https://github.com/fabiocaccamo/python-benedict
        - Source document: https://github.com/fabiocaccamo/python-benedict#readme
        - Source license: MIT License.

    Example:
        >>> dict_flatten({"a": {"b": 1}})
        {'a_b': 1}

    Returns:
        dict[str, Any]: Flattened dictionary.
    """
    from benedict import benedict

    return dict(benedict(mapping).flatten(separator=separator, indexes=indexes))


@requires(("python-benedict", "benedict"))
def dict_unflatten(mapping: Mapping[str, Any], *, separator: str = "_") -> dict[str, Any]:
    """Unflatten a dictionary.

    Args:
        mapping: Flattened mapping.
        separator: Separator between nested key parts.

    Note:
        - Source package: ``python-benedict``.
        - Source repository: https://github.com/fabiocaccamo/python-benedict
        - Source document: https://github.com/fabiocaccamo/python-benedict#readme
        - Source license: MIT License.

    Example:
        >>> dict_unflatten({"a_b": 1})
        {'a': {'b': 1}}

    Returns:
        dict[str, Any]: Nested dictionary.
    """
    from benedict import benedict

    return dict(benedict(mapping).unflatten(separator=separator))


@requires(("python-benedict", "benedict"))
def dict_to_json_safe(mapping: Mapping[str, Any], **kwargs: Any) -> str:
    """Serialize a mapping to JSON with python-benedict.

    Args:
        mapping: Mapping to serialize.
        **kwargs: Keyword arguments passed to ``benedict.to_json``.

    Note:
        - Source package: ``python-benedict``.
        - Source repository: https://github.com/fabiocaccamo/python-benedict
        - Source document: https://github.com/fabiocaccamo/python-benedict#readme
        - Source license: MIT License.

    Example:
        >>> dict_to_json_safe({"a": 1})

    Returns:
        str: JSON string.
    """
    from benedict import benedict

    return benedict(mapping).to_json(**kwargs)
