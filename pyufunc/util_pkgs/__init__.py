
"""
Utility packages.

This package provides adopted utility functions from various packages
"""

# TODO: add more utility packages, e.g., util_log, util_db, util_cache, etc.

# add adopted utility functions from psutil package
from ._psutil import (cpu_count, cpu_times, cpu_percent,
                      virtual_memory, swap_memory,
                      disk_usage,
                      sensor_temperatures, sensor_fans, sensor_battery)

from .__pkg_dependents_func_usage import pkg_dependents_func_usage, save_dict_to_json

__all__ = [
    # pkg_dependents_func_usage
    "pkg_dependents_func_usage", "save_dict_to_json",

    # psutil
    "cpu_count", "cpu_times", "cpu_percent",
    "virtual_memory", "swap_memory",
    "disk_usage",
    "sensor_temperatures", "sensor_fans", "sensor_battery",
]
