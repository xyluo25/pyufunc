# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 2nd 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import itertools

from pyufunc import util_ai
from pyufunc import util_algorithm
from pyufunc import util_magic
from pyufunc import util_data_processing
from pyufunc import util_datetime
from pyufunc import util_fullstack
from pyufunc import util_geo
from pyufunc import util_git_pypi
from pyufunc import util_gui
from pyufunc import util_img
from pyufunc import util_log
from pyufunc import util_network
from pyufunc import util_office
from pyufunc import util_optimization
from pyufunc import util_pathio
from pyufunc import util_test
from pyufunc import util_vis

from .pkg_configs import config_FUNC_KEYWORD


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
    "pkg_utils": ["show_util_func_by_category",
                  "show_util_func_by_keyword",
                  "find_util_func_by_keyword"],
}


def show_util_func_by_category(verbose: bool = True) -> None:
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
        return None
    return res_str


def show_util_func_by_keyword(verbose: bool = True) -> None:
    """show all available utility functions in pyufunc by prefix keywords.

    Args:
        verbose (bool, optional): whether to print string information. Defaults to True.

    Examples:
        >>> import pyufunc as uf
        >>> uf.show_utility_func_by_keyword()
        Available utility functions in pyufunc:

        -- non-keywords:
           ** point_to_circle_on_unit_radius
           ** path2linux
           ** path2uniform
           ** import_package
           ** func_running_time
           ** requires

        -- show:
           ** show_numpy_docstring_style
           ** show_available_utility_func
    """

    # get all function names with lower case
    all_func_str = sorted(list(itertools.chain.from_iterable(
        config_FUNC_CATEGORY.values())), key=str.lower)

    # get the prefix and suffix of the function name and add them to the corresponding list
    for func_str in all_func_str:
        # get the prefix and suffix of the function name
        prefix = func_str.split("_")[0]
        suffix = func_str.split("_")[-1]

        # if the prefix is not in FUNC_KEYWORD, add it
        if prefix in config_FUNC_KEYWORD and func_str not in config_FUNC_KEYWORD[prefix]:
            config_FUNC_KEYWORD[prefix].append(func_str)
        elif suffix in config_FUNC_KEYWORD and func_str not in config_FUNC_KEYWORD[suffix]:
            config_FUNC_KEYWORD[suffix].append(func_str)

        # add gmns to the keyword list
        elif "gmns" in func_str.lower() and func_str not in config_FUNC_KEYWORD["gmns"]:
            config_FUNC_KEYWORD["gmns"].append(func_str)
        else:
            config_FUNC_KEYWORD["non-keywords"].append(func_str)

    res_str_head = "Available utility functions in pyUFunc"
    res_str_by_keyword = ""
    func_count = 0

    for keyword in config_FUNC_KEYWORD:
        if config_FUNC_KEYWORD[keyword]:
            res_str_by_keyword += f"\n- {keyword}:\n"

            # add unique function names to the string
            for func in config_FUNC_KEYWORD[keyword]:
                res_str_by_keyword += f"  - {func}\n"
                func_count += 1

    res_str = f"{res_str_head} ({func_count}):\n{res_str_by_keyword}"

    if verbose:
        print(res_str)
        return None
    return res_str


def find_util_func_by_keyword(keyword: str, verbose: bool = True) -> list:
    """find all available utility functions in pyufunc by keyword.

    Args:
        keyword (str): the keyword
        verbose (bool, optional): whether to print string information. Defaults to True.

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
        return ""
    return res_str_lst
