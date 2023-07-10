# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import importlib
import subprocess
import sys
import inspect


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

        module = importlib.import_module(package_name)
    return module


# list all user-defined functions in a module
def list_functions(module):
    return [[name, obj] for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)]