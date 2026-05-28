# Package Claims and Evidence

This file records the claims pyufunc documentation should make, the evidence that
supports those claims, and claims that should be avoided unless stronger evidence
is added.

## Supported Claims

- pyufunc exposes a categorized collection of Python utility functions.
  - Evidence: `pyufunc.show_util_func_by_category(verbose=False)` reports 254 public utility entries in the current source tree.
  - Evidence: `docs/md_files/utility_function_by_category.md` and `docs/md_files/utility_function_by_keyword.md` are generated indexes of that public API.

- pyufunc includes wrappers around selected third-party utility packages.
  - Evidence: `pyufunc/util_pkgs/__init__.py` exports 94 entries from `util_pkgs`.
  - Evidence: third-party wrapper docstrings include source package, source repository, source documentation, source license, examples, and return descriptions.
  - Evidence: `THIRD_PARTY_LICENSES.md` summarizes third-party packages used by optional wrappers and optional helper functions.

- Package selection is informed by public package metadata and exploratory usage scans.
  - Evidence: `docs/md_files/utility_function_pkg_review.md` records PyPI version badges, PyPI download badges where available, GitHub latest-commit badges, repository links, and package descriptions.
  - Evidence: `datasets/util_pkgs_dependents_func_usage` contains JSON outputs from exploratory GitHub dependent scans for 16 packages.

- Some reviewed packages have observed dependent usage in the local scan data.
  - Evidence: `datasets/util_pkgs_dependents_func_usage/psutil.json` currently records 35 valid function references across 5 dependent repositories. Observed references include `virtual_memory`, `cpu_percent`, `Process`, `disk_usage`, `net_io_counters`, `cpu_count`, and `swap_memory`.
  - Evidence: `datasets/util_pkgs_dependents_func_usage/pyhelpers.json` currently records 175 valid function references across 4 dependent repositories. Observed references include `ops.confirmed`, `text.find_similar_str`, `store.load_pickle`, `store.save_pickle`, `dirs.cd`, `store.load_data`, `dirs.resolve_dir`, `ops.fake_requests_headers`, and `store.save_data`.
  - Evidence: `datasets/util_pkgs_dependents_func_usage/pyutil.json` currently records 20 valid function references across 13 dependent repositories. Observed references include `version_class.Version`, `mathutil.pad_size`, `assertutil.precondition`, and `mathutil.log_ceil`.

## Claim Boundaries

- Do not claim that all pyufunc functions are "widely used".
  - Reason: the local dependent scans are incomplete and several package scans show no observed references or were limited by GitHub rate limits.

- Do not claim that pyufunc consolidates "the most frequently used" utility functions unless a defined frequency metric and dataset are provided.
  - Reason: PyPI downloads, GitHub latest-commit badges, and partial dependent scans are useful signals, but they do not prove package-wide function frequency.

- Do not claim general performance improvement.
  - Reason: pyufunc currently provides utility functions and wrappers, not a benchmark suite comparing pyufunc functions against alternative implementations.

- Do not use promotional claims such as "remarkable", "go-to", "robust", "all-inclusive", or "let pyufunc take care of repetitive tasks" in academic or evidence-oriented documentation.
  - Reason: these terms are subjective and not tied to measurable evaluation criteria.

## Tradeoffs to Mention

- A larger utility namespace can increase search and selection overhead.
- Optional wrappers may require users to install additional dependencies.
- Centralized utility collections require ongoing maintenance for attribution, licensing, tests, and compatibility.
- Project-specific helper code can be more appropriate when behavior is domain-specific or when adding a package dependency is not justified.
