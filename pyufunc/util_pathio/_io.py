# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from pyufunc.util_pathio._path import path2linux, check_file_existence
import os
from pathlib import Path
import uuid
import sys


def get_file_size(filename: str | Path, unit: str = "kb") -> str:
    """Get the size of a file in the specified unit.

    Args:
        filename (str): The filename of the file to get the size of.
        unit (str, optional): the unit for the filesize ('kb', 'mb', 'gb', 'tb') . Defaults to "kb".

    Returns:
        str: _description_
    """

    # TDD, Test Driven Development: validate the input
    assert isinstance(filename, (str, Path)), f"filename must be a string or Path, not {type(filename)}"
    assert isinstance(unit, str), f"unit must be a string, not {type(unit)}"
    assert unit.lower() in {
        'kb',
        'mb',
        'gb',
        'tb',
    }, f"unit must be one of 'kb', 'mb', 'gb', 'tb', not {unit}"

    # format the filename to linux path
    filename = path2linux(filename)

    filename_short = os.path.basename(filename)

    # Check if the file exists
    assert os.path.isfile(filename), f"File {filename_short} does not found, please check the file path and try again"
    # if not os.path.isfile(filename):
    #     return f"File {filename_short} does not found, please check the file path and try again"

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

    # TDD, Test Driven Development: validate the input
    assert isinstance(directory, str), f"directory must be a string, not {type(directory)}"
    assert isinstance(unit, str), f"unit must be a string, not {type(unit)}"
    assert unit.lower() in {
        'kb',
        'mb',
        'gb',
        'tb',
    }, f"unit must be one of 'kb', 'mb', 'gb', 'tb', not {unit}"

    # format the directory to linux path
    directory = path2linux(directory)

    directory_short = os.path.basename(directory)

    # Check if the directory exists
    assert os.path.isdir(directory), f"Directory {directory_short} does not found, please check the directory path and try again"
    # if not os.path.isdir(directory):
    #     return f"Directory {directory_short} does not found, please check the directory path and try again"

    # Get the size of the directory in bytes
    size_bytes = sum(
        os.path.getsize(os.path.join(directory, file))
        for file in os.listdir(directory)
    )

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


def create_tempfile(base_dir: str = "./", ext: str = "txt") -> str:
    """Create a temporary file with the specified size.

    Args:
        base_dir (str, optional): The directory to create the file in. Defaults to "./".
        ext (str, optional): The extension of the file. Defaults to "txt".

    Returns:
        str: The path to the created file.

    Example:
        >>> from pyufunc import create_tempfile
        >>> create_tempfile(base_dir="./", ext="txt", size_in_kb=1)
        './file.txt'
    """

    # TDD, Test Driven Development: validate the input
    assert isinstance(base_dir, str), f"base_dir must be a string, not {type(base_dir)}"
    assert isinstance(ext, str), f"ext must be a string, not {type(ext)}"

    # check extension include the dot
    if not ext.startswith("."):
        ext = f".{ext}"

    # format the base_dir to linux path
    base_dir = path2linux(base_dir)

    # Create the temporary directory if it does not exist
    os.makedirs(base_dir, exist_ok=True)

    # Create the temporary file
    file_path = os.path.join(base_dir, f"tmpfile_{str(uuid.uuid4())}{ext}")

    # Create the file
    with open(file_path, "w") as f:
        f.write("")  # write an empty string to the file

    # return the path to the created file
    return file_path


def remove_file(filename: str | Path) -> None:
    """Remove a file from the filesystem.

    Args:
        filename (str): The filename of the file to remove.

    Returns:
        None

    Example:
        >>> from pyufunc import remove_file
        >>> remove_file("file.txt")
    """

    # TDD, Test Driven Development: validate the input
    assert isinstance(filename, (str, Path)), f"filename must be a string or Path, not {type(filename)}"

    # format the filename to linux path
    filename = path2linux(filename)

    filename_short = os.path.basename(filename)

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"File {filename_short} does not found, please check the file path and try again")
        return None

    # Remove the file
    os.remove(filename)
    return None


def add_dir_to_env(path_dir: str | Path = os.getcwd()) -> None:
    """Add a directory to the PATH environment variable.

    Args:
        path_dir (str | Path): The directory to add to the PATH.
            Defaults to the current working directory.

    Returns:
        None

    Example:
        >>> from pyufunc import add_dir_to_env
        >>> add_dir_to_env("/path/to/directory")
    """

    # TDD, Test Driven Development: validate the input
    assert isinstance(path_dir, (str, Path)), f"path_dir must be a string or Path, not {type(path_dir)}"

    # format the path_dir to linux path
    path_dir = path2linux(path_dir)

    # Add the directory to the PATH environment variable
    os.environ["PATH"] += os.pathsep + path_dir
    sys.path.append(path_dir)

    return None


def pickle_save(obj: object, filename: str | Path, base_dir: str = os.getcwd()) -> None:
    """Save an object to a file using the pickle module.

    The object could be a function, a class, a list, dictionary, a string, an int, float, tuple, set, or any other object that can be pickled.

    Args:
        obj: The object to save.
        filename (str | Path): The filename to save the object to.
        base_dir (str, optional): The directory to save the file in. Defaults to the current working directory.

    Raises:
        AssertionError: filename must be a string or Path, not {type(filename)}

    Returns:
        None

    Example:
        >>> from pyufunc import pickle_save
        >>> pickle_save(obj, "file.pkl")
    """
    import pickle

    # TDD, Test Driven Development: validate the input
    assert isinstance(filename, (str, Path)), f"filename must be a string or Path, not {type(filename)}"

    # format the filename to linux path
    filename = path2linux(filename)

    # Create the directory if it does not exist
    os.makedirs(base_dir, exist_ok=True)

    file_path = os.path.join(base_dir, filename)

    # Save the object to the file
    with open(file_path, "wb") as f:
        pickle.dump(obj, f)

    return None


def pickle_load(filename: str | Path) -> object:
    """Load an object from a file using the pickle module.

    Args:
        filename (str | Path): The filename to load the object from.

    Returns:
        object: _description_
    """

    import pickle

    # check file existence
    if not check_file_existence(filename):
        raise FileNotFoundError(f"File {filename} does not found, please check the file path and try again")

    # format the filename to linux path
    filename = path2linux(filename)

    # Load the object from the file
    with open(filename, "rb") as f:
        obj = pickle.load(f)

    return obj


# def write_yaml_file(func=None, *, log_dir: str | Path = LOGGING_FOLDER, ):
#     import yaml
#     with open(file_path, 'w') as f:
#         yaml.dump(data, f, default_flow_style=False)
