# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from __future__ import absolute_import
import copy
from pyufunc.util_magic._import_package import (
    is_module_importable,
    import_package)


# decorator with extra arguments
def requires(*args, **kwargs) -> object:
    """A decorator to wrap functions with extra dependencies.
    If the dependencies are not available, the function will not run.

    Args:
        *args: the required dependencies to run the function.
            - if argument is a string, module and import are the same.
            - if argument is a tuple or list, it has two elements:
                - first element is the module name, for pip or conda installation;
                - second element is the import name, for import the module;

        **kwargs: the optional arguments, including verbose and auto_install.

            verbose (bool, optional): print the processing message. Defaults to True.

            auto_install (bool, optional): install the missing dependencies automatically.
                Defaults to False.

    Returns:
        object: the decorated function.

    Note:
        user can parse the verbose and auto_install options to control the behavior of the decorator.

        verbose: print the error message if the dependencies are not available. Default is True.

        auto_install: install the missing dependencies automatically. Default is True.

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
    arg_install_name = []
    arg_import_name = []
    for arg in args:
        if isinstance(arg, str):
            arg_install_name.append(arg)
            arg_import_name.append(arg)
        elif isinstance(arg, (tuple, list)) and len(arg) == 2:
            arg_install_name.append(arg[0])
            arg_import_name.append(arg[1])
        else:
            raise ValueError("The input arguments should be strings or tuple with two elements.")

    def inner(function):
        # check if the dependencies are available
        available = [is_module_importable(arg) for arg in arg_import_name]
        if all(available):
            return function

        # get missing dependencies

        # missing_pkg_name include str, tuple, or list from input args
        missing_pkg_name = [arg for i, arg in enumerate(args) if not available[i]]

        missing_install_name = [arg for i, arg in enumerate(arg_install_name) if not available[i]]
        missing_import_name = [arg for i, arg in enumerate(arg_import_name) if not available[i]]

        # install the missing dependencies
        if auto_install:
            if verbose:
                print(f"  :Info: installing {','.join(missing_install_name)}...")
            for pkg_name in missing_pkg_name:
                import_package(pkg_name, verbose=verbose)
            available = [is_module_importable(arg) for arg in missing_import_name]
            if all(available):
                return function

        def passer(*args, **kwargs):
            if verbose:
                print(f"  :{function.__name__} missing dependency {','.join(missing_install_name)}")
                print("  :please install manually.")

            if verbose and not auto_install:
                print("  :You can set auto_install=True to install the package automatically,")
                print(f"  :eg. @requires{args_requires}" + ", auto_install=True)\n")
            return function(*args, **kwargs)

        return passer

    return inner
