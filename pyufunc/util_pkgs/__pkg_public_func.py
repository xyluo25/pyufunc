# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import annotations

import ast
import importlib
import importlib.metadata
import inspect
import json
import tarfile
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


_PYPI_JSON_URL = "https://pypi.org/pypi/{package_name}/json"
_SKIPPED_SOURCE_DIRS = {
    "__pycache__",
    ".git",
    ".github",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "benchmark",
    "benchmarks",
    "doc",
    "docs",
    "example",
    "examples",
    "test",
    "tests",
}
_SKIPPED_TOP_LEVEL_NAMES = {
    "benchmark",
    "benchmarks",
    "doc",
    "docs",
    "example",
    "examples",
    "test",
    "tests",
}


@dataclass(frozen=True)
class _ImportReference:
    """Store a source-level import that may re-export package functions."""

    module_name: str
    names: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    is_star_import: bool = False


@dataclass(frozen=True)
class _ModuleInfo:
    """Store static information parsed from one Python source module."""

    module_name: str
    path: Path
    is_package: bool
    functions: frozenset[str]
    all_names: frozenset[str] | None
    imports: tuple[_ImportReference, ...]


def pkg_public_func(pkg_name: str, *, import_name: str | None = None, verbose: bool = True) -> list[str]:
    """Show package-level public functions defined by a Python package.

    The function first inspects the package in the current Python environment.
    If the package cannot be imported, it downloads the latest distribution from
    PyPI into a temporary directory and statically inspects the package source.
    Downloaded distributions are not installed.

    Args:
        pkg_name: Package import name or PyPI distribution name. For packages
            whose distribution name differs from the import name, pass the PyPI
            name here and set ``import_name`` when needed.
        import_name: Optional import/package name override. For example,
            ``pkg_public_func("python-dateutil", import_name="dateutil")``.
        verbose: Whether to print fallback errors. Defaults to True.

    Note:
        - Source package: ``pyufunc``.
        - Source repository: https://github.com/xyluo25/pyufunc
        - Source document: https://pyufunc.readthedocs.io/en/latest/
        - Source license: MIT License.
        - Downloaded PyPI distributions are inspected in a temporary directory and are not installed.

    Example:
        >>> from pyufunc import pkg_public_func
        >>> public_funcs = pkg_public_func("pyufunc.util_img")
        >>> "img_to_bytes" in public_funcs
        True

        >>> pkg_public_func("python-dateutil", import_name="dateutil")  # doctest: +SKIP

    Returns:
        list[str]: Sorted package-level public function names. The list includes
        functions whose implementation belongs to the package itself, and
        excludes classes, modules, private names, and external functions.
    """
    _validate_package_name(pkg_name)

    import_errors: list[str] = []
    for candidate_import_name in _iter_import_name_candidates(pkg_name=pkg_name, import_name=import_name):
        try:
            package = importlib.import_module(candidate_import_name)
        except ImportError as exc:
            import_errors.append(f"{candidate_import_name}: {exc}")
            continue

        return _get_public_functions_from_imported_package(package=package, package_name=candidate_import_name)

    try:
        return _get_public_functions_from_pypi_distribution(
            distribution_name=pkg_name,
            import_name=import_name,
        )
    except (OSError, RuntimeError, ValueError, urllib.error.URLError, zipfile.BadZipFile, tarfile.TarError) as exc:
        if verbose:
            if import_errors:
                print(f"  :Info: could not import {pkg_name}: {'; '.join(import_errors)}")
            print(f"  :Info: could not inspect {pkg_name} from PyPI: {exc}")
        return []


def _validate_package_name(pkg_name: str) -> None:
    """Validate the package or distribution name argument."""
    if not isinstance(pkg_name, str) or not pkg_name.strip():
        raise ValueError("pkg_name must be a non-empty string.")


def _iter_import_name_candidates(pkg_name: str, import_name: str | None) -> list[str]:
    """Return import-name candidates for an installed package lookup."""
    candidates: list[str] = []

    if import_name:
        candidates.append(import_name)

    candidates.extend(_get_installed_top_level_names(pkg_name))
    candidates.append(pkg_name)
    candidates.append(pkg_name.replace("-", "_"))

    return _dedupe_preserve_order(candidate for candidate in candidates if _is_valid_module_name(candidate))


def _get_installed_top_level_names(distribution_name: str) -> list[str]:
    """Return top-level import names declared by an installed distribution."""
    try:
        distribution = importlib.metadata.distribution(distribution_name)
    except importlib.metadata.PackageNotFoundError:
        return []

    top_level_text = distribution.read_text("top_level.txt")
    if not top_level_text:
        return []

    return [name.strip() for name in top_level_text.splitlines() if _is_valid_top_level_name(name.strip())]


def _get_public_functions_from_imported_package(package: Any, package_name: str) -> list[str]:
    """Collect package-level public functions from an imported package."""
    exported_names = getattr(package, "__all__", None)
    if isinstance(exported_names, (list, tuple, set)):
        candidate_names = [name for name in exported_names if isinstance(name, str)]
    else:
        candidate_names = [name for name in dir(package) if not name.startswith("_")]

    public_functions: list[str] = []
    for name in candidate_names:
        if name.startswith("_"):
            continue

        try:
            member = getattr(package, name)
        except AttributeError:
            continue

        if inspect.isfunction(member) and _is_package_owned_function(member, package_name):
            public_functions.append(name)

    return sorted(set(public_functions), key=str.lower)


def _is_package_owned_function(function: Any, package_name: str) -> bool:
    """Return whether a runtime function is implemented by the target package."""
    function_module = getattr(function, "__module__", "")
    return function_module == package_name or function_module.startswith(f"{package_name}.")


def _get_public_functions_from_pypi_distribution(distribution_name: str, import_name: str | None) -> list[str]:
    """Download a PyPI distribution and collect public functions from source."""
    with tempfile.TemporaryDirectory(prefix="pyufunc_pkg_public_func_") as temp_dir:
        temp_path = Path(temp_dir)
        archive_path = _download_latest_distribution(distribution_name=distribution_name, output_dir=temp_path)
        extract_dir = temp_path / "extracted"
        extract_dir.mkdir()
        _extract_distribution_archive(archive_path=archive_path, output_dir=extract_dir)

        for package_name in _iter_source_package_names(
            extracted_dir=extract_dir,
            distribution_name=distribution_name,
            import_name=import_name,
        ):
            public_functions = _get_public_functions_from_source_tree(
                extracted_dir=extract_dir,
                package_name=package_name,
            )
            if public_functions:
                return public_functions

    return []


def _download_latest_distribution(distribution_name: str, output_dir: Path) -> Path:
    """Download the latest wheel or source distribution from PyPI."""
    metadata_url = _PYPI_JSON_URL.format(package_name=distribution_name)
    request = urllib.request.Request(metadata_url, headers={"User-Agent": "pyufunc-package-inspector"})

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            package_metadata = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"PyPI returned HTTP {exc.code} for {distribution_name}.") from exc

    release_files = _get_latest_release_files(package_metadata=package_metadata)
    selected_file = _select_distribution_file(release_files)
    if not selected_file:
        raise RuntimeError(f"No downloadable wheel or source distribution found for {distribution_name}.")

    download_url = selected_file["url"]
    filename = selected_file["filename"]
    archive_path = output_dir / filename

    request = urllib.request.Request(download_url, headers={"User-Agent": "pyufunc-package-inspector"})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive_path.write_bytes(response.read())

    return archive_path


def _get_latest_release_files(package_metadata: dict[str, Any]) -> list[dict[str, Any]]:
    """Return distribution files for the latest release in PyPI metadata."""
    version = package_metadata.get("info", {}).get("version")
    releases = package_metadata.get("releases", {})

    if isinstance(version, str) and isinstance(releases, dict):
        release_files = releases.get(version, [])
        if isinstance(release_files, list) and release_files:
            return [file for file in release_files if isinstance(file, dict)]

    urls = package_metadata.get("urls", [])
    if isinstance(urls, list):
        return [file for file in urls if isinstance(file, dict)]

    return []


def _select_distribution_file(release_files: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Select the best distribution file for static source inspection."""
    supported_files = [
        file
        for file in release_files
        if isinstance(file.get("url"), str)
        and isinstance(file.get("filename"), str)
        and file.get("packagetype") in {"bdist_wheel", "sdist"}
    ]

    if not supported_files:
        return None

    return sorted(supported_files, key=_distribution_file_priority)[0]


def _distribution_file_priority(release_file: dict[str, Any]) -> tuple[int, str]:
    """Return a stable priority key for selecting PyPI distribution files."""
    package_type = release_file.get("packagetype")
    filename = str(release_file.get("filename", ""))

    if package_type == "bdist_wheel" and filename.endswith("py3-none-any.whl"):
        return (0, filename)
    if package_type == "bdist_wheel":
        return (1, filename)
    if package_type == "sdist":
        return (2, filename)
    return (3, filename)


def _extract_distribution_archive(archive_path: Path, output_dir: Path) -> None:
    """Extract a wheel, zip, or tar source distribution."""
    archive_name = archive_path.name.lower()

    if archive_name.endswith((".whl", ".zip")):
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(output_dir)
        return

    if tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path) as archive:
            archive.extractall(output_dir)
        return

    raise ValueError(f"Unsupported distribution archive: {archive_path.name}")


def _iter_source_package_names(
    extracted_dir: Path,
    distribution_name: str,
    import_name: str | None,
) -> list[str]:
    """Return source package names to inspect in an extracted distribution."""
    candidates: list[str] = []

    if import_name:
        candidates.append(import_name)

    candidates.extend(_read_top_level_names(extracted_dir))
    candidates.append(distribution_name)
    candidates.append(distribution_name.replace("-", "_"))

    return _dedupe_preserve_order(candidate for candidate in candidates if _is_valid_module_name(candidate))


def _read_top_level_names(extracted_dir: Path) -> list[str]:
    """Read top-level package names from distribution metadata files."""
    names: list[str] = []

    for top_level_file in extracted_dir.rglob("top_level.txt"):
        try:
            top_level_text = top_level_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            top_level_text = top_level_file.read_text(encoding="latin-1")

        names.extend(name.strip() for name in top_level_text.splitlines() if _is_valid_top_level_name(name.strip()))

    return names


def _get_public_functions_from_source_tree(extracted_dir: Path, package_name: str) -> list[str]:
    """Collect package-level public functions by statically inspecting source."""
    module_sources = _collect_package_module_sources(extracted_dir=extracted_dir, package_name=package_name)
    if package_name not in module_sources:
        return []

    module_infos = {
        module_name: _parse_module_source(module_name=module_name, source_path=source_path)
        for module_name, source_path in module_sources.items()
    }

    public_functions = _resolve_public_functions(
        module_name=package_name,
        root_package_name=package_name,
        module_infos=module_infos,
        seen=set(),
    )
    return sorted(public_functions, key=str.lower)


def _collect_package_module_sources(extracted_dir: Path, package_name: str) -> dict[str, Path]:
    """Collect Python source files belonging to the requested package."""
    package_init_path = _find_package_init_path(extracted_dir=extracted_dir, package_name=package_name)
    if package_init_path:
        package_dir = package_init_path.parent
        module_sources: dict[str, Path] = {}

        for source_path in package_dir.rglob("*.py"):
            relative_path = source_path.relative_to(package_dir)
            if _is_skipped_source_path(relative_path):
                continue

            module_name = _source_path_to_module_name(
                package_name=package_name,
                relative_path=relative_path,
            )
            module_sources[module_name] = source_path

        return module_sources

    single_module_path = _find_single_module_path(extracted_dir=extracted_dir, package_name=package_name)
    if single_module_path:
        return {package_name: single_module_path}

    return {}


def _find_package_init_path(extracted_dir: Path, package_name: str) -> Path | None:
    """Find the package ``__init__.py`` file in an extracted distribution."""
    package_parts = tuple(package_name.split("."))
    matches = [
        source_path
        for source_path in extracted_dir.rglob("__init__.py")
        if tuple(source_path.parent.parts[-len(package_parts) :]) == package_parts
    ]
    if not matches:
        return None

    return min(matches, key=lambda path: len(path.parts))


def _find_single_module_path(extracted_dir: Path, package_name: str) -> Path | None:
    """Find a single-file module in an extracted distribution."""
    if "." in package_name:
        return None

    matches = [source_path for source_path in extracted_dir.rglob(f"{package_name}.py")]
    if not matches:
        return None

    return min(matches, key=lambda path: len(path.parts))


def _is_skipped_source_path(relative_path: Path) -> bool:
    """Return whether a source path belongs to a non-package support folder."""
    return any(part.lower() in _SKIPPED_SOURCE_DIRS for part in relative_path.parts)


def _source_path_to_module_name(package_name: str, relative_path: Path) -> str:
    """Convert a package-relative source path to a Python module name."""
    if relative_path.name == "__init__.py":
        if relative_path.parent == Path("."):
            return package_name
        return ".".join((package_name, *relative_path.parent.parts))

    module_parts = relative_path.with_suffix("").parts
    return ".".join((package_name, *module_parts))


def _parse_module_source(module_name: str, source_path: Path) -> _ModuleInfo:
    """Parse one Python source file into static module information."""
    source_text = _read_source_text(source_path)
    is_package = source_path.name == "__init__.py"

    try:
        module_ast = ast.parse(source_text)
    except SyntaxError:
        return _ModuleInfo(
            module_name=module_name,
            path=source_path,
            is_package=is_package,
            functions=frozenset(),
            all_names=None,
            imports=tuple(),
        )

    functions = {
        node.name
        for node in module_ast.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
    }

    return _ModuleInfo(
        module_name=module_name,
        path=source_path,
        is_package=is_package,
        functions=frozenset(functions),
        all_names=_extract_all_names(module_ast),
        imports=tuple(_extract_import_references(module_ast, module_name=module_name, is_package=is_package)),
    )


def _read_source_text(source_path: Path) -> str:
    """Read Python source text using UTF-8 with a Latin-1 fallback."""
    try:
        return source_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return source_path.read_text(encoding="latin-1")


def _extract_all_names(module_ast: ast.Module) -> frozenset[str] | None:
    """Extract simple string values assigned to ``__all__``."""
    all_names: set[str] | None = None

    for node in module_ast.body:
        if isinstance(node, ast.Assign) and any(_is_all_target(target) for target in node.targets):
            names = _literal_string_names(node.value)
            if names is not None:
                all_names = set(names)
        elif isinstance(node, ast.AugAssign) and _is_all_target(node.target):
            names = _literal_string_names(node.value)
            if names is not None:
                all_names = set() if all_names is None else all_names
                all_names.update(names)
        elif isinstance(node, ast.Expr):
            _update_all_names_from_method_call(node.value, all_names)

    return frozenset(all_names) if all_names is not None else None


def _is_all_target(target: ast.AST) -> bool:
    """Return whether an assignment target is ``__all__``."""
    return isinstance(target, ast.Name) and target.id == "__all__"


def _update_all_names_from_method_call(call_node: ast.AST, all_names: set[str] | None) -> None:
    """Update collected ``__all__`` names from simple append/extend calls."""
    if all_names is None or not isinstance(call_node, ast.Call):
        return

    if not isinstance(call_node.func, ast.Attribute):
        return

    if not isinstance(call_node.func.value, ast.Name) or call_node.func.value.id != "__all__":
        return

    if call_node.func.attr == "append" and call_node.args:
        name = _literal_string(call_node.args[0])
        if name:
            all_names.add(name)
    elif call_node.func.attr == "extend" and call_node.args:
        names = _literal_string_names(call_node.args[0])
        if names:
            all_names.update(names)


def _literal_string_names(node: ast.AST) -> list[str] | None:
    """Extract string names from a simple literal collection expression."""
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        names: list[str] = []
        for element in node.elts:
            name = _literal_string(element)
            if name is None:
                return None
            names.append(name)
        return names

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left_names = _literal_string_names(node.left)
        right_names = _literal_string_names(node.right)
        if left_names is not None and right_names is not None:
            return [*left_names, *right_names]

    return None


def _literal_string(node: ast.AST) -> str | None:
    """Return a literal string value from an AST node if available."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _extract_import_references(
    module_ast: ast.Module,
    *,
    module_name: str,
    is_package: bool,
) -> list[_ImportReference]:
    """Extract package-internal import references from module source."""
    imports: list[_ImportReference] = []

    for node in module_ast.body:
        if not isinstance(node, ast.ImportFrom):
            continue

        imported_module_name = _resolve_import_module(
            current_module_name=module_name,
            import_module_name=node.module,
            level=node.level,
            is_package=is_package,
        )
        if not imported_module_name:
            continue

        if len(node.names) == 1 and node.names[0].name == "*":
            imports.append(_ImportReference(module_name=imported_module_name, is_star_import=True))
            continue

        names = tuple((alias.name, alias.asname or alias.name) for alias in node.names if alias.name != "*")
        imports.append(_ImportReference(module_name=imported_module_name, names=names))

    return imports


def _resolve_import_module(
    *,
    current_module_name: str,
    import_module_name: str | None,
    level: int,
    is_package: bool,
) -> str:
    """Resolve an ``ImportFrom`` node to an absolute module name."""
    if level == 0:
        return import_module_name or ""

    current_package_name = current_module_name if is_package else current_module_name.rsplit(".", 1)[0]
    package_parts = current_package_name.split(".")

    if level > 1:
        package_parts = package_parts[: -(level - 1)]

    if not package_parts:
        return import_module_name or ""

    if import_module_name:
        package_parts.extend(import_module_name.split("."))

    return ".".join(package_parts)


def _resolve_public_functions(
    *,
    module_name: str,
    root_package_name: str,
    module_infos: dict[str, _ModuleInfo],
    seen: set[str],
) -> set[str]:
    """Resolve public function names exported by one package module."""
    if module_name in seen:
        return set()

    module_info = module_infos.get(module_name)
    if module_info is None:
        return set()

    seen.add(module_name)
    public_functions = set(module_info.functions)

    for import_reference in module_info.imports:
        if not _is_internal_module(import_reference.module_name, root_package_name):
            continue

        if import_reference.is_star_import:
            public_functions.update(
                _resolve_public_functions(
                    module_name=import_reference.module_name,
                    root_package_name=root_package_name,
                    module_infos=module_infos,
                    seen=seen.copy(),
                )
            )
            continue

        for imported_name, exported_name in import_reference.names:
            if exported_name.startswith("_"):
                continue

            resolved_module_name = import_reference.module_name
            resolved_function_name = imported_name

            nested_module_name = f"{import_reference.module_name}.{imported_name}"
            if nested_module_name in module_infos:
                continue

            if _module_exports_function(
                module_name=resolved_module_name,
                function_name=resolved_function_name,
                root_package_name=root_package_name,
                module_infos=module_infos,
                seen=seen.copy(),
            ):
                public_functions.add(exported_name)

    if module_info.all_names is not None:
        public_functions = {name for name in public_functions if name in module_info.all_names}

    return public_functions


def _module_exports_function(
    *,
    module_name: str,
    function_name: str,
    root_package_name: str,
    module_infos: dict[str, _ModuleInfo],
    seen: set[str],
) -> bool:
    """Return whether a module exports a public function with the given name."""
    module_info = module_infos.get(module_name)
    if module_info is None:
        return False

    if function_name in module_info.functions:
        return True

    exported_functions = _resolve_public_functions(
        module_name=module_name,
        root_package_name=root_package_name,
        module_infos=module_infos,
        seen=seen,
    )
    return function_name in exported_functions


def _is_internal_module(module_name: str, root_package_name: str) -> bool:
    """Return whether a module name belongs to the target package."""
    return module_name == root_package_name or module_name.startswith(f"{root_package_name}.")


def _is_valid_module_name(module_name: str) -> bool:
    """Return whether a dotted name is a valid Python module path."""
    return bool(module_name) and all(part.isidentifier() for part in module_name.split("."))


def _is_valid_top_level_name(name: str) -> bool:
    """Return whether a top-level metadata entry looks like a package name."""
    return bool(name) and name.isidentifier() and name.lower() not in _SKIPPED_TOP_LEVEL_NAMES


def _dedupe_preserve_order(values: Any) -> list[str]:
    """Return unique string values while preserving their first-seen order."""
    seen: set[str] = set()
    unique_values: list[str] = []

    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique_values.append(value)

    return unique_values


if __name__ == "__main__":
    public_funcs = pkg_public_func("pyufunc")
    print(public_funcs)
