# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

"""functions list in this module
    path2linux
"""


# path2linux
# path string in windows: 'C:\\Users\\Administrator\\Desktop\\test\\test.txt'
# path string in linux: 'C:/Users/Administrator/Desktop/test/test.txt'
# path string in mac: '/Users/Administrator/Desktop/test/test.txt'

# Windows is smart enough to handle all paths from other OSes, so we don't need to do anything.
# But for other OSes, they can not handle windows paths, so we need to convert them to linux paths.
# Finally, we can use linux paths in all OSes.

# The reason not using name: normalize_path or unify_path but path2linux is that: the author is a big fan of Linux.


import inspect
from pathlib import Path
import sys


def path2linux(path):
    return str(path).replace('\\', '/')

# Get a list of all names defined in the module
names = dir(Path(__file__).parent)


if __name__ == '__main__':
    print('names:', names)
    print('functions:')

    print([[name, obj] for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(obj)])