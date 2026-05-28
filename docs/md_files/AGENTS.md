Task: Analyze and extend pyufunc/util_pkgs with high-value utility wrappers.

Project context:
pyufunc is intended to collect commonly used utility functions from different libraries into a single cohesive package. The goal of util_pkgs is not to duplicate entire third-party libraries. Instead, util_pkgs should provide thin, well-documented, optional-dependency wrappers around highly useful functions from mature Python utility packages.

Primary goal:
Identify useful external packages and add only the most broadly useful wrapper functions to pyufunc/util_pkgs.

Important rules:

1. Do not copy large blocks of third-party source code.
2. Do not reimplement third-party libraries.
3. Prefer thin wrappers around external packages.
4. Keep dependencies optional whenever possible.
5. Use the existing pyufunc optional-dependency pattern, such as pyufunc.util_magic.requires, if available.
6. Do not add heavy required dependencies unless clearly justified.
7. Avoid duplicating functions already implemented in existing pyufunc modules, including:
   - util_pathio
   - util_datetime
   - util_data_processing
   - util_network
   - util_office
   - util_img
   - util_log
   - util_test
   - util_vis
   - util_optimization
   - util_geo
   - util_git_pypi
8. Preserve the current project style, naming conventions, import pattern, and package structure.
9. Add one wrapper module per source package when appropriate.
10. Export public functions through util_pkgs/__init__.py and __all__.
11. Add pytest tests for each new public wrapper.
12. Add Google-style docstrings, type hints, and simple examples.
13. Prefer simple, readable logic over clever or compact code.
14. Include clear exception messages when optional dependencies are missing or inputs are invalid.
15. Do not introduce unrelated refactoring.

Standard library first:
Before adding a wrapper around an external package, check whether the Python standard library already solves the problem clearly. Prefer standard-library modules such as pathlib, os, shutil, tempfile, json, csv, sqlite3, logging, datetime, itertools, functools, subprocess, zipfile, tarfile, hashlib, uuid, glob, re, and contextlib when they are sufficient.

Candidate external packages:
Study the following packages as possible sources of useful wrapper functions. Do not implement wrappers for all packages at once. Rank them first by usefulness, overlap with existing pyufunc functions, dependency weight, maturity, and ease of maintenance.

A. Core general utility packages:

1. more-itertools
2. toolz
3. boltons
4. pydash
5. funcy
6. python-benedict
7. glom
8. humanize
9. python-slugify
10. natsort

B. Path, file, and I/O utilities:
11. platformdirs
12. filelock
13. pathspec
14. fsspec
15. smart-open
16. watchdog
17. send2trash
18. fasteners
19. atomicwrites
20. appdirs

C. Validation, configuration, and object utilities:
21. validators
22. pydantic
23. attrs
24. cattrs
25. dacite
26. PyYAML
27. ruamel.yaml
28. tomlkit
29. python-dotenv
30. dynaconf

D. Network, HTTP, API, and retry utilities:
31. requests
32. httpx
33. aiohttp
34. tenacity
35. backoff
36. websockets
37. yarl
38. urllib3
39. requests-cache
40. requests-toolbelt

E. Logging, terminal, and progress utilities:
41. loguru
42. structlog
43. python-json-logger
44. colorlog
45. rich
46. tqdm
47. alive-progress
48. tabulate

F. Datetime and human-readable formatting:
49. python-dateutil
50. dateparser
51. pendulum
52. arrow
53. tzdata
54. pytz

G. Data processing and local analytics:
55. numpy
56. pandas
57. polars
58. pyarrow
59. duckdb
60. dask

H. Database and storage utilities:
61. sqlalchemy
62. alembic
63. redis
64. pymongo
65. psycopg2-binary
66. asyncpg

I. Office, document, and PDF utilities:
67. openpyxl
68. xlsxwriter
69. python-docx
70. python-pptx
71. pypdf
72. pdfplumber

J. Image and computer-vision utilities:
73. pillow
74. imageio
75. opencv-python
76. scikit-image

K. Testing and development utilities:
77. pytest
78. pytest-cov
79. coverage
80. hypothesis
81. ruff
82. tox

L. Optimization and graph utilities:
83. scipy
84. optuna
85. pulp
86. ortools
87. cvxpy
88. networkx

M. CLI and system utilities:
89. click
90. typer
91. psutil
92. GPUtil

Priority packages for the first implementation pass:
Focus first on packages that are lightweight, broadly useful, and a strong fit for util_pkgs.

Recommended first-pass packages:

1. platformdirs
2. filelock
3. pathspec
4. more-itertools
5. humanize
6. tenacity
7. validators
8. boltons
9. toolz
10. python-benedict
11. glom
12. natsort
13. python-slugify
14. loguru
15. rich
16. tqdm
17. python-dateutil
18. dateparser
19. PyYAML
20. tomlkit

Suggested module layout:
Create or update modules under pyufunc/util_pkgs using this pattern:

pyufunc/
  util_pkgs/
    __init__.py
    _platformdirs.py
    _filelock.py
    _pathspec.py
    _more_itertools.py
    _humanize.py
    _tenacity.py
    _validators.py
    _boltons.py
    _toolz.py
    _python_benedict.py
    _glom.py
    _natsort.py
    _slugify.py
    _loguru.py
    _rich.py
    _tqdm.py
    _dateutil.py
    _dateparser.py
    _pyyaml.py
    _tomlkit.py

Function selection rules:
For each candidate package, select only functions that meet most of these criteria:

1. The function solves a common repetitive task.
2. The function is easy to explain in one sentence.
3. The wrapper reduces boilerplate for pyufunc users.
4. The wrapper has low maintenance risk.
5. The wrapper does not hide too much important behavior from the original package.
6. The wrapper does not duplicate an existing pyufunc function.
7. The wrapper can be tested with small, deterministic pytest tests.
8. The wrapper can be implemented as a thin adapter.

Suggested wrapper ideas:
For platformdirs:

- get_user_data_dir
- get_user_config_dir
- get_user_cache_dir
- get_user_log_dir

For filelock:

- with_file_lock
- safe_write_text_with_lock
- safe_write_json_with_lock
- safe_write_pickle_with_lock

For pathspec:

- load_gitignore_patterns
- is_path_ignored
- filter_paths_by_gitignore
- collect_files_excluding_gitignore

For more-itertools:

- iter_chunked
- iter_windowed
- iter_unique
- iter_flatten
- iter_split_when

For humanize:

- human_file_size
- human_time_delta
- human_number
- human_intcomma

For tenacity:

- retry_call
- retry_with_backoff
- retry_on_exception
- retry_requests_get

For validators:

- is_valid_url
- is_valid_email
- is_valid_uuid
- is_valid_ipv4
- is_valid_ipv6

For boltons:

- remap_nested_dict
- flatten_iterable
- atomic_save_file
- slugify_text
- parse_timedelta_text

For toolz:

- groupby_key
- merge_dicts
- sliding_window
- pipe_call
- count_frequencies

For python-benedict:

- dict_get_by_path
- dict_set_by_path
- dict_flatten
- dict_unflatten
- dict_to_json_safe

For glom:

- safe_glom
- nested_get
- nested_assign
- nested_delete

For natsort:

- natural_sort
- natural_sort_paths
- natural_sort_dict_keys

For python-slugify:

- slugify_filename
- slugify_column_name
- slugify_text_safe

For loguru:

- setup_simple_logger
- setup_file_logger
- disable_logger
- enable_logger

For rich:

- print_table
- print_panel
- print_json
- print_markdown

For tqdm:

- progress_iter
- progress_range
- progress_apply

For python-dateutil:

- parse_datetime_safe
- add_months
- get_month_range
- get_relative_delta

For dateparser:

- parse_human_datetime
- parse_human_date
- parse_datetime_from_text

For PyYAML:

- read_yaml
- write_yaml
- yaml_to_dict
- dict_to_yaml

For tomlkit:

- read_toml
- write_toml
- update_toml_value

Implementation pattern:
Use optional imports inside functions instead of importing optional dependencies at module import time.

Example style:

from pyufunc.util_magic import requires

@requires("platformdirs")
def get_user_cache_dir(app_name: str = "pyufunc") -> str:
    """Return the user cache directory for an application.

    Args:
        app_name: Application name used to construct the cache directory.

    Returns:
        The platform-specific user cache directory as a string.
    """
    from platformdirs import user_cache_dir

    return user_cache_dir(app_name)

Testing requirements:

1. Add tests under the existing tests structure.
2. Test normal cases and simple edge cases.
3. Skip tests gracefully when optional packages are not installed.
4. Avoid tests that require internet access unless clearly marked.
5. Avoid tests that depend on user-specific machine paths unless using tempfile.
6. Use pytest tmp_path for file-system tests.
7. Keep tests small and deterministic.

Documentation requirements:
For each new wrapper:

1. Add a clear Google-style docstring.
2. Include Args, Returns, Raises when needed, and one short example when useful.
3. Mention the source package in the docstring or module comment.
4. Do not over-document obvious code.
5. Update util_pkgs/__init__.py.
6. Update any category listing or discovery mechanism used by pyufunc.

Ranking task before coding:
Before implementation, inspect the current pyufunc/util_pkgs directory and existing utility modules. Then create a short implementation plan with:

1. Existing util_pkgs functions.
2. Duplicates to avoid.
3. Top 10 packages to implement first.
4. Suggested wrapper functions for each selected package.
5. Files to modify.
6. Tests to add.

Acceptance criteria:
The task is complete only when:

1. New wrappers are implemented with optional dependencies.
2. Public functions are exported correctly.
3. Tests pass.
4. Existing behavior is not broken.
5. No unnecessary required dependencies are added.
6. Code is readable, typed, documented, and consistent with the project style.
7. The final summary explains what was added, what was skipped, and why.
