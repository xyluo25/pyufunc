# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from typing import TYPE_CHECKING
from pyufunc.util_magic import requires, import_package
if TYPE_CHECKING:
    import shutil


# check the current platform
def check_platform() -> str:
    """check the current platform

    Returns:
        str: the current platform

    Example:
        >>> from pyufunc import check_platform
        >>> check_platform()
        'Windows'

        >>> check_platform()
        'Linux'

        >>> check_platform()
        'Darwin'
    """

    import platform
    return "MacOS" if platform.system() == "Darwin" else platform.system()


# Windows
def is_windows() -> bool:
    """check if the current platform is Windows

    Returns:
        bool: True if the current platform is Windows, otherwise False

    Example:
        >>> from pyufunc import is_windows
        >>> is_windows()
        True

        >>> is_windows()
        False
    """

    import platform
    return platform.system() == "Windows"


# Linux
def is_linux() -> bool:
    """check if the current platform is Linux

    Returns:
        bool: True if the current platform is Linux, otherwise False

    Example:
        >>> from pyufunc import is_linux
        >>> is_linux()
        True

        >>> is_linux()
        False
    """

    import platform
    return platform.system() == "Linux"


# Mac/OSX
def is_mac() -> bool:
    """check if the current platform is Mac/OSX

    Returns:
        bool: True if the current platform is Mac/OSX, otherwise False

    Example:
        >>> from pyufunc import is_mac
        >>> is_mac()
        True

        >>> is_mac()
        False
    """

    import platform
    return platform.system() == "Darwin"


@requires("shutil", verbose=False)
def terminal_width() -> int:
    """get the terminal width

    Returns:
        int: the terminal width

    Example:
        >>> from pyufunc import get_terminal_width
        >>> get_terminal_width()
        80

        >>> get_terminal_width()
        120
    """

    import shutil
    return shutil.get_terminal_size().columns


@requires("shutil", verbose=False)
def terminal_height() -> int:
    """get the terminal height

    Returns:
        int: the terminal height

    Example:
        >>> from pyufunc import get_terminal_height
        >>> get_terminal_height()
        24

        >>> get_terminal_height()
        32
    """

    import shutil
    return shutil.get_terminal_size().lines
