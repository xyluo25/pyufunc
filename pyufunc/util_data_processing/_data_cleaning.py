# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, March 13th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import annotations

import math
from typing import TYPE_CHECKING
from pyufunc.util_magic._dependency_requires_decorator import requires

if TYPE_CHECKING:
    import pandas as pd


@requires('pandas')
def get_layer_boundary(df: pd.DataFrame, x_col_name: str, y_col_name: str,
                       base_interval: int = 1, percentile: float = .85) -> pd.DataFrame:
    """Get the boundary values of the target column based on the base column values.

    Notes:
        - x_col_name also known as x axis in 2D space, y_col_name also known as y axis in 2D space.
        - The boundary values are calculated based on the max value of the target column
            for each interval of the base column values.
        - The interval is defined by the base_interval parameter.
        - The percentile parameter is used to calculate the boundary values based on
            the max value of the target column for each interval.

    Args:
        df (pd.DataFrame): the input dataframe
        x_col_name (str): x column name
        y_col_name (str): y column name
        base_interval (int): interval for selecting boundary value. Defaults to 1.
        percentile (float): percentile value for each boundary. Defaults to .85.

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> from pyufunc import get_layer_boundary
        >>> df = pd.DataFrame({'x': np.random.randint(0, 100, 100),
        ...                    'y': np.random.rand(100)})
        >>> get_layer_boundary(df, 'x', 'y', base_interval=1, percentile=.85)

    Raises:
        Exception: if x_col_name or y_col_name is not in the dataframe columns

    Returns:
        pd.DataFrame: a dataframe with the boundary values of the target column based on the base column values.
    """

    import pandas as pd

    # TDD development
    if not {x_col_name, y_col_name}.issubset(df.columns):
        raise Exception(
            f'ERROR: {x_col_name} or {y_col_name} is not in the dataframe columns!')

    # get min and max values of the base column
    x_col_min, x_col_max = math.floor(
        df[x_col_name].min()), math.floor(df[x_col_name].max())

    # create criteria for filtering data
    # for each interval, get the mask values
    masks_list = [
        df[x_col_name].between(i, j) for i, j in zip(range(x_col_min,
                                                           x_col_max,
                                                           base_interval),
                                                     range(x_col_min + base_interval,
                                                           x_col_max + base_interval,
                                                           base_interval))]

    # get the target column values for each interval based on the mask values
    target_values = [df[y_col_name]
                     [i].max() * percentile for i in masks_list]
    return pd.DataFrame({x_col_name: range(x_col_min, x_col_max, base_interval),
                         y_col_name: target_values})
