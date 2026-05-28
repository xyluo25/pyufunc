"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around filelock.
# Source: https://github.com/tox-dev/py-filelock

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from pyufunc.util_magic import requires


@requires("filelock")
def with_file_lock(lock_path: str | Path, timeout: float = -1) -> Any:
    """Return a file lock context manager.

    Args:
        lock_path: Path to the lock file.
        timeout: Maximum seconds to wait for the lock. Use ``-1`` to wait forever.

    Note:
        - Source package: ``filelock``.
        - Source repository: https://github.com/tox-dev/py-filelock
        - Source document: https://py-filelock.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> with with_file_lock("data.lock"):
        ...     pass

    Returns:
        Any: A ``filelock.FileLock`` context manager.
    """
    from filelock import FileLock

    return FileLock(str(lock_path), timeout=timeout)


@requires("filelock")
def safe_write_text_with_lock(
    path: str | Path,
    text: str,
    *,
    lock_path: str | Path | None = None,
    encoding: str = "utf-8",
    timeout: float = -1,
) -> Path:
    """Write text while holding a file lock.

    Args:
        path: Destination file path.
        text: Text content to write.
        lock_path: Optional lock-file path. Defaults to ``path`` plus ``.lock``.
        encoding: Text encoding used for writing.
        timeout: Maximum seconds to wait for the lock.

    Note:
        - Source package: ``filelock``.
        - Source repository: https://github.com/tox-dev/py-filelock
        - Source document: https://py-filelock.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> safe_write_text_with_lock("note.txt", "hello")

    Returns:
        Path: The destination path.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with with_file_lock(_default_lock_path(destination, lock_path), timeout=timeout):
        destination.write_text(text, encoding=encoding)

    return destination


@requires("filelock")
def safe_write_json_with_lock(
    path: str | Path,
    data: Any,
    *,
    lock_path: str | Path | None = None,
    encoding: str = "utf-8",
    timeout: float = -1,
    **json_kwargs: Any,
) -> Path:
    """Write JSON while holding a file lock.

    Args:
        path: Destination file path.
        data: JSON-serializable data.
        lock_path: Optional lock-file path. Defaults to ``path`` plus ``.lock``.
        encoding: Text encoding used for writing.
        timeout: Maximum seconds to wait for the lock.
        **json_kwargs: Keyword arguments passed to ``json.dumps``.

    Note:
        - Source package: ``filelock``.
        - Source repository: https://github.com/tox-dev/py-filelock
        - Source document: https://py-filelock.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> safe_write_json_with_lock("data.json", {"ok": True})

    Returns:
        Path: The destination path.
    """
    text = json.dumps(data, **json_kwargs)
    return safe_write_text_with_lock(path, text, lock_path=lock_path, encoding=encoding, timeout=timeout)


@requires("filelock")
def safe_write_pickle_with_lock(
    path: str | Path,
    data: Any,
    *,
    lock_path: str | Path | None = None,
    timeout: float = -1,
    protocol: int = pickle.HIGHEST_PROTOCOL,
) -> Path:
    """Write pickle data while holding a file lock.

    Args:
        path: Destination file path.
        data: Object to pickle.
        lock_path: Optional lock-file path. Defaults to ``path`` plus ``.lock``.
        timeout: Maximum seconds to wait for the lock.
        protocol: Pickle protocol version.

    Note:
        - Source package: ``filelock``.
        - Source repository: https://github.com/tox-dev/py-filelock
        - Source document: https://py-filelock.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> safe_write_pickle_with_lock("data.pkl", {"ok": True})

    Returns:
        Path: The destination path.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with with_file_lock(_default_lock_path(destination, lock_path), timeout=timeout):
        destination.write_bytes(pickle.dumps(data, protocol=protocol))

    return destination


def _default_lock_path(path: Path, lock_path: str | Path | None) -> Path:
    return Path(lock_path) if lock_path is not None else path.with_name(f"{path.name}.lock")
