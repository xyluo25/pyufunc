# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, May 28th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import sys
import threading

# noinspection PyUnusedLocal
import functools
import signal


class __KThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False
        self.__run_backup = None

    # noinspection PyAttributeOutsideInit
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        return self.localtrace if why == 'call' else None

    def localtrace(self, frame, why, arg):
        if why == 'line':
            if self.killed:
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


# noinspection PyPep8Naming
class TIMEOUT_EXCEPTION(Exception):
    """function run timeout"""
    pass


def timeout(seconds: int) -> object:
    """A decorator to set the timeout for the function.

    Args:
        seconds (int): timeout seconds for the function.

    Returns:
        object: the decorated function.

    Examples:
        >>> from pyufunc import timeout
        >>> @timeout(5)
            def my_function():
                return "I'm running!"
        >>> my_function()
        "I'm running!"

        >>> @timeout(5)
            def my_function():
                import time
                time.sleep(10)
                return "I'm running!"
        >>> my_function()
        Error: my_function exceed 5 seconds timeout
    """

    def timeout_decorator(func):

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = __KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.is_alive()
            thd.kill()  # kill the child thread

            if alive:
                # raise TIMEOUT_EXCEPTION('function run too long, timeout %d seconds.' % seconds)
                raise TIMEOUT_EXCEPTION(f'{func.__name__} exceed {seconds} seconds timeout')
            return result[0] if result else result

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator


def timeout_linux(timeout: int):
    """A decorator to set the timeout for the function on linux system.
    Args:
        timeout (int): timeout seconds for the function.

    Returns:
        object: the decorated function.

    Examples:
        >>> from pyufunc import timeout_linux
        >>> @timeout_linux(5)
            def my_function():
                return "I'm running!"
        >>> my_function()
        "I'm running!"
        >>> @timeout_linux(5)
            def my_function():
                import time
                time.sleep(10)
                return "I'm running!"
        >>> my_function()
        Error: Function: my_function params: (), {} ,execution timed out: 5
    """

    def _timeout_linux(func, ):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def _timeout_handler(signum, frame):

                raise TimeoutError(
                    f"Function: {func} params: {args}, {kwargs} ,execution timed out: {timeout}")

            # timeout for linux system
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout)

            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)

        return wrapper

    return _timeout_linux
