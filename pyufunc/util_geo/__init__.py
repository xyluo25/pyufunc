# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from pyufunc.util_geo._geo_circle import create_circle_at_point_with_radius
from pyufunc.util_geo._geo_distance import (proj_point_to_line,
                                            calc_distance_on_unit_sphere,
                                            find_closest_point,
                                            get_coordinates_from_geom,
                                            find_k_nearest_points,
                                            )
from pyufunc.util_geo._coordinate_coversion import (
    cvt_wgs84_to_baidu09,
    cvt_wgs84_to_gcj02,
    cvt_gcj02_to_baidu09,
    cvt_gcj02_to_wgs84,
    cvt_baidu09_to_wgs84,
    cvt_baidu09_to_gcj02,
)

# GMNS: General Modeling Network Specification
import pyufunc.util_geo._gmns as gmns_geo
from pyufunc.util_geo._gmns import Node as GMNSNode
from pyufunc.util_geo._gmns import Link as GMNSLink
from pyufunc.util_geo._gmns import POI as GMNSPOI
from pyufunc.util_geo._gmns import Zone as GMNSZone
from pyufunc.util_geo._gmns import Agent as GMNSAgent
from pyufunc.util_geo._gmns import read_node as gmns_read_node
from pyufunc.util_geo._gmns import read_poi as gmns_read_poi
from pyufunc.util_geo._gmns import read_link as gmns_read_link
# from pyufunc.util_geo._gmns import read_zone_by_geometry as gmns_read_zone_by_geometry
# from pyufunc.util_geo._gmns import read_zone_by_centroid as gmns_read_zone_by_centroid
from pyufunc.util_geo._gmns import read_zone as gmns_read_zone

__all__ = [
    # geo_circle
    'create_circle_at_point_with_radius',

    # geo_distance
    'proj_point_to_line',
    'calc_distance_on_unit_sphere',
    'find_closest_point',
    'get_coordinates_from_geom',
    'find_k_nearest_points',

    # gmns
    "gmns_geo",
    "GMNSNode",
    "GMNSLink",
    "GMNSPOI",
    "GMNSZone",
    "GMNSAgent",
    "gmns_read_node",
    "gmns_read_poi",
    "gmns_read_link",
    # "gmns_read_zone_by_geometry",
    # "gmns_read_zone_by_centroid",
    "gmns_read_zone",

    # coordinate conversion
    "cvt_wgs84_to_baidu09",
    "cvt_wgs84_to_gcj02",
    "cvt_gcj02_to_baidu09",
    "cvt_gcj02_to_wgs84",
    "cvt_baidu09_to_wgs84",
    "cvt_baidu09_to_gcj02",

]