# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, April 9th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
from pyufunc.util_magic import requires, import_package
import numpy as np


# @requires("numpy", verbose=False)
def mean_absolute_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate mean absolute error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The mean absolute error

    Example:
        >>> from pyufunc import mean_absolute_error
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> mean_absolute_error(y_true, y_pred)
        0.5
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.mean(np.abs(y_true - y_pred))


# @requires("numpy", verbose=False)
def mean_squared_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate mean squared error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The mean squared error

    Example:
        >>> from pyufunc import mean_squared_error
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> mean_squared_error(y_true, y_pred)
        0.375
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.mean(np.square(y_true - y_pred))


# @requires("numpy", verbose=False)
def mean_squared_log_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate mean squared log error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The mean squared log error

    Example:
        >>> from pyufunc import mean_squared_log_error
        >>> y_true = [3, 5, 2.5, 7]
        >>> y_pred = [2.5, 5, 4, 8]
        >>> mean_squared_log_error(y_true, y_pred)
        0.03973012298459379
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.mean(np.square(np.log1p(y_true) - np.log1p(y_pred)))


# @requires("numpy", verbose=False)
def root_mean_squared_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate root mean squared error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The root mean squared error

    Example:
        >>> from pyufunc import root_mean_squared_error
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> root_mean_squared_error(y_true, y_pred)
        0.6123724356957945
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.sqrt(np.mean(np.square(y_true - y_pred)))


# @requires("numpy", verbose=False)
def mean_absolute_percentage_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate mean absolute percentage error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Returns:
        float, The mean absolute percentage error

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Example:
        >>> from pyufunc import mean_absolute_percentage_error
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> mean_absolute_percentage_error(y_true, y_pred)
        0.3273809523809524
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.mean(np.abs((y_true - y_pred) / y_true))


# @requires("numpy", verbose=False)
def mean_percentage_error(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate mean percentage error between y_true and y_pred

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The mean percentage error

    Example:
        >>> from pyufunc import mean_percentage_error
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> mean_percentage_error(y_true, y_pred)
        0.08134920634920635
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return np.mean((y_true - y_pred) / y_true)


# @requires("numpy", verbose=False)
def r2_score(y_true: Iterable, y_pred: Iterable) -> float:
    """Calculate R^2 (coefficient of determination) regression score function.

    Args:
        y_true: Iterable, The true values
        y_pred: Iterable, The predicted values

    Raises:
        TypeError: If y_true or y_pred is not an iterable object
        TypeError: Input should be an iterable object

    Returns:
        float, The R^2 score

    Example:
        >>> from pyufunc import r2_score
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> r2_score(y_true, y_pred)
        0.9486081370449679
    """
    # import_package("numpy", verbose=False)
    # import numpy as np

    # TDD: check if y_true and y_pred are iterable
    if not isinstance(y_true, Iterable):
        raise TypeError("Input should be an iterable object")
    if not isinstance(y_pred, Iterable):
        raise TypeError("Input should be an iterable object")

    # covert to numpy array if not
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    mean_y = np.mean(y_true)
    ss_res = np.sum(np.square(y_true - y_pred))
    ss_tot = np.sum(np.square(y_true - mean_y))

    return 1 - ss_res / ss_tot
