# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, February 15th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import math

__all__ = ["to_radians", "to_degrees", "point_to_circle"]


# convert degrees to radians
def to_radians(angle_in_degrees: float) -> float:
    """Convert degrees to radians

    Args:
        angle_in_degrees (float): angle in degrees

    Returns:
        float: the radians value

    Example:
        >>> to_radians(180)
        3.141592653589793
    """
    return (angle_in_degrees * math.pi) / 180


# convert radians to degrees
def to_degrees(angle_in_radians: float) -> float:
    """Convert radians to degrees

    Args:
        angle_in_radians (float): angle in radians

    Returns:
        float: the degrees value

    Example:
        >>> to_degrees(3.141592653589793)
        180.0
    """
    return (angle_in_radians * 180) / math.pi


def offset(point: list[float, float], distance: float, earth_radius: float, bearing: float) -> list:
    """ the function to calculate the new longitude and latitude by the distance and bearing from the original point

    Args:
        point (list[float, float]): the point of longitude and latitude in format [longitude, latitude]
        distance (float): the distance from the original point, unit is meter
        earth_radius (float): the earth radius, unit is meter
        bearing (float): the bearing from the original point, unit is radians

    Returns:
        list: the new longitude and latitude in degree format [longitude, latitude]
    """

    # convert longitude and latitude to radians
    lon1 = to_radians(point[0])
    lat1 = to_radians(point[1])

    d_by_r = distance / earth_radius

    # calculate the new longitude and latitude
    lat = math.asin(math.sin(lat1) * math.cos(d_by_r) + math.cos(lat1) * math.sin(d_by_r) * math.cos(bearing))
    lon = lon1 + math.atan2(math.sin(bearing) * math.sin(d_by_r) * math.cos(lat1),
                            math.cos(d_by_r) - math.sin(lat1) * math.sin(lat))
    return [to_degrees(lon), to_degrees(lat)]


def point_to_circle(center: list[float, float],
                    radius: float,
                    options={"edges": 32, "bearing": 0, "direction": 1}) -> dict:
    """ the function to generate a polygon by the center and radius

    Args:
        center (list[float, float]): the center point with format [longitude, latitude]
        radius (float): the radius of the circle, unit is meter
        options (dict, optional): set the circle options. Defaults to {"edges": 32, "bearing": 0, "direction": 1}.
            edges (int, optional): the edges of the polygon. Defaults to 32.
            bearing (float, optional): the bearing of the polygon. Defaults to 0.
            direction (int, optional): the direction of the polygon. Defaults to 1.

    Returns:
        dict: the polygon in geojson format

    Example:
        >>> point_to_circle([173.283966, -41.270634], 1000)


    """

    # the default earth radius in meters
    DEFAULT_EARTH_RADIUS = 6378137

    edges = options["edges"]
    earth_radius = DEFAULT_EARTH_RADIUS
    bearing = options["bearing"]
    direction = options["direction"]

    start = to_radians(bearing)
    coordinates = []
    for i in range(edges):
        coordinates.append(offset(center, radius, earth_radius, start + (direction * 2 * math.pi * -i) / edges))
    coordinates.append(coordinates[0])

    return {"type": "Polygon", "coordinates": coordinates}