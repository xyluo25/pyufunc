# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import re


def str_strip(string: str) -> str:
    """Convert all consecutive whitespace characters to `' '` (half-width whitespace),
    then return a copy of the string with leading and trailing whitespace removed.

    Args:
        string (str) : string

    Returns:
        str : string

    Example:
        >>> from pyufunc import str_strip
        >>> str_strip(" hoge   ")
        'hoge'
        >>> str_strip(" ho    ge   ")
        'ho ge'
        >>> str_strip("  ho    g　e")
        'ho g e'
    """
    return re.sub(pattern=r"[\s 　]+", repl=" ", string=str(string)).strip()
