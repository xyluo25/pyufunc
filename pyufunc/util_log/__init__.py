# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# We accept loguru as the default logger for pyufunc, because it is a powerful and easy-to-use logging library.
# It can be used to replace the built-in logging module in Python.
# It provides a simple and elegant API for logging, and it also supports asynchronous logging,
# which can improve the performance of logging in some cases.


from ._log_dir import (
    add_date_in_filename,
    generate_dir_with_date
)

# from ._lg_logger import get_logger as log_logger
from ._loguru import log_logger

__all__ = [
    # _log_dir
    "add_date_in_filename",
    "generate_dir_with_date",

    # _log_loguru
    "log_logger",
]
