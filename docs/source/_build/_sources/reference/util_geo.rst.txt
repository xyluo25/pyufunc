

.. _api.util_geo:

========
util_geo
========
.. currentmodule:: pyufunc

geo_distance
~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   calc_distance_on_unit_sphere
   calc_distance_on_unit_haversine
   find_k_nearest_points
   find_closest_point
   get_coordinates_from_geom
   proj_point_to_line

Coordinate Conversation
~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
    :toctree: api/

    cvt_wgs84_to_baidu09
    cvt_wgs84_to_gcj02
    cvt_gcj02_to_wgs84
    cvt_gcj02_to_baidu09
    cvt_baidu09_to_wgs84
    cvt_baidu09_to_gcj02

geo_circle
~~~~~~~~~~
.. autosummary::
   :toctree: api/

   create_circle_at_point_with_radius

geo_area
~~~~~~~~
.. autosummary::
   :toctree: api/

   calc_area_from_wkt_geometry

Download Elevation Tiff File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   download_elevation_tif_by

gmns_geo
~~~~~~~~
.. autosummary::
    :toctree: api/

    gmns_geo
    GMNSAgent
    GMNSNode
    GMNSLink
    GMNSPOI
    GMNSZone
    gmns_read_node
    gmns_read_link
    gmns_read_poi
    gmns_read_zone
    get_osm_place
