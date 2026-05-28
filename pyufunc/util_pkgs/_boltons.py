"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around boltons.
# Source: https://github.com/mahmoud/boltons

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyufunc.util_magic import requires


@requires("boltons")
def remap_nested_dict(mapping: Any, **kwargs: Any) -> Any:
    """Transform nested mappings and sequences with ``boltons.iterutils.remap``.

    Args:
        mapping: Nested data structure to transform.
        **kwargs: Keyword arguments passed to ``boltons.iterutils.remap``.

    Note:
        - Source package: ``boltons``.
        - Source repository: https://github.com/mahmoud/boltons
        - Source document: https://boltons.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> remap_nested_dict({"a": {"b": 1}})
        {'a': {'b': 1}}

    Returns:
        Any: Remapped data structure.
    """
    from boltons.iterutils import remap

    return remap(mapping, **kwargs)


@requires("boltons")
def flatten_iterable(iterable: Any) -> list[Any]:
    """Flatten one level of nested iterables.

    Args:
        iterable: Iterable containing nested iterables.

    Note:
        - Source package: ``boltons``.
        - Source repository: https://github.com/mahmoud/boltons
        - Source document: https://boltons.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> flatten_iterable([[1], [2, 3]])
        [1, 2, 3]

    Returns:
        list[Any]: Flattened values.
    """
    from boltons.iterutils import flatten

    return flatten(iterable)


@requires("boltons")
def atomic_save_file(
    path: str | Path,
    data: str | bytes,
    *,
    text_mode: bool = True,
    overwrite: bool = True,
) -> Path:
    """Atomically write text or bytes to a file.

    Args:
        path: Destination file path.
        data: Text or bytes to write.
        text_mode: If True, open the temporary part file in text mode.
        overwrite: If True, overwrite an existing destination.

    Note:
        - Source package: ``boltons``.
        - Source repository: https://github.com/mahmoud/boltons
        - Source document: https://boltons.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> atomic_save_file("note.txt", "hello")

    Returns:
        Path: The destination path.
    """
    from boltons.fileutils import atomic_save

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with atomic_save(str(destination), text_mode=text_mode, overwrite=overwrite) as file_obj:
        file_obj.write(data)

    return destination


@requires("boltons")
def slugify_text(text: str, *, delim: str = "_", lower: bool = True, ascii: bool = False) -> str:
    """Convert text to a slug with ``boltons.strutils.slugify``.

    Args:
        text: Text to slugify.
        delim: Delimiter inserted between words.
        lower: If True, lowercase the result.
        ascii: If True, normalize to ASCII.

    Note:
        - Source package: ``boltons``.
        - Source repository: https://github.com/mahmoud/boltons
        - Source document: https://boltons.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> slugify_text("Hello World")
        'hello_world'

    Returns:
        str: Slugified text.
    """
    from boltons.strutils import slugify

    return slugify(text, delim=delim, lower=lower, ascii=ascii)


@requires("boltons")
def parse_timedelta_text(text: str) -> Any:
    """Parse human-readable duration text into ``datetime.timedelta``.

    Args:
        text: Duration text accepted by ``boltons.timeutils.parse_timedelta``.

    Note:
        - Source package: ``boltons``.
        - Source repository: https://github.com/mahmoud/boltons
        - Source document: https://boltons.readthedocs.io/en/latest/
        - Source license: BSD License.

    Example:
        >>> parse_timedelta_text("1h")

    Returns:
        Any: Parsed ``datetime.timedelta`` value.
    """
    from boltons.timeutils import parse_timedelta

    return parse_timedelta(text)
