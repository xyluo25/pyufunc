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
ufunc_category = {
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
    "pkg_utils"           : __pkg_utils.__all__ + ["show_util_func_by_category", "show_util_func_by_keywords"],
}


def show_util_func_by_category(verbose: bool = False) -> None:
    """show all available utility functions in pyufunc by category or by prefix keywords.

    Args:
        verbose (bool, optional): whether to return string information. Defaults to False.

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

    res_str = "Available utility functions in pyUFunc:\n"

    for util_category in ufunc_category:
        if ufunc_category[util_category]:
            res_str += f"\n- {util_category}:\n"
            for func in ufunc_category[util_category]:
                res_str += f"  - {func}\n"

    print(res_str)
    return res_str if verbose else None


def show_util_func_by_keywords(verbose: bool = False) -> None:
    """show all available utility functions in pyufunc by prefix keywords.

    Args:
        verbose (bool, optional): whether to return string information. Defaults to False.

    Examples:
        >>> import pyufunc as uf
        >>> uf.show_utility_func_by_keywords()
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

    for func_str in list(chain.from_iterable(ufunc_category.values())):
        prefix = func_str.split("_")[0]
        if prefix in ufunc_keywords:
            ufunc_keywords[prefix].append(func_str)
        else:
            ufunc_keywords["non-keywords"].append(func_str)

    res_str = "Available utility functions in pyUFunc:\n"

    for keyword in ufunc_keywords:
        if ufunc_keywords[keyword]:
            res_str += f"\n- {keyword}:\n"
            for func in ufunc_keywords[keyword]:
                res_str += f"  - {func}\n"
    print(res_str)
    return res_str if verbose else None

__all__ = list(chain(*ufunc_category.values()))
