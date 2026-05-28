"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around platformdirs.
# Source: https://github.com/tox-dev/platformdirs

from pyufunc.util_magic import requires


@requires("platformdirs")
def get_user_data_dir(app_name: str = "pyufunc", app_author: str | None = None) -> str:
    """Return the platform-specific user data directory for an app.

    Args:
        app_name: Application name used to construct the directory.
        app_author: Optional application author used on platforms that need it.

    Note:
        - Source package: ``platformdirs``.
        - Source repository: https://github.com/tox-dev/platformdirs
        - Source document: https://platformdirs.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> get_user_data_dir("pyufunc")

    Returns:
        str: User data directory path.
    """
    from platformdirs import user_data_dir

    return user_data_dir(appname=app_name, appauthor=app_author)


@requires("platformdirs")
def get_user_config_dir(app_name: str = "pyufunc", app_author: str | None = None) -> str:
    """Return the platform-specific user config directory for an app.

    Args:
        app_name: Application name used to construct the directory.
        app_author: Optional application author used on platforms that need it.

    Note:
        - Source package: ``platformdirs``.
        - Source repository: https://github.com/tox-dev/platformdirs
        - Source document: https://platformdirs.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> get_user_config_dir("pyufunc")

    Returns:
        str: User config directory path.
    """
    from platformdirs import user_config_dir

    return user_config_dir(appname=app_name, appauthor=app_author)


@requires("platformdirs")
def get_user_cache_dir(app_name: str = "pyufunc", app_author: str | None = None) -> str:
    """Return the platform-specific user cache directory for an app.

    Args:
        app_name: Application name used to construct the directory.
        app_author: Optional application author used on platforms that need it.

    Note:
        - Source package: ``platformdirs``.
        - Source repository: https://github.com/tox-dev/platformdirs
        - Source document: https://platformdirs.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> get_user_cache_dir("pyufunc")

    Returns:
        str: User cache directory path.
    """
    from platformdirs import user_cache_dir

    return user_cache_dir(appname=app_name, appauthor=app_author)


@requires("platformdirs")
def get_user_log_dir(app_name: str = "pyufunc", app_author: str | None = None) -> str:
    """Return the platform-specific user log directory for an app.

    Args:
        app_name: Application name used to construct the directory.
        app_author: Optional application author used on platforms that need it.

    Note:
        - Source package: ``platformdirs``.
        - Source repository: https://github.com/tox-dev/platformdirs
        - Source document: https://platformdirs.readthedocs.io
        - Source license: MIT License.

    Example:
        >>> get_user_log_dir("pyufunc")

    Returns:
        str: User log directory path.
    """
    from platformdirs import user_log_dir

    return user_log_dir(appname=app_name, appauthor=app_author)
