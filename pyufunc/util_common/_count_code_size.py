
import os
from pathlib import Path
import contextlib
from pyufunc.util_pathio._path import path2linux
import warnings


def count_lines_of_code(package_path: str | Path, *, ext: str = "*", verbose: bool = False) -> int:

    """Counts the number of lines of code in a Python package.

    Args:
        package_path (str): The path to the package.
        ext (str): The extension of the files to count. Default is "*".
        verbose (bool): Whether to print the file paths being counted. Default is False.

    Returns:
        int: The number of lines of code in the package.

    Raises:
        TypeError: If package_path is not a string.
        TypeError: If ext is not a string.

    Example:
        >>> from pyufunc import count_lines_of_code
        >>> count_lines_of_code("pyufunc")
        5000

    """

    # Initialize the count
    count = 0

    if not isinstance(package_path, (str, Path)):
        warnings.warn("Package path must be a string or Path.", UserWarning)
        # raise TypeError("Package path must be a string or Path.")
        return count

    if not isinstance(ext, str):
        warnings.warn("Extension must be a string.", UserWarning)
        # raise TypeError("Extension must be a string.")
        return count

    # Standardize the package path to universal readable format
    package_path = path2linux(package_path)

    # Check if the package path is a file or directory
    is_file = os.path.isfile(package_path)
    is_dir = os.path.isdir(package_path)

    if not is_file and not is_dir:
        warnings.warn(f"'{package_path}' is not a file or directory, please check your input.", UserWarning)
        # raise FileNotFoundError(f"'{package_path}' is not a file or directory, please check your input.")
        return count

    # Standardize the extension
    if ext != "*" and "." not in ext:
        ext = f".{ext}"

    # Count the lines of code
    if verbose:
        print(f"Counting lines of code in '{package_path}'...")

    if is_file:
        if ext == "*" or package_path.endswith(ext):
            with open(package_path, "r") as f:
                with contextlib.suppress(Exception):
                    count += len(f.readlines())
        else:
            print(f"Package path '{package_path}' does not have the extension '{ext}'.")

        return count

    if is_dir:
        for root, directories, filenames in os.walk(package_path):
            for filename in filenames:
                if ext == "*" or (ext != "*" and filename.endswith(ext)):
                    with open(os.path.join(root, filename), "r") as f:
                        with contextlib.suppress(Exception):
                            count += len(f.readlines())
        return count

    return count
