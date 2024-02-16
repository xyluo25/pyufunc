# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import shapely
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection
from shapely.geometry.base import BaseGeometry
import numpy as np
import copy
from typing import Union, Iterable
import functools

from pyufunc.util_geo._geo_circle import point_to_circle_on_unit_radius


def proj_point_to_line(point: Point, line: LineString) -> Point:
    """Project a point to a line.

    See Also:
        - pyhelper.geo.project_point_to_line: https://pyhelpers.readthedocs.io/en/latest/index.html
        - https://shapely.readthedocs.io/en/stable/manual.html#object.project
        - https://shapely.readthedocs.io/en/stable/manual.html#object.interpolate

    Args:
        point (shapely.geometry.Point): the point to be projected
        line (shapely.geometry.LineString): the line to be projected to

    Returns:
        shapely.geometry.Point: the projected point on the line

    Example:
        >>> from shapely.geometry import Point, LineString
        >>> point = Point(0, 0)
        >>> line = LineString([(1, 1), (2, 2)])
        >>> projected_point = project_point_to_line(point, line)
        >>> projected_point
        POINT (0.5 0.5)
    """

    # TDD: Test-Driven Development, check data types of input arguments
    assert isinstance(point, Point), "The input point should be a shapely.Point object."
    assert isinstance(line, LineString), "The input line should be a shapely.LineString object."

    # get the coordinates of the point
    projected_point = line.interpolate(line.project(point))

    return projected_point


def calc_distance_on_unit_sphere(pt1: Union[Point, tuple, list, np.array],
                                 pt2: Union[Point, tuple, list, np.array],
                                 unit: str = 'km') -> float:
    """Calculate the distance between two points on the unit sphere.

    Args:
        pt1 (Point | tuple | list | np.array): the first point, in the format of (longitude, latitude)
        pt2 (Point | tuple | list | np.array): the second point, in the format of (longitude, latitude)
        unit (str, optional): distance unit, in "meter", "km", and "mile". Defaults to 'km'.

    Returns:
        float: the distance between two points on the unit sphere

    Example:
        >>> from shapely.geometry import Point
        >>> pt1 = Point(-0.1276474, 51.5073219)
        >>> pt2 = Point(-1.9026911, 52.4796992)
        >>> calc_distance_on_unit_sphere(pt1, pt2)
        162.66049633957005

    Note:
        - This function is modified from the original code available at: https://pyhelpers.readthedocs.io/en/latest/index.html.
        - It assumes the earth is perfectly spherical and returns the distance based on each point's longitude and latitude.

    """

    # TDD: Test-Driven Development, check data types of input arguments
    assert isinstance(pt1, (Point, tuple, list, np.ndarray)), "The input pt1 should be a shapely.Point, tuple, list, or np.array object."
    assert isinstance(pt2, (Point, tuple, list, np.ndarray)), "The input pt2 should be a shapely.Point, tuple, list, or np.array object."
    assert unit in ["meter", "km", "mile"], "The input unit should be in 'meter', 'km', or 'mile'."

    # the default earth radius in meters
    EARTH_RADIUS = {"meter": 6378137, "km": 6371.0, "mile": 3960.0}

    # get the earth radius
    earth_radius = EARTH_RADIUS.get(unit, 6371.0)

    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = np.pi / 180.0

    if not all(isinstance(x, shapely.geometry.Point) for x in (pt1, pt2)):
        try:
            pt1_, pt2_ = map(shapely.geometry.Point, (pt1, pt2))
        except Exception as e:
            print(e)
            return None
    else:
        pt1_, pt2_ = map(copy.copy, (pt1, pt2))

    # phi = 90 - latitude
    phi1 = (90.0 - pt1_.y) * degrees_to_radians
    phi2 = (90.0 - pt2_.y) * degrees_to_radians

    # theta = longitude
    theta1 = pt1_.x * degrees_to_radians
    theta2 = pt2_.x * degrees_to_radians

    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cosine = (np.sin(phi1) * np.sin(phi2) * np.cos(theta1 - theta2) + np.cos(phi1) * np.cos(phi2))
    arc_length = np.arccos(cosine) * earth_radius

    # To multiply arc by the radius of the earth in a set of units to get length.
    return arc_length


def find_closest_point(pt: Point, pts: MultiPoint, k_closest: int = 1) -> list:
    """Find the closest point from a list of reference points.

    Args:
        pt (Point): the point to start with
        pts (MultiPoint): list of reference points in the format of shapely.MultiPoint
        k_closest (int): k closest points for each starting point. Defaults to 1.

    Returns:
        list: list of k closest points for each point

    Example:
        >>> from shapely.geometry import Point, MultiPoint
        >>> pt = Point(0, 0)
        >>> pts = MultiPoint([(1, 1), (2, 2), (3, 3)])
        >>> find_closest_point(pt, pts)
        [POINT (1 1)]

        >>> find_closest_point(pt, pts, k_closest=5)
        [POINT (1 1), POINT (2 2), POINT (3 3)]

    Note:
        - This function is modified from the original code available at: https://pyhelpers.readthedocs.io/en/latest/index.html.
        - The function return the close point but not distance.
        - Because of unit issue, the distance can be calculated by calc_distance_on_unit_sphere.
    """

    # TDD: Test-Driven Development, check data types of input arguments
    assert isinstance(pt, Point), "The input pt should be a shapely.Point object."
    assert isinstance(pts, MultiPoint), "The input pts should be a shapely.MultiPoint object."
    assert isinstance(k_closest, int), "The input k_closest should be an int object."

    # Find the min value using the distance function with coord parameter
    points_in_order = sorted(pts.geoms, key=functools.partial(shapely.geometry.Point.distance, pt))
    # closest_point = min(pts.geoms, key=functools.partial(shapely.geometry.Point.distance, pt))

    if k_closest < len(points_in_order):
        closest_point = points_in_order[:k_closest]
        return closest_point
    return points_in_order


def get_coordinates_from_geom(geom_obj: BaseGeometry) -> np.ndarray:
    """Get the coordinates from a geometry object.

    Args:
        geom_obj (Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]):
        the geometry object

    Returns:
        np.ndarray: the coordinates of the geometry object in the format of numpy.ndarray

    Example:
        >>> from shapely.geometry import Point
        >>> pt = Point(0, 0)
        >>> get_coordinates_from_geom(pt)
        array([[0., 0.]])

        >>> from shapely.geometry import LineString
        >>> line = LineString([(0, 0), (1, 1)])
        >>> get_coordinates_from_geom(line)
        array([[0., 0.],
               [1., 1.]])

        >>> from shapely.geometry import Polygon
        >>> poly = Polygon([(0, 0), (1, 1), (1, 0)])
        >>> get_coordinates_from_geom(poly)
        array([[0., 0.],
               [1., 1.],
               [1., 0.],
               [0., 0.]])

    Note:
        - This function is modified from the original code available at: https://pyhelpers.readthedocs.io/en/latest/index.html.
        - It returns the coordinates of the geometry object in the format of numpy.ndarray.
    """

    # TDD: Test-Driven Development, check data types of input arguments
    assert isinstance(geom_obj, BaseGeometry), (
        "The input geom_obj should be a shapely.geometry.base.BaseGeometry object.")

    if isinstance(geom_obj, np.ndarray):
        coords = geom_obj

    elif isinstance(geom_obj, Iterable):  # (list, tuple)
        coords = np.array(geom_obj)

    else:
        assert isinstance(geom_obj, shapely.geometry.base.BaseGeometry)
        geom_type = geom_obj.geom_type

        if 'Collection' in geom_type:
            temp = [get_coordinates_from_geom(x) for x in geom_obj.__getattribute__('geoms')]
            coords = np.concatenate(temp)

        elif geom_type.startswith('Multi'):
            if 'Polygon' in geom_type:
                coords = np.vstack([np.array(x.exterior.coords) for x in geom_obj.geoms])
            else:
                coords = np.vstack([np.array(x.coords) for x in geom_obj.geoms])
        else:
            if 'Polygon' in geom_type:
                coords = np.array(geom_obj.exterior.coords)
            else:
                coords = np.array(geom_obj.coords)

    return coords


def find_closest_points(pts: BaseGeometry,
                        geom_obj: BaseGeometry,
                        radius: float,
                        k_closest: int = 0) -> dict:
    """Find the closest points from a list of points to a geometry object (points) within a given radius.

    Args:
        pts (Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]):
            the point or points to start with
        geom_obj (Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]):
            the geometry object to be searched
        radius (float): search radius for each target point. Unit in meters.
        k_closest (int): k closest points for each starting point within the radius constraint.
            If k_closest is 0, return all points within the radius. Defaults to 0.

    Returns:
        dict: the closest points for each point within the radius constraint
    """

    # TDD: Test-Driven Development, check data types of input arguments
    typing_set = (Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection)
    assert isinstance(pts, typing_set), (
        "The input pts should be a shapely.geometry.base.BaseGeometry object.")
    assert isinstance(geom_obj, typing_set), (
        "The input pts should be a shapely.geometry.base.BaseGeometry object. object.")
    assert isinstance(radius, (float, int)), "The input radius should be a float, int, or None object."
    assert isinstance(k_closest, int), "The input is_closest_only should be an int object."

    # get the coordinates of the starting point / points
    pts_coords = get_coordinates_from_geom(pts)

    # create a buffer for each starting point with the given radius in meters
    pts_coords_buffer = [Polygon(point_to_circle_on_unit_radius(coord, radius)["coordinates"]) for coord in pts_coords]

    # get the coordinates of the geometry object and create a multipoint object for the geometry object
    geom_pts_coords = get_coordinates_from_geom(geom_obj)
    geom_pts = MultiPoint(geom_pts_coords)

    # find the closest points for each starting point within the buffer
    closest_points = {}

    for coord, pt_buffer in zip(pts_coords, pts_coords_buffer):
        # find the intersection between the buffer and the geometry object
        intersected_pts = pt_buffer.intersection(geom_pts)

    return closest_points
