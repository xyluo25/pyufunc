# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from ._dict import (split_dict_by_chunk,
                    dict_split_by_chunk,
                    delete_dict_keys,
                    dict_delete_keys)
from ._int_to_alpha import cvt_int_to_alpha
from ._list import (split_list_by_equal_sublist,
                    split_list_by_fixed_length,
                    flat_nested_list)
from ._float import is_float
from ._str import str_strip

from ._dataclass import (create_dataclass,
                         create_dataclass_from_dict,
                         merge_dataclass,
                         extend_dataclass,
                         dataclass_dict_access)

__all__ = [
    # _dict
    "split_dict_by_chunk",
    "dict_split_by_chunk",
    "delete_dict_keys",
    "dict_delete_keys",

    # _int_to_alpha
    "cvt_int_to_alpha",

    # _list
    "split_list_by_equal_sublist",
    "split_list_by_fixed_length",
    "flat_nested_list",

    # _float
    "is_float",

    # _str
    "str_strip",

    # dataclass
    "create_dataclass",
    "create_dataclass_from_dict",
    "merge_dataclass",
    "extend_dataclass",
    "dataclass_dict_access",
]
