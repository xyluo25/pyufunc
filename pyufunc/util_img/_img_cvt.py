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


def cvt_img_to_bytes(img_path: str) -> bytes:
    """Convert image to bytes

    Args:
        img_path (str): image path, include all image format, e.g. .jpg, .png, .bmp, .gif, etc.

    Returns:
        bytes: the image bytes

    Example:
        >>> from pyufunc import cvt_img_to_bytes
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


def cvt_PIL_img_to_bytes(img: Image) -> bytes:
    """Convert PIL image to bytes

    Args:
        img (Image): PIL image object

    Returns:
        bytes: the image bytes

    Example:
        >>> from PIL import Image
        >>> from pyufunc import cvt_PIL_img_to_bytes
        >>> img = Image.open('test.jpg')
        >>> img_b = cvt_PIL_img_to_bytes(img)
        >>> print(img_b)
    """
    try:
        img_b = io.BytesIO()
        img.save(img_b, format='JPEG')
        return img_b.getvalue()
    except Exception:
        return bytes("", encoding='utf-8')


def cvt_img_bytes_to_PIL_img(img_b: bytes) -> Image:
    """Convert image bytes to PIL image

    Args:
        img_b (bytes): image bytes

    Returns:
        Image: PIL image object

    Example:
        >>> from PIL import Image
        >>> from pyufunc import cvt_img_bytes_to_PIL_img
        >>> img_path = 'test.jpg'
        >>> img_b = cvt_img_to_bytes(img_path)
        >>> img = cvt_img_bytes_to_PIL_img(img_b)
        >>> img.show()
    """
    try:
        img = Image.open(io.BytesIO(img_b))
        return img
    except Exception:
        return Image.new('RGB', (1, 1), (255, 255, 255))