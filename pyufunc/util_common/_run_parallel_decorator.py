# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 1st 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from __future__ import absolute_import
from multiprocessing import Pool
from typing import Iterable, Callable, Iterator
import os
from pyufunc.util_common._func_time_decorator import func_running_time


@func_running_time
def run_parallel(func: Callable, iterable: Iterable,
                 num_processes: int = os.cpu_count() - 1,
                 chunksize: int = 0) -> Iterator:
    """Run a function in parallel with multiple processors.

    Args:
        func (callable): The function to run in parallel.
        iterable (Iterable): The input iterable to the function.
        num_processes (int, optional): The number of processors to use. Defaults to os.cpu_count() - 1.
        chunksize (int, optional): The chunksize for the parallel processing. Defaults to "".

    Returns:
        Iterator: The results of the function.

    Raises:
        TypeError: If the input function is not callable,
            or if chunksize or num_processes are not integers,
            or if iterable is not an Iterable.

        TypeError: if the input iterable is not an Iterable
            The input iterable should be an Iterable.
        TypeError: if the input number of processors is not an integer
        TypeError: if the input chunksize should be an integer
        ValueError: if the input number of processors is not greater than 0
        ValueError: if the input chunksize is not greater than 0

    Examples:
        >>> import numpy as np
        >>> from pyufunc import run_parallel
        >>> def my_func(x):
                print(f"running {x}")
                return x**2
        >>> results = run_parallel(my_func, list(range(10)), num_processes=7)
        >>> for res in results:
                print(res)
        0, 1, 4, 9, 16, 25, 36, 49, 64, 81
    """

    # TDD, test-driven development: check inputs

    if not callable(func):
        raise TypeError("The input function should be a callable.")
    if not isinstance(iterable, Iterable):
        raise TypeError("The input iterable should be an Iterable.")
    if not isinstance(num_processes, int):
        raise TypeError("The input number of processors should be an integer.")
    if not isinstance(chunksize, int):
        raise TypeError("The input chunksize should be an integer.")

    # check the number of processors and chunksize are greater than 0
    if num_processes <= 0:
        raise ValueError("The input number of processors should be greater than 0.")
    if chunksize < 0:
        raise ValueError("The input chunksize should be greater than 0.")

    # Step 1: get the number of processors to use
    num_processors = min(num_processes, os.cpu_count() - 1)
    print(f"  :Info: using {num_processors} processors to run {func.__name__}...")

    # Step 2: check the chunksize
    if chunksize >= len(iterable):
        chunksize = len(iterable) // num_processors

    # Step 3: run the function in parallel
    with Pool(num_processors) as pool:
        if chunksize == 0:
            results = pool.map(func, iterable)
        else:
            results = pool.map(func, iterable, chunksize=chunksize)

    return results
