# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from _data_cleaning import get_layer_boundary
from ._dict import (dict_split_by_chunk,
                    dict_delete_keys)
from ._int_to_alpha import cvt_int_to_alpha
from ._list import (list_split_by_equal_sublist,
                    list_split_by_fixed_length,
                    list_flatten_nested)
from ._float import is_float
from ._str import (str_strip,
                   cvt_digit_str_to_int,
                   cvt_digit_str_to_float)

from ._dataclass import (create_dataclass,
                         create_dataclass_from_dict,
                         merge_dataclass,
                         extend_dataclass,
                         dataclass_dict_wrapper)

__all__ = [
    # _data_cleaning
    "get_layer_boundary",

    # _dict
    # "split_dict_by_chunk",
    "dict_split_by_chunk",
    # "delete_dict_keys",
    "dict_delete_keys",

    # _int_to_alpha
    "cvt_int_to_alpha",

    # _list
    "list_split_by_equal_sublist",
    "list_split_by_fixed_length",
    "list_flatten_nested",

    # _float
    "is_float",

    # _str
    "str_strip",
    "cvt_digit_str_to_int",
    "cvt_digit_str_to_float",

    # dataclass
    "create_dataclass",
    "create_dataclass_from_dict",
    "merge_dataclass",
    "extend_dataclass",
    "dataclass_dict_wrapper",
]
