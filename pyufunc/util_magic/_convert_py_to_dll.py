'''
##############################################################
# Created Date: Sunday, March 23rd 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''
import os
import platform
from typing import TYPE_CHECKING
from pathlib import Path
from pyufunc.util_magic._dependency_requires_decorator import requires, import_package

if TYPE_CHECKING:
    from setuptools import setup, Extension
    from Cython.Build import cythonize
    import shutil


@requires('setuptools', ('cython', 'Cython'), "shutil")
def cvt_py_to_dll(py_file: str, output_dir: str = "") -> bool:
    """
    Convert a Python file to a DLL using Cython and setuptools.

    Args:
        py_file (str): The path to the Python file to convert. It should have a .py or .pyx extension.
        output_dir (str): The directory where the DLL should be saved. Default is current directory.

    Raises:
        ValueError: If the provided file is not a .py or .pyx file.
        FileNotFoundError: If the DLL file is not found after conversion.

    Notes:
        - The function uses Cython to compile the Python file into a shared library (DLL).
        - It creates a temporary directory to perform the conversion and cleans it up afterwards.
        - The output DLL will have the same name as the input Python file (without extension).

    Example:
        >>> import pyufunc as pf
        >>> pf.cvt_py_to_dll('example.py', output_dir='output_directory')
        >>> # This will convert 'example.py' to 'example.pyd (Windows)/example.so (Linux or Macos)' in 'output_directory'.
        >>> import example # Now you can import the compiled module as a regular Python module.

    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    import_package('setuptools', verbose=False)
    import_package('cython', verbose=False)
    import_package('shutil', verbose=False)
    import shutil
    from setuptools import setup, Extension
    from Cython.Build import cythonize

    # check whether py_file extension is .py and .pyx
    if not (py_file.endswith('.py') or py_file.endswith('.pyx')):
        raise ValueError("The file must be a .py or .pyx file.")

    # get the name of the Python file without extension and directory
    py_file_abs = Path(py_file).resolve().absolute()
    py_file_dir = Path(py_file).parent.resolve().absolute()
    py_filename = Path(py_file).stem

    # create the template directory for conversion
    dir_temp = os.path.join(py_file_dir, 'temp_cython')
    os.makedirs(dir_temp, exist_ok=True)

    # Copy the Python file to the temporary directory if it is not already there
    shutil.copy(py_file_abs, os.path.join(dir_temp, f'{py_filename}.pyx'))

    # change the working directory to the temporary directory
    os.chdir(dir_temp)

    # Define the Cython extension module
    module_name = py_filename
    extension = Extension(
        name=module_name,
        sources=[f"{py_filename}.pyx"],  # Cython source file
    )

    # Setup to build the extension module
    setup(
        name=module_name,
        ext_modules=cythonize([extension]),
        script_args=["build_ext", "--inplace"],
        options={"build_ext": {"build_lib": dir_temp}},
    )

    # Move the generated DLL to the specified output directory
    # if it's Windows, check .pyd extension, else use .so for Unix-like systems
    if platform.system() == "Windows":
        # get all files in the temp directory with .pyd extension
        dll_pyd_files = [f for f in os.listdir(dir_temp) if f.endswith('.pyd')]
        if not dll_pyd_files:
            raise FileNotFoundError(
                "No .pyd file found in the temporary directory.")
        # use the first .pyd file found and rename it to the module name
        os.rename(os.path.join(dir_temp, dll_pyd_files[0]), os.path.join(
            dir_temp, f"{module_name}.pyd"))
        # set the dll_file to the renamed .pyd file
        dll_file = os.path.join(dir_temp, f"{module_name}.pyd")

    else:  # Unix-like systems (Linux, macOS)
        # get all .so files in the temp directory
        so_files = [f for f in os.listdir(dir_temp) if f.endswith('.so')]
        if not so_files:
            raise FileNotFoundError(
                "No .so file found in the temporary directory.")
        # use the first .so file found and rename it to the module name
        os.rename(os.path.join(dir_temp, so_files[0]), os.path.join(
            dir_temp, f"{module_name}.so"))

        # set the dll_file to the renamed .so file
        dll_file = os.path.join(dir_temp, f"{module_name}.so")

    # check if the dll_file exists
    if not os.path.exists(dll_file):
        raise FileNotFoundError(f"Failed to create the DLL: {dll_file}")

    # change working directory back to the original directory
    os.chdir(py_file_dir)

    # Move the DLL to the output directory
    if not output_dir:
        output_dir = os.getcwd()
    else:
        # check if output_dir exists, if not create it
        output_dir = Path(output_dir).resolve().absolute()
        if not output_dir.exists():
            os.getcwd()

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Move the DLL to the output directory
    shutil.move(dll_file, os.path.join(output_dir, os.path.basename(dll_file)))

    # Clean up the temporary directory
    shutil.rmtree(dir_temp, ignore_errors=True)
    return True
