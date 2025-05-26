'''
##############################################################
# Created Date: Friday, May 2nd 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

import os
import http.client as httplib
import urllib.parse as urlparse
import base64

_url = "www.overpass-api.de/api/interpreter"
# alternatives: overpass.kumi.systems/api/interpreter, sumo.dlr.de/osm/api/interpreter


def _readCompressed(conn, urlpath, query, filename):
    conn.request("POST", f"/{urlpath}", f"""
    <osm-script timeout="240" element-limit="1073741824">
    <union>
       {query}
       <recurse type="node-relation" into="rels"/>
       <recurse type="node-way"/>
       <recurse type="way-relation"/>
    </union>
    <union>
       <item/>
       <recurse type="way-node"/>
    </union>
    <print mode="body"/>
    </osm-script>""")
    response = conn.getresponse()
    # print(response.status, response.reason)
    if response.status == 200:
        print('valid responses got from API server.')
        print('receiving data...')
        with open(filename, "wb") as out:
            out.write(response.read())
        print(f'map data has been written to {filename}')


def get_osm_by_relation_id(relation_id, output_filepath='map.osm', url=_url) -> bool:
    """Downloads OpenStreetMap (OSM) data for a specified region using the Overpass API.

    This function queries the Overpass API for a given OSM relation ID, retrieves
    the corresponding map data, and saves it to a local file.

    Args:
        relation_id (int): The OSM relation ID for the area to be queried.
        output_filepath (str): The path where the downloaded OSM data will be saved.
            Defaults to 'map.osm'.
        url (str): The URL of the Overpass API endpoint. Defaults to 'www.overpass-api.de/api/interpreter'.

    See Also:
        SUMO Documentation: https://github.com/eclipse-sumo/sumo/blob/main/tools/osmGet.py
        osm2gmns Documentation: https://github.com/jiawlu/OSM2GMNS/blob/main/osm2gmns/downloader.py

    Example:
        >>> import pyufunc as pf
        >>> relation_id = 123456789  # Example relation ID (Get this from OSM)
        >>> pf.get_osm_by_relation_id(relation_id, output_filepath='my_map.osm')

    Returns:
        bool: True if the data was successfully downloaded and saved, False otherwise.
    """

    file_name, file_extension = os.path.splitext(output_filepath)
    if not file_extension:
        print(f'WARNING: no file extension in output_filepath {output_filepath}, '
              f'output_filepath is changed to {file_name}.osm')
        output_filepath = f'{file_name}.osm'
    elif file_extension not in ['.osm', '.xml']:
        print(f'WARNING: the file extension in output_filepath {output_filepath} is not supported, '
              f'output_filepath is changed to {file_name}.osm')
        output_filepath = f'{file_name}.osm'

    if "http" in url:
        url = urlparse.urlparse(url)
    else:
        url = urlparse.urlparse(f"https://{url}")
    if os.environ.get("https_proxy") is not None:
        headers = {}
        proxy_url = urlparse.urlparse(os.environ.get("https_proxy"))
        if proxy_url.username and proxy_url.password:
            auth = f'{proxy_url.username}:{proxy_url.password}'
            headers['Proxy-Authorization'] = f'Basic {base64.b64encode(auth)}'
        conn = httplib.HTTPSConnection(proxy_url.hostname, proxy_url.port)
        conn.set_tunnel(url.hostname, 443, headers)
    else:
        if url.scheme == "https":
            conn = httplib.HTTPSConnection(url.hostname, url.port)
        else:
            conn = httplib.HTTPConnection(url.hostname, url.port)

    if relation_id < 3600000000:
        relation_id += 3600000000
    _readCompressed(conn, url.path, f'<area-query ref="{relation_id}"/>', output_filepath)
    conn.close()


def extract_bbox_coordinates(bbox: str | tuple | list) -> tuple[float]:
    """Extracts bounding box coordinates from a string, tuple, or list.

    Args:
        bbox (str | tuple | list): Bounding box coordinates in the format
            "min_latitude, min_longitude, max_latitude, max_longitude" or
            (min_latitude, min_longitude, max_latitude, max_longitude).

    See Also:
        SUMO Documentation: https://github.com/eclipse-sumo/sumo/blob/main/tools/osmGet.py

    Example:
        >>> bbox = (-122.4194, 37.7749, -122.3894, 37.8049)
        >>> import pyufunc as pf
        >>> pf.extract_bbox_coordinates(bbox)
        (37.7749, -122.4194, 37.8049, -122.3894)

    Returns:
        tuple: A tuple containing the coordinates (west, south, east, north).
    """
    if isinstance(bbox, (tuple, list)) and len(bbox) == 4:
        west, south, east, north = [float(val) for val in bbox]
    elif isinstance(bbox, str):
        try:
            return tuple(float(val) for val in bbox.split(','))
        except ValueError as e:
            raise ValueError("bbox string must be in the format 'min_latitude,min_longitude,max_latitude,max_longitude'") from e
    else:
        raise TypeError("bbox must be a tuple/list of 4 coordinates or a string in the "
                        "format 'min_latitude,min_longitude,max_latitude,max_longitude'")

    if south > north or west > east or south < -90 or north > 90 or west < -180 or east > 180:
        raise Exception("Invalid geo-coordinates in bbox. "
                        "Please check the values in sequence: "
                        "west, south, east, north (min_lon, min_lat, max_lon, max_lat).")
    return (west, south, east, north)


def get_osm_by_bbox(bbox: str | tuple | list, output_filepath='map.osm', url=_url) -> bool:
    """Downloads OpenStreetMap (OSM) data for a specified bounding box using the Overpass API.

    This function queries the Overpass API for a given bounding box, retrieves
    the corresponding map data, and saves it to a local file.

    Args:
        bbox (tuple): A tuple containing the bounding box coordinates in the format
            (min_latitude, min_longitude, max_latitude, max_longitude).
        output_filepath (str): The path where the downloaded OSM data will be saved.
            Defaults to 'map.osm'.
        url (str): The URL of the Overpass API endpoint. Defaults to 'www.overpass-api.de/api/interpreter'.

    Example:
        >>> import pyufunc as pf
        >>> bbox = (-122.4194, 37.7749, -122.3894, 37.8049)  # Example bounding box:
        >>> pf.get_osm_by_bbox(bbox, output_filepath='my_map.osm')

    Returns:
        bool: True if the data was successfully downloaded and saved, False otherwise.
    """
    west, south, east, north = extract_bbox_coordinates(bbox)

    file_name, file_extension = os.path.splitext(output_filepath)
    if not file_extension:
        print(f'WARNING: no file extension in output_filepath {output_filepath}, '
              f'output_filepath is changed to {file_name}.osm')
        output_filepath = f'{file_name}.osm'
    elif file_extension not in ['.osm', '.xml']:
        print(f'WARNING: the file extension in output_filepath {output_filepath} is not supported, '
              f'output_filepath is changed to {file_name}.osm')
        output_filepath = f'{file_name}.osm'

    if "http" in url:
        url = urlparse.urlparse(url)
    else:
        url = urlparse.urlparse(f"https://{url}")
    if os.environ.get("https_proxy") is not None:
        headers = {}
        proxy_url = urlparse.urlparse(os.environ.get("https_proxy"))
        if proxy_url.username and proxy_url.password:
            auth = f'{proxy_url.username}:{proxy_url.password}'
            headers['Proxy-Authorization'] = f'Basic {base64.b64encode(auth)}'
        conn = httplib.HTTPSConnection(proxy_url.hostname, proxy_url.port)
        conn.set_tunnel(url.hostname, 443, headers)
    else:
        if url.scheme == "https":
            conn = httplib.HTTPSConnection(url.hostname, url.port)
        else:
            conn = httplib.HTTPConnection(url.hostname, url.port)

    _readCompressed(conn, url.path, f'<bbox-query n="{north}" s="{south}" w="{west}" e="{east}"/>', output_filepath)
    conn.close()


if __name__ == "__main__":
    relation_id = 128628
    bbox = (-122.4194, 37.7749, -122.3894, 37.8049)  # Example bounding box
    # get_osm_by_relation_id(relation_id, output_filepath='map.osm')
    get_osm_by_bbox(bbox, output_filepath='map.osm')
