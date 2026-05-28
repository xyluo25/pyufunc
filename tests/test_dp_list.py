# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 20th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
import pytest

from _path_setup import add_pkg_to_sys_path
from pyufunc import list_split_by_equal_sublist, list_split_by_fixed_length

add_pkg_to_sys_path("pyufunc")


class TestSplitListByEqualSublist:
    """Tests for equal-sublist list splitting."""

    def test_list_split_by_equal_sublist(self):
        """Split a list into the expected number of near-equal sublists."""
        lst = list(range(10))
        lst_ = list_split_by_equal_sublist(lst, num_of_sub=3)
        assert [list(dat) for dat in lst_] == [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def test_with_invalid_num_of_sub(self):
        """Reject a non-positive number of sublists."""
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_equal_sublist(list(range(10)), 0))
        assert "num_of_sub should be a positive integer" in str(excinfo.value)

    def test_with_invalid_lst_type(self):
        """Reject non-list input values."""
        lst = str(list(range(10)))
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_equal_sublist(lst, 3))
        assert "lst should be a list" in str(excinfo.value)

    def test_with_invalid_num_of_sub_type(self):
        """Reject non-integer sublist counts."""
        lst = list(range(10))
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_equal_sublist(lst, "3"))
        assert "num_of_sub should be an integer" in str(excinfo.value)

    def test_with_num_of_sub_greater_than_lst_length(self):
        """Return the original list when requested sublists exceed length."""
        lst = list(range(10))
        lst_ = list(list_split_by_equal_sublist(lst, num_of_sub=20))
        assert lst == lst_


class TestSplitListByFixedLength:
    """Tests for fixed-length list splitting."""

    def test_list_split_by_fixed_length(self):
        """Split a list into fixed-length chunks."""
        lst = list(range(10))
        lst_ = list_split_by_fixed_length(lst, fixed_length=3)
        assert [list(dat) for dat in lst_] == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    def test_with_invalid_length(self):
        """Reject a non-positive fixed length."""
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_fixed_length(list(range(10)), fixed_length=0))
        assert "fixed_length should be a positive integer" in str(excinfo.value)

    def test_with_invalid_lst_type(self):
        """Reject non-list input values."""
        lst = str(list(range(10)))
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_fixed_length(lst, fixed_length=3))
        assert "lst should be a list" in str(excinfo.value)

    def test_with_invalid_length_type(self):
        """Reject non-integer fixed lengths."""
        lst = list(range(10))
        with pytest.raises(AssertionError) as excinfo:
            list(list_split_by_fixed_length(lst, fixed_length="3"))
        assert "fixed_length should be an integer" in str(excinfo.value)

    def test_with_length_greater_than_lst_length(self):
        """Return the full list as one chunk when fixed length exceeds length."""
        lst = list(range(10))
        lst_ = list_split_by_fixed_length(lst, fixed_length=20)
        assert [list(dat) for dat in lst_] == [lst]
