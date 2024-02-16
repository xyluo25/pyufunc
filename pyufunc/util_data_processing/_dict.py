# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import itertools
from typing import Generator


def split_dict_by_chunk(dictionary: dict, chunk_size: int, pair_val: list = []) -> Generator:
    """Split dictionary into chunks

    Args:
        dictionary (dict): the input dictionary with key-value pairs
        chunk_size (int): the size of each chunk
        pair_val (list, optional): the return value associate with each chunk dictionary. Defaults to [].

    Returns:
        Generator: a generator of the list including a chunk value and the pair value: [chunk_dict, pair_val]

    Yields:
        Iterator[list]: a generator of the list including a chunk value and the pair value: [chunk_dict, pair_val]

    Examples:
        >>> import pyufunc as uf
        >>> d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> chunk_size = 2
        >>> pair_val = []
        >>> res = uf.split_dict_by_chunk(d, chunk_size, pair_val)
        >>> for r in res:
        ...     print(r)
        [{'a': 1, 'b': 2}]
        [{'c': 3, 'd': 4}]

    """
    iterator = iter(dictionary.items())
    for _ in range(0, len(dictionary), chunk_size):
        chunk = dict(itertools.islice(iterator, chunk_size))
        if chunk:  # check if chunk is not empty
            yield [chunk] + pair_val