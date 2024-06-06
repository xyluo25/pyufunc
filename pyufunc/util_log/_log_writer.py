# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from pyufunc.pkg_configs import config_logging
from functools import partial, wraps
from pathlib import Path
import logging
import datetime
import os
from pyufunc.util_pathio._path import path2linux


def log_writer(func=None, *, log_dir: str | Path = config_logging["log_folder"], log_formatter: int = 4):

    @wraps(func)
    def wrapper(func, *args, **kwargs):
        """The actual logic"""
        # Do something with first and second and produce a `result` of type `R`

        # covert log_dir to absolute path for all OSes
        log_dir_abs = path2linux(log_dir)

        # create log folder if not exist
        if not os.path.isdir(log_dir_abs):
            os.makedirs(log_dir_abs, exist_ok=True)

        # create log file using current date
        __filename = path2linux(
            os.path.join(log_dir_abs,
                         f'{datetime.datetime.now().strftime("%Y_%m_%d")}.log'))

        # Create a logger
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.WARNING)

        # Create a file handler and set the log file
        file_handler = logging.FileHandler(__filename)
        formatter = config_logging["log_formatter"][log_formatter]
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Create a stream handler to capture print statements
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(formatter)

        # Add the stream handler to the logger
        logger.addHandler(stream_handler)

        # print("first:", log_dir)
        # print("second:", log_formatter)
        return func(*args, **kwargs)

    # Without arguments `func` is passed directly to the decorator
    # print("func:", func)

    if func is not None:
        if not callable(func):
            raise TypeError(
                "Not a callable. Did you use a non-keyword argument?")
        logging.info("without arguments")
        # print("without arguments")
        return partial(wrapper, func)

    # With arguments, we need to return a function that accepts the function
    def decorator(func):
        logging.info("with arguments")
        # print("with arguments")
        return partial(wrapper, func)
    return decorator
