# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# import modules with same name from different folder in python
from __future__ import absolute_import

# import all modules
from .util_ai import *  # machine learning functions
from .util_common import *  # unclassified functions are here
from .util_data_processing import *  # data processing functions including algorithms
from .util_datetime import *  # datetime functions
from .util_fullstack import *  # fullstack functions, including front end and back end
from .util_geo import *  # geographic functions
from .util_git_pypi import *  # git and pypi functions
from .util_gui import *  # GUI functions
from .util_log import *  # logging functions
from .util_network import *  # network functions
from .util_office import *  # office functions
from .util_optimization import *  # optimization functions
from .util_pathio import *  # path and IO functions
from .util_test import *  # test functions
from .util_vis import *  # visualization functions

# import package configurations and utilities
from .pkg_config import *
from .pkg_utils import *

from pyufunc.util_log.loga import Loga


if IS_LOG:
    print(f"    :Logging is enabled, please check the log file in folder: {LOGGING_FOLDER}")
    print("    :If you want to disable logging, please add pyutilfunc.IS_LOG = False in your code.")


loga = Loga(
    do_print=True,  # print each log to console
    do_write=True,  # write each log to file
    logfile="mylog.txt",  # custom path to logfile
)


__all__ = [
    # util_ai

    # util_common

    # util_data_processing

    # util_datetime

    # util_fullstack

    # util_geo

    # util_git_pypi

    # util_gui

    # util_log

    # util_network

    # util_office

    # util_optimization

    # util_pathio

    # util_test

    # util_vis

]