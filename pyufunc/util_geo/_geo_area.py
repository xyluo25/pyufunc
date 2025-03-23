# -*- coding:utf-8 -*-
##############################################################
# Created Date: Tuesday, February 6th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import os
from typing import TYPE_CHECKING

from pyufunc.util_magic import requires, import_package

if TYPE_CHECKING:
    from pyproj import Transformer
    import shapely


@requires("pyproj", "shapely", verbose=False)
def calc_area_from_wkt_geometry(wkt_geometry: str, unit: str = "sqm", verbose: bool = False) -> float:
    """
    Calculate the area of a geometry in WKT format.

    Args:
        wkt_geometry (str): The geometry in WKT format.
        transformer (Transformer): The transformer to convert the geometry to the target CRS.
        unit (str): The unit of the area. Default is "sqm". Options are "sqm", "sqft"

    Example:
        >>> from pyufunc import calc_area_from_wkt_geometry
        >>> from pyproj import Transformer
        >>> wkt_geometry = "POLYGON ((-74.006 40.712, -74.006 40.712, -74.006 40.712, -74.006 40.712))"
        >>> calc_area_from_wkt_geometry(wkt_geometry, unit="sqm")

    Return:
        float: The area of the geometry in specified unit.

    """
    import_package("shapely", verbose=False)
    import_package("pyproj", verbose=False)
    import shapely
    from pyproj import Transformer

    # TDD
    if unit not in ["sqm", "sqft"]:
        raise ValueError("unit must be one of ['sqm', 'sqft']")

    geometry_shapely = shapely.from_wkt(wkt_geometry)

    # Set up a Transformer to convert from WGS 84 to UTM zone 18N (EPSG:32618)
    transformer = Transformer.from_crs(
        "EPSG:4326", "EPSG:32618", always_xy=True)

    # Transform the polygon's coordinates to UTM
    if isinstance(geometry_shapely, shapely.MultiPolygon):
        transformed_polygons = []
        for polygon in geometry_shapely.geoms:
            transformed_coords = [transformer.transform(
                x, y) for x, y in polygon.exterior.coords]
            transformed_polygons.append(
                shapely.Polygon(transformed_coords))
        transformed_geometry = shapely.MultiPolygon(
            transformed_polygons)
    else:
        transformed_coords = [transformer.transform(
            x, y) for x, y in geometry_shapely.exterior.coords]
        transformed_geometry = shapely.Polygon(transformed_coords)

    if unit == "sqm":
        if verbose:
            print("Area in sqm:")
        return transformed_geometry.area
    else:
        if verbose:
            print("Area in sqft:")
        return transformed_geometry.area * 10.7639104
