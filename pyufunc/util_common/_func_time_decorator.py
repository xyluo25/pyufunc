# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
import datetime
from functools import wraps


# decorator without arguments
def func_running_time(func: object) -> object:
    """A decorator to measure the time of a function or class method.
    It is useful to use this function in test, debug, logging and running time measurement.

    Note:
        It's equivalent to the func_time as func_running_time have been used in many packages,
        and we keep both of them for compatibility.

    Location:
        The function defined in pyufunc/utils.py.

    Args:
        func (object): the function or class method to be measured.

    Returns:
        object: the decorated function or class method.

    Examples:
        >>> @func_running_time
            def func():
                print("main function...)
                time.sleep(3)
                return

        >>> func()
            INFO Begin to run function: func …
            main function...
            INFO Finished running function: func, total: 3s
    """

    @wraps(func)
    def inner(*args, **kwargs):
        # print(f'  :INFO: begin to run function: {func.__name__} …')
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_diff = datetime.datetime.now() - time_start
        print(
            f'  :INFO: finished function: {func.__name__}, total: {time_diff.seconds}s \n')
        return res

    return inner


def func_time(func: object) -> object:
    """A decorator to measure the time of a function or class method.
    It is useful to use this function in test, debug, logging and running time measurement.

    Note:
        It's equivalent to the func_running_time as func_running_time have been used in many packages.
        We keep both of them for compatibility.

    Location:
        The function defined in pyufunc/utils.py.

    Args:
        func (object): the function or class method to be measured.

    Returns:
        object: the decorated function or class method.

    Examples:
        >>> @func_running_time
            def func():
                print("main function...)
                time.sleep(3)
                return

        >>> func()
            INFO Begin to run function: func …
            main function...
            INFO Finished running function: func, total: 3s
    """

    @wraps(func)
    def inner(*args, **kwargs):
        # print(f'  :INFO: begin to run function: {func.__name__} …')
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_diff = datetime.datetime.now() - time_start
        print(
            f'  :INFO: finished function: {func.__name__}, total: {time_diff.seconds}s \n')
        return res

    return inner
