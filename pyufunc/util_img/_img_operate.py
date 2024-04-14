# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, March 29th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Any

# https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import
if TYPE_CHECKING:
    # import modules from 3rd party libraries
    type_checking = True

    import numpy as np
    import cv2
    from PIL import Image

from pyufunc.pkg_utils import requires, import_package


@requires(("pillow", "PIL"), verbose=False)
def is_PIL_img(img: Any) -> bool:
    """Check if the input object is a PIL image

    Args:
        img (Any): input object

    Returns:
        bool: True if the input object is a PIL image, otherwise False

    Example:
        >>> import cv2
        >>> from PIL import Image
        >>> from pyufunc import is_pil_image
        >>> img_cv = cv2.imread('test.jpg')
        >>> img_pil = Image.open('test.jpg')
        >>> print(is_pil_image(img_cv))
        False
        >>> print(is_pil_image(img_pil))
        True
    """
    import_package(("pillow", "PIL"), verbose=False)
    from PIL import Image

    return isinstance(img, Image.Image)


@requires("numpy", verbose=False)
def is_CV_img(img: Any) -> bool:
    """Check if the input object is a CV image

    Args:
        img (Any): input object

    Returns:
        bool: True if the input object is a CV image, otherwise False

    Example:
        >>> import cv2
        >>> from PIL import Image
        >>> from pyufunc import is_cv_image
        >>> img_cv = cv2.imread('test.jpg')
        >>> img_pil = Image.open('test.jpg')
        >>> print(is_cv_image(img_cv))
        True
        >>> print(is_cv_image(img_pil))
        False
    """
    # import necessary modules
    import_package("numpy", verbose=False)
    import numpy as np

    return isinstance(img, np.ndarray)


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_PIL_to_CV(img: Image.Image) -> np.ndarray:
    """Convert PIL image to CV image

    Args:
        img (Image.Image): PIL image object

    Returns:
        np.ndarray: CV image array

    Example:
        >>> import cv2
        >>> from PIL import Image
        >>> from pyufunc import cvt_img_PIL_to_CV
        >>> img_pil = Image.open('test.jpg')
        >>> img_cv = cvt_img_PIL_to_CV(img_pil)

    """
    # import necessary models
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)

    import numpy as np
    import cv2
    from PIL import Image

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_CV_to_PIL(img: np.ndarray) -> Image.Image:
    """Convert CV image to PIL image

    Args:
        img (np.ndarray): CV image array

    Returns:
        Image.Image: PIL image object

    Example:
        >>> import cv2
        >>> from PIL import Image
        >>> from pyufunc import cvt_img_CV_to_PIL
        >>> img_cv = cv2.imread('test.jpg')
        >>> img_pil = cvt_img_CV_to_PIL(img_cv)
    """
    # import necessary models
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import cv2
    from PIL import Image

    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_translate(img: Union[np.ndarray, str, Image.Image],
                  dx: float,
                  dy: float,
                  verbose: bool = True) -> np.ndarray:
    """Translate image with a given distance in x-axis and y-axis

    Args:
        img (Union[np.ndarray, str, Image.Image]): image array or image path or PIL image object
        dx (float): translate distance in x-axis, unit: pixel
        dy (float): translate distance in y-axis, unit: pixel
        verbose (bool, optional): print out processing message, default is True

    Returns:
        np.ndarray: the translated image

    Example:
        >>> import cv2
        >>> from pyufunc import img_translate
        >>> img = cv2.imread('test.jpg')
        >>> img_t = img_translate(img, 100, 100)
        >>> cv2.imshow('translated image', img_t)
        >>> cv2.waitKey(0)
        >>> cv2.destroyAllWindows()
    """

    # import necessary models
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import numpy as np
    import cv2
    from PIL import Image

    # TDD, Test-Driven Development
    # check if the input image is a string
    if not isinstance(img, (str, Image.Image, np.ndarray)):
        raise Exception("Error: the input image should be a string or a PIL image or a CV image")

    # if the input image is a string, read the image
    if isinstance(img, str):
        try:
            img = cv2.imread(img)
        except Exception as e:
            raise Exception(f"Error: {e}") from e

    # check if the input image is a PIL image
    # if it is a PIL image, convert it to a CV image
    if isinstance(img, Image.Image):
        img = cvt_img_PIL_to_CV(img)

    # get the height and width of image
    height, width = img.shape[:2]

    # get the translation matrix
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    img_t = cv2.warpAffine(img, M, (width, height))

    # whether to print out processing message
    if verbose:
        print(f"Image width: {width} pixels, height: {height} pixels")

    return img_t


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_rotate(img: Union[np.ndarray, str, Image.Image],
               angle: float,
               center: tuple[float, float] = None,
               scale: float = 1.0,
               verbose: bool = True) -> np.ndarray:
    """Rotate image with a given angle at a given center

    Args:
        img (Union[np.ndarray, str, Image.Image]): image array or image path or PIL image object
        angle (float): rotate angle, unit: degree
        center (tuple[int, int], optional): rotate center [width, height], default is None,
            center is the center of image, unit: pixel
        scale (float, optional): scale factor, default is 1.0
        verbose (bool, optional): print out processing message, default is True

    Returns:
        np.ndarray: the rotated image

    Example:
        >>> import cv2
        >>> from pyufunc import img_rotate
        >>> img = cv2.imread('test.jpg')
        >>> img_r = img_rotate(img, 45)
        >>> cv2.imshow('rotated image', img_r)
        >>> cv2.waitKey(0)
        >>> cv2.destroyAllWindows()
    """

    # import necessary models
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import numpy as np
    import cv2
    from PIL import Image

    # TDD, Test-Driven Development
    # check if the input image is a string
    if not isinstance(img, (str, Image.Image, np.ndarray)):
        raise Exception("Error: the input image should be a string or a PIL image or a CV image")

    # if the input image is a string, read the image
    if isinstance(img, str):
        try:
            img = cv2.imread(img)
        except Exception as e:
            raise Exception(f"Error: {e}") from e

    # check if the input image is a PIL image
    if isinstance(img, Image.Image):
        img = cvt_img_PIL_to_CV(img)

    # get the height and width of image
    height, width = img.shape[:2]

    # if center is None, set center to the center of image
    img_center = (width // 2, height // 2)

    # rotate center
    if center is None:
        center = img_center

    # check center within the range of image
    if center[0] < 0 or center[0] >= width or center[1] < 0 or center[1] >= height:
        print(f"Error: x should be within the range of 0 to {width}, y should be within the range of 0 to {height}")
        raise Exception("Error: center should be within the range of image")

    # check scale factor that within the range of 0.0 to 1.0
    if scale < 0.0 or scale > 1.0:
        raise Exception("Error: scale factor should be within the range of 0.0 to 1.0")

    # get the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, scale)

    # rotate the image
    img_r = cv2.warpAffine(img, M, (width, height))

    if verbose:
        print(f"Image width: {width} pixels, height: {height} pixels")
        print(f"Image center: {img_center}, rotate center: {center}")

    return img_r


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_rotate_bound(img: Union[np.ndarray, str, Image.Image],
                     angle: float,
                     verbose: bool = True) -> np.ndarray:
    """Rotate image with a given angle, and keep the whole image in the frame

    Args:
        img (Union[np.ndarray, str, Image.Image]): image array or image path or PIL image object
        angle (float): rotate angle, unit: degree
        verbose (bool, optional): if true, print out processing message. Defaults to True.

    Returns:
        np.ndarray: the rotated image

    Example:
        >>> import cv2
        >>> from pyufunc import img_rotate_bound
        >>> img = cv2.imread('test.jpg')
        >>> img_rb = img_rotate_bound(img, 45)
        >>> cv2.imshow('rotated image', img_rb)
        >>> cv2.waitKey(0)
        >>> cv2.destroyAllWindows()
    """

    # import necessary modules
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import numpy as np
    import cv2
    from PIL import Image

    # TDD, Test-Driven Development
    # check if the input image is a string
    if not isinstance(img, (str, Image.Image, np.ndarray)):
        raise Exception("Error: the input image should be a string or a PIL image or a CV image")

    # if the input image is a string, read the image
    if isinstance(img, str):
        try:
            img = cv2.imread(img)
        except Exception as e:
            raise Exception(f"Error: {e}") from e

    # check if the input image is a PIL image
    if isinstance(img, Image.Image):
        img = cvt_img_PIL_to_CV(img)

    # get the height and width of image
    height, width = img.shape[:2]

    # get the center of image
    center_x, center_y = width / 2, height / 2

    # get the rotation matrix
    # clockwise: negative angle
    # get sin and cos of the angle
    M = cv2.getRotationMatrix2D((center_x, center_y), -angle, 1.0)
    sin_val = np.abs(M[0, 1])
    cos_val = np.abs(M[0, 0])

    # new bounding shape
    new_width = int((height * sin_val) + (width * cos_val))
    new_height = int((height * cos_val) + (width * sin_val))

    # update the rotation matrix
    M[0, 2] += (new_width / 2) - center_x
    M[1, 2] += (new_height / 2) - center_y

    # rotate the image
    img_rb = cv2.warpAffine(img, M, (new_width, new_height))

    if verbose:
        print(f"Image width: {width} pixels, height: {height} pixels")
        print(f"New image width: {new_width} pixels, height: {new_height} pixels")

    return img_rb


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_resize(img: Union[np.ndarray, str, Image.Image],
               width: int = None,
               height: int = None,
               inter: int = None,
               verbose: bool = True) -> np.ndarray:
    """Resize image

    Args:
        img (Union[np.ndarray, str, Image.Image]): image array or image path or PIL image object
        width (int, optional): target width, default is None, unit: pixel
        height (int, optional): target height, default is None, unit: pixel
        inter (int, optional): interpolation method, default is cv2.INTER_AREA
        verbose (bool, optional): print out processing message, default is True

    Returns:
        np.ndarray: the resized image

    Example:
        >>> import cv2
        >>> from pyufunc import img_resize
        >>> img = cv2.imread('test.jpg')
        >>> img_r = img_resize(img, width=100, height=100)
        >>> cv2.imshow('resized image', img_r)
        >>> cv2.waitKey(0)
        >>> cv2.destroyAllWindows()
    """

    # import necessary modules
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import numpy as np
    import cv2
    from PIL import Image

    # TDD, Test-Driven Development
    # check if the input image is a string
    if not isinstance(img, (str, Image.Image, np.ndarray)):
        raise Exception("Error: the input image should be a string or a PIL image or a CV image")

    # if the input image is a string, read the image
    if isinstance(img, str):
        try:
            img = cv2.imread(img)
        except Exception as e:
            raise Exception(f"Error: {e}") from e

    # check if the input image is a PIL image
    if isinstance(img, Image.Image):
        img = cvt_img_PIL_to_CV(img)

    # set the default interpolation method
    if inter is None:
        inter = cv2.INTER_AREA

    # get the height and width of image
    img_height, img_width = img.shape[:2]

    # if both the width and height are None, return the original image
    if width is None and height is None:
        return img

    # if the width is None, calculate the ratio of the height
    if width is None:
        ratio = height / float(img_height)
        dim = (int(img_width * ratio), height)

    # if the height is None, calculate the ratio of the width
    else:
        ratio = width / float(img_width)
        dim = (width, int(img_height * ratio))

    # resize the image
    img_rsz = cv2.resize(img, dim, interpolation=inter)

    if verbose:
        print(f"Image width: {img_width} pixels, height: {img_height} pixels")
        print(f"Resized image width: {dim[0]} pixels, height: {dim[1]} pixels")

    return img_rsz


@requires("numpy", ("opencv-python", "cv2"), ("pillow", "PIL"), verbose=False)
def img_show(img: Union[str, np.ndarray, Image.Image],
             is_PIL_show: bool = False,
             verbose: bool = True) -> None:
    """Show image in a window from image path or image array or PIL image object

    Args:
        img (Union[str, np.ndarray, Image.Image]): image path or image array or PIL image object
        is_PIL_show (bool, optional): if True, show the image as a PIL image, default is False
            else, show the image as a CV image

        verbose (bool, optional): print out processing message, default is True

    Example:
        >>> import cv2
        >>> from pyufunc import img_show
        >>> img = cv2.imread('test.jpg')
        >>> img_show(img)
    """

    # import necessary modules
    import_package("numpy", verbose=False)
    import_package(("opencv-python", "cv2"), verbose=False)
    import_package(("pillow", "PIL"), verbose=False)
    import cv2
    from PIL import Image
    import numpy as np

    # TDD, Test-Driven Development
    # check if the input image is a string
    if not isinstance(img, (str, Image.Image, np.ndarray)):
        raise Exception("Error: the input image should be a string or a PIL image or a CV image")

    # if the input image is a string, read the image
    if isinstance(img, str):
        try:
            img_cv = cv2.imread(img)
            img_pil = Image.open(img)
        except Exception as e:
            raise Exception(f"Error: {e}") from e

    # check if the input image is a PIL image
    if isinstance(img, Image.Image):
        img_cv = cvt_img_PIL_to_CV(img)
        img_pil = img

    # check if the input image is a CV image
    if isinstance(img, np.ndarray):
        img_cv = img
        img_pil = cvt_img_CV_to_PIL(img)

    if is_PIL_show:
        if verbose:
            print("  Show image using PIL, if you want to show the image using OpenCV, set is_PIL_show=False")

        img_pil.show()
        return None

    if verbose:
        print("  Show image using OpenCV in default, if you want to show the image using PIL, set is_PIL_show=True")

    cv2.imshow('image', img_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return None
