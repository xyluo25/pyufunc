# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, February 14th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import absolute_import
from pathlib import Path
import os

try:
    import pyufunc as pf
except ImportError:
    current_path = Path(os.path.abspath(__file__)).parent
    root_path = Path(os.path.abspath(__file__)).parent.parent.parent
    print("root_path: ", root_path)
    os.chdir(root_path)
    import pyufunc as pf
    os.chdir(current_path)


def update_util_func_by_keywords_md(path_keyword: str) -> None:
    with open(path_keyword, "r", encoding="utf-8") as f:
        keyword = f.read()
    f.close()

    util_func_starting = keyword.find("Available utility functions in pyUFunc")

    keyword_new = keyword[:util_func_starting] + pf.show_util_func_by_keyword(False)

    with open(path_keyword, "w", encoding="utf-8") as f_new:
        f_new.write(keyword_new)
    f_new.close()
    return None


def update_util_func_by_category_md(path_category: str) -> None:
    with open(path_category, "r", encoding="utf-8") as f:
        category = f.read()
    f.close()

    util_func_starting = category.find("Available utility functions in pyUFunc")

    category_new = category[:util_func_starting] + pf.show_util_func_by_category(False)

    with open(path_category, "w", encoding="utf-8") as f_new:
        f_new.write(category_new)
    f_new.close()
    return None


if __name__ == "__main__":
    path_category = "./utility_function_by_category.md"
    path_keyword = "./utility_function_by_keyword.md"\

    update_util_func_by_keywords_md(path_keyword)
    update_util_func_by_category_md(path_category)
