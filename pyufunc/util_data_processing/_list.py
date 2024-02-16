# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


def split_list_by_size(lst, sub_len):
    """
    Split a list into (evenly sized) sub-lists.

    See also [`OPS-SLBS-1 <https://stackoverflow.com/questions/312443/>`_].

    :param lst: a list of any
    :type lst: list
    :param sub_len: length of a sub-list
    :type sub_len: int
    :return: a sequence of ``sub_len``-sized sub-lists from ``lst``
    :rtype: typing.Generator[list]

    **Examples**::

        >>> from pyhelpers.ops import split_list_by_size

        >>> lst_ = list(range(0, 10))
        >>> lst_
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> lists = split_list_by_size(lst_, sub_len=3)
        >>> list(lists)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """

    for i in range(0, len(lst), sub_len):
        yield lst[i:i + sub_len]


def split_list(lst, num_of_sub):
    """
    Split a list into a number of equally-sized sub-lists.

    See also [`OPS-SL-1 <https://stackoverflow.com/questions/312443/>`_].

    :param lst: a list of any
    :type lst: list
    :param num_of_sub: number of sub-lists
    :type num_of_sub: int
    :return: a total of ``num_of_sub`` sub-lists from ``lst``
    :rtype: typing.Generator[list]

    **Examples**::

        >>> from pyhelpers.ops import split_list

        >>> lst_ = list(range(0, 10))
        >>> lst_
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> lists = split_list(lst_, num_of_sub=3)
        >>> list(lists)
        [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
    """

    chunk_size = math.ceil(len(lst) / num_of_sub)
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def split_iterable(iterable, chunk_size):
    """
    Split a list into (evenly sized) chunks.

    See also [`OPS-SI-1 <https://stackoverflow.com/questions/24527006/>`_].

    :param iterable: iterable object
    :type iterable: typing.Iterable
    :param chunk_size: length of a chunk
    :type chunk_size: int
    :return: a sequence of equally-sized chunks from ``iterable``
    :rtype: typing.Generator[typing.Iterable]

    **Examples**::

        >>> from pyhelpers.ops import split_iterable
        >>> import pandas

        >>> iterable_1 = list(range(0, 10))
        >>> iterable_1
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        >>> iterable_1_ = split_iterable(iterable_1, chunk_size=3)
        >>> type(iterable_1_)
        generator

        >>> for dat in iterable_1_:
        ...     print(list(dat))
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9]

        >>> iterable_2 = pandas.Series(range(0, 20))
        >>> iterable_2
        0      0
        1      1
        2      2
        3      3
        4      4
        5      5
        6      6
        7      7
        8      8
        9      9
        10    10
        11    11
        12    12
        13    13
        14    14
        15    15
        16    16
        17    17
        18    18
        19    19
        dtype: int64

        >>> iterable_2_ = split_iterable(iterable_2, chunk_size=5)

        >>> for dat in iterable_2_:
        ...     print(list(dat))
        [0, 1, 2, 3, 4]
        [5, 6, 7, 8, 9]
        [10, 11, 12, 13, 14]
        [15, 16, 17, 18, 19]
    """

    iterator = iter(iterable)
    for x in iterator:
        yield itertools.chain([x], itertools.islice(iterator, chunk_size - 1))



def get_extreme_outlier_bounds(num_dat, k=1.5):
    """
    Get upper and lower bounds for extreme outliers.

    :param num_dat: an array of numbers
    :type num_dat: array-like
    :param k: a scale coefficient associated with interquartile range, defaults to ``1.5``
    :type k: float, int
    :return: lower and upper bound
    :rtype: tuple

    **Examples**::

        >>> from pyhelpers.ops import get_extreme_outlier_bounds
        >>> import pandas

        >>> data = pandas.DataFrame(range(100), columns=['col'])
        >>> data
            col
        0     0
        1     1
        2     2
        3     3
        4     4
        ..  ...
        95   95
        96   96
        97   97
        98   98
        99   99

        [100 rows x 1 columns]

        >>> data.describe()
                      col
        count  100.000000
        mean    49.500000
        std     29.011492
        min      0.000000
        25%     24.750000
        50%     49.500000
        75%     74.250000
        max     99.000000

        >>> lo_bound, up_bound = get_extreme_outlier_bounds(data, k=1.5)
        >>> lo_bound, up_bound
        (0.0, 148.5)
    """

    q1, q3 = np.percentile(num_dat, 25), np.percentile(num_dat, 75)
    iqr = q3 - q1

    lower_bound = np.max([0, q1 - k * iqr])
    upper_bound = q3 + k * iqr

    return lower_bound, upper_bound

