# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import socket
import re


def get_host_name() -> str:
    """Get the computer name.

    Returns:
        str: computer name.

    Examples:
        >>> import pyufunc as pf
        >>> pf.get_computer_name()
        'Xiangyong-PC'

    """
    return socket.gethostname()


def get_host_ip() -> str:
    """Get the computer IP address.

    Returns:
        str: computer IP address.

    Examples:
        >>> import pyufunc as pf
        >>> pf.get_computer_ip()
        '10.155.33.252'

    """
    computer_name = get_host_name()
    return socket.gethostbyname(computer_name)


def validate_url(url: str) -> bool:
    """Validate the URL.

    Args:
        url (str): the URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    return bool(re.match(r'^https?:/{2}\w.+$', url))
