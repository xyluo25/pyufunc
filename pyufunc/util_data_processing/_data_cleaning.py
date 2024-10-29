# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, March 13th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import math
import pandas as pd


def get_layer_boundary(df: pd.DataFrame, base_col_name: str, target_col_name: str,
                       base_interval: int = 1, percentile: float = .85) -> pd.DataFrame:
    """Get the boundary values of the target column based on the base column values.

    Args:
        df (pd.DataFrame): the input dataframe
        base_col_name (str): base column name
        target_col_name (str): target column name
        base_interval (int): interval for selecting boundary value. Defaults to 1.
        percentile (float): percentile value for each boundary. Defaults to .85.

    Example:
        >>> import pandas as pd
        >>> import numpy as np
        >>> from pyufunc import get_layer_boundary
        >>> df = pd.DataFrame({'base': np.random.randint(0, 100, 100),
        ...                    'target': np.random.rand(100)})
        >>> get_layer_boundary(df, 'base', 'target', base_interval=1, percentile=.85)

    Raises:
        Exception: if base_col_name or target_col_name is not in the dataframe columns

    Returns:
        pd.DataFrame: _description_
    """

    # TDD development
    if not {base_col_name, target_col_name}.issubset(df.columns):
        raise Exception(
            f'ERROR: {base_col_name} or {target_col_name} is not in the dataframe columns!')

    # get min and max values of the base column
    base_col_min, base_col_max = math.floor(
        df[base_col_name].min()), math.floor(df[base_col_name].max())

    # create criteria for filtering data
    # for each interval, get the mask values
    masks_list = [
        df[base_col_name].between(i, j) for i, j in zip(range(base_col_min,
                                                              base_col_max,
                                                              base_interval),
                                                        range(base_col_min + base_interval,
                                                              base_col_max,
                                                              base_interval))]

    # get the target column values for each interval based on the mask values
    target_values = [df[target_col_name]
                     [i].max() * percentile for i in masks_list]
    return pd.DataFrame({base_col_name: range(base_col_min, base_col_max - base_interval),
                         target_col_name: target_values})
