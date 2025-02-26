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
        >>> str_strip("  ho    g e")
        'ho g e'
    """
    return re.sub(pattern=r"[\s  ]+", repl=" ", string=str(string)).strip()


def str_digit_to_int(string: str) -> int:
    """Convert a string to an integer.

    Args:
        string (str) : string

    Returns:
        int : integer

    Example:
        >>> from pyufunc import str_digit_to_int
        >>> str_digit_to_int("123")
        123
        >>> str_digit_to_int("123.0")
        123
        >>> str_digit_to_int("123.9")
        123
    """

    # TDD
    if not isinstance(string, str):
        raise TypeError("The input must be a string.")

    try:
        return int(re.sub(pattern=r"\.\d+", repl="", string=string))
    except ValueError:
        try:
            return int(float(string))
        except Exception as e:
            raise Exception(f"Error: {e}") from e
    except Exception as e:
        raise Exception(f"Error: {e}") from e


def str_digit_to_float(string: str) -> float:
    """Convert a string to a float.

    Args:
        string (str) : string

    Returns:
        float : float

    Example:
        >>> from pyufunc import str_digit_to_float
        >>> str_digit_to_float("123")
        123.0
        >>> str_digit_to_float("123.0")
        123.0
        >>> str_digit_to_float("123.9")
        123.9
    """

    # TDD
    if not isinstance(string, str):
        raise TypeError("The input must be a string.")

    try:
        return float(string)
    except Exception as e:
        raise Exception(f"Error: {e}") from e
