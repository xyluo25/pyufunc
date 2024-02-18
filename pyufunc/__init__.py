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

import pyufunc.util_ai as util_ai
import pyufunc.util_common as util_common
import pyufunc.util_data_processing as util_data_processing
import pyufunc.util_datetime as util_datetime
import pyufunc.util_fullstack as util_fullstack
import pyufunc.util_geo as util_geo
import pyufunc.util_git_pypi as util_git_pypi
import pyufunc.util_gui as util_gui
import pyufunc.util_img as util_img
import pyufunc.util_log as util_log
import pyufunc.util_network as util_network
import pyufunc.util_office as util_office
import pyufunc.util_optimization as util_optimization
import pyufunc.util_pathio as util_pathio
import pyufunc.util_test as util_test
import pyufunc.util_vis as util_vis
import pyufunc.pkg_utils as pkg_utils

# **** specify the available utility functions by category **** #
ufunc_category = {
    "util_ai"             : util_ai.__all__,
    "util_common"         : util_common.__all__,
    "util_data_processing": util_data_processing.__all__,
    "util_datetime"       : util_datetime.__all__,
    "util_fullstack"      : util_fullstack.__all__,
    "util_geo"            : util_geo.__all__,
    "util_git_pypi"       : util_git_pypi.__all__,
    "util_gui"            : util_gui.__all__,
    "util_img"            : util_img.__all__,
    "util_log"            : util_log.__all__,
    "util_network"        : util_network.__all__,
    "util_office"         : util_office.__all__,
    "util_optimization"   : util_optimization.__all__,
    "util_pathio"         : util_pathio.__all__,
    "util_test"           : util_test.__all__,
    "util_vis"            : util_vis.__all__,
    "pkg_utils"           : pkg_utils.__all__ + ["show_util_func_by_category", "show_util_func_by_keywords"],
}


def show_util_func_by_category() -> None:
    """show all available utility functions in pyufunc by category or by prefix keywords.

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

    # print all available utility functions
    print("Available utility functions in pyUFunc:")

    def _print_func(func_list: list):
        for func in func_list:
            print(f"  - {func}")

    for util_category in ufunc_category:
        if ufunc_category[util_category]:
            print(f"- {util_category}:")
            _print_func(ufunc_category[util_category])
            print()


def show_util_func_by_keywords() -> None:
    """show all available utility functions in pyufunc by prefix keywords.

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

    # print all available utility functions
    print("Available utility functions in pyUFunc:")

    def _print_func(func_list: list):
        for func in func_list:
            print(f"  - {func}")

    for keyword in ufunc_keywords:
        if ufunc_keywords[keyword]:
            print(f"- {keyword}:")
            _print_func(ufunc_keywords[keyword])
            print()

__all__ = list(chain(*ufunc_category.values()))
