# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 6th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Union
from pyufunc.pkg_configs import config_datetime_fmt
from pyufunc.util_common import requires, import_package

if TYPE_CHECKING:
    import dateutil


@requires(("python-dateutil", "dateutil"))
def fmt_dt_to_str(dt: Union[datetime.datetime, str] = "",
                  dt_fmt: str = "") -> str:
    """Format datetime to datetime string

    Args:
        dt (datetime, str): the datetime to be formatted. Defaults to datetime.datetime.now().
        dt_fmt (int): the format of the datetime. Defaults ("%Y-%m-%d %H:%M:%S").

    See Also:
        pyufunc.pkg_configs.config_datetime_fmt : pre-defined datetime string formats

    Returns:
        str : the formatted datetime string

    Example:
        >>> from pyufunc import fmt_dt_to_str
        >>> fmt_dt_to_str()
        '2024-02-06'

        >>> fmt_dt_to_str(df_fmt="%Y/%m/%d %H:%M:%S")
        '2024/02/06 00:00:00'

        >>> fmt_dt_to_str("2024-02-06", df_fmt="%Y/%m/%d")
        '2024/02/06'

        >>> fmt_dt_to_str("2024-02-06", df_fmt="%Y/%m/%d %H:%M:%S")
        '2024/02/06 00:00:00'

        >>> fmt_dt_to_str(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
        '2024/02/06 11:11:11'
    """
    import_package(("python-dateutil", "dateutil"))
    import dateutil

    # if the dt is empty, use the current datetime
    if not dt:
        dt = datetime.datetime.now()

    # check if the dt is a string, if yes, convert it to datetime object
    if isinstance(dt, str):
        try:
            dt = dateutil.parser.parse(dt)
        except Exception as e:
            print(e)
            print(f"Cannot convert {dt} to datetime object. return the original value.")
            return dt

    # check if the input format is valid
    if not isinstance(dt, (datetime.datetime, str)):
        # convert input datetime string to datetime object
        print(f"The {dt} is not a str or datetime object. return the original value.")
        return dt

    # check if the input format is valid
    if not isinstance(dt_fmt, str):
        # use default format
        dt_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

    if dt_fmt not in config_datetime_fmt.values():
        dt_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

    print("type dt", type(dt))
    try:
        return dt.strftime(dt_fmt)
    except Exception as e:
        print(e)
        print("Cannot convert the datetime to the specified format. return the original datetime.")
        return dt


@requires(("python-dateutil", "dateutil"))
def fmt_str_to_dt(dt_str: str) -> datetime.datetime:
    """Format datetime string to datetime

    Args:
        dt_str (str): the datetime string to be formatted.

    See Also:
        pyufunc.pkg_configs.config_datetime_fmt : pre-defined datetime string formats

    Returns:
        datetime.datetime : the formatted datetime

    Example:
        >>> from pyufunc import fmt_str_to_dt
        >>> fmt_str_to_dt("2024-02-06 11:11:11")
        datetime.datetime(2024, 2, 6, 11, 11, 11)

    """
    # import dateutil
    import_package(("python-dateutil", "dateutil"))
    import dateutil

    # check if the dt is a string
    if not isinstance(dt_str, str):
        print("The input datetime is not a str. return the original input.")
        return dt_str

    return dateutil.parser.parse(dt_str)
