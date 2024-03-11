# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, March 11th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import re


def is_valid_email(email: str) -> bool:
    """check if the email is valid

    Args:
        email (str): email address, eg. luoxiangyong01@gmail.com

    Returns:
        bool: True if the email is valid, False otherwise

    Examples:
        >>> from pyufunc import is_valid_email
        >>> is_valid_email("luoxiangyong01@gamil.com")
        True
        >>> is_valid_email("luoxiangyong01")
        False

    """

    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
