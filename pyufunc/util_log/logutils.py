# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from pathlib import Path
import logging
import datetime
import os
import sys
from functools import wraps

from pyutilfunc.pathio.pathutils import path2linux
from pyutilfunc.pkg_config import LOGGING_FOLDER

import datetime
import logging
import os


def log_writer1(path:str=f"../../syslogs/",info:str="",warning:str="",error:str="",debug: str="",critical: set="") -> None:
    """A function tool to track log info

    Args:
        path (str): [The path to save log file] Defaults to "current folder"
        info (str, optional): [description]. Defaults to "".
        warning (str, optional): [description]. Defaults to "".
        error (str, optional): [description]. Defaults to "".
        debug (str, optional): [description]. Defaults to "".
        critical (set, optional): [description]. Defaults to "".
    """

    if not isinstance(path, str):
        raise Exception("Invalid input, path type error...")
    if not isinstance(info, str):
        raise Exception("Invalid input, info type error...")
    if not isinstance(warning, str):
        raise Exception("Invalid input, warning type error...")
    if not isinstance(error, str):
        raise Exception("Invalid input, error type error...")
    if not isinstance(debug, str):
        raise Exception("Invalid input, debug type error...")
    if not isinstance(critical, str):
        raise Exception("Invalid input, critical type...")


    __filename = os.path.join(path,"log_%s.log"%datetime.datetime.today().strftime("%Y-%m-%d"))

    # datetime,python file name, logging level, message
    logging.basicConfig(filename=__filename,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',level=logging.DEBUG)

    if info:
        logging.info(info)
    if warning:
        logging.warning(warning)
    if error:
        logging.error(error)
    if debug:
        logging.debug(debug)
    if critical:
        logging.critical(critical)


def print_and_log(*args, log_level="info", **kwargs):

    kwargs_new = {}
    kwargs_unknown = []
    for key, value in kwargs.items():
        # standard print kwargs
        if key in ["sep", "end", "file", "flush"]:
            kwargs_new[key] = value
        # non-standard print kwargs
        else:
            kwargs_unknown.append(f"{key}={value}")

    print(*args, kwargs_unknown, **kwargs_new)

    if log_level.lower() == "info":
        logging.info(*args)
    elif log_level.lower() == "warning":
        logging.warning(*args)
    elif log_level.lower() == "error":
        logging.error(*args)
    elif log_level.lower() == "debug":
        logging.debug(*args)
    elif log_level.lower() == "critical":
        logging.critical(*args)
    else:
        print(" :info, invalid log level, message will not be logged...")


def log_writer(func, log_dir: str | Path = LOGGING_FOLDER) -> None:

    @wraps(func)
    def wrapper(*args, **kwargs):
        # covert log_dir to absolute path for all OSes
        log_dir_abs = path2linux(log_dir)

        # create log folder if not exist
        if not os.path.isdir(log_dir_abs):
            os.makedirs(log_dir_abs, exist_ok=True)

        # create log file using current date
        __filename = path2linux(
            os.path.join(log_dir_abs,
                         f'{datetime.datetime.now().strftime("%Y_%m_%d")}.log'))

        print("filename:", __filename)
        logging.basicConfig(filename=__filename,
                            format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

        res = func(*args, **kwargs)

        return res

    return wrapper


# this function will track error message from log file
def log_error_tracker(path:str=f"../../syslogs/",filename_pattern:str="",level:str="ERROR") -> str:

    _filename = "log_%s.log"%datetime.datetime.today().strftime("%Y_%m_%d")

    if filename_pattern:
        _filename = filename_pattern

    filename = os.path.join(path,_filename)

    with open(filename,"r",encoding="utf-8") as f:
        message_list= []
        for message in f.readlines()[::-1]:
            if level in message:
                message_list.append(message)
    return message_list
