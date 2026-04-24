# Changelog

All notable changes to this project will be documented in this file (v0.4.2~).

The format is based on [**Keep a Changelog**](https://keepachangelog.com/en/1.0.0/), and this project adheres to [**Semantic Versioning**](**https://semver.org/spec/v2.0.0.html**).

This is the list of changes to pyufunc between each release. For full details, see the [**Commit Logs**](https://github.com/xyluo25/pyufunc/commits/).

## [Unreleased] - 2026-04-24

Types of changes: ***Added**, **Changed**, **Deprecated**, **Removed**, **Fixed**, **Security***

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
