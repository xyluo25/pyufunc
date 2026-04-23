'''
##############################################################
# Created Date: Thursday, April 23rd 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

# This module including adopted functions from psutil package.

# The source code of psutil is available at: https://github.com/giampaolo/psutil

# Please refer to the official documentation for more details: https://psutil.readthedocs.io/en/latest/

# Original license of psutil is BSD 3-Clause License,
# and we will keep the original license and copyright notice in the adopted code.

from typing import TYPE_CHECKING
from pyufunc.util_magic import requires

if TYPE_CHECKING:
    import psutil


@requires('psutil')
def cpu_times(percpu: bool = False) -> "psutil.cpu_times":
    """Count the CPU times.

    Args:
        percpu (bool, optional): If True, return a list of CPU times for each CPU. Defaults to False.

    Notes:
        - This function is adopted from psutil.cpu_times().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#cpu

    Returns:
        psutil.cpu_times: A named tuple representing the CPU times.
    """

    import psutil
    return psutil.cpu_times(percpu=percpu)


@requires('psutil')
def cpu_count(logical: bool = True) -> int:
    """Return the number of logical or physical CPUs in the system.

    Args:
        logical (bool): If True, return the number of logical CPUs.
            If False, return the number of physical CPU cores. Defaults to True.

    Notes:
        - This function is adopted from psutil.cpu_count().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#cpu

    Returns:
        int: The number of logical or physical CPUs in the system.
    """

    import psutil
    return psutil.cpu_count(logical=logical)


@requires('psutil')
def cpu_percent(interval: float = None, percpu: bool = False) -> "psutil.cpu_percent":
    """Return a float representing the current system-wide CPU utilization as a percentage.

    Args:
        interval (float): The interval in seconds to wait before calculating the CPU utilization. Defaults to None.
            If interval is > 0.0, measures CPU times before and after the interval (blocking).
            If 0.0 or None, returns the utilization since the last call or module import, returning immediately.
            That means the first time this is called and return a meaningless 0.0 value (supposed to ignore).
            In this case it is recommended for accuracy that this function
            be called with at least 0.1 seconds between calls.
        percpu (bool): If True, returns a list of floats representing each logical CPU. Defaults to False.
    Notes:
        - This function is adopted from psutil.cpu_percent().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#cpu
    Returns:
        psutil.cpu_percent: A float representing the current system-wide CPU utilization as a percentage,
            or a list of floats if percpu is True.
    """

    import psutil
    return psutil.cpu_percent(interval=interval, percpu=percpu)


@requires('psutil')
def virtual_memory(unit: str = "bytes") -> "psutil.virtual_memory":
    """Return statistics about system memory usage (RAM). All values are expressed in bytes.

    Args:
        unit (str): The unit of the returned values. Defaults to "bytes".
            - "bytes": Return values in bytes.
            - "KB": Return values in kilobytes.
            - "MB": Return values in megabytes.
            - "GB": Return values in gigabytes.
            If the unit is not recognized, it will default to "bytes".

    Notes:
        - This function is adopted from psutil.virtual_memory().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#memory
    Returns:
        psutil.virtual_memory: A named tuple representing the system memory usage statistics.
    """
    import psutil
    vir_mem = psutil.virtual_memory()._asdict()

    if unit in ("KB", "kB", "kb", "Kb"):
        for key in vir_mem:
            if key == "percent":
                continue
            vir_mem[key] /= 1024
    elif unit in ("MB", "mB", "mb", "Mb"):
        for key in vir_mem:
            if key == "percent":
                continue
            vir_mem[key] /= (1024 ** 2)
    elif unit in ("GB", "gB", "gb", "Gb"):
        for key in vir_mem:
            if key == "percent":
                continue
            vir_mem[key] /= (1024 ** 3)

    return psutil._ntuples.svmem(**vir_mem)


@requires('psutil')
def swap_memory(unit: str = "bytes") -> "psutil.swap_memory":
    """Return statistics about system swap memory usage. All values are expressed in bytes.

    Args:
        unit (str): The unit of the returned values. Defaults to "bytes".
            - "bytes": Return values in bytes.
            - "KB": Return values in kilobytes.
            - "MB": Return values in megabytes.
            - "GB": Return values in gigabytes.
            If the unit is not recognized, it will default to "bytes".

    Notes:
        - This function is adopted from psutil.swap_memory().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#memory
    Returns:
        psutil.swap_memory: A named tuple representing the system swap memory usage statistics.
    """

    import psutil
    swap_mem = psutil.swap_memory()._asdict()

    if unit in ("KB", "kB", "kb", "Kb"):
        for key in swap_mem:
            if key == "percent":
                continue
            swap_mem[key] /= 1024
    elif unit in ("MB", "mB", "mb", "Mb"):
        for key in swap_mem:
            if key == "percent":
                continue
            swap_mem[key] /= (1024 ** 2)
    elif unit in ("GB", "gB", "gb", "Gb"):
        for key in swap_mem:
            if key == "percent":
                continue
            swap_mem[key] /= (1024 ** 3)

    return psutil._ntuples.sswap(**swap_mem)


@requires('psutil')
def disk_usage(path: str = "/", *, unit: str = "bytes") -> "psutil.disk_usage":
    """Return disk usage statistics about the given path as a named tuple including total, used and free space.

    Args:
        path (str): The path to check the disk usage for. Defaults to "/".
        unit (str): The unit of the returned values. Defaults to "bytes".
            - "bytes": Return values in bytes.
            - "KB": Return values in kilobytes.
            - "MB": Return values in megabytes.
            - "GB": Return values in gigabytes.
            If the unit is not recognized, it will default to "bytes".

    Notes:
        - This function is adopted from psutil.disk_usage().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#disks
    Returns:
        psutil.disk_usage: A named tuple representing the disk usage statistics for the given path.
    """

    import psutil
    disk_usage = psutil.disk_usage(path)._asdict()

    if unit in ("KB", "kB", "kb", "Kb"):
        for key in disk_usage:
            if key == "percent":
                continue
            disk_usage[key] /= 1024
    elif unit in ("MB", "mB", "mb", "Mb"):
        for key in disk_usage:
            if key == "percent":
                continue
            disk_usage[key] /= (1024 ** 2)
    elif unit in ("GB", "gB", "gb", "Gb"):
        for key in disk_usage:
            if key == "percent":
                continue
            disk_usage[key] /= (1024 ** 3)

    return psutil._ntuples.sdiskusage(**disk_usage)


@requires('psutil')
def sensor_temperatures() -> "psutil.sensors_temperatures":
    """Return hardware temperatures.

    Notes:
        - This function is adopted from psutil.sensors_temperatures().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#sensors
    Returns:
        psutil.sensors_temperatures: A dictionary where keys are sensor labels and values are lists of named tuples
            representing the temperature readings for each sensor.
    """
    import psutil
    return psutil.sensors_temperatures()


@requires('psutil')
def sensor_fans() -> "psutil.sensors_fans":
    """Return hardware fans speed.

    Notes:
        - This function is adopted from psutil.sensors_fans().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#sensors

    Returns:
        psutil.sensors_fans: A dictionary where keys are sensor labels and values are lists of named tuples
            representing the fan speed readings for each sensor.
    """
    import psutil
    return psutil.sensors_fans()


@requires('psutil')
def sensor_battery(time_unit: str = "seconds") -> "psutil.sensors_battery":
    """Return battery status information.

    Args:
        time_unit (str): The unit of the returned time values. Defaults to "seconds".
            - "seconds": Return time values in seconds.
            - "minutes": Return time values in minutes.
            - "hours": Return time values in hours.
            If the unit is not recognized, it will default to "seconds".

    Notes:
        - This function is adopted from psutil.sensors_battery().
        - the original license of psutil is BSD 3-Clause License, and we will keep the license in our project.
        - For more details, please refer to the official documentation:
            https://psutil.readthedocs.io/latest/api.html#sensors
    Returns:
        psutil.sensors_battery: A named tuple representing the battery status information,
            or None if no battery is found.
    """
    import psutil
    battery = psutil.sensors_battery()._asdict()

    for key in battery:
        if key in ("secsleft"):
            if time_unit in ("minutes", "minute", "min", "m"):
                battery[key] /= 60
            elif time_unit in ("hours", "hour", "h"):
                battery[key] /= 3600

    return psutil._ntuples.sbattery(**battery)
