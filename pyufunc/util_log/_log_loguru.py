# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, May 28th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING
from pyufunc.util_common import requires, import_package

# https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import
if TYPE_CHECKING:
    import loguru


@requires("loguru")
def log_logger(log_file: str = "log.log") -> loguru.logger:

    import_package("loguru", verbose=False)
    from loguru import logger

    return logger

# logger = loguru_logger()