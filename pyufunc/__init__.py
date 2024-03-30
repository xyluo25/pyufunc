# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# import modules with same name from different folder in python
from __future__ import absolute_import
from itertools import chain

# import all modules
from .util_ai import *  # machine learning functions
from .util_common import *  # unclassified functions are here
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

# import package configurations and utilities
from .pkg_configs import *
from .pkg_configs import FUNC_KEYWORD
from .pkg_utils import *

import pyufunc.util_ai as __util_ai
import pyufunc.util_common as __util_common
import pyufunc.util_data_processing as __util_data_processing
import pyufunc.util_datetime as __util_datetime
import pyufunc.util_fullstack as __util_fullstack
import pyufunc.util_geo as __util_geo
import pyufunc.util_git_pypi as __util_git_pypi
import pyufunc.util_gui as __util_gui
import pyufunc.util_img as __util_img
import pyufunc.util_log as __util_log
import pyufunc.util_network as __util_network
import pyufunc.util_office as __util_office
import pyufunc.util_optimization as __util_optimization
import pyufunc.util_pathio as __util_pathio
import pyufunc.util_test as __util_test
import pyufunc.util_vis as __util_vis
import pyufunc.pkg_utils as __pkg_utils

# **** specify the available utility functions by category **** #
FUNC_CATEGORY = {
    "util_ai"             : __util_ai.__all__,
    "util_common"         : __util_common.__all__,
    "util_data_processing": __util_data_processing.__all__,
    "util_datetime"       : __util_datetime.__all__,
    "util_fullstack"      : __util_fullstack.__all__,
    "util_geo"            : __util_geo.__all__,
    "util_git_pypi"       : __util_git_pypi.__all__,
    "util_gui"            : __util_gui.__all__,
    "util_img"            : __util_img.__all__,
    "util_log"            : __util_log.__all__,
    "util_network"        : __util_network.__all__,
    "util_office"         : __util_office.__all__,
    "util_optimization"   : __util_optimization.__all__,
    "util_pathio"         : __util_pathio.__all__,
    "util_test"           : __util_test.__all__,
    "util_vis"            : __util_vis.__all__,
    "pkg_utils"           : __pkg_utils.__all__ + ["show_util_func_by_category",
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

        -- util_common:
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
    for util_category in FUNC_CATEGORY:
        if FUNC_CATEGORY[util_category]:
            res_str_by_category += f"\n- {util_category}:\n"
            for func in FUNC_CATEGORY[util_category]:
                res_str_by_category += f"  - {func}\n"
                func_count += 1

    res_str = res_str_head + f" ({func_count}):\n" + res_str_by_category

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

    for func_str in list(chain.from_iterable(FUNC_CATEGORY.values())):
        prefix = func_str.split("_")[0]
        if prefix in FUNC_KEYWORD:
            FUNC_KEYWORD[prefix].append(func_str)
        else:
            FUNC_KEYWORD["non-keywords"].append(func_str)

    res_str_head = "Available utility functions in pyUFunc"
    res_str_by_keyword = ""
    func_count = 0

    for keyword in FUNC_KEYWORD:
        if FUNC_KEYWORD[keyword]:
            res_str_by_keyword += f"\n- {keyword}:\n"
            for func in FUNC_KEYWORD[keyword]:
                res_str_by_keyword += f"  - {func}\n"
                func_count += 1

    res_str = res_str_head + f" ({func_count}):\n" + res_str_by_keyword

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

    for func_str in list(chain.from_iterable(FUNC_CATEGORY.values())):
        if keyword.lower() in func_str.lower():
            res_str_by_keyword += f"  \n{func_count + 1}. {func_str}\n"
            res_str_lst.append(func_str)
            func_count += 1

    if verbose:
        res_str_head = f"Available functions by keyword: {keyword}"
        res_str = res_str_head + f" ({func_count}):\n" + res_str_by_keyword

        print(res_str)
        return ""
    return res_str_lst

__all__ = list(chain(*FUNC_CATEGORY.values()))
