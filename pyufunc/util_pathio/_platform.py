# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

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
    return platform.system()


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