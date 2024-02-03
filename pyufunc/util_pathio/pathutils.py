# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

"""functions in this module
    path2linux
    path2uniform
    get_filenames_by_ext
    check_files_existence
    check_filename
"""


from __future__ import absolute_import
from pathlib import Path
import os


def path2linux(path: str | Path) -> str:
    """convert path to linux path for all OSes

    Windows is smart enough to handle all paths from other OSes, but for other OSes, they can not handle windows paths.
    linux paths are friendly to all OSes, Finally, we use linux paths in all OSes.

    Besides, the reason not use normalize_path or unify_path or path2uniform but path2linux is that: the author is a big fan of Linux.
    As an alternative, you can use path2uniform, which is the same as path2linux.

    Location:
        pyutilkit/pathio/pathutils.py

    Args:
        path (str | Path): _description_

    Returns:
        str: a unified linux path

    Examples:
        >>> import pyutilkit as uk
        >>> uk.path2linux('C:\\Users\\Administrator\\Desktop\\test\\test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
        >>> uk.path2linux('./test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
    """

    # the absolute path
    path = os.path.abspath(path)

    try:
        return path.replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def path2uniform(path: str | Path) -> str:
    """Convert path to a uniform path for all OSes
    This function is an alternative function of path2linus.

    References:
        source: https://github.com/mikeqfu/pyhelpers (GNU)

    Location:
        pyutilkit/pathio/pathutils.py

    Args:
        path (str | Path): the path to be converted

    Returns:
        str: a uniform path

    Examples:
        >>> import pyutilkit as uk
        >>> uk.path2linux('C:\\Users\\Administrator\\Desktop\\test\\test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
        >>> uk.path2linux('./test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
    """

    # the absolute path
    path = os.path.abspath(path)

    try:
        return path.replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def get_filenames_by_ext(path_to_dir: str | Path, file_ext="csv", incl_subdir: bool = False) -> list[str]:
    """Get a list of filenames in a folder by file extension

    Location:
        pyutilkit/pathio/pathutils.py

    References:
        https://github.com/mikeqfu/pyhelpers (GNU)

    Args:
        path_to_dir (str | Path): the path to the folder
        file_ext (str, optional): the file extension to be specified. Defaults to "csv".
        incl_subdir (bool, optional): Whether to traverse all files inside sub folder. Defaults to False.

    Returns:
        list[str]: a list of filenames with absolute paths

    Examples:
        >>> import pyutilkit as uk
        >>> uk.get_filenames_by_ext('./', 'py')
        ['C:/Users/Administrator/Desktop/test/test.py']

    """

    if incl_subdir:
        files_list = []
        for root, _, files in os.walk(path_to_dir):
            files_list.extend([os.path.join(root, file) for file in files])

        if file_ext in {None, "*", "all"}:
            return [path2linux(file) for file in files_list]

        return [path2linux(file) for file in files_list if file.endswith(file_ext)]

    # Files in the first layer of the folder
    if file_ext in {None, "*", "all"}:
        return [path2linux(os.path.join(path_to_dir, file)) for file in os.listdir(path_to_dir)]

    return [path2linux(os.path.join(path_to_dir, file)) for file in os.listdir(path_to_dir)
            if file.endswith(file_ext)]


def check_files_existence(filenames: list[str | Path], path_to_dir: str | Path = "", incl_subdir: bool = False) -> bool:
    """Check if provided list of files exist in the given directory

    Location:
        pyutilkit/pathio/pathutils.py

    References:
        https://github.com/xyluo25/utdf2gmns (Apache)
        https://github.com/mikeqfu/pyhelpers (GNU)

    Args:
        filenames (list[str  |  Path]): a list of filenames to be checked
        path_to_dir (str | Path, optional): the given directory. Defaults to "".
            if path_to_dir is not given, use the current working directory

    Returns:
        bool: True if all files exist in the given directory, otherwise False

    Examples:
        >>> import pyutilkit as uk
        >>> uk.check_files_existence(['./test.py', './test.txt'])
        False
    """

    # if path_to_dir is not given, use the current working directory
    if not path_to_dir:
        path_to_dir = path2linux(Path.cwd().absolute())

    # get all filenames in the given directory
    filenames_in_dir = get_filenames_by_ext(path_to_dir, file_ext=None, incl_subdir=incl_subdir)

    # format the input check filenames
    filenames = [path2linux(filename) for filename in filenames]

    filenames_short = [filename.split("/")[-1] for filename in filenames]
    filenames_in_dir_short = [filename.split("/")[-1] for filename in filenames_in_dir]

    # check if all filenames in the given directory, mast have same length of filenames
    mask = [filename in filenames_in_dir_short for filename in filenames_short]

    if all(mask):
        return True

    err_prt_dat = [filenames_short[i] for i in range(len(filenames_short)) if not mask[i]]
    err_msg = f"Error: Required files are not satisfied, missing files are: {err_prt_dat}"
    print(err_msg)
    return False


def check_filename(filename: str | Path, suffix_num: int = 1) -> str:
    """validate the filename, if the file exists, add a suffix number to the file name, and return the new file name
    if the file does not exist, return the original file name

    This function is extremely useful when you want to save a file, but not sure if the file already exists.

    Location:
        pyutilkit/pathio/pathutils.py

    Args:
        filename (str | Path): the filename to be validated
        suffix_num (int, optional): the integer number to be added to the end of filename. Defaults to 1.

    Returns:
        str: validated filename

    Examples:
        >>> import pyutilkit as uk
        >>> uk.validate_filename('./test.txt')
        >>> # file not exist, return the same absolute file name
        'C:/Users/Administrator/Desktop/test/test.txt'

        >>> uk.validate_filename('./test.txt')
        >>> # file exist, return the file name with suffix number added by 1
        'C:/Users/Administrator/Desktop/test/test(1).txt'

    """

    # convert the path to standard linux path
    filename_abspath = path2linux(os.path.abspath(filename))

    # get the file suffix
    file_suffix = filename_abspath.split(".")[-1]
    file_without_suffix = filename_abspath[:-len(file_suffix) - 1]

    # remove the suffix if the file name contains "("
    if "(" in file_without_suffix:
        file_without_suffix = file_without_suffix.split("(")[0]

    # if the file exist, return the file name with suffix number added by 1
    if os.path.exists(filename_abspath):
        filename_update = f"{file_without_suffix}({suffix_num}).{file_suffix}"
        return check_filename(filename_update, suffix_num + 1)

    # if the file does not exist, return the same file name
    return filename_abspath
