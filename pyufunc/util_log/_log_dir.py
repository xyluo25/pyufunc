# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, May 16th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from datetime import datetime as dt
import datetime
import os
from pyufunc.util_pathio._path import path2linux
from pyufunc.util_datetime._dt_format import fmt_str_to_dt, fmt_dt_to_str
from pyufunc.pkg_configs import config_datetime_fmt


def add_date_in_filename(filename: str,
                         date: str | dt = "",
                         format="%Y-%m-%d",
                         as_prefix: bool = False,
                         as_suffix: bool = True,
                         verbose: bool = True) -> str:
    try:
        if date:
            # convert input date as date_str
            if isinstance(date, str):
                date_str = fmt_dt_to_str(date, )
            elif isinstance(date, datetime):
                date_str = date.strftime(format)
            else:
                raise ValueError("date should be str or datetime")
        else:
            date_str = datetime.datetime.now().strftime(format)

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


def generate_log_dir_with_date(root_dir: str,
                               date: str | dt = "",
                               date_fmt: str = "%Y-%m-%d",
                               exist_ok: bool = True):

    if date:
        # convert input date as date_str
        if isinstance(date, str):
            date_ist = fmt_str_to_dt(date)
        elif isinstance(date, datetime):
            date_ist = date
        else:
            raise ValueError("date should be str or datetime")
    else:
        date_ist = datetime.now()

    current_month_year = date_ist.strftime("%Y-%B")
    date_str = date_ist.strftime(date_fmt)

    # generate log directory
    log_dir = os.path.join(root_dir, *[current_month_year, date_str])
    log_dir_standard = path2linux(log_dir)

    # make recursive directory
    os.makedirs(log_dir_standard, exist_ok=exist_ok)
    return log_dir_standard
