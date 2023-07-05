# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, July 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import importlib
import subprocess
import sys


def import_package(package_name: str, options: list = []) -> object:
    """import a python package, if not exist, install it and import it again.

    Args:
        package_name (str): the package name
        options (list, optional): the installation optional inputs,
            eg: "--user",'--force-reinstall', '--ignore-installed'. Defaults to [].

    Returns:
        object: the imported package
    """

    try:
        # import package from current environment
        module = importlib.import_module(package_name)
    except ImportError:
        # install package into current environment
        outputs = []
        try:
            all_args = [sys.executable, '-m', 'pip',
                        'install', '--user', *options, package_name]

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
