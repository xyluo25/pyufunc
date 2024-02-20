# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 20th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import

import pytest
from pyufunc.util_data_processing._list import split_list_by_equal_sublist, split_list_by_fixed_length


class TestSplitListByEqualSublist:
    def test_split_list_by_equal_sublist(self):
        lst = list(range(10))
        lst_ = split_list_by_equal_sublist(lst, num_of_sub=3)
        assert [list(dat) for dat in lst_] == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_with_invalid_num_of_sub(self):
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_equal_sublist(list(range(10)), 0))
        assert "num_of_sub should be a positive integer" in str(excinfo.value)

    def test_with_invalid_lst_type(self):
        lst = str(list(range(10)))
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_equal_sublist(lst, 3))
        assert "lst should be a list" in str(excinfo.value)

    def test_with_invalid_num_of_sub_type(self):
        lst = list(range(10))
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_equal_sublist(lst, "3"))
        assert "num_of_sub should be an integer" in str(excinfo.value)

    def test_with_num_of_sub_greater_than_lst_length(self):
        lst = list(range(10))
        lst_ = list(split_list_by_equal_sublist(lst, num_of_sub=20))
        assert lst == lst_


class TestSplitListByFixedLength:
    def test_split_list_by_fixed_length(self):
        lst = list(range(10))
        lst_ = split_list_by_fixed_length(lst, fixed_length=3)
        assert [list(dat) for dat in lst_] == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    def test_with_invalid_length(self):
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_fixed_length(list(range(10)), fixed_length=0))
        assert "fixed_length should be a positive integer" in str(excinfo.value)

    def test_with_invalid_lst_type(self):
        lst = str(list(range(10)))
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_fixed_length(lst, fixed_length=3))
        assert "lst should be a list" in str(excinfo.value)

    def test_with_invalid_length_type(self):
        lst = list(range(10))
        with pytest.raises(AssertionError) as excinfo:
            list(split_list_by_fixed_length(lst, fixed_length="3"))
        assert "fixed_length should be an integer" in str(excinfo.value)

    def test_with_length_greater_than_lst_length(self):
        lst = list(range(10))
        lst_ = split_list_by_fixed_length(lst, fixed_length=20)
        assert [list(dat) for dat in lst_] == [lst]