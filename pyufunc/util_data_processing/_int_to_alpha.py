# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, February 16th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


def cvt_int_to_alpha(num: int) -> str:
    """
    Convert an integer to an alphabet string.

    Args:
        num (int): an integer

    Returns:
        str: an alphabet string

    Example::
        >>> from pyufunc import cvt_int_to_alpha
        >>> cvt_int_to_alpha(0)
        'A'
        >>> cvt_int_to_alpha(25)
        'Z'
        >>> cvt_int_to_alpha(26)
        'AA'
        >>> cvt_int_to_alpha(27)
        'AB'
    """
    # alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num < 26:
        # return alpha[num]
        return chr(num + 65)
    else:
        return cvt_int_to_alpha((num // 26) - 1) + cvt_int_to_alpha(num % 26)