# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, February 4th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from ._google_numpy_docstring import (show_docstring_headers,
                                      show_docstring_google,
                                      show_docstring_numpy
                                      )

from ._password_generator import generate_password

from ._import_package import (
    is_module_importable,
    import_package,
    get_user_defined_func,
    is_user_defined_func)

from ._decorator_dependency_requires import requires
from ._decorator_func_time import func_running_time, func_time
from ._decorator_run_parallel import run_parallel
from ._decorator_end_of_life import end_of_life


__all__ = ["show_docstring_headers",
           "show_docstring_google",
           "show_docstring_numpy",
           "generate_password",
           "requires",
           "func_running_time",
           "func_time",
           "run_parallel",
           "end_of_life",
           "import_package",
           "is_module_importable",
           "get_user_defined_func",
           "is_user_defined_func",

           ]