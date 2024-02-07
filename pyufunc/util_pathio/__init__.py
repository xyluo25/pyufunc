# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from ._argparse import *
from ._io import (get_file_size,
                  get_dir_size)
from ._path import (path2linux,
                    path2uniform,
                    get_filenames_by_ext,
                    check_files_existence,
                    check_filename)
from ._platform import (check_platform,
                        is_windows,
                        is_linux,
                        is_mac)


__all__ = [
    # argparse

    # io
    "get_file_size",
    "get_dir_size",

    # path
    'path2linux',
    'path2uniform',
    "get_filenames_by_ext",
    "check_files_existence",
    "check_filename",

    # platform
    "check_platform",
    "is_windows",
    "is_linux",
    "is_mac"

]
