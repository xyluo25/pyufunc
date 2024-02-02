# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# import modules with same name from different folder in python
from __future__ import absolute_import

from .pkg_config import *
from .pkg_utils import *
from .logutil import *

from pyutilfunc.logutil.loga import Loga


if IS_LOG:
    print(f"    :Logging is enabled, please check the log file in folder: {LOGGING_FOLDER}")
    print("    :If you want to disable logging, please add pyutilfunc.IS_LOG = False in your code.")


loga = Loga(
    do_print=True,  # print each log to console
    do_write=True,  # write each log to file
    logfile="mylog.txt",  # custom path to logfile
)
