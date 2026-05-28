"""
Utility packages.

This package provides adopted utility functions from various packages
"""

# TODO: add more utility packages, e.g., util_log, util_db, util_cache, etc.

# add adopted utility functions from psutil package
from ._psutil import (
    Process,
    boot_time,
    cpu_count,
    cpu_freq,
    cpu_percent,
    cpu_times,
    disk_io_counters,
    disk_usage,
    getloadavg,
    net_io_counters,
    process_iter,
    sensor_battery,
    sensor_fans,
    sensor_temperatures,
    sensors_temperatures,
    swap_memory,
    virtual_memory,
)

# add adopted utility functions from pyhelpers package
from ._pyhelpers import (
    cd,
    confirmed,
    fake_requests_headers,
    find_similar_str,
    load_data,
    load_pickle,
    merge_dicts,
    osgb36_to_wgs84,
    remove_punctuation,
    resolve_dir,
    save_data,
    save_pickle,
    update_dict_keys,
    wgs84_to_osgb36,
)

# add adopted utility functions from pyutil package
from ._pyutil import Version, log_ceil, pad_size, precondition

# add adopted utility functions from imutils package
from ._imutils import (
    auto_canny,
    grab_contours,
    is_cv2,
    is_cv3,
    is_cv4,
    opencv2matplotlib,
    resize,
    rotate,
    rotate_bound,
    skeletonize,
    translate,
    url_to_image,
)

from ._platformdirs import get_user_cache_dir, get_user_config_dir, get_user_data_dir, get_user_log_dir
from ._filelock import (
    safe_write_json_with_lock,
    safe_write_pickle_with_lock,
    safe_write_text_with_lock,
    with_file_lock,
)
from ._pathspec import (
    collect_files_excluding_gitignore,
    filter_paths_by_gitignore,
    is_path_ignored,
    load_gitignore_patterns,
)
from ._more_itertools import iter_chunked, iter_flatten, iter_split_when, iter_unique, iter_windowed
from ._humanize import human_file_size, human_intcomma, human_number, human_time_delta
from ._tenacity import retry_call, retry_on_exception, retry_with_backoff
from ._boltons import atomic_save_file, flatten_iterable, parse_timedelta_text, remap_nested_dict, slugify_text
from ._toolz import (
    toolz_count_frequencies,
    toolz_groupby_key,
    toolz_merge_dicts,
    toolz_pipe_call,
    toolz_sliding_window,
)
from ._python_benedict import dict_flatten, dict_get_by_path, dict_set_by_path, dict_to_json_safe, dict_unflatten
from ._loguru import disable_logger, enable_logger, setup_file_logger, setup_simple_logger

from .__pkg_dependents_func_usage import pkg_dependents_func_usage, save_dict_to_json
from .__pkg_public_func import pkg_public_func

__all__ = [
    # pkg_dependents_func_usage
    "pkg_dependents_func_usage",
    "save_dict_to_json",
    "pkg_public_func",
    # psutil
    "Process",
    "boot_time",
    "cpu_count",
    "cpu_freq",
    "cpu_percent",
    "cpu_times",
    "disk_io_counters",
    "disk_usage",
    "getloadavg",
    "net_io_counters",
    "process_iter",
    "sensor_battery",
    "sensor_fans",
    "sensor_temperatures",
    "sensors_temperatures",
    "swap_memory",
    "virtual_memory",
    # pyhelpers
    "cd",
    "confirmed",
    "fake_requests_headers",
    "find_similar_str",
    "load_data",
    "load_pickle",
    "merge_dicts",
    "osgb36_to_wgs84",
    "remove_punctuation",
    "resolve_dir",
    "save_data",
    "save_pickle",
    "update_dict_keys",
    "wgs84_to_osgb36",
    # pyutil
    "Version",
    "log_ceil",
    "pad_size",
    "precondition",
    # imutils
    "auto_canny",
    "grab_contours",
    "is_cv2",
    "is_cv3",
    "is_cv4",
    "opencv2matplotlib",
    "resize",
    "rotate",
    "rotate_bound",
    "skeletonize",
    "translate",
    "url_to_image",
    # platformdirs
    "get_user_cache_dir",
    "get_user_config_dir",
    "get_user_data_dir",
    "get_user_log_dir",
    # filelock
    "safe_write_json_with_lock",
    "safe_write_pickle_with_lock",
    "safe_write_text_with_lock",
    "with_file_lock",
    # pathspec
    "collect_files_excluding_gitignore",
    "filter_paths_by_gitignore",
    "is_path_ignored",
    "load_gitignore_patterns",
    # more-itertools
    "iter_chunked",
    "iter_flatten",
    "iter_split_when",
    "iter_unique",
    "iter_windowed",
    # humanize
    "human_file_size",
    "human_intcomma",
    "human_number",
    "human_time_delta",
    # tenacity
    "retry_call",
    "retry_on_exception",
    "retry_with_backoff",
    # boltons
    "atomic_save_file",
    "flatten_iterable",
    "parse_timedelta_text",
    "remap_nested_dict",
    "slugify_text",
    # toolz
    "toolz_count_frequencies",
    "toolz_groupby_key",
    "toolz_merge_dicts",
    "toolz_pipe_call",
    "toolz_sliding_window",
    # python-benedict
    "dict_flatten",
    "dict_get_by_path",
    "dict_set_by_path",
    "dict_to_json_safe",
    "dict_unflatten",
    # loguru
    "disable_logger",
    "enable_logger",
    "setup_file_logger",
    "setup_simple_logger",
]
