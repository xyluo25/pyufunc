# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
import importlib
import subprocess
import sys
import inspect
from typing import Union


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
