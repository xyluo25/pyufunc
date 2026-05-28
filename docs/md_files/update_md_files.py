# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, February 14th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import absolute_import
from pathlib import Path
import os
import sys

try:
    import pyufunc as pf
except ImportError:
    current_path = Path(os.path.abspath(__file__)).parent
    root_path = Path(os.path.abspath(__file__)).parent.parent.parent
    print("root_path: ", root_path)
    os.chdir(root_path)
    sys.path.insert(0, str(root_path))
    import pyufunc as pf

    os.chdir(current_path)

KEYWORD_GROUPS = (
    "show",
    "get",
    "generate",
    "create",
    "find",
    "calc",
    "run",
    "group",
    "check",
    "validate",
    "list",
    "img",
    "fmt",
    "cvt",
    "is",
    "proj",
    "github",
    "pypi",
    "error",
    "algo",
    "gmns",
    "pytest",
)


def _format_util_func_by_category(config_func_category: dict) -> str:
    res_str_by_category = ""
    func_count = 0
    for util_category, func_lst in config_func_category.items():
        if func_lst:
            res_str_by_category += f"\n- {util_category}:\n"
            for func in sorted(func_lst, key=str.lower):
                res_str_by_category += f"  - {func}\n"
                func_count += 1
    return f"Available utility functions in pyUFunc ({func_count}):\n{res_str_by_category}"


def _get_all_util_func_names(config_func_category: dict) -> list[str]:
    """Return unique utility function names from the category map.

    Args:
        config_func_category (dict): Mapping from utility categories to function names.

    Returns:
        list[str]: Sorted unique function names.
    """
    func_names = {func_name for func_lst in config_func_category.values() for func_name in func_lst}
    return sorted(func_names, key=str.lower)


def _matches_keyword_group(func_name: str, keyword: str) -> bool:
    """Return whether a function belongs in a keyword group.

    Args:
        func_name (str): Utility function name.
        keyword (str): Keyword group name.

    Returns:
        bool: ``True`` when the function should be displayed in the group.
    """
    func_name_lower = func_name.lower()
    keyword_lower = keyword.lower()

    if keyword_lower == "error":
        return keyword_lower in func_name_lower.split("_")
    return func_name_lower == keyword_lower or func_name_lower.startswith(f"{keyword_lower}_")


def _format_util_func_by_keyword(config_func_category: dict) -> str:
    """Format utility functions grouped by commonly used name prefixes.

    Args:
        config_func_category (dict): Mapping from utility categories to function names.

    Returns:
        str: Markdown content for the generated keyword section.
    """
    func_names = _get_all_util_func_names(config_func_category)
    grouped_func_names: set[str] = set()
    section_entries: list[tuple[str, list[str]]] = []

    for keyword in KEYWORD_GROUPS:
        keyword_func_names = [func_name for func_name in func_names if _matches_keyword_group(func_name, keyword)]
        if keyword_func_names:
            grouped_func_names.update(keyword_func_names)
            section_entries.append((keyword, keyword_func_names))

    non_keyword_func_names = [func_name for func_name in func_names if func_name not in grouped_func_names]
    section_entries.insert(0, ("non-keywords", non_keyword_func_names))

    res_str_by_keyword = ""
    for keyword, keyword_func_names in section_entries:
        if keyword_func_names:
            res_str_by_keyword += f"\n- {keyword}:\n"
            for func_name in keyword_func_names:
                res_str_by_keyword += f"  - {func_name}\n"

    return f"Available utility functions in pyUFunc ({len(func_names)}):\n{res_str_by_keyword}"


def update_util_func_by_keywords_md(path_keyword: str) -> None:
    """Update the keyword utility listing in a Markdown file.

    Args:
        path_keyword (str): Path to the keyword Markdown file.
    """
    with open(path_keyword, "r", encoding="utf-8") as f:
        keyword = f.read()
    f.close()

    util_func_starting = keyword.find("Available utility functions in pyUFunc")

    keyword_new = keyword[:util_func_starting] + _format_util_func_by_keyword(pf.show_util_func_by_category(False))

    with open(path_keyword, "w", encoding="utf-8") as f_new:
        f_new.write(keyword_new)
    f_new.close()
    return None


def update_util_func_by_category_md(path_category: str) -> None:
    """Update the category utility listing in a Markdown file.

    Args:
        path_category (str): Path to the category Markdown file.
    """
    with open(path_category, "r", encoding="utf-8") as f:
        category = f.read()
    f.close()

    util_func_starting = category.find("Available utility functions in pyUFunc")

    category_new = category[:util_func_starting] + _format_util_func_by_category(pf.show_util_func_by_category(False))

    with open(path_category, "w", encoding="utf-8") as f_new:
        f_new.write(category_new)
    f_new.close()
    return None


if __name__ == "__main__":
    path_category = "./utility_function_by_category.md"
    path_keyword = "./utility_function_by_keyword.md"

    update_util_func_by_keywords_md(path_keyword)
    update_util_func_by_category_md(path_category)
