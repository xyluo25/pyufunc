"""
##############################################################
# Created Date: Thursday, May 28th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes thin wrappers around tenacity.
# Source: https://github.com/jd/tenacity

from collections.abc import Callable
from typing import Any

from pyufunc.util_magic import requires


@requires("tenacity")
def retry_call(
    function: Callable[..., Any],
    *args: Any,
    attempts: int = 3,
    wait_seconds: float = 0,
    retry_exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    **kwargs: Any,
) -> Any:
    """Call a function with retry attempts.

    Args:
        function: Callable to execute.
        *args: Positional arguments passed to ``function``.
        attempts: Maximum number of attempts.
        wait_seconds: Fixed wait time between attempts.
        retry_exceptions: Exception type or tuple of exception types to retry.
        **kwargs: Keyword arguments passed to ``function``.

    Raises:
        BaseException: Re-raises the final exception when retries are exhausted.

    Note:
        - Source package: ``tenacity``.
        - Source repository: https://github.com/jd/tenacity
        - Source document: https://tenacity.readthedocs.io/en/latest/
        - Source license: Apache License 2.0.

    Example:
        >>> retry_call(lambda: "ok")
        'ok'

    Returns:
        Any: Return value from ``function``.
    """
    from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_fixed

    retryer = Retrying(
        stop=stop_after_attempt(attempts),
        wait=wait_fixed(wait_seconds),
        retry=retry_if_exception_type(retry_exceptions),
        reraise=True,
    )
    for attempt in retryer:
        with attempt:
            return function(*args, **kwargs)

    return None


@requires("tenacity")
def retry_with_backoff(
    function: Callable[..., Any] | None = None,
    *,
    attempts: int = 3,
    min_seconds: float = 1,
    max_seconds: float = 10,
    multiplier: float = 1,
    retry_exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> Callable[..., Any]:
    """Decorate a function with exponential backoff retry behavior.

    Args:
        function: Optional function to decorate.
        attempts: Maximum number of attempts.
        min_seconds: Minimum exponential wait in seconds.
        max_seconds: Maximum exponential wait in seconds.
        multiplier: Exponential wait multiplier.
        retry_exceptions: Exception type or tuple of exception types to retry.

    Note:
        - Source package: ``tenacity``.
        - Source repository: https://github.com/jd/tenacity
        - Source document: https://tenacity.readthedocs.io/en/latest/
        - Source license: Apache License 2.0.

    Example:
        >>> retrying = retry_with_backoff(lambda: "ok", attempts=1)
        >>> retrying()
        'ok'

    Returns:
        Callable[..., Any]: Decorated callable or decorator.
    """
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

    decorator = retry(
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(multiplier=multiplier, min=min_seconds, max=max_seconds),
        retry=retry_if_exception_type(retry_exceptions),
        reraise=True,
    )
    return decorator if function is None else decorator(function)


@requires("tenacity")
def retry_on_exception(
    function: Callable[..., Any] | None = None,
    *,
    attempts: int = 3,
    wait_seconds: float = 0,
    retry_exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> Callable[..., Any]:
    """Decorate a function to retry on selected exceptions.

    Args:
        function: Optional function to decorate.
        attempts: Maximum number of attempts.
        wait_seconds: Fixed wait time between attempts.
        retry_exceptions: Exception type or tuple of exception types to retry.

    Note:
        - Source package: ``tenacity``.
        - Source repository: https://github.com/jd/tenacity
        - Source document: https://tenacity.readthedocs.io/en/latest/
        - Source license: Apache License 2.0.

    Example:
        >>> retrying = retry_on_exception(lambda: "ok", attempts=1)
        >>> retrying()
        'ok'

    Returns:
        Callable[..., Any]: Decorated callable or decorator.
    """
    from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

    decorator = retry(
        stop=stop_after_attempt(attempts),
        wait=wait_fixed(wait_seconds),
        retry=retry_if_exception_type(retry_exceptions),
        reraise=True,
    )
    return decorator if function is None else decorator(function)
