"""
##############################################################
# Created Date: Thursday, April 23rd 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module including adopted functions from psutil package.

# The source code of psutil is available at: https://github.com/giampaolo/psutil

# Please refer to the official documentation for more details: https://psutil.readthedocs.io/en/latest/

# Original license of psutil is BSD 3-Clause License,
# and we will keep the original license and copyright notice in the adopted code.

from collections.abc import Iterator
from typing import TYPE_CHECKING
from pyufunc.util_magic import requires

if TYPE_CHECKING:
    import psutil


@requires("psutil")
def Process(pid: int | None = None) -> "psutil.Process":
    """Return a process object for a process ID.

    Args:
        pid (int | None): Process ID. If None, psutil returns the current process.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> current_process = Process()
        >>> current_process.pid > 0  # doctest: +SKIP

    Returns:
        psutil.Process: Process object for the requested process.
    """
    import psutil

    return psutil.Process(pid=pid)


@requires("psutil")
def process_iter(attrs: list[str] | None = None, ad_value=None) -> "Iterator[psutil.Process]":
    """Return an iterator over running process objects.

    Args:
        attrs (list[str] | None): Process attributes to retrieve. Defaults to None.
        ad_value: Value used for missing attributes. Defaults to None.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> processes = process_iter(attrs=["pid", "name"])
        >>> next(processes)  # doctest: +SKIP

    Returns:
        psutil.process_iter: Iterator over process objects.
    """
    import psutil

    return psutil.process_iter(attrs=attrs, ad_value=ad_value)


@requires("psutil")
def cpu_times(percpu: bool = False) -> "psutil.cpu_times":
    """Count the CPU times.

    Args:
        percpu (bool, optional): If True, return a list of CPU times for each CPU. Defaults to False.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> cpu_times()  # doctest: +SKIP

    Returns:
        psutil.cpu_times: A named tuple representing the CPU times.
    """
    import psutil

    return psutil.cpu_times(percpu=percpu)


@requires("psutil")
def cpu_count(logical: bool = True) -> int | None:
    """Return the number of logical or physical CPUs in the system.

    Args:
        logical (bool): If True, return the number of logical CPUs.
        If False, return the number of physical CPU cores. Defaults to True.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> cpu_count()  # doctest: +SKIP

    Returns:
        int: The number of logical or physical CPUs in the system.
    """
    import psutil

    return psutil.cpu_count(logical=logical)


@requires("psutil")
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

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> cpu_percent(interval=None)  # doctest: +SKIP

    Returns:
        psutil.cpu_percent: A float representing the current system-wide CPU utilization as a percentage,
        or a list of floats if percpu is True.
    """
    import psutil

    return psutil.cpu_percent(interval=interval, percpu=percpu)


@requires("psutil")
def cpu_freq(percpu: bool = False) -> "psutil.cpu_freq":
    """Return CPU frequency information.

    Args:
        percpu (bool): If True, return CPU frequency per CPU. Defaults to False.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> cpu_freq()  # doctest: +SKIP

    Returns:
        psutil.cpu_freq: CPU frequency information.
    """
    import psutil

    return psutil.cpu_freq(percpu=percpu)


@requires("psutil")
def getloadavg() -> tuple[float, float, float]:
    """Return average system load over the last 1, 5, and 15 minutes.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> getloadavg()  # doctest: +SKIP

    Returns:
        tuple[float, float, float]: System load averages.
    """
    import psutil

    return psutil.getloadavg()


@requires("psutil")
def virtual_memory(unit: str = "bytes") -> "psutil.virtual_memory":
    """Return statistics about system memory usage (RAM). All values are expressed in bytes.

    Args:
        unit (str): The unit of the returned values. Defaults to "bytes".
        - "bytes": Return values in bytes.
        - "KB": Return values in kilobytes.
        - "MB": Return values in megabytes.
        - "GB": Return values in gigabytes.
        If the unit is not recognized, it will default to "bytes".

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> virtual_memory()  # doctest: +SKIP

    Returns:
        psutil.virtual_memory: A named tuple representing the system memory usage statistics.
    """
    import psutil

    vir_mem = psutil.virtual_memory()._asdict()

    for key in vir_mem:
        if unit in {"KB", "kB", "kb", "Kb"}:
            if key == "percent":
                continue
            vir_mem[key] /= 1024
        elif unit in {"MB", "mB", "mb", "Mb"}:
            if key == "percent":
                continue
            vir_mem[key] /= 1024**2
        elif unit in {"GB", "gB", "gb", "Gb"}:
            if key == "percent":
                continue
            vir_mem[key] /= 1024**3

    return psutil._ntuples.svmem(**vir_mem)


@requires("psutil")
def swap_memory(unit: str = "bytes") -> "psutil.swap_memory":
    """Return statistics about system swap memory usage. All values are expressed in bytes.

    Args:
        unit (str): The unit of the returned values. Defaults to "bytes".
        - "bytes": Return values in bytes.
        - "KB": Return values in kilobytes.
        - "MB": Return values in megabytes.
        - "GB": Return values in gigabytes.
        If the unit is not recognized, it will default to "bytes".

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> swap_memory()  # doctest: +SKIP

    Returns:
        psutil.swap_memory: A named tuple representing the system swap memory usage statistics.
    """
    import psutil

    swap_mem = psutil.swap_memory()._asdict()

    for key in swap_mem:
        if unit in {"KB", "kB", "kb", "Kb"}:
            if key == "percent":
                continue
            swap_mem[key] /= 1024
        elif unit in {"MB", "mB", "mb", "Mb"}:
            for key in swap_mem:
                if key == "percent":
                    continue
                swap_mem[key] /= 1024**2
        elif unit in {"GB", "gB", "gb", "Gb"}:
            for key in swap_mem:
                if key == "percent":
                    continue
                swap_mem[key] /= 1024**3

    return psutil._ntuples.sswap(**swap_mem)


@requires("psutil")
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

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> disk_usage("/")  # doctest: +SKIP

    Returns:
        psutil.disk_usage: A named tuple representing the disk usage statistics for the given path.
    """
    import psutil

    disk_usage = psutil.disk_usage(path)._asdict()

    for key in disk_usage:
        if unit in {"KB", "kB", "kb", "Kb"}:
            if key == "percent":
                continue
            disk_usage[key] /= 1024
        elif unit in {"MB", "mB", "mb", "Mb"}:
            if key == "percent":
                continue
            disk_usage[key] /= 1024**2
        elif unit in {"GB", "gB", "gb", "Gb"}:
            if key == "percent":
                continue
            disk_usage[key] /= 1024**3

    return psutil._ntuples.sdiskusage(**disk_usage)


@requires("psutil")
def disk_io_counters(perdisk: bool = False, nowrap: bool = True) -> "psutil.disk_io_counters":
    """Return disk I/O statistics.

    Args:
        perdisk (bool): If True, return statistics per disk. Defaults to False.
        nowrap (bool): If True, adjust counters that wrap around. Defaults to True.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> disk_io_counters()  # doctest: +SKIP

    Returns:
        psutil.disk_io_counters: Disk I/O statistics.
    """
    import psutil

    return psutil.disk_io_counters(perdisk=perdisk, nowrap=nowrap)


@requires("psutil")
def net_io_counters(pernic: bool = False, nowrap: bool = True) -> "psutil.net_io_counters":
    """Return network I/O statistics.

    Args:
        pernic (bool): If True, return statistics per NIC. Defaults to False.
        nowrap (bool): If True, adjust counters that wrap around. Defaults to True.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> net_io_counters()  # doctest: +SKIP

    Returns:
        psutil.net_io_counters: Network I/O statistics.
    """
    import psutil

    return psutil.net_io_counters(pernic=pernic, nowrap=nowrap)


@requires("psutil")
def boot_time() -> float:
    """Return the system boot time as seconds since the epoch.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> boot_time()  # doctest: +SKIP

    Returns:
        float: System boot time as seconds since the epoch.
    """
    import psutil

    return psutil.boot_time()


@requires("psutil")
def sensor_temperatures() -> "psutil.sensors_temperatures":
    """Return hardware temperatures.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> sensor_temperatures()  # doctest: +SKIP

    Returns:
        psutil.sensors_temperatures: A dictionary where keys are sensor labels and values are lists of named tuples
        representing the temperature readings for each sensor.
    """
    import psutil

    return psutil.sensors_temperatures()


@requires("psutil")
def sensors_temperatures() -> "psutil.sensors_temperatures":
    """Return hardware temperatures.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> sensors_temperatures()  # doctest: +SKIP

    Returns:
        psutil.sensors_temperatures: Temperature sensor readings.
    """
    return sensor_temperatures()


@requires("psutil")
def sensor_fans() -> "psutil.sensors_fans":
    """Return hardware fans speed.

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> sensor_fans()  # doctest: +SKIP

    Returns:
        psutil.sensors_fans: A dictionary where keys are sensor labels and values are lists of named tuples
        representing the fan speed readings for each sensor.
    """
    import psutil

    return psutil.sensors_fans()


@requires("psutil")
def sensor_battery(time_unit: str = "seconds") -> "psutil.sensors_battery":
    """Return battery status information.

    Args:
        time_unit (str): The unit of the returned time values. Defaults to "seconds".
        - "seconds": Return time values in seconds.
        - "minutes": Return time values in minutes.
        - "hours": Return time values in hours.
        If the unit is not recognized, it will default to "seconds".

    Note:
        - Source package: ``psutil``.
        - Source repository: https://github.com/giampaolo/psutil
        - Source document: https://psutil.readthedocs.io/en/latest/
        - Source license: BSD 3-Clause License.

    Example:
        >>> sensor_battery()  # doctest: +SKIP

    Returns:
        psutil.sensors_battery: A named tuple representing the battery status information,
        or None if no battery is found.
    """
    import psutil

    battery = psutil.sensors_battery()._asdict()

    for key in battery:
        if key in ("secsleft"):
            if time_unit in {"minutes", "minute", "min", "m"}:
                battery[key] /= 60
            elif time_unit in {"hours", "hour", "h"}:
                battery[key] /= 3600

    return psutil._ntuples.sbattery(**battery)
