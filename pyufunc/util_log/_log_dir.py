# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, May 16th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import datetime
import os
from pyufunc.util_pathio._path import path2linux
from pyufunc.util_datetime._dt_format import fmt_str_to_dt, fmt_dt_to_str
from pyufunc.pkg_configs import config_datetime_fmt


def add_date_in_filename(filename: str,
                         date: str | datetime.datetime = "",
                         *,
                         dt_fmt="%Y-%m-%d",
                         as_prefix: bool = False,
                         as_suffix: bool = True,
                         verbose: bool = True) -> str:
    """Add date str in filename

    Args:
        filename (str): filename string
        date (str | datetime.datetime, optional): specify the date to add. Defaults to "".
        dt_fmt (str, optional): format the date in filename. Defaults to "%Y-%m-%d".
        as_prefix (bool, optional): if True, add date as prefix. Defaults to False.
        as_suffix (bool, optional): if True, add date as suffix. Defaults to True.
        verbose (bool, optional): if True, print out processing message. Defaults to True.

    Raises:
        ValueError: date should be str or datetime

    Returns:
        str: filename with date

    Example:
        >>> from pyufunc import add_date_in_filename
        >>> add_date_in_filename("test.txt", date="2024-05-16", as_prefix=True)
        "2024_05_16_test.txt"

        >>> add_date_in_filename("test.txt", date="2024-05-16", as_suffix=True)
        "test_2024_05_16.txt"

        >>> add_date_in_filename("test.txt", date="2024-05-16", dt_fmt="%m-%d-%Y")
        "test_05_16_2024.txt"

    """
    try:
        # check dt_fmt
        if not dt_fmt:
            dt_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

        if dt_fmt not in config_datetime_fmt.values():
            dt_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

        if date:
            # convert input date as date_str
            if isinstance(date, str):
                date_str = fmt_dt_to_str(date, dt_fmt)
            elif isinstance(date, datetime):
                date_str = date.strftime(dt_fmt)
            else:
                raise ValueError("date should be str or datetime")
        else:
            date_str = datetime.datetime.now().strftime(dt_fmt)

        date_str = date_str.replace("-", "_")

        filename_no_ext, ext = os.path.splitext(filename)
        # filename_no_ext = f"{filename_no_ext}_{date_str}"

        res_filename = f"{filename_no_ext}{ext}"

        if as_prefix:
            res_filename = f"{date_str}_{filename_no_ext}{ext}"

        if as_suffix:
            res_filename = f"{filename_no_ext}_{date_str}{ext}"

        return path2linux(res_filename)
    except Exception as e:
        print(e)
        if verbose:
            print("Could not add date in filename")
        return filename


def generate_dir_with_date(root_dir: str = "",
                           date: str | datetime.datetime = "",
                           *,
                           date_fmt: str = "%Y-%m-%d",
                           year_month_fmt: str = "%Y-%B",
                           exist_ok: bool = True) -> str:
    """Generate directory with date

    Args:
        root_dir (str, optional): specify root dir, if not specified, use current dir. Defaults to "".
        date (str | datetime.datetime, optional): specify the date. if not specified, use current date. Defaults to "".
        date_fmt (str, optional): date format. Defaults to "%Y-%m-%d".
        year_month_fmt (str, optional): year and month format. Defaults to "%Y-%B".
        exist_ok (bool, optional): whether is create direct is it's exist. Defaults to True.

    Raises:
        ValueError: date should be str or datetime

    Returns:
        str: directory string created with date
    """

    # check root directory
    if not root_dir:
        root_dir = os.getcwd()

    if not isinstance(root_dir, str):
        root_dir = os.getcwd()

    # check date format
    if not date_fmt:
        date_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

    if not isinstance(date_fmt, str):
        date_fmt = config_datetime_fmt[0]  # "%Y-%m-%d"

    # check year_month format
    if not year_month_fmt:
        year_month_fmt = config_datetime_fmt[29]  # "%Y-%m"

    if not isinstance(year_month_fmt, str):
        year_month_fmt = config_datetime_fmt[29]  # "%Y-%m"

    # create date instance
    if date:
        # convert input date as date_str
        if isinstance(date, str):
            date_ist = fmt_str_to_dt(date)
        elif isinstance(date, datetime):
            date_ist = date
        else:
            raise ValueError("date should be str or datetime")
    else:
        date_ist = datetime.datetime.now()

    # get current month and year
    current_month_year = date_ist.strftime(year_month_fmt)
    date_str = date_ist.strftime(date_fmt)

    # generate log directory
    log_dir = os.path.join(root_dir, *[current_month_year, date_str])
    log_dir_standard = path2linux(log_dir)

    # make recursive directory
    os.makedirs(log_dir_standard, exist_ok=exist_ok)
    return log_dir_standard
