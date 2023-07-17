# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# import modules with same name from different folder in python
from __future__ import absolute_import
from pathlib import Path

import pyutilfunc as uf
import pyutilfunc.pathio as pio

from pyutilfunc.logutil.te import log_writer2
import os


@log_writer2
def spam(a: int) -> int:
    return a


@log_writer2(log_dir=uf.LOGGING_FOLDER, log_formatter=3)
def eggs(a: int) -> int:
    raise Exception("This is an exception")
    # return a
