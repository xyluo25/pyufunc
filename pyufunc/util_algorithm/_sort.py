# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, April 6th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from typing import Iterable


def quick_sort(array: Iterable, verbose: bool = False) -> Iterable:
    """Sort the input array using quick sort algorithm.

    Args:
        array (Iterable): iterable object to be sorted.
        verbose (bool, optional): Whether to print out running time. Defaults to False.

    Raises:
        ValueError: Input should be iterable.

    Returns:
        Iterable: sorted array

    Example:
        >>> from pyufunc import quick_sort
        >>> quick_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> quick_sort([3, 6, 8, 10, 1, 2, 1], verbose=True)
        Running time of quick_sort: O(n log n)
        [1, 1, 2, 3, 6, 8, 10]
    """

    # TDD: Test-Driven Development
    # check if the input is iterable or not
    if not isinstance(array, Iterable):
        raise ValueError("Input should be iterable")

    if len(array) <= 1:
        return array

    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    if verbose:
        print("Running time of quick_sort: O(n log n)")

    return quick_sort(left) + middle + quick_sort(right)


def selection_sort(array: Iterable, verbose: bool = False) -> Iterable:
    """Sort the input array using selection sort algorithm.

    Args:
        array (Iterable): iterable object to be sorted.
        verbose (bool, optional): whether to print out running time. Defaults to False.

    Raises:
        ValueError: Input should be iterable.

    Returns:
        Iterable: sorted array

    Example:
        >>> from pyufunc import selection_sort
        >>> selection_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> selection_sort([3, 6, 8, 10, 1, 2, 1], verbose=True)
        Running time of selection_sort: O(n^2)
        [1, 1, 2, 3, 6, 8, 10]
    """

    # TDD: Test-Driven Development
    # check if the input is iterable or not
    if not isinstance(array, Iterable):
        raise ValueError("Input should be iterable")

    for i in range(len(array)):
        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[min_idx] > array[j]:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        array[i], array[min_idx] = array[min_idx], array[i]

    if verbose:
        print("Running time of selection_sort: O(n^2)")

    return array


def bubble_sort(array: Iterable, verbose: bool = False) -> Iterable:
    """Sort the input array using bubble sort algorithm.

    Args:
        array (Iterable): iterable object to be sorted.
        verbose (bool, optional): whether to print out running time. Defaults to False.

    Raises:
        ValueError: Input should be iterable.

    Returns:
        Iterable: sorted array

    Example:
        >>> from pyufunc import bubble_sort
        >>> bubble_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> bubble_sort([3, 6, 8, 10, 1, 2, 1], verbose=True)
        Running time of bubble_sort: O(n^2)
        [1, 1, 2, 3, 6, 8, 10]
    """

    # TDD: Test-Driven Development
    # check if the input is iterable or not
    if not isinstance(array, Iterable):
        raise ValueError("Input should be iterable")

    n = len(array)
    # Traverse through all array elements
    for i in range(n):
        swapped = False

        # Last i elements are already in place
        for j in range(n - i - 1):

            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True

        # IF no two elements were swapped
        # by the inner loop, then break
        if not swapped:
            break

    if verbose:
        print("Running time of bubble_sort: O(n^2)")

    return array


def insertion_sort():
    pass


def merge_sort():
    pass


def heap_sort():
    pass


def bucket_sort():
    pass


def cycle_sort():
    pass


def cocktail_sort():
    pass


def counting_sort():
    pass


def radix_sort():
    pass


def bingo_sort():
    pass


def shell_sort():
    pass


def tim_sort():
    pass


def comb_sort():
    pass


def pigeonhole_sort():
    pass


def strand_sort():
    pass


def bitonic_sort():
    pass


def pancake_sort():
    pass


def permutation_sort():
    pass


def gnome_sort():
    pass


def sleep_sort():
    pass


def structure_sort():
    pass


def stooge_sort():
    pass


def tag_sort():
    pass


def spread_sort():
    pass


def odd_even_sort():
    pass


def merge_sort_3_way():
    pass
