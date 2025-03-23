# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import annotations
from typing import TYPE_CHECKING
import pandas as pd

from pyufunc.util_magic import func_running_time


@func_running_time
def group_dt_yearly(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by year.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int): the time interval to groupby. Defaults to 1.
        col (list): specify input column names.
            if your input column name is not same as default col name, use your own col name.
            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by year with count, mean and sum.

    Example:
        >>> import pandas as pd
        >>> import pyufunc as pf
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2021-12-31", freq="M"), "value": range(24)})
        >>> pf.group_yearly(df, interval=1, col=["datetime", "value"])
        The group_yearly require at least two columns
        first column: datetime
        second column: value
            datetime	count	mean	sum
        0	2020-12-31	12	    5.5	    66
        1	2021-12-31	12	   17.5	    210

    """

    col = ["datetime", "value"] if col is None else col

    print("The group_yearly require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(
        pd.Grouper(key="datetime",
                   axis=0,
                   freq=f"{interval}YE")).agg(["count", "mean", "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res


@func_running_time
def group_dt_monthly(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by month.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int, optional): the time interval to groupby. Defaults to 1.
        col (list, optional): specify input column names.
            if your input column name is not same as default col name, use your own col name.
            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by month with count, mean and sum.

    Example:
        >>> import pyufunc as pf
        >>> import pandas as pd
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2020-12-31", freq="D"), "value": range(366)})
        >>> pf.group_monthly(df, interval=1, col=["datetime", "value"])
        The group_monthly require at least two columns
        first column: datetime
        second column: value
           datetime	count	mean	sum
        0	2020-01-31	31	15.0	465
        1	2020-02-29	29	45.0	1305
        2	2020-03-31	31	75.0	2325
        3	2020-04-30	30	105.5	3165
        4	2020-05-31	31	136.0	4216
        5	2020-06-30	30	166.5	4995
        6	2020-07-31	31	197.0	6107
        7	2020-08-31	31	228.0	7068
        8	2020-09-30	30	258.5	7755
        9	2020-10-31	31	289.0	8959
        10	2020-11-30	30	319.5	9585
        11	2020-12-31	31	350.0	10850
    """

    col = ["datetime", "value"] if col is None else col

    print("The group_monthly require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(
        pd.Grouper(key="datetime",
                   axis=0,
                   freq=f"{interval}ME")).agg(["count", "mean", "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res


@func_running_time
def group_dt_weekly(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by week.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int, optional): the time interval to groupby. Defaults to 1.
        col (list, optional): specify input column names.
            if your input column name is not same as default col name, use your own col name.
            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by week with count, mean and sum.

    Example:
        >>> import pyufunc as pf
        >>> import pandas as pd
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2020-12-31", freq="D"), "value": range(366)})
        >>> pf.group_weekly(df, interval=1, col=["datetime", "value"])
        The group_weekly require at least two columns
        first column: datetime
        second column: value
           datetime	count	mean	sum
        0	2020-01-05	5	2.0	10
        1	2020-01-12	7	8.0	56
        2	2020-01-19	7	15.0	105
        3	2020-01-26	7	22.0	154
        4	2020-02-02	7	29.0	203

    """

    col = ["datetime", "value"] if col is None else col
    print("The group_weekly require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(pd.Grouper(key="datetime",
                                          axis=0,
                                          freq=f"{interval}W")).agg(["count",
                                                                     "mean",
                                                                     "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res


@func_running_time
def group_dt_daily(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by day.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int, optional): the time interval to groupby. Defaults to 1.
        col (list, optional): specify input column names.
            if your input column name is not same as default col name, use your own col name.
            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by day with count, mean and sum.

    Example:
        >>> import pyufunc as pf
        >>> import pandas as pd
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2020-12-31", freq="D"), "value": range(366)})
        >>> pf.group_daily(df, interval=1, col=["datetime", "value"])
         The group_daily require at least two columns
            first column: datetime
            second column: value
            datetime	count	mean	sum
            0	2020-01-01	1	0.0	    0
            1	2020-01-02	1	1.0	    1
            2	2020-01-03	1	2.0	    2
            3	2020-01-04	1	3.0	    3
            4	2020-01-05	1	4.0	    4

    """

    if col is None:
        col = ["datetime", "value"]
    print("The group_daily require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(
        pd.Grouper(key="datetime",
                   axis=0,
                   freq=f"{interval}D")).agg(["count", "mean", "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res


# @requires("pandas", verbose=False)
@func_running_time
def group_dt_hourly(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by hour.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int, optional): the time interval to groupby. Defaults to 1.
        col (list, optional): specify input column names.
            if your input column name is not same as default col name, use your own col name.
            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by hour with count, mean and sum.

    Example:
        >>> import pyufunc as pf
        >>> import pandas as pd
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2020-01-02", freq="h"), "value": range(25)})
        >>> pf.group_hourly(df, interval=1, col=["datetime", "value"])
        The group_hourly require at least two columns
        first column: datetime
        second column: value
            datetime	    count  mean	    sum
        0	2020-01-01 00:00:00	1	0.0	    0
        1	2020-01-01 01:00:00	1	1.0	    1
        2	2020-01-01 02:00:00	1	2.0	    2
        3	2020-01-01 03:00:00	1	3.0	    3
        4	2020-01-01 04:00:00	1	4.0	    4
        5	2020-01-01 05:00:00	1	5.0	    5

    """

    if col is None:
        col = ["datetime", "value"]
    print("The group_hourly require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(
        pd.Grouper(key="datetime",
                   axis=0,
                   freq=f"{interval}h")).agg(["count", "mean", "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res


@func_running_time
def group_dt_minutely(df: pd.DataFrame, interval: int = 1, col: list = None) -> pd.DataFrame:
    """Group the DataFrame by minute.

    Args:
        df (pd.DataFrame): input DataFrame with datetime and value columns
        interval (int, optional): the time interval to groupby. Defaults to 1.
        col (list, optional): specify input column names.

            if your input column name is not same as default col name, use your own col name.

            e.g. ["your_datetime_col_name", "your_value_col_name"]. Defaults to ["datetime", "value"].

    Returns:
        pd.DataFrame: grouped DataFrame by minute with count, mean and sum.

    Example:
        >>> import pyufunc as pf
        >>> import pandas as pd
        >>> df = pd.DataFrame({"datetime": pd.date_range(start="2020-01-01",
        end="2020-01-02", freq="min"), "value": range(1441)})
        >>> pf.group_minutely(df, interval=1, col=["datetime", "value"])
        The group_minutely require at least two columns
        first column: datetime
        second column: value
                datetime	count	mean	sum
        0	2020-01-01 00:00:00	1	0.0	    0
        1	2020-01-01 00:01:00	1	1.0	    1
        2	2020-01-01 00:02:00	1	2.0	    2
        3	2020-01-01 00:03:00	1	3.0	    3
        4	2020-01-01 00:04:00	1	4.0	    4

    """

    if col is None:
        col = ["datetime", "value"]
    print("The group_minutely require at least two columns\n",
          "first column: datetime\n",
          "second column: value")
    interval = interval if interval > 0 else ""
    dataframe = df[col]
    dataframe.columns = ["datetime", "value"]
    dataframe["datetime"] = pd.to_datetime(dataframe["datetime"])
    df_res = dataframe.groupby(
        pd.Grouper(key="datetime",
                   axis=0,
                   freq=f"{interval}min")).agg(["count", "mean", "sum"])
    df_res.reset_index(inplace=True)
    df_res.columns = [i[0] if i[0] == "datetime" else i[1]
                      for i in list(df_res.columns)]
    return df_res