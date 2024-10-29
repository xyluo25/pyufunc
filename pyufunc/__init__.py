# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
import sys

# import all modules
from .util_ai import *  # machine learning functions  # noqa: F403
from .util_algorithm import *  # algorithm functions  # noqa: F403
from .util_magic import *  # unclassified functions are here  # noqa: F403
from .util_data_processing import *  # data processing functions including algorithms  # noqa: F403
from .util_datetime import *  # datetime functions  # noqa: F403
from .util_fullstack import *  # fullstack functions, including front end and back end  # noqa: F403
from .util_geo import *  # geographic functions  # noqa: F403
from .util_git_pypi import *  # git and pypi functions  # noqa: F403
from .util_gui import *  # GUI functions    # noqa: F403
from .util_img import *  # image functions   # noqa: F403
from .util_log import *  # logging functions    # noqa: F403
from .util_network import *  # network functions    # noqa: F403
from .util_office import *  # office functions  # noqa: F403
from .util_optimization import *  # optimization functions  # noqa: F403
from .util_pathio import *  # path and IO functions  # noqa: F403
from .util_test import *  # test functions  # noqa: F403
from .util_vis import *  # visualization functions  # noqa: F403

# import package configurations and utilities
from .pkg_configs import *  # noqa: F403

from .__init import (show_util_func_by_category,
                     show_util_func_by_keyword,
                     find_util_func_by_keyword,
                     config_FUNC_CATEGORY)


def check_python_version(min_version: str = "3.10") -> tuple:
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

check_python_version()

__all__ = [func for fn_lst in list(config_FUNC_CATEGORY.values()) for func in fn_lst]