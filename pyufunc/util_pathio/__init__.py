# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from ._argparse import with_argparse
from ._io import (get_file_size,
                  size_of_file,

                  get_dir_size,
                  size_of_dir,

                  create_tempfile,
                  file_remove,
                  file_delete,

                  add_dir_to_env,
                  pickle_save,
                  pickle_load,
                  find_duplicate_files,
                  remove_duplicate_files,
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
                    add_pkg_to_sys_path,
                    find_executable_from_PATH_on_win,
                    find_fname_from_PATH_on_win,
                    )
from ._platform import (check_platform,
                        is_windows,
                        is_linux,
                        is_mac,
                        terminal_width,
                        terminal_height,
                        )


__all__ = [
    # argparse
    "with_argparse",

    # io
    "get_file_size",
    "size_of_file",
    "get_dir_size",
    "size_of_dir",
    "create_tempfile",
    "file_remove",
    "file_delete",
    "add_dir_to_env",
    "pickle_save",
    "pickle_load",
    "find_duplicate_files",
    "remove_duplicate_files",

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
    "add_pkg_to_sys_path",
    "find_executable_from_PATH_on_win",
    "find_fname_from_PATH_on_win",

    # platform
    "check_platform",
    "is_windows",
    "is_linux",
    "is_mac",
    "terminal_width",
    "terminal_height",

]
