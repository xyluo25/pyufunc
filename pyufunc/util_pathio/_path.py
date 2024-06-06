# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from __future__ import absolute_import
from pathlib import Path
import os
import re
from typing import Callable, Union
from pyufunc.pkg_configs import config_color


def path2linux(path: str | Path) -> str:
    """convert path to linux path for all OSes

    Windows is smart enough to handle all paths from other OSes, but for other OSes, they can not handle windows paths.
    linux paths are friendly to all OSes, Finally, we use linux paths in all OSes.

    Besides, the reason not use normalize_path or unify_path or path2uniform but path2linux is that: the author is a big fan of Linux.

    As an alternative, you can use path2uniform, which is the same as path2linux.

    Location:
        pyufunc/util_pathio/_path.py

    Args:
        path (str | Path): _description_

    Returns:
        str: a unified linux path

    Examples:
        >>> import pyufunc as uf
        >>> uf.path2linux('C:\\Users\\Administrator\\Desktop\\test\\test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
        >>> uf.path2linux('./test.txt')
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
        pyufunc/util_pathio/_path.py

    Args:
        path (str | Path): the path to be converted

    Returns:
        str: a uniform path

    Examples:
        >>> import pyufunc as uf
        >>> uf.path2linux('C:\\Users\\Administrator\\Desktop\\test\\test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
        >>> uf.path2linux('./test.txt')
        'C:/Users/Administrator/Desktop/test/test.txt'
    """

    # the absolute path
    path = os.path.abspath(path)

    try:
        return path.replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def get_filenames_by_ext(dir_path: str | Path, file_ext: str | list = "csv", incl_subdir: bool = False) -> list[str]:
    """Get a list of filenames in a folder by file extension

    Location:
        pyufunc/util_pathio/_path.py

    References:
        https://github.com/mikeqfu/pyhelpers (GNU)

    See Also:
        get_files_by_ext

    Args:
        dir_path (str | Path): the path to the folder
        file_ext (str | list | tuple, optional): the file extension to be specified. Defaults to "csv".
        incl_subdir (bool, optional): Whether to traverse all files inside sub folder. Defaults to False.

    Returns:
        list[str]: a list of filenames with absolute paths

    Examples:
        >>> import pyufunc as uf
        >>> uf.get_filenames_by_ext('./', 'py')
        ['C:/Users/Administrator/Desktop/test/test.py']

    """

    # convert file extension to tuple
    if isinstance(file_ext, str):
        file_ext = (file_ext,)
    if isinstance(file_ext, (list, tuple)):
        file_ext = tuple(file_ext)

    if not file_ext:
        file_ext = ("*",)

    if incl_subdir:
        files_list = []
        for root, _, files in os.walk(dir_path):
            files_list.extend([os.path.join(root, file) for file in files])

        if file_ext[0] in {None, "*", "all"}:
            return [path2linux(file) for file in files_list]

        return [path2linux(file) for file in files_list if file.endswith(file_ext)]

    # Files in the first layer of the folder
    if file_ext[0] in {None, "*", "all"}:
        return [path2linux(os.path.join(dir_path, file)) for file in os.listdir(dir_path)]

    return [path2linux(os.path.join(dir_path, file)) for file in os.listdir(dir_path)
            if file.endswith(file_ext)]


def get_files_by_ext(dir_path: str | Path, file_ext: str | list = "csv", incl_subdir: bool = False) -> list[str]:
    """Get a list of filenames in a folder by file extension

    Location:
        pyufunc/util_pathio/_path.py

    References:
        https://github.com/mikeqfu/pyhelpers (GNU)

    See Also:
        get_filenames_by_ext

    Args:
        dir_path (str | Path): the path to the folder
        file_ext (str | list | tuple, optional): the file extension to be specified. Defaults to "csv".
        incl_subdir (bool, optional): Whether to traverse all files inside sub folder. Defaults to False.

    Returns:
        list[str]: a list of filenames with absolute paths

    Examples:
        >>> import pyufunc as uf
        >>> uf.get_filenames_by_ext('./', 'py')
        ['C:/Users/Administrator/Desktop/test/test.py']

    """

    # convert file extension to tuple
    if isinstance(file_ext, str):
        file_ext = (file_ext,)
    if isinstance(file_ext, (list, tuple)):
        file_ext = tuple(file_ext)

    if not file_ext:
        file_ext = ("*",)

    if incl_subdir:
        files_list = []
        for root, _, files in os.walk(dir_path):
            files_list.extend([os.path.join(root, file) for file in files])

        if file_ext[0] in {None, "*", "all"}:
            return [path2linux(file) for file in files_list]

        return [path2linux(file) for file in files_list if file.endswith(file_ext)]

    # Files in the first layer of the folder
    if file_ext[0] in {None, "*", "all"}:
        return [path2linux(os.path.join(dir_path, file)) for file in os.listdir(dir_path)]

    return [path2linux(os.path.join(dir_path, file)) for file in os.listdir(dir_path)
            if file.endswith(file_ext)]


def check_files_in_dir(filenames: list[str | Path], dir_path: str | Path = "", incl_subdir: bool = False) -> bool:
    """Check if provided list of files exist in the given directory

    Location:
        pyufunc/util_pathio/_path.py

    References:
        https://github.com/xyluo25/utdf2gmns (Apache)
        https://github.com/mikeqfu/pyhelpers (GNU)

    Args:
        filenames (list[str  |  Path]): a list of filenames to be checked
        dir_path (str | Path, optional): the given directory. Defaults to "".
            if dir_path is not given, use the current working directory

    Returns:
        bool: True if all files exist in the given directory, otherwise False

    Examples:
        >>> import pyufunc as uf
        >>> uf.check_files_existence(['./test.py', './test.txt'])
        False
    """

    # if dir_path is not given, use the current working directory
    if not dir_path:
        dir_path = path2linux(Path.cwd().absolute())

    # get all filenames in the given directory
    filenames_in_dir = get_filenames_by_ext(
        dir_path, file_ext="*", incl_subdir=incl_subdir)

    # format the input check filenames
    filenames = [path2linux(filename) for filename in filenames]

    filenames_short = [filename.split("/")[-1] for filename in filenames]
    filenames_in_dir_short = [filename.split("/")[-1] for filename in filenames_in_dir]

    # check if all filenames in the given directory, mast have same length of filenames
    mask = [filename in filenames_in_dir_short for filename in filenames_short]

    if all(mask):
        return True

    err_prt_dat = [filenames_short[i] for i in range(len(filenames_short)) if not mask[i]]
    err_msg = f"Error: files existence are not satisfied, missing files are: {err_prt_dat}"
    print(err_msg)
    return False


def check_filename(filename: str | Path) -> bool:
    """validate the filename, if the file exists, return True, otherwise False

    Location:
        pyufunc/util_pathio/_path.py

    See Also:
        check_file_existence

    Args:
        filename (str | Path): the filename to be validated

    Returns:
        bool: True if the file exists, otherwise False

    Examples:
        >>> import pyufunc as uf
        >>> uf.check_filename('./test.txt')
        False

    """

    # convert the path to standard linux path
    filename_abspath = path2linux(os.path.abspath(filename))

    # if the file exist, return True, otherwise False
    return bool(os.path.exists(filename_abspath))


def check_file_existence(filename: str | Path) -> bool:
    """validate the filename, if the file exists, return True, otherwise False

    Location:
        pyufunc/util_pathio/_path.py

    See Also:
        check_filename

    Args:
        filename (str | Path): the filename to be validated

    Returns:
        bool: True if the file exists, otherwise False

    Examples:
        >>> import pyufunc as uf
        >>> uf.check_filename('./test.txt')
        False
    """

    # convert the path to standard linux path
    filename_abspath = path2linux(os.path.abspath(filename))

    # if the file exist, return True, otherwise False
    return bool(os.path.exists(filename_abspath))


def generate_unique_filename(filename: str | Path, suffix_num: int = 1) -> str:
    """generate a unique filename by adding a suffix number to the end of the filename

    This function is extremely useful when you want to save a file, but not sure if the file already exists.

    Location:
        pyufunc/util_pathio/_path.py

    See Also:
        create_unique_filename

    Args:
        filename (str | Path): the filename to be validated

    Returns:
        str: validated filename

    Examples:
        >>> import pyufunc as uf
        >>> uf.generate_unique_filename('./test.txt')
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

    # if the file does not exist, return the same file name
    if os.path.exists(filename_abspath):
        filename_update = f"{file_without_suffix}({suffix_num}).{file_suffix}"
        return generate_unique_filename(filename_update, suffix_num + 1)

    return filename_abspath


def create_unique_filename(filename: str | Path, suffix_num: int = 1) -> str:
    """generate a unique filename by adding a suffix number to the end of the filename

    This function is extremely useful when you want to save a file, but not sure if the file already exists.

    Location:
        pyufunc/util_pathio/_path.py

    See Also:
        generate_unique_filename

    Args:
        filename (str | Path): the filename to be validated

    Returns:
        str: validated filename

    Examples:
        >>> import pyufunc as uf
        >>> uf.generate_unique_filename('./test.txt')
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

    # if the file does not exist, return the same file name
    if os.path.exists(filename_abspath):
        filename_update = f"{file_without_suffix}({suffix_num}).{file_suffix}"
        return generate_unique_filename(filename_update, suffix_num + 1)

    return filename_abspath


def show_dir_in_tree(dir_name: Union[str, Path],
                     pattern: str = "**/*",
                     *,
                     show_all=False,
                     max_level=-1,
                     **kwargs) -> None:
    """list contents of directories in a tree-like format.

    Args:
        *args/**kwargs  : Argments for ``root = Path(*args, **kwargs)``
        pattern (str)   : Argments for ``root.glob(pattern)``
        show_all (bool) : Whether not to ignore entries starting with .
        max_level (int) : Max display depth of the directory tree.

    """

    def _toCOLOR_create(color: str = "") -> Callable[[str, bool], str]:
        color = color.upper()

        def _enable_vts() -> bool:
            """Enable Virtual Terminal Sequences (ANSI escape sequences) in Windows10."""
            INVALID_HANDLE_VALUE = -1
            # STD_INPUT_HANDLE     = -10
            STD_OUTPUT_HANDLE = -11
            # STD_ERROR_HANDLE     = -12
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            # ENABLE_LVB_GRID_WORLDWIDE = 0x0010
            try:
                from ctypes import windll, wintypes, byref
                from functools import reduce
                hOut = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
                if hOut == INVALID_HANDLE_VALUE:
                    return False
                dwMode = wintypes.DWORD()
                if windll.kernel32.GetConsoleMode(hOut, byref(dwMode)) == 0:
                    return False
                dwMode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING  # ENABLE_LVB_GRID_WORLDWIDE
                if windll.kernel32.SetConsoleMode(hOut, dwMode) == 0:
                    return False
            except Exception:
                return False
            return True

        __WINDOWS_VTS_SETUP__ = _enable_vts() if os.name == "nt" else True

        if __WINDOWS_VTS_SETUP__ and (color in config_color.keys()):
            charcode = config_color[color]
            def func(x, is_bg=False): return f"{charcode[is_bg]}{str(x)}\x1b[0m"
            func.__doc__ = f"""Convert the output color to {color}

            Args:
                x (str)      : string
                is_bg (bool) : Whether to change the background color or not.

            Examples:
                >>> from pycharmers.utils import to{color}
                >>> print(to{color}("hoge"), is_bg=False)
                {func('hoge', is_bg=False)}
                >>> print(to{color}("hoge"), is_bg=True)
                {func('hoge', is_bg=True)}
            """
        else:
            def func(x, is_bg=False): return str(x)
            func.__doc__ = "Convert to string."
        return func

    class Tree:
        def __init__(self, filepaths=[], show_all=False, max_level=-1):
            """Initialize Tree class.
            Args:
                filepaths (list): Filepaths which is to be printed.
                show_all (bool) : Whether not to ignore entries starting with .
                max_level (int) : Max display depth of the directory tree.
            """
            self.filepaths = filepaths
            self.show_all = show_all
            self.max_level = max_level

        def _init(self):
            self.num_directories = 0
            self.num_files = 0

        def register(self, path):
            if os.path.isdir(path):
                self.num_directories += 1
            else:
                self.num_files += 1

        @staticmethod
        def pathjoin(dir_name: str, *filename: str) -> str:
            """Join two or more pathname components, inserting '/' as needed, and remove './' at the begining."""
            return re.sub(pattern=r"^\.\/", repl="", string=os.path.join(dir_name, *filename))

        def run(self, dirname):
            """Run ``tree`` command.

            Args:
                dirname: path to root directory .
            """
            self._init()
            print(_toCOLOR_create(color="BLUE")(dirname))
            self.walk(dirname=dirname, depth=1, print_prefix="")
            print(f"\n{_toCOLOR_create(color='GREEN')(self.num_directories)} directories, {_toCOLOR_create(color='GREEN')(self.num_files)} files.")

        def walk(self, dirname, depth=1, print_prefix=""):
            """Print filecontens in ``dirname`` recursively.

            Args:
                dirname (str)      : path to current directory.
                depth (int)        : current depth.
                print_prefix (str) : Prefix for clean output.
            """
            filenames = sorted(
                [
                    fn
                    for fn in os.listdir(dirname)
                    if len(self.filepaths) != 0 and any(
                        fp.startswith(self.pathjoin(dirname, fn))
                        for fp in self.filepaths
                    )
                ]
            )
            num_filenames = len(filenames)

            prefixes = ("├── ", "│   ")
            for i, fn in enumerate(filenames):
                if fn[0] == "." and (not self.show_all):
                    continue
                abspath = os.path.join(dirname, fn)
                # Remember the file contents.
                self.register(abspath)
                # Update prefixes for the last entries.
                if i == num_filenames - 1:
                    prefixes = ("└── ", "    ")
                # Print and walk recursively.
                if os.path.isdir(abspath):
                    fn = _toCOLOR_create("BLUE")(fn)
                print(print_prefix + prefixes[0] + fn)
                if os.path.isdir(abspath) and depth != self.max_level:
                    self.walk(dirname=abspath, depth=depth + 1,
                              print_prefix=print_prefix + prefixes[1])

    # check inputs
    if not isinstance(dir_name, (str, Path)):
        raise ValueError("dir_name should be a string or Path object.")

    if not isinstance(pattern, str):
        raise ValueError("pattern should be a string.")

    # check pattern
    if "**/*" not in pattern:
        pattern = f"**/*{pattern}"

    args = (dir_name, )
    root = Path(*args, **kwargs)
    filepaths = [str(p) for p in root.glob(pattern)]
    tree = Tree(filepaths=filepaths, show_all=show_all, max_level=max_level)
    tree.run(str(root))
