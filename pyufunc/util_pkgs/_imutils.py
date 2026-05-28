"""
##############################################################
# Created Date: Thursday, April 23rd 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo.
##############################################################
"""

# This module includes adopted wrapper functions from the imutils package.

# The utility package review references the source repository:
# https://github.com/PyImageSearch/imutils

# The current PyPI metadata points to: https://github.com/jrosebr1/imutils

from typing import Any

from pyufunc.util_magic import requires


@requires("imutils", ("opencv-python", "cv2"))
def translate(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.translate``.

    Args:
        *args: Positional arguments passed to ``imutils.translate``.
        **kwargs: Keyword arguments passed to ``imutils.translate``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> translate(image, 25, -75)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.translate``.
    """
    import imutils

    return imutils.translate(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def rotate(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.rotate``.

    Args:
        *args: Positional arguments passed to ``imutils.rotate``.
        **kwargs: Keyword arguments passed to ``imutils.rotate``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> rotate(image, 45)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.rotate``.
    """
    import imutils

    return imutils.rotate(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def rotate_bound(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.rotate_bound``.

    Args:
        *args: Positional arguments passed to ``imutils.rotate_bound``.
        **kwargs: Keyword arguments passed to ``imutils.rotate_bound``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> rotate_bound(image, 45)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.rotate_bound``.
    """
    import imutils

    return imutils.rotate_bound(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def resize(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.resize``.

    Args:
        *args: Positional arguments passed to ``imutils.resize``.
        **kwargs: Keyword arguments passed to ``imutils.resize``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> resize(image, width=400)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.resize``.
    """
    import imutils

    return imutils.resize(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def skeletonize(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.skeletonize``.

    Args:
        *args: Positional arguments passed to ``imutils.skeletonize``.
        **kwargs: Keyword arguments passed to ``imutils.skeletonize``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> skeletonize(image)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.skeletonize``.
    """
    import imutils

    return imutils.skeletonize(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def opencv2matplotlib(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.opencv2matplotlib``.

    Args:
        *args: Positional arguments passed to ``imutils.opencv2matplotlib``.
        **kwargs: Keyword arguments passed to ``imutils.opencv2matplotlib``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> opencv2matplotlib(image)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.opencv2matplotlib``.
    """
    import imutils

    return imutils.opencv2matplotlib(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def url_to_image(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.url_to_image``.

    Args:
        *args: Positional arguments passed to ``imutils.url_to_image``.
        **kwargs: Keyword arguments passed to ``imutils.url_to_image``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> url_to_image("https://example.com/image.png")  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.url_to_image``.
    """
    import imutils

    return imutils.url_to_image(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def auto_canny(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.auto_canny``.

    Args:
        *args: Positional arguments passed to ``imutils.auto_canny``.
        **kwargs: Keyword arguments passed to ``imutils.auto_canny``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> auto_canny(image)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.auto_canny``.
    """
    import imutils

    return imutils.auto_canny(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def grab_contours(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.grab_contours``.

    Args:
        *args: Positional arguments passed to ``imutils.grab_contours``.
        **kwargs: Keyword arguments passed to ``imutils.grab_contours``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> grab_contours(contours)  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.grab_contours``.
    """
    import imutils

    return imutils.grab_contours(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def is_cv2(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.is_cv2``.

    Args:
        *args: Positional arguments passed to ``imutils.is_cv2``.
        **kwargs: Keyword arguments passed to ``imutils.is_cv2``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> is_cv2()  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.is_cv2``.
    """
    import imutils

    return imutils.is_cv2(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def is_cv3(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.is_cv3``.

    Args:
        *args: Positional arguments passed to ``imutils.is_cv3``.
        **kwargs: Keyword arguments passed to ``imutils.is_cv3``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> is_cv3()  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.is_cv3``.
    """
    import imutils

    return imutils.is_cv3(*args, **kwargs)


@requires("imutils", ("opencv-python", "cv2"))
def is_cv4(*args: Any, **kwargs: Any) -> Any:
    """Forward to ``imutils.is_cv4``.

    Args:
        *args: Positional arguments passed to ``imutils.is_cv4``.
        **kwargs: Keyword arguments passed to ``imutils.is_cv4``.

    Note:
        - Source package: ``imutils``.
        - Source repository: https://github.com/jrosebr1/imutils
        - Source document: https://github.com/jrosebr1/imutils#readme
        - Source license: MIT License.

    Example:
        >>> is_cv4()  # doctest: +SKIP

    Returns:
        Any: Return value from ``imutils.is_cv4``.
    """
    import imutils

    return imutils.is_cv4(*args, **kwargs)
