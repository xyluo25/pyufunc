# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from pyufunc.util_pathio._path import path2linux
import os
import sys


def get_file_size(filename: str, unit: str = "kb") -> str:
    """Get the size of a file in the specified unit.

    Args:
        filename (str): The filename of the file to get the size of.
        unit (str, optional): the unit for the filesize ('kb', 'mb', 'gb', 'tb') . Defaults to "kb".

    Returns:
        str: _description_
    """

    import os

    # format the filename to linux path
    filename = path2linux(filename)

    filename_short = os.path.basename(filename)

    # Check if the file exists
    if not os.path.isfile(filename):
        return f"File {filename_short} does not found, please check the file path and try again"

    # Get the file size in bytes
    size_bytes = os.path.getsize(filename)

    # Convert the size to the specified unit
    if unit.lower() == 'kb':
        return f"Filesize: {filename_short} {size_bytes / 1024} {unit}"
    elif unit.lower() == 'mb':
        return f"Filesize: {filename_short} {size_bytes / (1024 ** 2)} {unit}"
    elif unit.lower() == 'gb':
        return f"Filesize: {filename_short} {size_bytes / (1024 ** 3)} {unit}"
    elif unit.lower() == 'tb':
        return f"Filesize: {filename_short} {size_bytes / (1024 ** 4)} {unit}"

    return f"Filesize: {filename_short} {size_bytes / 1024} kb"


def get_dir_size(directory: str, unit: str = "kb") -> str:
    """Get the size of a directory in the specified unit.

    Args:
        directory (str): The directory to get the size of.
        unit (str, optional): the unit for the directory ('kb', 'mb', 'gb', 'tb'). Defaults to "kb".

    Returns:
        str: the size of the directory in the specified unit.
    """

    import os

    # format the directory to linux path
    directory = path2linux(directory)

    directory_short = os.path.basename(directory)

    # Check if the directory exists
    if not os.path.isdir(directory):
        return f"Directory {directory_short} does not found, please check the directory path and try again"

    # Get the size of the directory in bytes
    size_bytes = sum([os.path.getsize(os.path.join(directory, file)) for file in os.listdir(directory)])

    # Convert the size to the specified unit
    if unit.lower() == 'kb':
        return f"Directory size: {directory_short} {size_bytes / 1024} {unit}"
    elif unit.lower() == 'mb':
        return f"Directory size: {directory_short} {size_bytes / (1024 ** 2)} {unit}"
    elif unit.lower() == 'gb':
        return f"Directory size: {directory_short} {size_bytes / (1024 ** 3)} {unit}"
    elif unit.lower() == 'tb':
        return f"Directory size: {directory_short} {size_bytes / (1024 ** 4)} {unit}"

    # return the size in kb by default
    return f"Directory size: {directory_short} {size_bytes / 1024} kb"


# def write_yaml_file(func=None, *, log_dir: str | Path = LOGGING_FOLDER, ):
#     import yaml
#     with open(file_path, 'w') as f:
#         yaml.dump(data, f, default_flow_style=False)
