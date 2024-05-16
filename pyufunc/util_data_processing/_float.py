# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, May 16th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from typing import Any


def is_float(value: Any = "") -> bool:
    """Check if the value can be converted to float

    Args:
        val (Any): the value to be checked

    Returns:
        bool : if the value can be converted to float

    Examples:
        >>> from pyufunc import is_cvt_to_float
        >>> is_cvt_to_float(1)
        True
        >>> is_cvt_to_float("1")
        True
        >>> is_cvt_to_float("1.0")
        True
        >>> is_cvt_to_float("1.0.0")
        False
        >>> is_cvt_to_float("abc")
        False
    """

    if value and isinstance(value, (int, float, str)):
        try:
            float(value)
            return True
        except ValueError:
            return False
    else:
        return False
