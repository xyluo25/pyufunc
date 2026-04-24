# Changelog

All notable changes to this project will be documented in this file (v0.4.2~).

The format is based on [**Keep a Changelog**](https://keepachangelog.com/en/1.0.0/), and this project adheres to [**Semantic Versioning**](**https://semver.org/spec/v2.0.0.html**).

This is the list of changes to pyufunc between each release. For full details, see the [**Commit Logs**](https://github.com/xyluo25/pyufunc/commits/).

## [Unreleased]

Types of changes: ***Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security***

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
