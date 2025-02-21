# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 6th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import datetime
from typing import Union


def get_time_diff_in_unit(start_time: Union[datetime.datetime, str],
                          end_time: Union[datetime.datetime, str],
                          unit: str = "seconds") -> float:
    """Calculate the time difference between two datetime objects/strings

    Args:
        start_time (Union[datetime.datetime, str]): datetime object or string
        end_time (Union[datetime.datetime, str]): datetime object or string
        unit (str, optional): time unit to be calculated. Defaults to "seconds".

            Candidates: ["seconds", "minutes", "hours", "days", "second", "minute",

            "hour", "day", "week", "weeks", "month", "months", "year", "years"]

    Returns:
        float: the time difference in the desired unit

    Example:
        >>> from pyufunc import get_time_diff_in_unit
        >>> get_time_diff_in_unit("2024-02-06 11:11:11", "2024-02-07 11:11:11", "days")
        Time difference between 2024-02-06 11:11:11 and 2024-02-07 11:11:11: 1.0 days
        1.0 days

        >>> get_time_diff_in_unit("2024-02-06 11:11:11", "2024-02-07 11:11:11", "hours")
        Time difference between 2024-02-06 11:11:11 and 2024-02-07 11:11:11: 24.0 hours
        24.0 hours

        >>> get_time_diff_in_unit("2024-02-06 11:11:11", "2024-02-07 11:11:11", "minutes")
        Time difference between 2024-02-06 11:11:11 and 2024-02-07 11:11:11: 1440.0 minutes
        1440.0 minutes

        >>> get_time_diff_in_unit("2024-02-06 11:11:11", "2024-02-07 11:11:11", "seconds")
        Time difference between 2024-02-06 11:11:11 and 2024-02-07 11:11:11: 86400.0 seconds
        86400.0 seconds

        >>> get_time_diff_in_unit(datetime.datetime.now(), datetime.datetime.now() - datetime.timedelta(60), "day")
        Time difference between 2024-02-06 11:11:11 and 2023-12-08 11:11:11: 60.0 days
        60.0 days

    """

    # check if the start time and end time are datetime objects
    if isinstance(start_time, str):
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

    if isinstance(end_time, str):
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    # check if the start time is earlier than the end time
    if start_time > end_time:
        start_time, end_time = end_time, start_time

    # calculate the time difference
    time_diff = end_time - start_time

    # convert the time difference to the desired unit
    unit_convert_dict = {
        "seconds": time_diff.total_seconds(),
        "minutes": time_diff.total_seconds() / 60,
        "hours": time_diff.total_seconds() / 3600,
        "days": time_diff.total_seconds() / 86400,

        "second": time_diff.total_seconds(),
        "minute": time_diff.total_seconds() / 60,
        "hour": time_diff.total_seconds() / 3600,
        "day": time_diff.total_seconds() / 86400,

        "week": time_diff.total_seconds() / 604800,
        "weeks": time_diff.total_seconds() / 604800,
        "month": time_diff.total_seconds() / 2628000,
        "months": time_diff.total_seconds() / 2628000,
        "year": time_diff.total_seconds() / 31536000,
        "years": time_diff.total_seconds() / 31536000,

        "default": time_diff.total_seconds(),
    }

    unit_str = unit.lower()
    if unit_str in unit_convert_dict:
        print(f"Time difference between {start_time} and {end_time}: {unit_convert_dict[unit_str]} {unit}")
        return unit_convert_dict[unit_str]
    print(f"Warning: {unit} is not a valid unit, the default unit is seconds")
    return unit_convert_dict["default"]


def time_unit_converter(value: float, from_unit: str, to_unit: str, verbose: bool = True) -> float:
    """ Convert a time value between seconds, minutes, hours, days, years

    Args:
        value (float): The numerical value to convert.
        from_unit (str): The unit of the input value.
        to_unit (str): The desired output unit.

    Example:
        >>> from pyufunc import time_unit_converter
        >>> time_unit_converter(1, "hours", "minutes")
        60.0

    Returns:
        float: The converted value in the target unit.

    Raises:
        ValueError: If an invalid unit is provided.
    """

    # Define aliases to standardize unit names.
    unit_aliases = {
        "s": "seconds", "sec": "seconds", "secs": "seconds", "second": "seconds", "seconds": "seconds",
        "m": "minutes", "min": "minutes", "mins": "minutes", "minute": "minutes", "minutes": "minutes",
        "h": "hours", "hr": "hours", "hrs": "hours", "hour": "hours", "hours": "hours",
        "d": "days", "day": "days", "days": "days",
        "y": "years", "yr": "years", "yrs": "years", "year": "years", "years": "years",
        "season": "season", "seasons": "season",
        "quarter": "quarter", "quarters": "quarter",
        "lunar year": "lunar year", "lunar years": "lunar year"
    }

    # Conversion factors in seconds.
    conversion_factors = {
        "seconds": 1,
        "minutes": 60,                     # 60 seconds
        "hours": 3600,                     # 60 minutes * 60 seconds
        "days": 86400,                     # 24 hours * 3600 seconds
        "years": 31536000,                 # 365 days * 86400 seconds
    }

    # Normalize the provided unit strings.
    from_unit_norm = unit_aliases.get(from_unit.lower().strip())
    to_unit_norm = unit_aliases.get(to_unit.lower().strip())

    if from_unit_norm is None or to_unit_norm is None:
        raise ValueError("Invalid unit provided. Allowed units: seconds, minutes, hours, days, years, season, quarter, lunar year.")

    # Convert the input value to seconds.
    value_in_seconds = value * conversion_factors[from_unit_norm]

    # Convert from seconds to the target unit.
    result = value_in_seconds / conversion_factors[to_unit_norm]

    if verbose:
        print(f"  :{value} {from_unit_norm} is approximately {result} {to_unit_norm}")
    return result