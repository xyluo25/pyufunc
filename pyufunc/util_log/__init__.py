# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

# The log section embedded in pyufunc is kuai_log, which is a logging library.
# kuai_log is a easy version of nb_log, which is another logging library.
# The reason for using kuai_log is that it is more lightweight than nb_log.
# nb_log is one of the most powerful logging libraries in Python.

# the source code for kuai_log: https://github.com/ydf0509/kuai_log
# the source code for nb_log: https://github.com/ydf0509/nb_log


from ._log_dir import (
    add_date_in_filename,
    generate_dir_with_date
)

from ._lg_logger import get_logger as log_logger
from ._log_writer import log_writer

__all__ = [
    # _log_dir
    "add_date_in_filename",
    "generate_dir_with_date",

    # _logger
    "log_logger",

    # _log_writer
    "log_writer",
]
