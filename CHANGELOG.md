# Changelog

All notable changes to this project will be documented in this file (v0.4.2~).

The format is based on [**Keep a Changelog**](https://keepachangelog.com/en/1.0.0/), and this project adheres to [**Semantic Versioning**](https://semver.org/spec/v2.0.0.html).

This is the list of changes to pyufunc between each release. For full details, see the [**Commit Logs**](https://github.com/xyluo25/pyufunc/commits/).

## [Unreleased]

Types of changes: ***Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security***

## [0.5.1] - 2026-05-28

This release summarizes changes since `v0.4.5`.

### Added

- Add selected `util_pkgs` wrappers for `psutil`, `pyhelpers`, `pyutil`, `imutils`, `platformdirs`, `filelock`, `pathspec`, `more-itertools`, `humanize`, `tenacity`, `boltons`, `toolz`, `python-benedict`, and `loguru`.
- Add package inspection helpers, including `pkg_public_func`, `pkg_dependents_func_usage`, and `save_dict_to_json`.
- Add exploratory dependent-usage JSON datasets under `datasets/util_pkgs_dependents_func_usage`.
- Add `THIRD_PARTY_LICENSES.md` and package metadata links for third-party license information.
- Add `PACKAGE_CLAIMS.md` to document supported claims, evidence sources, claim boundaries, and tradeoffs.
- Add ReadTheDocs API references for selected third-party wrappers and third-party license documentation.
- Add a custom autosummary class template for generated class API pages.

### Changed

- Keep optional dependency installation disabled by default in `import_package`; users must pass `auto_install=True` to run pip automatically.
- Update `requires` so missing dependencies are reported without installing packages unless `auto_install=True` is explicitly passed.
- Update README and documentation language to use objective, evidence-bounded claims instead of broad statements such as "widely used" or general performance improvement.
- Update utility package review documentation with PyPI version badges, download badges, latest-commit badges, repository links, package licenses, and selected package metadata.
- Update generated utility indexes for function categories and keyword search.
- Update Ruff configuration to use Google-style docstring checks.
- Update package metadata for version `0.5.1`, the revised project description, and third-party license file inclusion.

### Removed

- Remove obsolete public utility categories from package exports and documentation, including `util_dababase`, `util_fullstack`, `util_gui`, `util_optimization`, and `util_vis`.
- Remove unused optional placeholder modules for AI, office, testing, visualization, and optimization helpers that are not part of the maintained public API.

### Fixed

- Ensure `@requires(..., verbose=False)` still skips wrapped functions when required dependencies are missing.
- Preserve wrapped function metadata in `requires` by using `functools.wraps`.
- Fix ReadTheDocs autodoc and docutils warnings from generated `__init__` method pages, stale API references, and malformed docstring markup.
- Fix stale `show_public_func` references by using `pkg_public_func`.
- Fix documentation links and malformed MyST markup in release notes.
- Expand tests for optional dependency handling, removed public packages, package inspection helpers, selected third-party wrappers, and existing utility behavior.

### Security

- Disable automatic installation of missing dependencies by default to avoid unexpected package installation in CI, offline, or security-sensitive environments.

## [0.4.5] - 2026-05-26

### Changed

- Move package configuration from `cfg.py` to `__cfg.py` and update imports.
- Continue standardizing utility function docstrings, formatting, and input validation.
- Update utility modules across data processing, datetime, geo, GitHub/PyPI, image, magic, office, path/IO, and package-wrapper helpers.
- Update project packaging files and dependency lock data for the release.

### Fixed

- Fix package import and utility discovery behavior after the configuration module rename.
- Improve test coverage for core utilities, path/IO helpers, and list helper behavior.

## [0.4.3] - 2026-04-24

### Added

- Add `CONTRIBUTING.md` with contribution guidelines.
- Add `requirements_dev.txt` for development and documentation dependencies.
- Add `tests/test_core_utilities.py` and additional tests to improve package coverage.
- Add `util_pkgs` utilities adopted from `psutil`, including CPU, memory, disk, swap, and sensor helpers.
- Add documentation entries for new utility functions, including `get_active_python_env`, OSM helpers, `github_private_file_downloader`, and `time_str_to_seconds`.
- Add release notes assets and restructure release notes under `docs/source/release_notes`.

### Changed

- Update `requires` and `import_package` behavior to avoid installing optional dependencies unless the user explicitly opts in.
- Refactor package initialization and utility references for cleaner function discovery.
- Rename `pkg_configs.py` to `cfg.py` and update configuration imports.
- Update README examples, badges, links, and documentation structure.
- Move package metadata to the modern `pyproject.toml` build configuration and remove legacy setup usage.
- Reformat and refactor utility modules across AI, datetime, geo, git/PyPI, image, magic, office, path/IO, and testing helpers.
- Update documentation generation and API reference pages for the revised package layout.

### Removed

- Remove legacy `setup.py`.
- Remove the legacy `pyufunc/__init.py` file.
- Remove the old `pkg_utils` reference page in favor of `cfg`.
- Remove obsolete logging helper modules, including `_lg_datetime.py`, `_lg_logger.py`, `_lg_rotate_file_writer.py`, `_lg_stream.py`, and `_log_writer.py`.
- Remove `docs/source/how_to_guide` pages that were superseded by the new documentation layout.
- Remove pinned runtime dependencies from `requirements.txt`.

### Fixed

- Fix import failures after installation by removing top-level optional dependency imports.
- Fix circular-import risk around `pyufunc.util_magic.requires` by decoupling low-level import helpers from `util_data_processing`.
- Fix optional pandas, numpy, and shapely imports so `pyufunc` can import without those packages installed.
- Fix class-level `@requires` usage that could replace classes with dependency placeholder functions.
- Fix submodule dependency on `from pyufunc import requires` by importing the decorator directly.
- Fix README links and badge formatting.

## [0.4.2] - 2026-03-23

### Changed

- Disable auto-install of required packages, instead, will print out the message to remind user on missing dependency.
- Restructure the package loading for better function reference

### Fixed

- On initial installation of the package, the package will not install 'potential' dependencies until user run the specific function.

### Removed

- pkg_util removed and implemented in \_\_init__.py instead.
- removed show_util_func_by_keyword function

## [0.4.1] - 2025-07-29

### Added

- Add `pyufunc.find_executable_from_PATH_on_linux` as a new function to find an executable in the system PATH on Linux
- Enhance `pyufunc.gmns_real_link` print out message when the link is not found in the GMNS data
- Add `pyufunc.github_private_file_downloader` as a new function to download a private file from GitHub using a personal access token
- Add `pyufunc.time_str_to_seconds` as a new function to convert a time string in the format "HH:MM:SS" to seconds
- Add `pyufunc.cvt_py_to_dll` as a new function to convert a Python file to a DLL file using Cython
- Add `pyufunc.time_unit_converter` as a new function to convert time units between different formats (e.g., seconds, minutes, hours)
- Add `pyufunc.calc_distance_on_unit_haversine` as a new function to calculate the distance between two points on a unit sphere using the haversine formula
