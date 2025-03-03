'''
##############################################################
# Created Date: Sunday, March 2nd 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

import os
import sys
import subprocess
import shutil
from pyufunc.util_pathio._path import path2linux
from pyufunc.util_pathio._platform import is_windows, is_linux, is_mac


def venv_create(*, venv_name: str = "", venv_dir: str = "", pkg_name: str = "pyufunc", verbose: bool = True) -> bool:
    """Create a virtual environment in the specified folder with the specified name.

    Args:
        venv_name (str): the name of the virtual environment
        venv_dir (str): the path to the folder where the virtual environment will be created
        pkg_name (str): the name of the package to be installed in the virtual environment
        verbose (bool): whether to print the progress

    Raises:
        Exception: if env_name is not a string, or folder_path is not a string

    Returns:
        bool: True if the virtual environment is created successfully, False otherwise
    """
    # Default values for env_name and folder_path if not provided
    if not venv_name:
        venv_name = "venv_pf"

    if not venv_dir:
        venv_dir = os.getcwd()

    # TDD for venv_name
    if not isinstance(venv_name, str):
        raise Exception("env_name must be a string")
    if not isinstance(venv_dir, str):
        raise Exception("folder_path must be a string")

    # Create the virtual environment
    try:
        # Ensure the folder exists
        os.makedirs(venv_dir, exist_ok=True)

        # Full path to the virtual environment
        venv_path = path2linux(os.path.join(venv_dir, venv_name))

        # Create the virtual environment
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        # subprocess.run(["python", "-m", "venv", venv_path], check=True)

        if verbose:
            print(f"  :Virtual environment {venv_name} created at: {venv_path}")
    except subprocess.CalledProcessError as e:
        print(f"  :Failed to create virtual environment. Error: {e}")
        return False

    # Find the executable python in the virtual environment
    if is_windows():
        python_executable = path2linux(os.path.join(venv_path, 'Scripts', 'python.exe'))
        # activate_path = pf.path2linux(os.path.join(venv_path, "Scripts", "activate"))
        # subprocess.run([activate_path], shell=True, check=True)

    elif is_linux() or is_mac():
        python_executable = path2linux(os.path.join(venv_path, 'bin', 'python'))
        # activate_path = os.path.join(venv_path, "bin", "activate")
        # subprocess.run(["source", activate_path], shell=True, check=True)

    else:
        raise Exception("  :Unsupported OS to crate virtual environment!")

    # Install the realtwin package in the virtual environment
    try:
        subprocess.check_call([python_executable, '-m', 'pip', 'install', pkg_name])
        print(f"  :Successfully installed {pkg_name} in the virtual environment.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  :Failed to install {pkg_name}. Error: {e}")
    except Exception as e:
        print(f"  :An unexpected error occurred: {e}")

    return False


def venv_delete(*, venv_name: str = "", venv_dir: str = "", verbose: bool = True) -> bool:
    """Delete the virtual environment in the specified folder with the specified name.

    Args:
        venv_name (str): the name of the virtual environment
        venv_dir (str): the path to the folder where the virtual environment will be deleted
        verbose (bool): whether to print the progress

    Returns:
        bool: True if the virtual environment is deleted successfully, False otherwise
    """

    # Default values for env_name and folder_path if not provided
    if not venv_name:
        venv_name = "venv_pf"

    if not venv_dir:
        venv_dir = os.getcwd()

    # Full path to the virtual environment
    venv_path = path2linux(os.path.join(venv_dir, venv_name))

    # check if venv_path exists
    if not os.path.exists(venv_path):
        print(f"  :Virtual environment: {venv_path} does not exist, please check your inputs")
        return False

    if verbose:
        print(f"  :Deleting virtual environment '{venv_name}'")

    # Delete the virtual environment
    shutil.rmtree(venv_path)
    print(f"  :Virtual environment '{venv_name}' deleted successfully.")

    return True


def venv_activate() -> bool:
    print("In order to activate your virtual environment, \n"
          "please be aware the different IDE (integrated development environment) may need different actions.\n"
          "For cmd: https://python.land/virtual-environments/virtualenv \n"
          "For VS Code: https://code.visualstudio.com/docs/python/environments \n"
          "For PyCharm: https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html \n")
    return True