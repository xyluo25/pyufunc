"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around pathspec.
# Source: https://github.com/cpburnz/python-pathspec

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from pyufunc.util_magic import requires


@requires("pathspec")
def load_gitignore_patterns(gitignore_path: str | Path) -> Any:
    """Load a gitignore-style file into a pathspec matcher.

    Args:
        gitignore_path: Path to a gitignore-style pattern file.

    Note:
        - Source package: ``pathspec``.
        - Source repository: https://github.com/cpburnz/python-pathspec
        - Source document: https://python-path-specification.readthedocs.io/en/latest/index.html
        - Source license: Mozilla Public License 2.0.

    Example:
        >>> spec = load_gitignore_patterns(".gitignore")

    Returns:
        Any: A ``pathspec.PathSpec`` instance.
    """
    from pathspec import PathSpec

    lines = Path(gitignore_path).read_text(encoding="utf-8").splitlines()
    return PathSpec.from_lines("gitignore", lines)


@requires("pathspec")
def is_path_ignored(path: str | Path, patterns: Any | Iterable[str], *, root: str | Path | None = None) -> bool:
    """Return whether a path matches gitignore-style patterns.

    Args:
        path: Path to check.
        patterns: A ``pathspec.PathSpec`` instance or iterable of patterns.
        root: Optional root used to relativize ``path`` before matching.

    Note:
        - Source package: ``pathspec``.
        - Source repository: https://github.com/cpburnz/python-pathspec
        - Source document: https://python-path-specification.readthedocs.io/en/latest/index.html
        - Source license: Mozilla Public License 2.0.

    Example:
        >>> is_path_ignored("build/out.txt", ["build/"])
        True

    Returns:
        bool: True when the path is ignored.
    """
    pathspec = _coerce_pathspec(patterns)
    return bool(pathspec.match_file(_match_path(path, root=root)))


@requires("pathspec")
def filter_paths_by_gitignore(
    paths: Iterable[str | Path],
    patterns: Any | Iterable[str],
    *,
    root: str | Path | None = None,
) -> list[Path]:
    """Return paths that are not ignored by gitignore-style patterns.

    Args:
        paths: Paths to filter.
        patterns: A ``pathspec.PathSpec`` instance or iterable of patterns.
        root: Optional root used to relativize paths before matching.

    Note:
        - Source package: ``pathspec``.
        - Source repository: https://github.com/cpburnz/python-pathspec
        - Source document: https://python-path-specification.readthedocs.io/en/latest/index.html
        - Source license: Mozilla Public License 2.0.

    Example:
        >>> filter_paths_by_gitignore(["a.py", "build/a.py"], ["build/"])
        [WindowsPath('a.py')]

    Returns:
        list[Path]: Paths that do not match the ignore patterns.
    """
    pathspec = _coerce_pathspec(patterns)
    return [Path(path) for path in paths if not pathspec.match_file(_match_path(path, root=root))]


@requires("pathspec")
def collect_files_excluding_gitignore(root_dir: str | Path, gitignore_path: str | Path | None = None) -> list[Path]:
    """Collect files under a directory while excluding gitignore matches.

    Args:
        root_dir: Directory to scan recursively.
        gitignore_path: Optional gitignore-style file. Defaults to ``root_dir/.gitignore``.

    Note:
        - Source package: ``pathspec``.
        - Source repository: https://github.com/cpburnz/python-pathspec
        - Source document: https://python-path-specification.readthedocs.io/en/latest/index.html
        - Source license: Mozilla Public License 2.0.

    Example:
        >>> collect_files_excluding_gitignore(".")

    Returns:
        list[Path]: Files not ignored by the gitignore patterns.
    """
    root = Path(root_dir)
    ignore_file = Path(gitignore_path) if gitignore_path is not None else root / ".gitignore"
    patterns = load_gitignore_patterns(ignore_file) if ignore_file.exists() else []
    files = [path for path in root.rglob("*") if path.is_file()]
    return filter_paths_by_gitignore(files, patterns, root=root)


def _coerce_pathspec(patterns: Any | Iterable[str]) -> Any:
    from pathspec import PathSpec

    if isinstance(patterns, PathSpec):
        return patterns

    return PathSpec.from_lines("gitignore", list(patterns))


def _match_path(path: str | Path, *, root: str | Path | None) -> str:
    path_obj = Path(path)
    if root is not None:
        try:
            path_obj = path_obj.relative_to(Path(root))
        except ValueError:
            pass
    return path_obj.as_posix()
