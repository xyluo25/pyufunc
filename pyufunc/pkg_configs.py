# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
from pyufunc.util_pathio._path import path2linux


# **** Package Info **** #
pkg_version = "0.2.0"
pkg_name = "pyufunc"
pkg_author = "Mr. Xiangyong Luo, Dr. Xuesong Simon Zhou"
pkg_email = "luoxiangyong01@gmail.com, xzhou74@asu.edu"


# **** Logging **** #
# system logging
IS_LOG = True

# logging default folder
LOGGING_FOLDER = path2linux(os.path.join(os.getcwd(), "syslogs"))

# **** Datetime Formats **** #
pkg_dt_fmt_seq = {
    0 : "%Y-%m-%d %H:%M:%S",  # "YYYY-MM-DD HH:MM:SS", 2023-07-09 11:11:11
    1 : "%Y-%m-%d %H:%M:%S.%f",  # "YYYY-MM-DD HH:MM:SS.MS", 2023-07-09 11:11:11.123456

    2 : "%m/%d/%Y %H:%M:%S",  # "MM/DD/YYYY HH:MM:SS", 07/09/2023 11:11:11
    3 : "%m/%d/%Y %H:%M:%S.%f",  # "MM/DD/YYYY HH:MM:SS.MS", 07/09/2023 11:11:11.123456

    4 : "%d/%m/%Y %H:%M:%S",  # "DD/MM/YYYY HH:MM:SS", 09/07/2023 11:11:11
    5 : "%d/%m/%Y %H:%M:%S.%f",  # "DD/MM/YYYY HH:MM:SS.MS", 09/07/2023 11:11:11.123456

    6 : "%Y-%m-%d",  # "YYYY-MM-DD", 2023-07-09
    7 : "%m/%d/%Y",  # "MM/DD/YYYY", 07/09/2023
    8 : "%d/%m/%Y",  # "DD/MM/YYYY", 09/07/2023

    9 : "%H:%M:%S",  # "HH:MM:SS", 11:11:11
    10 : "%H:%M:%S.%f",  # "HH:MM:SS.MS", 11:11:11.123456
}

# **** pyufunc prefix keywords **** #
ufunc_keywords = {
    "non-keywords": [],
    "show"        : [],
    "get"         : [],
    "generate"    : [],
    "create"      : [],
    "find"        : [],
    "calc"        : [],
    "group"       : [],
    "check"       : [],
    "validate"    : [],
    "list"        : [],
    "split"       : [],
    "fmt"         : [],
    "cvt"         : [],
    "is"          : [],
    "proj"        : [],
    "github"      : [],
    "pypi"        : []

}
