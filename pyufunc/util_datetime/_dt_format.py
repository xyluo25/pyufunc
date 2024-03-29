# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 6th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import datetime
from typing import Union
from pyufunc.pkg_configs import pkg_datetime_fmt


def fmt_dt_to_str(dt: Union[datetime.datetime, str] = datetime.datetime.now(),
                  format_seq: int = 1) -> str:
    """Format datetime to datetime string

    Args:
        dt (datetime, optional): the datetime to be formatted. Defaults to datetime.datetime.now().
        format_seq (int): the format of the datetime. Defaults to 0 ("%Y-%m-%d %H:%M:%S").

    See Also:
        pyufunc.pkg_configs.pkg_datetime_fmt : pre-defined datetime string formats

    Returns:
        str : the formatted datetime string

    Example:
        >>> from pyufunc import fmt_dt_to_str
        >>> fmt_dt_to_str()
        '2024-02-06 11:11:11'

        >>> fmt_dt_to_str("2024-02-06 11:11:11", 20)

    """

    # check if the dt is a string
    if isinstance(dt, str):
        # convert input datetime string to datetime object
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

    # pre-defined datetime string formats: pyufunc.pkg_configs.pkg_dt_fmt_seq
    if format_seq not in pkg_datetime_fmt:
        print("The format_seq is not valid. use format_seq = 0 as the default format: %Y-%m-%d %H:%M:%S")
        return dt.strftime(pkg_datetime_fmt[1])

    try:
        return dt.strftime(pkg_datetime_fmt[format_seq])
    except Exception as e:
        print(e)
        print("Cannot convert the datetime to the specified format. return the original datetime.")
        return dt
