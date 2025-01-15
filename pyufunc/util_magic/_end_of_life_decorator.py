# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from functools import wraps


def end_of_life(func: object = None, **kwargs) -> object:
    """A decorator to mark the end of life of a function or class method.
    It's useful to use this function to remind users to avoid using the deprecated functions.

    Args:
        *args: the required dependencies to run the function.

            - if argument is a string, module and import are the same.

            - if argument is a tuple or list, it has two elements:
                first element is the module name, for pip or conda installation;
                second element is the import name, for import the module;

        **kwargs: the optional arguments, including message.
            message (str, optional): the additional message to the users.

    Returns:
        object: the decorated function.

    Examples:
        >>> from pyufunc import end_of_life
        >>> @end_of_life
            def my_func():
                return "I'm running!"

        >>> my_func()
          :Warning: my_func is deprecated and will be removed in the future.
        I'm running!

        >>>@end_of_life(message="Please use the new function instead.")
           def my_func():
              return "I'm running!"

        >>> my_func()
            :Warning: my_func is deprecated and will be removed in the future.
            :Please use the new function instead.
        I'm running!
    """

    # kwargs from decorator
    # print("kwargs: ", kwargs)
    message = kwargs.get("message", None)

    def inner(func_obj: object) -> object:
        @wraps(func_obj)
        def wrapper(*args, **kwargs):
            # kwargs from function
            print(f"  :Warning: {func_obj.__name__} is deprecated and will be removed in the future version.")

            if message:
                print(f"  :{message}")

            return func_obj(*args, **kwargs)
        return wrapper

    return inner(func) if func else inner
