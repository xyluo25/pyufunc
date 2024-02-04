# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
from pyufunc.util_pathio._path import path2linux


# **** Package Info **** #
pkg_version = "0.0.1"
pkg_name = "pyufunc"
pkg_author = "Mr. Xiangyong Luo"
pkg_email = "luoxiangyong01@gmail.com"


# **** Logging **** #
# system logging
IS_LOG = True

# logging default folder
LOGGING_FOLDER = path2linux(os.path.join(os.getcwd(), "syslogs"))