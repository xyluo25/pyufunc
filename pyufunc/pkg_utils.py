# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
import importlib
import subprocess
import sys
import inspect
import datetime
from functools import wraps

"""TODO
a decorator to run function in multiple processors
a decorator to run function in multiple threads
...

"""


def import_package(package_name: str, options: list = ["--user"]) -> object:
    """import a python package, if not exist, install it and import it again.
    This function can be used in any package to avoid too much pre-installation of dependencies.
    In other words, this function will install the package only if it is needed.

    Location:
        The function defined in pyutilkit/utils.py.

    Args:
        package_name (str): the package name, eg: "numpy" or "numpy==1.19.5".
        options (list, optional): the installation optional inputs,
            eg: '--force-reinstall', '--ignore-installed'. Defaults to ["--user"].

    Returns:
        object: the imported package

    Examples:
        >>> numpy = import_package("numpy") # equal to "import numpy as numpy"

        >>> numpy = import_package("numpy")
            :Package numpy not existed in current env, install and re-import...
        >>> numpy = import_package("numpy==1.19.5")
            :Package numpy==1.19.5 not existed in current env, install and re-import...
    """

    try:
        # import package from current environment
        module = importlib.import_module(package_name)
    except ImportError:
        # install package into current environment
        outputs = []
        try:
            print(f"    :{package_name} not existed in current env, install and re-import...")
            all_args = [sys.executable, '-m', 'pip',
                        'install', *options, package_name]

            result = subprocess.run(
                all_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')
            outputs.extend((stdout, stderr))

            result.check_returncode()

        # if install failed, print the error message
        except Exception as e:
            if len(outputs) == 2:
                [print(output, end='') for output in outputs]
            else:
                print(e)
            return

        # import package from current environment after installation
        module = importlib.import_module(package_name)
    return module


def func_running_time(func: object) -> object:
    """A decorator to measure the time of a function or class method.
    It is useful to use this function in test, debug, logging and running time measurement.

    Location:
        The function defined in pyutilkit/utils.py.

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
        print(f'  :INFO Begin to run function: {func.__name__} …')
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_diff = datetime.datetime.now() - time_start
        print(
            f'  :INFO Finished running function: {func.__name__}, total: {time_diff.seconds}s')
        print()
        return res

    return inner


def get_user_defined_func(module: object = sys.modules[__name__]) -> list:
    """list all user-defined functions in a module.

    Location:
        The function defined in pyutilfunc/utils.py

    Args:
        module (object, optional): the module name. Defaults to sys.modules[__name__].

    Returns:
        list: a list of user-defined functions in the module.

    Examples:
        >>> import ufunc as uf
        >>> uf.get_user_defined_func()
        ['func_running_time', 'generate_password', 'import_package', 'get_user_defined_func']
    """

    # check if the model is a module
    if not inspect.ismodule(module):
        raise ValueError("The input is not a module.")

    # get all functions in the module
    func_all = [[name, obj] for name, obj in inspect.getmembers(
        module) if inspect.isfunction(obj)]

    # filter out the functions defined in the module
    func_filtered = list(filter(lambda x: (
        x[1].__module__ == module.__name__ and not x[0].startswith("__")), func_all))
    return [func[0] for func in func_filtered]





__all__ = get_user_defined_func()
