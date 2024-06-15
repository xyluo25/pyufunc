# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, March 29th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING
import io

# https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import
if TYPE_CHECKING:
    # check the support version of python
    # https://pillow.readthedocs.io/en/stable/installation.html
    from PIL import Image
    import numpy as np
    import cv2

from pyufunc.util_common._dependency_requires_decorator import requires
from pyufunc.util_common._import_package import import_package
from ._img_operate import img_CV_to_PIL, img_PIL_to_CV


def img_to_bytes(img_path: str) -> bytes:
    """Convert image to bytes

    Args:
        img_path (str): image path, include all image format, e.g. .jpg, .png, .bmp, .gif, etc.

    Returns:
        bytes: the image bytes

    Example:
        >>> from pyufunc import img_to_bytes
        >>> img_path = 'test.jpg'
        >>> img_b = cvt_img_to_bytes(img_path)
        >>> print(img_b)
    """
    try:
        with open(img_path, 'rb') as f:
            img_b = f.read()
    except Exception:
        img_b = bytes("", encoding='utf-8')
    return img_b


def img_PIL_to_bytes(img: Image) -> bytes:
    """Convert PIL image to bytes

    Args:
        img (Image): PIL image object

    Returns:
        bytes: the image bytes

    Example:
        >>> from PIL import Image
        >>> from pyufunc import img_PIL_to_bytes
        >>> img = Image.open('test.jpg')
        >>> img_b = img_PIL_to_bytes(img)
        >>> print(img_b)
    """
    try:
        img_b = io.BytesIO()
        img.save(img_b, format='JPEG')
        return img_b.getvalue()
    except Exception:
        print("Error: fail to convert PIL image to bytes, return empty bytes")
        return bytes("", encoding='utf-8')


@requires(("pillow", "PIL"))
def img_bytes_to_PIL(img_b: bytes) -> Image:
    """Convert image bytes to PIL image

    Args:
        img_b (bytes): image bytes

    Returns:
        Image: PIL image object

    Example:
        >>> from PIL import Image
        >>> from pyufunc import img_bytes_to_PIL
        >>> img_path = 'test.jpg'
        >>> img_b = cvt_img_to_bytes(img_path)
        >>> img = cvt_img_bytes_to_PIL_img(img_b)
        >>> img.show()
    """

    import_package(("pillow", "PIL"))
    from PIL import Image

    try:
        return Image.open(io.BytesIO(img_b))
    except Exception:
        print("Error: fail to convert image bytes to PIL image, return a white image")
        return Image.new('RGB', (1, 1), (255, 255, 255))


def img_bytes_to_CV(img_b: bytes) -> np.ndarray:
    """Convert image bytes to OpenCV numpy array

    Args:
        img_b (bytes): image bytes

    Returns:
        np.ndarray: OpenCV numpy array

    Example:
        >>> from pyufunc img_bytes_to_CVk, img_show
        >>> from PIL import Image
        >>> img_path = 'test.jpg'
        >>> img_b = cvt_img_to_bytes(img_path)
        >>> img = img_bytes_to_CV(img_b)
        >>> img_show(img)

    """
    img_pil = img_bytes_to_PIL(img_b)
    return img_PIL_to_CV(img_pil)


def img_CV_to_bytes(img: np.ndarray) -> bytes:
    """Convert OpenCV numpy array to image bytes

    Args:
        img (np.ndarray): OpenCV numpy array

    Returns:
        bytes: image bytes

    Example:
        >>> from pyufunc import img_CV_to_bytes, img_show
        >>> import cv2
        >>> img = cv2.imread('test.jpg')
        >>> img_b = img_CV_to_bytes(img)
        >>> img_show(img)
    """

    img_pil = img_CV_to_PIL(img)
    return img_PIL_to_bytes(img_pil)
