# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import itertools
from typing import Union


def dict_split_by_chunk(dictionary: dict, chunk_size: int) -> list:
    """Split dictionary into a list of chunks

    Args:
        dictionary (dict): the input dictionary with key-value pairs
        chunk_size (int): the size of each chunk

    Returns:
        list: a list of the chunk_dict

    See also:
        split_dict_by_chunk

    Examples:
        >>> import pyufunc as uf
        >>> d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> chunk_size = 2
        >>> res = uf.split_dict_by_chunk(d, chunk_size)
        >>> res
        [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]

    """

    chunk_lst = []
    iterator = iter(dictionary.items())
    for _ in range(0, len(dictionary), chunk_size):
        if chunk := dict(itertools.islice(iterator, chunk_size)):
            chunk_lst.append(chunk)
    return chunk_lst


def dict_delete_keys(dictionary: dict, keys: Union[list, str, tuple]) -> dict:
    """Delete keys from dictionary

    Args:
        dictionary (dict): the input dictionary with key-value pairs
        keys (list): the keys to be deleted

    Returns:
        dict: the dictionary after deleting keys

    Examples:
        >>> import pyufunc as uf
        >>> d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> keys = ['a', 'b']
        >>> res = uf.delete_dict_keys(d, keys)
        >>> res
        {'c': 3, 'd': 4}

    """

    if not isinstance(keys, (list, str, tuple)):
        raise ValueError("keys must be a list, str or tuple")

    if isinstance(keys, str):
        keys = [keys]

    return {k: v for k, v in dictionary.items() if k not in keys}
