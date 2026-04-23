# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from functools import wraps


def end_of_life(func_or_class: object = None, **kwargs) -> object:
    """A decorator to mark the end of life of a function or class method.
    It's useful to use this function to remind users to avoid using the deprecated functions.

    Args:
        func_or_class: the function or class method to be decorated.
        kwargs: the optional arguments, including message.
            message(str): the additional message to the users.
            msg(str): the additional message to the users.

    Examples:
        >>> from pyufunc import end_of_life
        >>> @end_of_life
        >>> def my_func():
        >>>    return "I'm running!"

        >>> my_func()
        >>> :Warning: my_func is deprecated and will be removed in the future.
        >>> I'm running!

        >>> @end_of_life(message="Please use the new function instead.")
        >>> def my_func():
        >>>    return "I'm running!"

        >>> my_func()
        >>> :Warning: my_func is deprecated and will be removed in the future.
        >>> :Please use the new function instead.
        >>> I'm running!

    Returns:
        object: the decorated function.

    """

    # kwargs from decorator
    # print("kwargs: ", kwargs)
    message = kwargs.get("message", kwargs.get("msg", None))

    def inner(func_obj: object) -> object:
        @wraps(func_obj)
        def wrapper(*args, **kwargs):
            # kwargs from function
            print(f"  :Warning: {func_obj.__name__} is deprecated and will be removed in the future version.")

            if message:
                print(f"  :{message}")

            return func_obj(*args, **kwargs)
        return wrapper

    return inner(func_or_class) if func_or_class else inner
