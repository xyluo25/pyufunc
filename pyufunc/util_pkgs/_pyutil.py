"""
##############################################################
# Created Date: Thursday, April 23rd 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes adopted wrapper functions from the pyutil package.

# The source code of pyutil is available at: https://github.com/tpltnt/pyutil

# The utility package review also references the historical source repository:
# https://github.com/zooko/pyutil

# Original license metadata for the current PyPI source distribution declares
# GPL-2.0-or-later. These wrappers forward to pyutil at runtime and do not copy
# pyutil implementation code into pyufunc.

from typing import Any

from pyufunc.util_magic import requires


@requires("pyutil")
def Version(*args: Any, **kwargs: Any) -> Any:
    """Instantiate ``pyutil.version_class.Version``.

    Args:
        *args: Positional arguments passed to ``pyutil.version_class.Version``.
        **kwargs: Keyword arguments passed to ``pyutil.version_class.Version``.

    Note:
        - Source package: ``pyutil``.
        - Source repository: https://github.com/tpltnt/pyutil
        - Source document: https://github.com/tpltnt/pyutil#readme
        - Source license: GPL-2.0-or-later.

    Example:
        >>> Version("1.2.3")  # doctest: +SKIP

    Returns:
        Any: Instance returned by ``pyutil.version_class.Version``.
    """
    from pyutil.version_class import Version as _Version

    return _Version(*args, **kwargs)


@requires("pyutil")
def pad_size(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyutil.mathutil.pad_size``.

    Args:
        *args: Positional arguments passed to ``pyutil.mathutil.pad_size``.
        **kwargs: Keyword arguments passed to ``pyutil.mathutil.pad_size``.

    Note:
        - Source package: ``pyutil``.
        - Source repository: https://github.com/tpltnt/pyutil
        - Source document: https://github.com/tpltnt/pyutil#readme
        - Source license: GPL-2.0-or-later.

    Example:
        >>> pad_size(7, 3)  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyutil.mathutil.pad_size``.
    """
    from pyutil.mathutil import pad_size as _pad_size

    return _pad_size(*args, **kwargs)


@requires("pyutil")
def log_ceil(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyutil.mathutil.log_ceil``.

    Args:
        *args: Positional arguments passed to ``pyutil.mathutil.log_ceil``.
        **kwargs: Keyword arguments passed to ``pyutil.mathutil.log_ceil``.

    Note:
        - Source package: ``pyutil``.
        - Source repository: https://github.com/tpltnt/pyutil
        - Source document: https://github.com/tpltnt/pyutil#readme
        - Source license: GPL-2.0-or-later.

    Example:
        >>> log_ceil(10, 2)  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyutil.mathutil.log_ceil``.
    """
    from pyutil.mathutil import log_ceil as _log_ceil

    return _log_ceil(*args, **kwargs)


@requires("pyutil")
def precondition(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``pyutil.assertutil.precondition``.

    Args:
        *args: Positional arguments passed to ``pyutil.assertutil.precondition``.
        **kwargs: Keyword arguments passed to ``pyutil.assertutil.precondition``.

    Note:
        - Source package: ``pyutil``.
        - Source repository: https://github.com/tpltnt/pyutil
        - Source document: https://github.com/tpltnt/pyutil#readme
        - Source license: GPL-2.0-or-later.

    Example:
        >>> precondition(lambda value: value > 0)  # doctest: +SKIP

    Returns:
        Any: Return value from ``pyutil.assertutil.precondition``.
    """
    from pyutil.assertutil import precondition as _precondition

    return _precondition(*args, **kwargs)
