# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from pyufunc.util_geo._geo_distance import (proj_point_to_line,
                                            calc_distance_on_unit_sphere,
                                            calc_distance_on_unit_haversine,
                                            find_closest_point,
                                            get_coordinates_from_geom,
                                            find_k_nearest_points,
                                            )
from pyufunc.util_geo._coordinate_convert import (
    cvt_wgs84_to_baidu09,
    cvt_wgs84_to_gcj02,
    cvt_gcj02_to_baidu09,
    cvt_gcj02_to_wgs84,
    cvt_baidu09_to_wgs84,
    cvt_baidu09_to_gcj02,
)
from pyufunc.util_geo._geo_circle import create_circle_at_point_with_radius

from pyufunc.util_geo._geo_area import calc_area_from_wkt_geometry
from pyufunc.util_geo._geo_tif import download_elevation_tif_by

# GMNS: General Modeling Network Specification
# import pyufunc.util_geo._gmns as gmns_geo
from pyufunc.util_geo._gmns import Node as gmns_Node
from pyufunc.util_geo._gmns import Link as gmns_Link
from pyufunc.util_geo._gmns import POI as gmns_POI
from pyufunc.util_geo._gmns import Zone as gmns_Zone
from pyufunc.util_geo._gmns import Agent as gmns_Agent
from pyufunc.util_geo._gmns import read_node as gmns_read_node
from pyufunc.util_geo._gmns import read_poi as gmns_read_poi
from pyufunc.util_geo._gmns import read_link as gmns_read_link
from pyufunc.util_geo._gmns import read_zone as gmns_read_zone
from pyufunc.util_geo._get_osm_place import get_osm_place
from pyufunc.util_geo._get_osm_data import get_osm_by_relation_id, get_osm_by_bbox, extract_bbox_coordinates


__all__ = [
    # geo_area
    'calc_area_from_wkt_geometry',

    # geo_circle
    'create_circle_at_point_with_radius',

    # geo_distance
    'proj_point_to_line',
    'calc_distance_on_unit_sphere',
    'calc_distance_on_unit_haversine',
    'find_closest_point',
    'get_coordinates_from_geom',
    'find_k_nearest_points',

    # gmns
    # "gmns_geo",
    "gmns_Node",
    "gmns_Link",
    "gmns_POI",
    "gmns_Zone",
    "gmns_Agent",
    "gmns_read_node",
    "gmns_read_poi",
    "gmns_read_link",
    # "gmns_read_zone_by_geometry",
    # "gmns_read_zone_by_centroid",
    "gmns_read_zone",

    # coordinate convert
    "cvt_wgs84_to_baidu09",
    "cvt_wgs84_to_gcj02",
    "cvt_gcj02_to_baidu09",
    "cvt_gcj02_to_wgs84",
    "cvt_baidu09_to_wgs84",
    "cvt_baidu09_to_gcj02",

    # find osm place
    "get_osm_place",

    # geo_tif
    "download_elevation_tif_by",

    # get osm data
    "get_osm_by_relation_id",
    "get_osm_by_bbox",
    "extract_bbox_coordinates",
]