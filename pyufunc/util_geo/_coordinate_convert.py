# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, April 14th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from math import pi as PI
from math import sin, cos, sqrt, fabs, atan2


def cvt_gcj02_to_baidu09(gcj_lng: float, gcj_lat: float) -> tuple[float, float]:
    """Convert coordinate from GCJ02 to Baidu09.

    Args:
        gcj_lng (float): longitude in GCJ02 coordinate system.
        gcj_lat (float): latitude in GCJ02 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in Baidu09 coordinate system. (lng, lat)

    Example:
        >>> from pyufunc import gcj02_to_baidu09
        >>> gcj02_to_baidu09(113.8344944, 22.6897065)
        (113.8410533339616, 22.695460615640712)

    See Also:
        - https://github.com/sshuair/coord-convert
    """
    # TDD: check if the input is valid
    if not isinstance(gcj_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(gcj_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= gcj_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= gcj_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= gcj_lng <= 137.8347:
        raise ValueError(
            "Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= gcj_lat <= 55.8271:
        raise ValueError(
            "Latitude outside of China, please don't use this function for coordinates outside of China.")

    x_pi = PI * 3000.0 / 180.0

    z = sqrt(gcj_lng**2 + gcj_lat**2) + 0.00002 * sin(gcj_lat * x_pi)
    theta = atan2(gcj_lat, gcj_lng) + 0.000003 * cos(gcj_lng * x_pi)
    baidu_lng = z * cos(theta) + 0.0065
    baidu_lat = z * sin(theta) + 0.006

    return (baidu_lng, baidu_lat)


def cvt_baidu09_to_gcj02(baidu_lng: float, baidu_lat: float) -> tuple[float, float]:
    """Convert coordinate from Baidu09 to GCJ02.

    Args:
        baidu_lng (float): longitude in Baidu09 coordinate system.
        baidu_lat (float): latitude in Baidu09 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in GCJ02 coordinate system. (lng, lat)

    See Also:
        - https://github.com/sshuair/coord-convert

    Example:
        >>> from pyufunc import baidu09_to_gcj02
        >>> baidu09_to_gcj02(113.8410533, 22.6954606)
        (113.83449473213525, 22.689705802564674)

    """
    # TDD: check if the input is valid
    if not isinstance(baidu_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(baidu_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= baidu_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= baidu_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= baidu_lng <= 137.8347:
        raise ValueError(
            "Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= baidu_lat <= 55.8271:
        raise ValueError(
            "Latitude outside of China, please don't use this function for coordinates outside of China.")

    x_pi = PI * 3000.0 / 180.0

    # coordinate adjustment
    lng = baidu_lng - 0.0065
    lat = baidu_lat - 0.006

    z = sqrt(lng**2 + lat**2) - 0.00002 * sin(lat * x_pi)
    theta = atan2(lat, lng) - 0.000003 * cos(lng * x_pi)
    gcj_lng = z * cos(theta)
    gcj_lat = z * sin(theta)

    return (gcj_lng, gcj_lat)


def cvt_wgs84_to_gcj02(wgs84_lng: float, wgs84_lat: float) -> tuple[float, float]:
    """Convert coordinate from WGS84 to GCJ02. GCJ02 also known as Mars coordinate system.

    Args:
        wgs84_lng (float): longitude in WGS84 coordinate system.
        wgs84_lat (float): latitude in WGS84 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in GCJ02 coordinate system. (lng, lat)

    Example:
        >>> from pyufunc import wgs84_to_gcj02
        >>> wgs84_to_gcj02(113.8294754, 22.6926477)
        (113.83449435090813, 22.689706503327333)

    See Also:
        - https://github.com/sshuair/coord-convert
    """

    # TDD: check if the input is valid
    if not isinstance(wgs84_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(wgs84_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= wgs84_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= wgs84_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= wgs84_lng <= 137.8347:
        raise ValueError("Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= wgs84_lat <= 55.8271:
        raise ValueError("Latitude outside of China, please don't use this function for coordinates outside of China.")

    # a: the semi-major axis of the earth
    # f: the flattening of the earth
    # b: the semi-minor axis of the earth
    # ee: the eccentricity of the earth
    a = 6378245.0
    f = 1 / 298.3
    b = a * (1 - f)
    ee = 1 - b**2 / a**2

    lat_delta = _cvt_lat(wgs84_lng - 105.0, wgs84_lat - 35.0)
    lng_delta = _cvt_lon(wgs84_lng - 105.0, wgs84_lat - 35.0)

    # latitude adjustment
    lat_radius = wgs84_lat / 180.0 * PI
    lat_0 = sin(lat_radius)
    lat_1 = 1 - ee * lat_0 * lat_0
    lat_2 = sqrt(lat_1)
    lat_delta = (lat_delta * 180.0) / ((a * (1 - ee)) / (lat_1 * lat_2) * PI)
    lng_delta = (lng_delta * 180.0) / (a / lat_2 * cos(lat_radius) * PI)

    gcj02_lng = wgs84_lng + lng_delta
    gcj02_lat = wgs84_lat + lat_delta

    return (gcj02_lng, gcj02_lat)


def cvt_gcj02_to_wgs84(gcj_lng: float, gcj_lat: float) -> tuple[float, float]:
    """Convert coordinate from GCJ02 to WGS84.

    Args:
        gcj_lng (float): longitude in GCJ02 coordinate system.
        gcj_lat (float): latitude in GCJ02 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in WGS84 coordinate system. (lng, lat)

    See Also:
        - https://github.com/sshuair/coord-convert

    Example:
        >>> from pyufunc import gcj02_to_wgs84
        >>> gcj02_to_wgs84(113.8344944, 22.6897065)
        (113.82948917244678, 22.6926579036743)
    """
    # TDD: check if the input is valid
    if not isinstance(gcj_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(gcj_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= gcj_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= gcj_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= gcj_lng <= 137.8347:
        raise ValueError("Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= gcj_lat <= 55.8271:
        raise ValueError("Latitude outside of China, please don't use this function for coordinates outside of China.")

    # a: the semi-major axis of the earth
    # f: the flattening of the earth
    # b: the semi-minor axis of the earth
    # ee: the eccentricity of the earth
    a = 6378245.0
    f = 1 / 298.3
    b = a * (1 - f)
    ee = 1 - b**2 / a**2

    lat_delta = _cvt_lat(gcj_lng - 105.0, gcj_lat - 35.0)
    lng_delta = _cvt_lon(gcj_lng - 105.0, gcj_lat - 35.0)
    lat_radius = gcj_lat / 180.0 * PI
    lat_0 = sin(lat_radius)
    lat_1 = 1 - ee * lat_0**2
    lat_2 = sqrt(lat_1)
    lat_delta = (lat_delta * 180.0) / ((a * (1 - ee)) / (lat_1 * lat_2) * PI)
    lng_delta = (lng_delta * 180.0) / (a / lat_2 * cos(lat_radius) * PI)

    lng = gcj_lng + lng_delta
    lat = gcj_lat + lat_delta

    return (gcj_lng * 2 - lng, gcj_lat * 2 - lat)


def cvt_baidu09_to_wgs84(baidu_lng: float, baidu_lat: float) -> tuple[float, float]:
    """Convert coordinate from Baidu09 to WGS84.

    Args:
        baidu_lng (float): longitude in Baidu09 coordinate system.
        baidu_lat (float): latitude in Baidu09 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in WGS84 coordinate system. (lng, lat)

    See Also:
        - https://github.com/sshuair/coord-convert

    Example:
        >>> from pyufunc import baidu09_to_wgs84
        >>> baidu09_to_wgs84(113.8410533, 22.6954606)
        (113.82948950551985, 22.692657207035214)
    """
    # TDD: check if the input is valid
    if not isinstance(baidu_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(baidu_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= baidu_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= baidu_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= baidu_lng <= 137.8347:
        raise ValueError(
            "Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= baidu_lat <= 55.8271:
        raise ValueError(
            "Latitude outside of China, please don't use this function for coordinates outside of China.")

    gcj_lng, gcj_lat = cvt_baidu09_to_gcj02(baidu_lng, baidu_lat)
    wgs84_lng, wgs84_lat = cvt_gcj02_to_wgs84(gcj_lng, gcj_lat)

    return (wgs84_lng, wgs84_lat)


def cvt_wgs84_to_baidu09(wgs84_lng: float, wgs84_lat: float) -> tuple[float, float]:
    """Convert coordinate from WGS84 to Baidu09. Baidu09 also known as BD09 coordinate system.

    Args:
        wgs84_lng (float): longitude in WGS84 coordinate system.
        wgs84_lat (float): latitude in WGS84 coordinate system.

    Returns:
        tuple[float, float]: longitude and latitude in Baidu09 coordinate system. (lng, lat)

    Example:
        >>> from pyufunc import wgs84_to_baidu09
        >>> wgs84_to_baidu09(113.8294754, 22.6926477)
        (113.84105328499314, 22.69546061836469)

    Note:
        Baidu09 is a coordinate system used by Baidu Map, the coordinate system is based on GCJ02.
        if the input is not in China, the result may be inaccurate.
        The package will check if the input is valid, and raise an error if the input is invalid.
    """

    # TDD: check if the input is valid
    if not isinstance(wgs84_lng, (int, float)):
        raise TypeError("Invalid input for longitude.")
    if not isinstance(wgs84_lat, (int, float)):
        raise TypeError("Invalid input for latitude.")

    # Check if the input is in the valid range
    if not -180.0 <= wgs84_lng <= 180.0:
        raise ValueError("Longitude out of range, between -180 and 180.")
    if not -90.0 <= wgs84_lat <= 90.0:
        raise ValueError("Latitude out of range, between -90 and 90.")

    # check if the input is in China
    if not 72.004 <= wgs84_lng <= 137.8347:
        raise ValueError(
            "Longitude outside of China, please don't use this function for coordinates outside of China.")
    if not 0.8293 <= wgs84_lat <= 55.8271:
        raise ValueError(
            "Latitude outside of China, please don't use this function for coordinates outside of China.")

    gcj_lng, gcj_lat = cvt_wgs84_to_gcj02(wgs84_lng, wgs84_lat)
    baidu_lng, baidu_lat = cvt_gcj02_to_baidu09(gcj_lng, gcj_lat)

    return (baidu_lng, baidu_lat)


def _cvt_lat(lng: float, lat: float) -> float:
    """latitude adjustment based on the longitude and latitude.

    Args:
        x (float): longitude
        y (float): latitude

    Returns:
        float: latitude adjustment on spherical coordinate system.
    """

    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * \
        lat * lat + 0.1 * lng * lat + 0.2 * sqrt(fabs(lng))
    ret = ret + (20.0 * sin(6.0 * lng * PI) + 20.0 *
                 sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret = ret + (20.0 * sin(lat * PI) + 40.0 * sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret = ret + (160.0 * sin(lat / 12.0 * PI) + 320.0 *
                 sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def _cvt_lon(lng: float, lat: float) -> float:
    """longitude adjustment based on the longitude and latitude.

    Args:
        x (float): longitude
        y (float): latitude

    Returns:
        float: longitude adjustment on spherical coordinate system.
    """
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * \
        lng + 0.1 * lng * lat + 0.1 * sqrt(fabs(lng))
    ret = ret + (20.0 * sin(6.0 * lng * PI) + 20.0 *
                 sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret = ret + (20.0 * sin(lng * PI) + 40.0 * sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret = ret + (150.0 * sin(lng / 12.0 * PI) + 300.0 *
                 sin(lng * PI / 30.0)) * 2.0 / 3.0
    return ret
