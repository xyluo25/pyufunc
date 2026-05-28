"""
##############################################################
# Created Date: Thursday, April 23rd 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module including adopted functions from pyhelpers package.

# Source code of pyhelpers is available at: https://github.com/mikeqfu/pyhelpers

# Please refer to the official documentation for more details: https://pyhelpers.readthedocs.io/en/latest/

# Original license of pyhelpers is MIT License,
# and we will keep the original license and copyright notice in the adopted code.

from typing import Any

from pyufunc.util_magic import requires


@requires("pyhelpers")
def find_similar_str(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.text.find_similar_str``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.text.find_similar_str``.
        **kwargs: Keyword arguments passed to ``pyhelpers.text.find_similar_str``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> find_similar_str("appel", ["apple", "pear"])  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.text.find_similar_str``.
    """
    from pyhelpers.text import find_similar_str as _find_similar_str

    return _find_similar_str(*args, **kwargs)


@requires("pyhelpers")
def remove_punctuation(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.text.remove_punctuation``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.text.remove_punctuation``.
        **kwargs: Keyword arguments passed to ``pyhelpers.text.remove_punctuation``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> remove_punctuation("hello, world!")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.text.remove_punctuation``.
    """
    from pyhelpers.text import remove_punctuation as _remove_punctuation

    return _remove_punctuation(*args, **kwargs)


@requires("pyhelpers")
def confirmed(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.ops.confirmed``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.ops.confirmed``.
        **kwargs: Keyword arguments passed to ``pyhelpers.ops.confirmed``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> confirmed("Continue?")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.ops.confirmed``.
    """
    from pyhelpers.ops import confirmed as _confirmed

    return _confirmed(*args, **kwargs)


@requires("pyhelpers")
def fake_requests_headers(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.ops.fake_requests_headers``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.ops.fake_requests_headers``.
        **kwargs: Keyword arguments passed to ``pyhelpers.ops.fake_requests_headers``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> fake_requests_headers()  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.ops.fake_requests_headers``.
    """
    from pyhelpers.ops import fake_requests_headers as _fake_requests_headers

    return _fake_requests_headers(*args, **kwargs)


@requires("pyhelpers")
def update_dict_keys(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.ops.update_dict_keys``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.ops.update_dict_keys``.
        **kwargs: Keyword arguments passed to ``pyhelpers.ops.update_dict_keys``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> update_dict_keys({"old": 1}, {"old": "new"})  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.ops.update_dict_keys``.
    """
    from pyhelpers.ops import update_dict_keys as _update_dict_keys

    return _update_dict_keys(*args, **kwargs)


@requires("pyhelpers")
def merge_dicts(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.ops.merge_dicts``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.ops.merge_dicts``.
        **kwargs: Keyword arguments passed to ``pyhelpers.ops.merge_dicts``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> merge_dicts({"a": 1}, {"b": 2})  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.ops.merge_dicts``.
    """
    from pyhelpers.ops import merge_dicts as _merge_dicts

    return _merge_dicts(*args, **kwargs)


@requires("pyhelpers")
def load_pickle(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.store.load_pickle``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.store.load_pickle``.
        **kwargs: Keyword arguments passed to ``pyhelpers.store.load_pickle``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> load_pickle("data.pkl")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.store.load_pickle``.
    """
    from pyhelpers.store import load_pickle as _load_pickle

    return _load_pickle(*args, **kwargs)


@requires("pyhelpers")
def save_pickle(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.store.save_pickle``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.store.save_pickle``.
        **kwargs: Keyword arguments passed to ``pyhelpers.store.save_pickle``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> save_pickle({"ok": True}, "data.pkl")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.store.save_pickle``.
    """
    from pyhelpers.store import save_pickle as _save_pickle

    return _save_pickle(*args, **kwargs)


@requires("pyhelpers")
def load_data(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.store.load_data``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.store.load_data``.
        **kwargs: Keyword arguments passed to ``pyhelpers.store.load_data``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> load_data("data.pkl")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.store.load_data``.
    """
    from pyhelpers.store import load_data as _load_data

    return _load_data(*args, **kwargs)


@requires("pyhelpers")
def save_data(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.store.save_data``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.store.save_data``.
        **kwargs: Keyword arguments passed to ``pyhelpers.store.save_data``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> save_data({"ok": True}, "data.pkl")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.store.save_data``.
    """
    from pyhelpers.store import save_data as _save_data

    return _save_data(*args, **kwargs)


@requires("pyhelpers")
def cd(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.dirs.cd``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.dirs.cd``.
        **kwargs: Keyword arguments passed to ``pyhelpers.dirs.cd``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> with cd("."):
        ...     pass  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.dirs.cd``.
    """
    from pyhelpers.dirs import cd as _cd

    return _cd(*args, **kwargs)


@requires("pyhelpers")
def resolve_dir(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.dirs.resolve_dir``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.dirs.resolve_dir``.
        **kwargs: Keyword arguments passed to ``pyhelpers.dirs.resolve_dir``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> resolve_dir(".")  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.dirs.resolve_dir``.
    """
    from pyhelpers.dirs import resolve_dir as _resolve_dir

    return _resolve_dir(*args, **kwargs)


@requires("pyhelpers")
def wgs84_to_osgb36(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.geom.wgs84_to_osgb36``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.geom.wgs84_to_osgb36``.
        **kwargs: Keyword arguments passed to ``pyhelpers.geom.wgs84_to_osgb36``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> wgs84_to_osgb36(51.5, -0.1)  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.geom.wgs84_to_osgb36``.
    """
    from pyhelpers.geom import wgs84_to_osgb36 as _wgs84_to_osgb36

    return _wgs84_to_osgb36(*args, **kwargs)


@requires("pyhelpers")
def osgb36_to_wgs84(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyhelpers.geom.osgb36_to_wgs84``.

    Args:
        *args: Positional arguments passed to ``pyhelpers.geom.osgb36_to_wgs84``.
        **kwargs: Keyword arguments passed to ``pyhelpers.geom.osgb36_to_wgs84``.

    Note:
        - Source package: ``pyhelpers``.
        - Source repository: https://github.com/mikeqfu/pyhelpers
        - Source document: https://pyhelpers.readthedocs.io/
        - Source license: MIT License.

    Example:
        >>> osgb36_to_wgs84(530000, 180000)  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyhelpers.geom.osgb36_to_wgs84``.
    """
    from pyhelpers.geom import osgb36_to_wgs84 as _osgb36_to_wgs84

    return _osgb36_to_wgs84(*args, **kwargs)
