# -*- coding:utf-8 -*-
##############################################################
# Created Date: Thursday, February 15th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
import math
from typing import Iterable, Union, TYPE_CHECKING
from pyufunc.util_magic import requires, import_package

#  https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import
if TYPE_CHECKING:
    from shapely.geometry import Point


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


def _offset(point: Point, distance: float, earth_radius: float, bearing: float) -> list:
    """ the function to calculate the new longitude and latitude by the distance and bearing from the original point

    Args:
        point (shapely.geometry.Point): the point of longitude and latitude in format POINT (longitude, latitude)
        distance (float): the distance from the original point, unit is meter
        earth_radius (float): the earth radius, unit is meter
        bearing (float): the bearing from the original point, unit is radians

    Returns:
        list: the new longitude and latitude in degree format [longitude, latitude]
    """

    from shapely.geometry import Point

    # TDD, test driven development: input validation
    assert isinstance(point, Point), "the point should be a shapely.geometry.Point"

    # convert longitude and latitude to radians
    lon1 = to_radians(point.x)
    lat1 = to_radians(point.y)

    d_by_r = distance / earth_radius

    # calculate the new longitude and latitude
    lat = math.asin(math.sin(lat1) * math.cos(d_by_r) + math.cos(lat1) * math.sin(d_by_r) * math.cos(bearing))
    lon = lon1 + math.atan2(math.sin(bearing) * math.sin(d_by_r) * math.cos(lat1),
                            math.cos(d_by_r) - math.sin(lat1) * math.sin(lat))
    return [to_degrees(lon), to_degrees(lat)]


@requires("shapely", verbose=False)
def create_circle_at_point_with_radius(point: Union[Point, Iterable[float]],
                                       radius: float,
                                       options: dict = None,
                                       verbose: bool = False) -> dict:
    """Generate a polygon by the center point and radius

    Args:
        point (shapely.geometry.Point, Iterable[float]): the center point with format [longitude, latitude]
        radius (float): the radius of the circle, unit is meter
        options (dict, optional): set the circle options. Defaults to {"edges": 32, "bearing": 0, "direction": 1}.

            edges (int, optional): the edges of the polygon. Defaults to 32.

            bearing (float, optional): the bearing of the polygon. Defaults to 0.

            direction (int, optional): the direction of the polygon. Defaults to 1.

        verbose (bool, optional): print the log information. Defaults to False.

    Returns:
        dict: the polygon in geojson format

    Example:
        >>> point_to_circle([173.283966, -41.270634], 1000)
        {'type': 'Polygon',
        'coordinates': [[111.9356, 33.42434831528412],
        [111.93539001956194, 33.42433105423093],
        [111.9351881087969, 33.424279934424106],
        [111.93500202722797, 33.42419692042648],
        [111.93483892600284, 33.424085202505225],
        [111.93470507305837, 33.42394907401863],
        [111.93460561223992, 33.4237937664093],
        [111.93454436563354, 33.423625248147346],
        [111.9345236867064, 33.423449995352435],
        [111.93454436989548, 33.42327474291128],
        [111.93460562011492, 33.4231062256568],
        [111.93470508334758, 33.42295091955525],
        [111.93483893713979, 33.422814792847205],
        [111.93500203751717, 33.4227030767045],
        [111.93518811667192, 33.422620064214655],
        [111.93539002382387, 33.42256894541529],
        [111.9356, 33.422551684715884],
        [111.9358099761761, 33.42256894541529],
        [111.93601188332806, 33.422620064214655],
        [111.93619796248281, 33.4227030767045],
        [111.93636106286019, 33.422814792847205],
        [111.93649491665239, 33.42295091955525],
        [111.93659437988505, 33.4231062256568],
        [111.93665563010453, 33.42327474291128],
        [111.9366763132936, 33.423449995352435],
        [111.93665563436643, 33.423625248147346],
        [111.93659438776005, 33.4237937664093],
        [111.9364949269416, 33.42394907401863],
        [111.93636107399713, 33.424085202505225],
        [111.936197972772, 33.42419692042648],
        [111.93601189120308, 33.424279934424106],
        [111.93580998043805, 33.42433105423093],
        [111.9356, 33.42434831528412]]}

    """
    if options is None:
        options = {"edges": 32, "bearing": 0, "direction": 1}
    # import shapely.geometry.Point
    import_package("shapely", verbose=False)
    from shapely.geometry import Point

    # TDD, test driven development: input validation
    assert isinstance(point, (Point, Iterable)), "the point should be a shapely.geometry.Point or a list of longitude and latitude"
    assert isinstance(radius, (int, float)), "the radius should be a number"
    assert isinstance(options, dict), "the options should be a dictionary"

    if verbose:
        print(" :Info: the unit in point_to_circle_on_unit_radius is meter, please convert the unit if necessary.")

    # convert point to shapely.geometry.Point
    if not isinstance(point, Point):
        point = Point(point)

    # the default earth radius in meters
    DEFAULT_EARTH_RADIUS = 6378137

    edges = options["edges"]
    earth_radius = DEFAULT_EARTH_RADIUS
    bearing = options["bearing"]
    direction = options["direction"]

    start = to_radians(bearing)
    coordinates = [
        _offset(
            point,
            radius,
            earth_radius,
            start + (direction * 2 * math.pi * -i) / edges,
        )
        for i in range(edges)
    ]
    # convert nested level 3 to level 2
    coordinates.append(coordinates[0])

    return {"type": "Polygon", "coordinates": coordinates}
