# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from pyufunc.util_magic._import_package import is_module_importable, import_package

F = TypeVar("F", bound=Callable[..., Any])


# decorator with extra arguments
def requires(*args, **kwargs) -> Callable[[F], F]:
    """Wrap a function with extra dependency checks.

    If the dependencies are not available, the function will not run.

    Args:
        *args: Required dependency specifications. Each value can be a package
            name string, or a two-item tuple/list of
            ``(install_name, import_name)`` when the installation name differs
            from the import name.
        **kwargs: Optional decorator settings. Supported keys are ``verbose``
            for printing dependency messages and ``auto_install`` for explicitly
            installing missing packages. ``verbose`` defaults to ``True`` and
            ``auto_install`` defaults to ``False``.

    Notes:
        Missing dependencies are reported and the wrapped function is skipped.
        Dependencies are installed only when ``auto_install=True`` is passed
        explicitly.

    Examples:
        >>> @requires("numpy", "pandas", verbose=False)
        ... def my_function():
        ...     return "I'm running!"
        >>> my_function()
        "I'm running!"

    Returns:
        The decorated function wrapper.
    """
    # get the verbose option, default is True
    # the verbose option is used to print the error message
    verbose = kwargs.get("verbose", True)
    auto_install = kwargs.get("auto_install", False)
    # args_requires = copy.deepcopy(args)

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

    def inner(function: F) -> F:
        # check if the dependencies are available
        available = [is_module_importable(arg) for arg in arg_import_name]
        if all(available):
            return function

        # get missing dependencies
        # missing_pkg_name include str, tuple, or list from input args
        missing_pkg_name = [arg for i, arg in enumerate(args) if not available[i]]

        missing_install_name = [arg for i, arg in enumerate(arg_install_name) if not available[i]]
        missing_import_name = [arg for i, arg in enumerate(arg_import_name) if not available[i]]

        # install the missing dependencies automatically if auto_install is True
        if auto_install:
            if verbose:
                print(f"  :Info: installing {','.join(missing_install_name)}...")
            for pkg_name in missing_pkg_name:
                import_package(pkg_name, verbose=verbose, auto_install=True)
            available = [is_module_importable(arg) for arg in missing_import_name]
            if all(available):
                return function

        @wraps(function)
        def passer(*args, **kwargs):
            if verbose:
                print(
                    f"  :{function.__name__} missing dependency {','.join(missing_install_name)}"
                    ", please install manually or use pyufunc package: "
                    "pf.import_package(<module_name>, auto_install=True)."
                )
            # if verbose and not auto_install:
            #     print("  :You can set auto_install=True to install the package automatically,")
            #     print(f"  :eg. @requires{args_requires}" + ", auto_install=True)\n")
            return None

        return cast(F, passer)

    return inner
