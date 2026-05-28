"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around loguru.
# Source: https://github.com/Delgan/loguru

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from pyufunc.util_magic import requires


@requires("loguru")
def setup_simple_logger(*, level: str = "INFO", format_str: str | None = None, colorize: bool = False) -> int:
    """Add a simple stderr loguru logger.

    Args:
        level: Minimum log level.
        format_str: Optional log message format.
        colorize: If True, enable colorized output.

    Note:
        - Source package: ``loguru``.
        - Source repository: https://github.com/Delgan/loguru
        - Source document: https://loguru.readthedocs.io/en/stable/index.html
        - Source license: MIT License.

    Example:
        >>> handler_id = setup_simple_logger(level="INFO")

    Returns:
        int: Loguru handler ID.
    """
    from loguru import logger

    logger_kwargs: dict[str, Any] = {"level": level, "colorize": colorize}
    if format_str is not None:
        logger_kwargs["format"] = format_str

    return logger.add(sys.stderr, **logger_kwargs)


@requires("loguru")
def setup_file_logger(
    log_file: str | Path,
    *,
    level: str = "INFO",
    rotation: str | int | None = None,
    retention: str | int | None = None,
    **kwargs: Any,
) -> int:
    """Add a file sink to the loguru logger.

    Args:
        log_file: Destination log file path.
        level: Minimum log level.
        rotation: Optional loguru rotation setting.
        retention: Optional loguru retention setting.
        **kwargs: Extra keyword arguments passed to ``logger.add``.

    Note:
        - Source package: ``loguru``.
        - Source repository: https://github.com/Delgan/loguru
        - Source document: https://loguru.readthedocs.io/en/stable/index.html
        - Source license: MIT License.

    Example:
        >>> handler_id = setup_file_logger("app.log")

    Returns:
        int: Loguru handler ID.
    """
    from loguru import logger

    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    return logger.add(path, level=level, rotation=rotation, retention=retention, **kwargs)


@requires("loguru")
def disable_logger(name: str = "") -> None:
    """Disable loguru logging for a logger name.

    Args:
        name: Logger name. Use an empty string to disable the root namespace.

    Note:
        - Source package: ``loguru``.
        - Source repository: https://github.com/Delgan/loguru
        - Source document: https://loguru.readthedocs.io/en/stable/index.html
        - Source license: MIT License.

    Example:
        >>> disable_logger("my_package")

    Returns:
        None.
    """
    from loguru import logger

    logger.disable(name)


@requires("loguru")
def enable_logger(name: str = "") -> None:
    """Enable loguru logging for a logger name.

    Args:
        name: Logger name. Use an empty string to enable the root namespace.

    Note:
        - Source package: ``loguru``.
        - Source repository: https://github.com/Delgan/loguru
        - Source document: https://loguru.readthedocs.io/en/stable/index.html
        - Source license: MIT License.

    Example:
        >>> enable_logger("my_package")

    Returns:
        None.
    """
    from loguru import logger

    logger.enable(name)
