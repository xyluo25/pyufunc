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
from multiprocessing import Pool
from typing import Iterable, Callable, Iterator, Union
import os


# specify the available utility functions for importing all
__all__ = [
    "import_package",
    "requires",
    "func_running_time",
    "func_time",
    "run_parallel",
    "get_user_defined_func",
    "is_user_defined_func",
    "is_module_importable",
]


def import_package(pkg_name: Union[str, tuple, list],
                   options: list = ["--user"],
                   verbose: bool = True) -> object:
    """import a python package, if not exist, install the package and import it again.
    This function can be used in any package to avoid too much pre-installation of dependencies.
    In other words, this function will install the package only if it is needed.

    Location:
        The function defined in pyufunc/pkg_utils.py.

    Args:
        package_name (str): the package name, it can be a string or tuple or list.
            if it's a string, it's the package name for both installation and import.

            if it's a tuple or list, it has two elements:
                first element is the package name, for pip or conda installation;
                second element is the package name, for import the package;

            eg: "numpy" or "numpy==1.19.5";
            eg: ("pillow", "PIL");
            eg: ["pillow==8.3.1", "PIL"];
            eg: ["opencv-python", "cv2"];
        options (list, optional): the installation optional inputs,
            eg: '--force-reinstall', '--ignore-installed'. Defaults to ["--user"].
        verbose (bool, optional): print the error message if the package is not available.
            Defaults to True.

    Returns:
        object: the imported package

    Note:
        if the module name different from import name
        eg. module name is 'pillow', import name is 'PIL'
        please use tuple or list to specify the module name and import name
        e.g. import_package(('pillow', 'PIL'))

    Examples:
        >>> numpy = import_package("numpy") # equal to "import numpy as numpy"
        >>> np = import_package("numpy")  # equal to "import numpy as np"

        # not existed
        >>> numpy = import_package("numpy")

        :numpy not existed in current env, installing...

        # specify the version

        >>> numpy = import_package("numpy==1.19.5")

        :Package numpy==1.19.5 not existed in current env, installing...

        # different name for installation and import
        >>> PIL = import_package(("pillow", "PIL"))
        >>> cv2 = import_package(["opencv-python", "cv2"])
        >>> cv2 = import_package(["opencv-python", "cv2"], options=["--force-reinstall"])
        >>> cv2 = import_package(["opencv-python==4.9.0.80", "cv2"])
    """

    # TDD, test-driven development: check inputs
    assert isinstance(pkg_name, (str, tuple, list)), "The input pkg_name should be a string or tuple or list."

    # Step 1: check if the package name is a string
    if isinstance(pkg_name, str):
        module_name = pkg_name
        import_name = pkg_name

    elif isinstance(pkg_name, (tuple, list)) and len(pkg_name) == 2:
        module_name = pkg_name[0]
        import_name = pkg_name[1]

    else:
        raise ValueError("The input pkg_name should be a string, tuple or list with two elements.")

    try:
        # import package from current environment
        module = importlib.import_module(import_name)
    except Exception:

        if verbose:
            print(f"  :installing {module_name}...")

        # install package to current environment
        outputs = []
        try:
            all_args = [sys.executable, '-m', 'pip', 'install', *options, module_name]

            result = subprocess.run(
                all_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')
            outputs.extend((stdout, stderr))

            result.check_returncode()

        # if install failed, print the error message
        except Exception as e:
            print(f"  :Info: failed to install {module_name}. please install it manually.")

            if verbose:
                if len(outputs) == 2:
                    [print(f"  :{output}", end='') for output in outputs]
                else:
                    print(f"  :{e}")
            return None

        # import package from current environment after installation
        try:
            module = importlib.import_module(import_name)

            if verbose:
                print(f"  :{module_name} has been installed successfully.")

        except Exception:
            return None

    return module


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
            f'  :INFO: finished function: {func.__name__}, total: {time_diff.seconds}s')
        print()
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
            f'  :INFO: finished function: {func.__name__}, total: {time_diff.seconds}s')
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
    return "site-packages" not in func_file and "python" not in func_file.lower()


def is_module_importable(module_name: str) -> bool:
    """Safely import a module and return a boolean. If the module is not importable, return False.

    Args:
        module_name (str): the module name to import.

    Returns:
        bool: True if the module is importable, False otherwise.

    Note:
        This function is useful to check if a module is installed in the current environment.

    Examples:
        >>> from pyufunc import is_module_importable
        >>> is_module_importable("numpy")
        True
        >>> is_module_importable("unknown_module")
        False
    """

    # TDD, test-driven development: check inputs
    assert isinstance(module_name, str), "The input module name should be a string."

    try:
        exec(f"import {module_name}")
        is_importable = True
    except ImportError:
        is_importable = False

    return is_importable


# decorator with extra arguments
def requires(*args, **kwargs) -> object:
    """A decorator to wrap functions with extra dependencies.
    If the dependencies are not available, the function will not run.

    Args:
        *args: the required dependencies to run the function.
            if argument is a string, module and import are the same.
            if argument is a tuple or list, it has two elements:
                first element is the module name, for pip or conda installation;
                second element is the import name, for import the module;
        **kwargs: the optional arguments, including verbose and auto_install.
            verbose (bool, optional): print the processing message. Defaults to True.
            auto_install (bool, optional): install the missing dependencies automatically.
                Defaults to False.

    Returns:
        object: the decorated function.

    Note:
        user can parse the verbose and auto_install options to control the behavior of the decorator.
        verbose: print the error message if the dependencies are not available.
            Default is True.

        auto_install: install the missing dependencies automatically.
            Default is True.

        eg: @requires("numpy", "pandas", verbose=False)
        eg: @requires("numpy", "pandas", verbose=True, auto_install=True)
        eg: @requires("numpy", "pandas", verbose=False, auto_install=True)
        eg: @requires(("pillow", "PIL"), "pandas", verbose=True, auto_install=True)

    Examples:

        # Example 1: the function will not run if the dependencies are not available

        >>> @requires("numpy", "pandas", "unknown_module", verbose=True, auto_install=False)
            def my_function():
               return "I'm running!"

        >>> my_function()
        Error: missing dependencies: ['numpy', 'pandas'], please install them first.
        not running the function: my_function

        # Example 2: the function will run if the dependencies are available

        >>> @requires("numpy", "pandas", verbose=True, auto_install=True)
            def my_function():
                return "I'm running!"

        >>> my_function()
        "I'm running!"

    """

    # get the verbose option, default is True
    # the verbose option is used to print the error message
    verbose = kwargs.get("verbose", True)
    auto_install = kwargs.get("auto_install", False)
    args_requires = copy.deepcopy(args)

    # test
    # print("args: ", args)
    # print("kwargs: ", kwargs)
    # print("verbose: ", verbose)
    # print("auto_install: ", auto_install)
    # print()

    # check if the dependencies have different names
    # if the argument are not strings, it's tuple or list
    # first element is the module name, for pip or conda installation
    # second element is the module name, for import the module
    arg_module_name = []
    arg_import_name = []
    for arg in args:
        if isinstance(arg, str):
            arg_module_name.append(arg)
            arg_import_name.append(arg)
        elif isinstance(arg, (tuple, list)) and len(arg) == 2:
            arg_module_name.append(arg[0])
            arg_import_name.append(arg[1])
        else:
            raise ValueError("The input arguments should be strings or tuple with two elements.")

    def inner(function):
        # check if the dependencies are available
        available = [is_module_importable(arg) for arg in arg_import_name]
        if all(available):
            return function

        # get missing dependencies
        missing_pkg_name = [arg for i, arg in enumerate(args) if not available[i]]
        missing_module_name = [arg for i, arg in enumerate(arg_module_name) if not available[i]]
        missing_import_name = [arg for i, arg in enumerate(arg_import_name) if not available[i]]

        # install the missing dependencies
        if auto_install:
            if verbose:
                print(f"  :Info: installing {','.join(missing_module_name)}...")
            for pkg_name in missing_pkg_name:
                import_package(pkg_name, verbose=verbose)
            available = [is_module_importable(arg) for arg in missing_import_name]
            if all(available):
                return function

        def passer(*args, **kwargs):
            if verbose:
                print(f"  :{function.__name__} missing dependency {','.join(missing_module_name)}")
                print("  :please install manually.")

            if verbose and not auto_install:
                print("  :You can set auto_install=True to install the package automatically,")
                print(f"  :eg. @requires{args_requires}" + ", auto_install=True)\n")
            return function(*args, **kwargs)

        return passer

    return inner


@func_running_time
def run_parallel(func: Callable, iterable: Iterable,
                 num_processes: int = os.cpu_count() - 1, chunksize: int = 0) -> Iterator:
    """Run a function in parallel with multiple processors.

    Args:
        func (callable): The function to run in parallel.
        iterable (Iterable): The input iterable to the function.
        num_processes (int, optional): The number of processors to use. Defaults to os.cpu_count() - 1.
        chunksize (int, optional): The chunksize for the parallel processing. Defaults to "".

    Returns:
        Iterator: The results of the function.

    Raises:
        TypeError: If the input function is not callable,
            or if chunksize or num_processes are not integers,
            or if iterable is not an Iterable.

        TypeError: if the input iterable is not an Iterable
            The input iterable should be an Iterable.
        TypeError: if the input number of processors is not an integer
        TypeError: if the input chunksize should be an integer
        ValueError: if the input number of processors is not greater than 0
        ValueError: if the input chunksize is not greater than 0

    Examples:
        >>> import numpy as np
        >>> from pyufunc import run_parallel
        >>> def my_func(x):
                print(f"running {x}")
                return x**2
        >>> results = run_parallel(my_func, list(range(10)), num_processes=7)
        >>> for res in results:
                print(res)
        0, 1, 4, 9, 16, 25, 36, 49, 64, 81
    """

    # TDD, test-driven development: check inputs

    if not callable(func):
        raise TypeError("The input function should be a callable.")
    if not isinstance(iterable, Iterable):
        raise TypeError("The input iterable should be an Iterable.")
    if not isinstance(num_processes, int):
        raise TypeError("The input number of processors should be an integer.")
    if not isinstance(chunksize, int):
        raise TypeError("The input chunksize should be an integer.")

    # check the number of processors and chunksize are greater than 0
    if num_processes <= 0:
        raise ValueError("The input number of processors should be greater than 0.")
    if chunksize < 0:
        raise ValueError("The input chunksize should be greater than 0.")

    # Step 1: get the number of processors to use
    num_processors = min(num_processes, os.cpu_count() - 1)
    print(f"  :Info: using {num_processors} processors to run {func.__name__}...")

    # Step 2: check the chunksize
    if chunksize >= len(iterable):
        chunksize = len(iterable) // num_processors

    # Step 3: run the function in parallel
    with Pool(num_processors) as pool:
        if chunksize == 0:
            results = pool.map(func, iterable)
        else:
            results = pool.map(func, iterable, chunksize=chunksize)

    return results
