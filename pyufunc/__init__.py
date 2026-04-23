"""
# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
"""

import sys
import itertools

from .util_ai import *  # machine learning functions
from .util_algorithm import *  # algorithm functions
from .util_magic import *  # unclassified functions are here
from .util_data_processing import *  # data processing functions including algorithms
from .util_datetime import *  # datetime functions
from .util_fullstack import *  # fullstack functions, including front end and back end
from .util_geo import *  # geographic functions
from .util_git_pypi import *  # git and pypi functions
from .util_gui import *  # GUI functions
from .util_img import *  # image functions
from .util_log import *  # logging functions
from .util_network import *  # network functions
from .util_office import *  # office functions
from .util_optimization import *  # optimization functions
from .util_pathio import *  # path and IO functions
from .util_test import *  # test functions
from .util_vis import *  # visualization functions

# import adopted functions from other packages
from .util_pkgs import *

__version__ = "0.4.2"
__name__ = "pyufunc"
__author__ = "Mr. Xiangyong Luo, Dr. Xuesong Simon Zhou"
__email__ = "luoxiangyong01@gmail.com"


def show_util_func_by_category(verbose: bool = True) -> dict:
    """show all available utility functions in pyufunc by category or by prefix keywords.

    Args:
        verbose (bool, optional): whether to print out information. Defaults to True.

    Examples:
        >>> import pyufunc as uf
        >>> uf.show_utility_func_by_category()
        Available utility functions in pyufunc:

        -- util_magic:
           ** show_supported_docstring_header
           ** show_google_docstring_style
           ** show_numpy_docstring_style
           ** generate_password

        -- util_datetime:
           ** fmt_dt_to_str
           ** fmt_dt
           ** list_all_timezones
           ** get_timezone
           ** cvt_dt_to_tz
           ** get_time_diff_in_unit
    """
    # import package configurations and utilities
    from . import (
        util_ai,
        util_algorithm,
        util_magic,
        util_data_processing,
        util_datetime,
        util_fullstack,
        util_geo,
        util_git_pypi,
        util_gui,
        util_img,
        util_log,
        util_network,
        util_office,
        util_optimization,
        util_pathio,
        util_test,
        util_vis,
        util_pkgs,
    )

    config_FUNC_CATEGORY = {
        "util_ai": util_ai.__all__,
        "util_algorithm": util_algorithm.__all__,
        "util_magic": util_magic.__all__,
        "util_data_processing": util_data_processing.__all__,
        "util_datetime": util_datetime.__all__,
        "util_fullstack": util_fullstack.__all__,
        "util_geo": util_geo.__all__,
        "util_git_pypi": util_git_pypi.__all__,
        "util_gui": util_gui.__all__,
        "util_img": util_img.__all__,
        "util_log": util_log.__all__,
        "util_network": util_network.__all__,
        "util_office": util_office.__all__,
        "util_optimization": util_optimization.__all__,
        "util_pathio": util_pathio.__all__,
        "util_test": util_test.__all__,
        "util_vis": util_vis.__all__,
        "util_pkgs": util_pkgs.__all__,
        "pkg_utils": ["show_util_func_by_category",
                      "show_util_func_by_keyword",
                      "find_util_func_by_keyword"],
    }

    res_str_head = "Available utility functions in pyUFunc"
    res_str_by_category = ""
    func_count = 0
    for util_category in config_FUNC_CATEGORY:
        if config_FUNC_CATEGORY[util_category]:
            res_str_by_category += f"\n- {util_category}:\n"
            for func in sorted(config_FUNC_CATEGORY[util_category], key=str.lower):
                res_str_by_category += f"  - {func}\n"
                func_count += 1

    res_str = f"{res_str_head} ({func_count}):\n{res_str_by_category}"

    if verbose:
        print(res_str)
        return
    return config_FUNC_CATEGORY


def find_util_func_by_keyword(keyword: str = None, verbose: bool = True) -> list:
    """find all available utility functions in pyufunc by keyword.

    Args:
        keyword (str): the keyword in the utility function.
            if keyword is empty, it will return total number of utility functions in pyufunc.
            - Recommended keyword include:
                cvt: convert or conversion
                fmt: format or formatting
                is: check if something is something else, e.g., is_digit
                calc: calculate or calculation
                get: get or obtain something
                show: show or display something
                generate: generate or creation
                create: create or construction
                find: find or search something
                run: run or execute something
                group: group or clustering something
                check: check or validation something
                validate: validate or verification something
                list: list or enumeration something
                img: image processing related functions
                split: split or segmentation something
                proj: projection related functions
                github: functions related to github
                pypi: functions related to pypi
                error: functions related to error handling
                algo: functions related to algorithms
                gmns: functions related to General Modeling Network Specification
                pytest: functions related pytest usage

        verbose (bool): whether to print string information. Defaults to True.

    Returns:
        list: if verbose is True, print the result string; otherwise return the result list.

    Examples:
        >>> import pyufunc as uf
        >>> uf.find_func_by_keyword("show")
        Available functions by keyword: show
           - show_numpy_docstring_style
           - show_available_utility_func
           ...
    """
    # get all functions by category
    config_FUNC_CATEGORY = show_util_func_by_category(verbose=False)

    # if keyword is empty, return total number of utility functions in pyufunc
    if keyword is None or keyword.strip() == "":
        total_func_count = sum(len(func_lst) for func_lst in config_FUNC_CATEGORY.values())
        res_str = f"Total number of utility functions in pyufunc: {total_func_count}"
        if verbose:
            print(res_str)
        return res_str

    # find all functions that contain the keyword in their name (case-insensitive)
    res_str_by_keyword = ""
    res_str_lst = []
    func_count = 0

    for func_str in list(itertools.chain.from_iterable(config_FUNC_CATEGORY.values())):
        if keyword.lower() in func_str.lower():
            res_str_by_keyword += f"  \n{func_count + 1}. {func_str}\n"
            res_str_lst.append(func_str)
            func_count += 1

    if verbose:
        res_str_head = f"Available functions by keyword: {keyword}"
        res_str = f"{res_str_head} ({func_count}):\n{res_str_by_keyword}"
        print(res_str)
    return res_str_lst


def __check_python_version(min_version: str = "3.10") -> tuple:
    # Split the version string and convert to tuple of integers
    version_tuple = tuple(map(int, sys.version.split()[0].split('.')))

    # Check if the version is greater than or equal to the minimum version required
    major, minor = min_version.split(".")
    try:
        if version_tuple < (int(major), int(minor)):
            raise EnvironmentError(
                f"Python version {min_version} or higher is required.")
    except Exception:
        print(f"pyufunc supports Python {min_version} or higher.")
    return version_tuple

__check_python_version()

# __all__ = [func for fn_lst in list(config_FUNC_CATEGORY.values()) for func in fn_lst]