# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from ._argparse import *
from ._io import (get_file_size,
                  get_dir_size,
                  create_tempfile,
                  remove_file,
                  add_dir_to_env,
                  pickle_save,
                  pickle_load,
                  )
from ._path import (path2linux,
                    path2uniform,
                    get_filenames_by_ext,
                    get_files_by_ext,
                    check_files_in_dir,
                    check_filename,
                    check_file_existence,
                    generate_unique_filename,
                    create_unique_filename,
                    show_dir_in_tree,
                    )
from ._platform import (check_platform,
                        is_windows,
                        is_linux,
                        is_mac,
                        get_terminal_width,
                        get_terminal_height,
                        )


__all__ = [
    # argparse

    # io
    "get_file_size",
    "get_dir_size",
    "create_tempfile",
    "remove_file",
    "add_dir_to_env",
    "pickle_save",
    "pickle_load",

    # path
    'path2linux',
    'path2uniform',
    "get_filenames_by_ext",
    "get_files_by_ext",
    "check_files_in_dir",
    "check_filename",
    "check_file_existence",
    "generate_unique_filename",
    "create_unique_filename",
    "show_dir_in_tree",

    # platform
    "check_platform",
    "is_windows",
    "is_linux",
    "is_mac",
    "get_terminal_width",
    "get_terminal_height",

]
