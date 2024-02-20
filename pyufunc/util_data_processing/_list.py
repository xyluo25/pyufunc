# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from typing import Generator


def split_list_by_equal_sublist(lst: list, num_of_sub: int) -> Generator:
    """Split a list into a number of equally-sized sub-lists.

    See Also:
        [`OPS-SL-1 <https://stackoverflow.com/questions/312443/>`_].

    Args:
        lst (list): a list of elements
        num_of_sub (int): number of sub-lists

    Returns:
        Generator: a sequence of sub-lists

    Examples:
        >>> import pyufunc as uf
        >>> lst = list(range(0, 10))
        >>> lst
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> lst_ = uf.split_list_by_equal_chunks(lst, num_of_sub=3)
        >>> for dat in lst_:
        ...     print(list(dat))
        [0, 1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]
    """

    # TDD, Test-Driven Development: validate inputs
    assert isinstance(lst, list), "lst should be a list"
    assert isinstance(num_of_sub, int), "num_of_sub should be an integer"
    assert num_of_sub > 0, "num_of_sub should be a positive integer"

    if num_of_sub >= len(lst):
        print(f"  num_of_sub: {num_of_sub} is greater than or equal to the length of lst: {len(lst)}")
        print(f"  Return the original list: {lst}")
        yield from lst
    else:
        sub_size, mod_value = divmod(len(lst), num_of_sub)
        # equally split the list
        if mod_value == 0:
            for i in range(0, len(lst), sub_size):
                yield lst[i:i + sub_size]

        # split the list with the mod value
        else:
            mod_value_count = 0
            for i in range(num_of_sub):
                if mod_value_count < mod_value:
                    yield lst[i * (sub_size + 1):(i + 1) * (sub_size + 1)]
                    mod_value_count += 1
                else:
                    yield lst[i * sub_size + mod_value:(i + 1) * sub_size + mod_value]


def split_list_by_fixed_length(lst: list, fixed_length: int) -> Generator:
    """Split a list into sublist of the same specified length

    See Also:
        [`OPS-SL-2 <https://stackoverflow.com/questions/312443/>`_].

    Args:
        lst (list): a list of elements
        length (int): the length of each sub-list

    Returns:
        Generator: a sequence of sub-lists

    Examples:
        >>> import pyufunc as uf
        >>> lst = list(range(0, 10))
        >>> lst
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> lst_ = uf.split_list_by_fixed_length(lst, fix_length=3)
        >>> for dat in lst_:
        ...     print(list(dat))
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9]
    """

    # TDD, Test-Driven Development: validate inputs
    assert isinstance(lst, list), "lst should be a list"
    assert isinstance(fixed_length, int), "fixed_length should be an integer"
    assert fixed_length > 0, "fixed_length should be a positive integer"

    for i in range(0, len(lst), fixed_length):
        yield lst[i:i + fixed_length]
