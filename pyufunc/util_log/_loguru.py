# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, May 28th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
from pyufunc.util_magic import requires

# https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import


@requires("loguru")
def log_logger():

    import loguru  # pyright: ignore[reportMissingImports]
    # from loguru import logger
    return loguru.logger
