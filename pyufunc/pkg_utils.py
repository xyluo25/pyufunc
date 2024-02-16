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
import copy
from itertools import chain

from pyufunc.pkg_configs import ufunc_prefix_keywords as ufunc_keywords

# import local modules
from pyufunc import (util_ai,
                     util_common,
                     util_data_processing,
                     util_datetime,
                     util_fullstack,
                     util_geo,
                     util_git_pypi,
                     util_gui,
                     util_img,
                     util_log,
                     util_network,
                     util_office,
                     util_optimization,
                     util_pathio,
                     util_test,
                     util_vis)

# specify the available utility functions for importing all
__all__ = ["import_package",
           "func_running_time",
           "get_user_defined_func",
           "is_user_defined_func",
           "is_module_importable",
           "requires",
           "show_util_func_by_category",
           "show_util_func_by_keywords"]

# specify the available utility functions by category
ufunc_category = {
    "util_ai": util_ai.__all__,
    "util_common": util_common.__all__,
    "util_data_processing": util_data_processing.__all__,
    "util_datetime": util_datetime.__all__,
    "util_fullstack": util_fullstack.__all__,
    "util_geo": util_geo.__all__,
    "util_git_pypi": util_git_pypi.__all__,
    "util_gui": util_gui.__all__,
    "util_img": util_img.__all__,
    "util_log": util_log.__all__,
    "util_network": util_network.__all__,
    "util_office": util_office.__all__,
    "util_optimization": util_optimization.__all__,
    "util_pathio": util_pathio.__all__,
    "util_test": util_test.__all__,
    "util_vis": util_vis.__all__,
    "pkg_utils": __all__
}



"""TODO
a decorator to run function in multiple processors
a decorator to run function in multiple threads
...

"""


def import_package(pkg_name: str, options: list = ["--user"]) -> object:
    """import a python package, if not exist, install the package and import it again.
    This function can be used in any package to avoid too much pre-installation of dependencies.
    In other words, this function will install the package only if it is needed.

    Location:
        The function defined in pyufunc/utils.py.

    Args:
        package_name (str): the package name, eg: "numpy" or "numpy==1.19.5".
        options (list, optional): the installation optional inputs,
            eg: '--force-reinstall', '--ignore-installed'. Defaults to ["--user"].

    Returns:
        object: the imported package

    Examples:
        >>> numpy = import_package("numpy") # equal to "import numpy as numpy"

        >>> numpy = import_package("numpy")
            :Package numpy not existed in current env, install the package first and import again...

        >>> numpy = import_package("numpy==1.19.5")
            :Package numpy==1.19.5 not existed in current env, install the package first and import again...

        >>> np = import_package("numpy")  # equal to "import numpy as np"
    """

    # TDD, test-driven development: check inputs
    assert isinstance(pkg_name, str), "The input package name should be a string."

    try:
        # import package from current environment
        module = importlib.import_module(pkg_name)
    except ImportError:
        # install package onto current environment
        outputs = []
        try:
            print(f"  :{pkg_name} not existed in current env, install the package first and import again...")
            all_args = [sys.executable, '-m', 'pip',
                        'install', *options, pkg_name]

            result = subprocess.run(
                all_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')
            outputs.extend((stdout, stderr))

            result.check_returncode()

        # if install failed, print the error message
        except Exception as e:
            print("  :Info: failed to install the package. please install it manually.")
            print(f"  :Use pip or conda to install it, e.g. 'pip install {pkg_name}'. ")
            if len(outputs) == 2:
                [print(output, end='') for output in outputs]
            else:
                print(e)
            return

        # import package from current environment after installation
        module = importlib.import_module(pkg_name)
    return module


def func_running_time(func: object) -> object:
    """A decorator to measure the time of a function or class method.
    It is useful to use this function in test, debug, logging and running time measurement.

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
        print(f'  :INFO: begin to run function: {func.__name__} …')
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_diff = datetime.datetime.now() - time_start
        print(
            f'  :INFO: finished running function: {func.__name__}, total: {time_diff.seconds}s')
        print()
        return res

    return inner


def get_user_defined_func(module: object = sys.modules[__name__]) -> list:
    """list all user-defined functions in a module.

    Args:
        module (object, optional): the module name. Defaults to sys.modules[__name__].

    Returns:
        list: a list of user-defined functions in the module.

    Examples:
        >>> import ufunc as uf
        >>> uf.get_user_defined_func()
        ['func_running_time', 'generate_password', 'import_package', 'get_user_defined_func']
    """

    # Step 1: check if the model is a module
    if not inspect.ismodule(module):
        raise ValueError("The input is not a module.")

    # Step 2: list all attributes in the module
    all_func = dir(module)
    user_defined_func = []
    # Step 3: filter the user-defined functions
    for func_name in all_func:
        obj = getattr(module, func_name)
        if inspect.isfunction(obj):
            user_defined_func.append(func_name)
        # if inspect.ismodule(obj):
        #     get_user_defined_func(obj, pre_defined_func)

    return list(set(user_defined_func))


def is_user_defined_func(func_obj: object) -> bool:
    """Check if a function is user-defined.

    Args:
        func_obj (object): the function object.

    Returns:
        bool: True if the function is user-defined, False otherwise.

    Examples:
        >>> import pyufunc as uf
        >>> uf.is_user_defined_func(uf.func_running_time)
        True

        >>> uf.is_user_defined_func(os.path.join)
        False
    """

    try:
        # Try to get the file where the function is defined
        func_file = inspect.getfile(func_obj)
    except TypeError:
        # This might happen if it's a built-in function or built-in method, which are not user-defined
        return False
    except Exception as e:
        # Handle other possible exceptions, such as the function being a built-in method of a built-in type
        print(f"  :Info: could not determine the {func_obj} is user-defined: {e}")
        return False

    # Check if the function is defined in the script's main file or a user-defined module
    # This is a simple check and might need to be adjusted based on your project structure
    if "site-packages" in func_file or "python" in func_file.lower():
        # The function is likely imported from an installed package or the standard library
        return False

    return True  # The function is likely user-defined


def is_module_importable(module_name: str) -> bool:
    """Safely import a module and return a boolean. If the module is not importable, return False.

    Args:
        modname (str): the module name to import.

    Returns:
        bool: True if the module is importable, False otherwise.

    Note:
        This function is useful to check if a module is installed in the current environment.

    Examples:

    """

    # TDD, test-driven development: check inputs
    assert isinstance(module_name, str), "The input module name should be a string."

    try:
        exec(f"import {module_name}")
        is_importable = True
    except ImportError:
        is_importable = False

    return is_importable


def requires(*args, **kwargs) -> object:
    """A decorator to wrap functions with extra dependencies.
    If the dependencies are not available, the function will not run.

    Returns:
        object: the decorated function.

    Examples:
        # Example 1: the function will not run if the dependencies are not available
        >>> @requires("numpy", "pandas", "unknown_module")
            def my_function():
                return "I'm running!"
        >>> my_function()
            Error: missing dependencies: ['numpy', 'pandas'], please install them first.
            not running the function: my_function

        # Example 2: the function will run if the dependencies are available
        >>> @requires("numpy", "pandas")
            def my_function():
                return "I'm running!"
        >>> my_function()
            "I'm running!"

    """

    # Step 1: get the verbose option, default is True
    # the verbose option is used to print the error message
    v = kwargs.get("verbose", True)

    # Step 2: get the required dependencies
    wanted = copy.deepcopy(args)

    def inner(function):
        available = [is_module_importable(arg) for arg in args]
        if all(available):
            return function
        else:
            def passer(*args, **kwargs):
                if v:
                    missing = [arg for i, arg in enumerate(wanted) if not available[i]]
                    print(f"  :Error: missing dependencies: {missing}, please install them first.")
                    print(f"  :Use pip or conda to install it, e.g. 'pip install {missing}'. ")
                    assert False, f"Missing required dependencies, not running the function: {function.__name__}"
                else:
                    pass

            return passer

    return inner


def show_util_func_by_category() -> None:
    """show all available utility functions in pyufunc by category or by prefix keywords.

    Examples:
        >>> import pyufunc as uf
        >>> uf.show_utility_func_by_category()
        Available utility functions in pyufunc:

        -- util_common:
           ** show_supported_docstring_header
           ** show_google_docstring_style
           ** show_numpy_docstring_style
           ** generate_password

        -- util_datetime:
           ** fmt_dt_to_str
           ** fmt_dt
           ** list_all_timezones
           ** get_timezone
           ** cvt_dt_to_tz
           ** get_time_diff_in_unit

    """

    # print all available utility functions
    print("Available utility functions in pyufunc:")

    def print_func(func_list: list):
        for func in func_list:
            print(f"   ** {func}")

    for util_category in ufunc_category:
        if ufunc_category[util_category]:
            print(f"-- {util_category}:")
            print_func(ufunc_category[util_category])
            print()


def show_util_func_by_keywords() -> None:
    """show all available utility functions in pyufunc by prefix keywords.

    Examples:
        >>> import pyufunc as uf
        >>> uf.show_utility_func_by_keywords()
        Available utility functions in pyufunc:

        -- non-keywords:
           ** point_to_circle_on_unit_radius
           ** path2linux
           ** path2uniform
           ** import_package
           ** func_running_time
           ** requires

        -- show:
           ** show_numpy_docstring_style
           ** show_available_utility_func
    """

    for func_str in list(chain.from_iterable(ufunc_category.values())):
        prefix = func_str.split("_")[0]
        if prefix in ufunc_keywords:
            ufunc_keywords[prefix].append(func_str)
        else:
            ufunc_keywords["non-keywords"].append(func_str)

    # print all available utility functions
    print("Available utility functions in pyufunc:")

    def print_func(func_list: list):
        for func in func_list:
            print(f"   ** {func}")

    for keyword in ufunc_keywords:
        if ufunc_keywords[keyword]:
            print(f"-- {keyword}:")
            print_func(ufunc_keywords[keyword])
            print()
