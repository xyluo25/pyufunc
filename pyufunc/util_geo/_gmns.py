
# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, September 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
# GMNS: General Modeling Network Specification
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING, Any
import os
from dataclasses import dataclass, field, asdict, fields
from multiprocessing import Pool

from pyufunc.util_magic._func_time_decorator import func_time
from pyufunc.util_pathio._path import path2linux
from pyufunc.util_magic._dependency_requires_decorator import requires
from pyufunc.util_magic._import_package import import_package
from pyufunc.pkg_configs import config_gmns
from pyufunc.util_data_processing._dataclass import dataclass_extend, dataclass_from_dict

import pandas as pd

if TYPE_CHECKING:
    import shapely
    from tqdm import tqdm
    from pyproj import Transformer

__all__ = ['Node', 'Link', 'POI', 'Zone', 'Agent',
           'read_node', 'read_poi', 'read_link', 'read_zone']


@dataclass
class Node:
    """A node in the network.

    Attributes:
        id: The node ID.
        x_coord: The x coordinate of the node.
        y_coord: The y coordinate of the node.
        production: The production of the node.
        attraction: The attraction of the node.
        is_boundary: The boundary flag of the node. = 1 (current node is boundary node)
        zone_id: The zone ID. default == -1, only three conditions to become an activity node
                1) POI node, 2) is_boundary node(freeway),  3) residential in activity_type
        poi_id: The POI ID of the node. default = -1; to be assigned to a POI ID after reading poi.csv
        activity_type: The activity type of the node. provided from osm2gmns such as motoway, residential, ...
        geometry: The geometry of the node. based on wkt format.
        _zone_id: The zone ID. default == -1,
                this will be assigned if field zone_id exists in the node.csv and is not empty
    """
    id: int = 0
    x_coord: float = -1
    y_coord: float = -1
    production: float = 0
    attraction: float = 0
    # is_boundary: int = 0
    # ctrl_type: int = -1
    zone_id: int | None = None
    # poi_id: int = -1
    # activity_type: str = ''
    geometry: str = ''
    _zone_id: int = -1

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return asdict(self)

    def to_networkx(self) -> tuple:
        # covert to networkx node
        # networkx.add_nodes_from([(id, attr_dict), ])
        return (self.id, self.as_dict())


@dataclass
class POI:
    """A POI in the network.

    Attributes:
        id      : The POI ID.
        x_coord : The x coordinate of the POI.
        y_coord : The y coordinate of the POI.
        count   : The count of the POI. Total POI values for this POI node or POI zone
        area    : The area of the POI. Total area of polygon for this POI zone. unit is square meter
        building: The type of the POI. Default is empty string
        geometry: The polygon of the POI. based on wkt format. Default is empty string
        zone_id : The zone ID. mapping from zone
    """

    id: int = 0
    x_coord: float = 0
    y_coord: float = 0
    count: int = 1
    building: str = ""
    amenity: str = ""
    centroid: str = ""
    area: str = ""
    trip_rate: dict = field(default_factory=dict)
    geometry: str = ''
    zone_id: int = -1

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return asdict(self)

    def to_networkx(self) -> tuple:
        # convert to networkx node
        # networkx.add_nodes_from([(id, attr_dict), ])
        return (self.id, self.as_dict())


@dataclass
class Zone:
    """A zone in the network.

    Attributes:
        id              : The zone ID.
        name            : The name of the zone.
        x_coord      : The centroid x coordinate of the zone.
        y_coord      : The centroid y coordinate of the zone.
        centroid        : The centroid of the zone. (x, y) based on wkt format
        x_max           : The max x coordinate of the zone.
        x_min           : The min x coordinate of the zone.
        y_max           : The max y coordinate of the zone.
        y_min           : The min y coordinate of the zone.
        node_id_list    : Node IDs which belong to this zone.
        poi_id_list     : The POIs which belong to this zone.
        production      : The production of the zone.
        attraction      : The attraction of the zone.
        production_fixed: The fixed production of the zone (implement different models).
        attraction_fixed: The fixed attraction of the zone (implement different models).
        geometry        : The geometry of the zone. based on wkt format
    """

    id: int = 0
    name: str = ''
    x_coord: float = 0
    y_coord: float = 0
    centroid: str = ""
    x_max: float = 0
    x_min: float = 0
    y_max: float = 0
    y_min: float = 0
    node_id_list: list = field(default_factory=list)
    poi_id_list: list = field(default_factory=list)
    production: float = 0
    attraction: float = 0
    production_fixed: float = 0
    attraction_fixed: float = 0
    geometry: str = ''

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return asdict(self)

    # @property
    # def as_dict(self):
    #     return asdict(self)


@dataclass
class Agent:
    """An agent in the network.

    Attributes:
        id: The agent ID. default = 0
        agent_type: The agent type. default = ''
        o_zone_id: The origin zone ID. default = 0
        d_zone_id: The destination zone ID. default = 0
        o_zone_name: The origin zone name. default = ''
        d_zone_name: The destination zone name. default = ''

        o_node_id: The origin node ID. default = 0
        d_node_id: The destination node ID. default = 0

        path_node_seq_no_list: The path node sequence number list. default = []
        path_link_seq_no_list: The path link sequence number list. default = []
        path_cost: The path cost. default = 0

        b_generated: The flag of whether the agent is generated. default = False
        b_complete_trip: The flag of whether the agent completes the trip. default = False

        geometry: The geometry of the agent. based on wkt format. default = ''
        departure_time: The departure time of the agent. unit is second. default = 0
    """

    id: int = 0
    agent_type: str = ''
    o_zone_id: int = 0
    d_zone_id: int = 0
    o_zone_name: str = ''
    d_zone_name: str = ''

    # some attributes to be assigned later
    o_node_id: int = 0
    d_node_id: int = 0
    path_node_seq: list = field(default_factory=list)
    path_link_seq: list = field(default_factory=list)
    path_cost = 0
    b_generated: bool = False
    b_complete_trip: bool = False
    geometry: str = ''
    departure_time: int = 0  # unit is second

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return asdict(self)


@dataclass
class Link:
    """A link in the network.

    Args:
        id: The link ID.
        name: The name of the link.
        from_node_id: The from node ID of the link.
        to_node_id: The to node ID of the link.
        length: The length of the link.
        lanes: The lanes of the link.
        dir_flag: The direction flag of the link.
        free_speed: The free speed of the link.
        free_speed_raw: The raw free speed of the link.
        capacity: The capacity of the link.
        link_type: The type of the link.
        mode_type: The mode type of the link. walk, bike, drive, transit, ...
        facility_type: The facility type of the link.
        geometry: The geometry of the link. based on wkt format.
        as_dict: The method to convert the link to a dictionary.
        to_networkx: The method to convert the link to a networkx edge tuple format.
            (from_node_id, to_node_id, attr_dict)
    """

    id: int = 0
    name: str = ""
    from_node_id: int = -1
    to_node_id: int = -1
    length: float = -1
    lanes: int = 0
    dir_flag: int = 1
    free_speed: float = 0
    free_speed_raw: str = ""
    capacity: float = 0
    link_type: int = -1
    facility_type: str = ""
    # link_type_name: str = ""
    geometry: str = ""
    mode_type: str = ""  # mode_type: walk, bike, drive, transit, in the column of allowed_uses

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Key {key} not found in {self.__class__.__name__}")

    def as_dict(self):
        return {f.name: getattr(self, f.name) for f in fields(self)}

    def to_networkx(self) -> tuple:
        # convert to networkx edge
        # networkx.add_edges_from([(from_node_id, to_node_id, attr_dict), ])
        return (self.from_node_id, self.to_node_id, {**self.as_dict(), **{"weight": self.length}})


@requires("shapely", verbose=False)
def _create_node_from_dataframe(df_node: pd.DataFrame) -> dict[int, Node]:
    """Create Node from df_node.

    Args:
        df_node (pd.DataFrame): the dataframe of node from node.csv

    Returns:
        dict[int, Node]: a dict of nodes.{node_id: Node}
    """

    import_package("shapely", verbose=False)
    import shapely

    # Reset index to avoid index error
    df_node = df_node.reset_index(drop=True)
    col_names = df_node.columns.tolist()

    if "node_id" in col_names:
        col_names.remove("node_id")

    # get node dataclass fields
    # Get the list of attribute names
    node_attr_names = [f.name for f in fields(Node)]

    # check difference between node_attr_names and col_names
    diff = list(set(col_names) - set(node_attr_names))

    # create attributes for node class if diff is not empty
    if diff:
        diff_attr = [(val, str, "") for val in diff]
        Node_ext = dataclass_extend(Node, diff_attr)
    else:
        Node_ext = Node

    node_dict = {}
    for i in range(len(df_node)):
        try:
            # check whether zone_id field in node.csv or not
            # if zone_id field exists and is not empty, assign it to _zone_id
            try:
                _zone_id = int(df_node.loc[i, 'zone_id'])

                # check if _zone is none or empty, assign -1
                if pd.isna(_zone_id) or not _zone_id:
                    _zone_id = -1

            except Exception:
                _zone_id = -1

            # get node id
            node_id = int(df_node.loc[i, 'node_id'])
            x_coord = float(df_node.loc[i, 'x_coord'])
            y_coord = float(df_node.loc[i, 'y_coord'])

            node = Node_ext()

            for col in col_names:
                setattr(node, col, df_node.loc[i, col])

            node.id = node_id
            node._zone_id = _zone_id
            node.geometry = shapely.Point(x_coord, y_coord)

            node_dict[node_id] = asdict(node)

        except Exception as e:
            raise Exception(f"  : Unable to create node: {node_id}, error: {e}")

    return node_dict


@requires("shapely", "pyproj", verbose=False)
def _create_poi_from_dataframe(df_poi: pd.DataFrame) -> dict[int, POI]:
    """Create POI from df_poi.

    Args:
        df_poi (pd.DataFrame): the dataframe of poi from poi.csv

    Returns:
        dict[int, POI]: a dict of POIs.{poi_id: POI}
    """
    import_package("shapely", verbose=False)
    import_package("pyproj", verbose=False)
    import shapely
    from pyproj import Transformer

    df_poi = df_poi.reset_index(drop=True)
    col_names = df_poi.columns.tolist()

    if "poi_id" in col_names:
        col_names.remove("poi_id")

    # get node dataclass fields
    # Get the list of attribute names
    poi_attr_names = [f.name for f in fields(POI)]

    # check difference between node_attr_names and col_names
    diff = list(set(col_names) - set(poi_attr_names))

    # create attributes for node class if diff is not empty
    if diff:
        diff_attr = [(val, Any, "") for val in diff]
        POI_ext = dataclass_extend(POI, diff_attr)
    else:
        POI_ext = POI

    poi_dict = {}

    for i in range(len(df_poi)):
        try:
            centroid = shapely.from_wkt(df_poi.loc[i, 'centroid'])

            # check if area is empty or not
            area = df_poi.loc[i, 'area']
            if pd.isna(area) or not area:
                geometry_shapely = shapely.from_wkt(df_poi.loc[i, 'geometry'])

                # Set up a Transformer to convert from WGS 84 to UTM zone 18N (EPSG:32618)
                transformer = Transformer.from_crs(
                    "EPSG:4326", "EPSG:32618", always_xy=True)

                # Transform the polygon's coordinates to UTM
                transformed_coords = [transformer.transform(
                    x, y) for x, y in geometry_shapely.exterior.coords]
                transformed_polygon = shapely.Polygon(transformed_coords)

                # square meters
                area_sqm = transformed_polygon.area

                # square feet
                # area = area_sqm * 10.7639104

                area = area_sqm

            elif area > 90000:
                area = 0
            else:
                pass

            # get poi id
            poi_id = int(df_poi.loc[i, 'poi_id'])

            poi = POI_ext()

            for col in col_names:
                setattr(poi, col, df_poi.loc[i, col])

            poi.id = poi_id
            poi.x_coord = centroid.x
            poi.y_coord = centroid.y
            poi.area = area

            poi_dict[poi_id] = asdict(poi)
        except Exception as e:
            raise Exception(f"  : Unable to create poi: {poi_id}, error: {e}")
    return poi_dict


@requires("shapely", verbose=False)
def _create_zone_from_dataframe_by_geometry(df_zone: pd.DataFrame) -> dict[int, Zone]:
    """Create Zone from df_zone.

    Args:
        df_zone (pd.DataFrame): the dataframe of zone from zone.csv, the required fields are: [zone_id, geometry]

    Returns:
        dict[int, Zone]: a dict of Zones.{zone_id: Zone}
    """

    import_package("shapely", verbose=False)
    import shapely

    df_zone = df_zone.reset_index(drop=True)
    col_names = df_zone.columns.tolist()

    if "zone_id" in col_names:
        col_names.remove("zone_id")

    # get node dataclass fields
    # Get the list of attribute names
    zone_attr_names = [f.name for f in fields(Zone)]

    # check difference between node_attr_names and col_names
    diff = list(set(col_names) - set(zone_attr_names))

    # create attributes for node class if diff is not empty
    if diff:
        diff_attr = [(val, Any, "") for val in diff]
        Zone_ext = dataclass_extend(Zone, diff_attr)
    else:
        Zone_ext = Zone

    zone_dict = {}

    for i in range(len(df_zone)):
        try:
            zone_id = df_zone.loc[i, 'zone_id']
            zone_geometry = df_zone.loc[i, 'geometry']

            zone_geometry_shapely = shapely.from_wkt(zone_geometry)
            centroid_wkt = zone_geometry_shapely.centroid.wkt
            x_coord = zone_geometry_shapely.centroid.x
            y_coord = zone_geometry_shapely.centroid.y

            zone = Zone_ext()

            for col in col_names:
                setattr(zone, col, df_zone.loc[i, col])

            zone.id = zone_id
            zone.name = zone_id
            zone.x_coord = x_coord
            zone.y_coord = y_coord
            zone.centroid = centroid_wkt
            zone.x_min = zone_geometry_shapely.bounds[0]
            zone.y_min = zone_geometry_shapely.bounds[1]
            zone.x_max = zone_geometry_shapely.bounds[2]
            zone.y_max = zone_geometry_shapely.bounds[3]

            # save zone to zone_dict
            zone_dict[zone_id] = asdict(zone)
        except Exception as e:
            raise Exception(f"  : Unable to create zone: {zone_id}, error: {e}")
    return zone_dict


@requires("shapely", verbose=False)
def _create_zone_from_dataframe_by_centroid(df_zone: pd.DataFrame) -> dict[int, Zone]:
    """Create Zone from df_zone.

    Args:
        df_zone (pd.DataFrame): the dataframe of zone from zone.csv, the required fields are: [zone_id, geometry]

    Returns:
        dict[int, Zone]: a dict of Zones.{zone_id: Zone}
    """

    import_package("shapely", verbose=False)
    import shapely

    df_zone = df_zone.reset_index(drop=True)
    col_names = df_zone.columns.tolist()

    if "zone_id" in col_names:
        col_names.remove("zone_id")

    # get node dataclass fields
    # Get the list of attribute names
    zone_attr_names = [f.name for f in fields(Zone)]

    # check difference between node_attr_names and col_names
    diff = list(set(col_names) - set(zone_attr_names))

    # create attributes for node class if diff is not empty
    if diff:
        diff_attr = [(val, Any, "") for val in diff]
        Zone_ext = dataclass_extend(Zone, diff_attr)
    else:
        Zone_ext = Zone

    zone_dict = {}

    for i in range(len(df_zone)):
        try:
            zone_id = df_zone.loc[i, 'zone_id']
            x_coord = df_zone.loc[i, 'x_coord']
            y_coord = df_zone.loc[i, 'y_coord']

            # load zone geometry
            try:
                zone_geometry = df_zone.loc[i, 'geometry']
            except Exception:
                zone_geometry = ""

            zone_centroid_shapely = shapely.Point(x_coord, y_coord)
            centroid_wkt = zone_centroid_shapely.wkt

            zone = Zone_ext()

            for col in col_names:
                setattr(zone, col, df_zone.loc[i, col])

            zone.id = zone_id
            zone.name = zone_id
            zone.centroid = centroid_wkt
            zone.geometry = zone_geometry

            # save zone to zone_dict
            zone_dict[zone_id] = asdict(zone)
        except Exception as e:
            raise Exception(f"  : Unable to create zone: {zone_id}, error: {e}")
    return zone_dict


def _create_link_from_dataframe(df_link: pd.DataFrame) -> dict[int, Zone]:
    """Create Link from df_link.

    Args:
        df_link (pd.DataFrame): dataframe of link from link.csv

    Returns:
        dict[int, Zone]: a dict of Link.{link_id: Link}
    """

    df_link = df_link.reset_index(drop=True)
    col_names = df_link.columns.tolist()

    if "link_id" in col_names:
        col_names.remove("link_id")

    if "allowed_uses" in col_names:
        col_names.remove("allowed_uses")

    # get node dataclass fields
    # Get the list of attribute names
    link_attr_names = [f.name for f in fields(Link)]

    # check difference between node_attr_names and col_names
    diff = list(set(col_names) - set(link_attr_names))

    # create attributes for node class if diff is not empty
    if diff:
        diff_attr = [(val, Any, "") for val in diff]
        Link_ext = dataclass_extend(Link, diff_attr)
    else:
        Link_ext = Link

    link_dict = {}
    for i in range(len(df_link)):
        try:
            link_id = df_link.loc[i, 'link_id']

            link = Link_ext()

            # assign values to link attributes
            for col in col_names:
                setattr(link, col, df_link.loc[i, col])

            # assign additional values to link attributes
            link.id = link_id
            link.mode_type = df_link.loc[i, 'allowed_uses']

            # save link to link_dict
            link_dict[link_id] = asdict(link)

        except Exception as e:
            raise Exception(f"Error: Unable to create link {link_id}: error: {e}")

    return link_dict

# main functions for reading node, poi, link, zone files and network


@func_time
@requires("tqdm", verbose=False)
def read_node(node_file: str = "", cpu_cores: int = 1, verbose: bool = False) -> dict[int: Node]:
    """Read node.csv file and return a dict of nodes.

    Args:
        node_file (str, optional): node file path. Defaults to "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to 1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: File: {node_file} does not exist.

    Returns:
        dict: a dict of nodes.

    Examples:
        >>> node_dict = read_node(node_file = r"../dataset/ASU/node.csv")
        >>> node_dict[1]
        Node(id=1, zone_id=0, x_coord=0.0, y_coord=0.0, is_boundary=0, geometry='POINT (0 0)',...)

        # if node_file does not exist, raise error
        >>> node_dict = read_node(node_file = r"../dataset/ASU/node.csv")
        FileNotFoundError: File: ../dataset/ASU/node.csv does not exist.
    """
    import_package("tqdm", verbose=False)
    from tqdm import tqdm

    # convert path to linux path
    node_file = path2linux(node_file)

    # check if node_file exists
    if not os.path.exists(node_file):
        raise FileNotFoundError(f"File: {node_file} does not exist.")

    # read node.csv with specified columns and chunksize for iterations
    node_required_cols = config_gmns["node_fields"]
    chunk_size = config_gmns["data_chunk_size"]

    # read first two rows to check whether required fields are in node.csv
    df_node_2rows = pd.read_csv(node_file, nrows=2)
    col_names = df_node_2rows.columns.tolist()

    if "zone_id" in col_names and "zone_id" not in node_required_cols:
        node_required_cols.append("zone_id")

    if verbose:
        print(f"  : Reading node.csv with specified columns: {node_required_cols} \
                    \n    and chunksize {chunk_size} for iterations...")

    try:
        # Get total rows in poi.csv and calculate total chunks
        total_rows = sum(1 for _ in open(node_file)) - 1  # Exclude header row
        total_chunks = total_rows // chunk_size + 1
        df_node_chunk = pd.read_csv(
            node_file, usecols=node_required_cols, chunksize=chunk_size)
    except Exception as e:
        raise Exception(f"Error: Unable to read node.csv file for: {e}")

    if verbose:
        print(f"  : Parallel creating Nodes using Pool with {cpu_cores} CPUs. Please wait...")

    node_dict_final = {}

    # Parallel processing using Pool
    with Pool(cpu_cores) as pool:
        # results = pool.map(_create_node_from_dataframe, df_node_chunk)
        results = list(
            tqdm(pool.imap(_create_node_from_dataframe, df_node_chunk), total=total_chunks))
        pool.close()
        pool.join()

    # results = process_map(_create_node_from_dataframe, df_node_chunk, max_workers=cpu_cores)

    for node_dict in results:
        node_dict_final.update(node_dict)

    if verbose:
        print(f"  : Successfully loaded node.csv: {len(node_dict_final)} Nodes loaded.")

    node_dict_final = {k: dataclass_from_dict("Node", v) for k, v in node_dict_final.items()}

    return node_dict_final


@func_time
@requires("tqdm", verbose=False)
def read_poi(poi_file: str = "", cpu_cores: int = 1, verbose: bool = False) -> dict[int: POI]:
    """Read poi.csv file and return a dict of POIs.

    Args:
        poi_file (str): The poi.csv file path. default is "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to 1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: if poi_file does not exist.

    Returns:
        dict: A dict of POIs.

    Examples:
        >>> poi_dict = read_poi(poi_file = r"../dataset/ASU/poi.csv")
        >>> poi_dict[1]
        POI(id=1, x_coord=0.0, y_coord=0.0, area=[0, 0.0], poi_type='residential', geometry='POINT (0 0)')

        # if poi_file does not exist, raise error
        >>> poi_dict = read_poi(poi_file = r"../dataset/ASU/poi.csv")
        FileNotFoundError: File: ../dataset/ASU/poi.csv does not exist.

    """
    import_package("tqdm", verbose=False)
    from tqdm import tqdm

    # convert path to linux path
    poi_file = path2linux(poi_file)

    # check if poi_file exists
    if not os.path.exists(poi_file):
        raise FileNotFoundError(f"File: {poi_file} does not exist.")

    # Read poi.csv with specified columns and chunksize for iterations
    poi_required_cols = config_gmns["poi_fields"]
    chunk_size = config_gmns["data_chunk_size"]

    if verbose:
        print(f"  : Reading poi.csv with specified columns: {poi_required_cols} \
                    \n    and chunksize {chunk_size} for iterations...")
    try:
        # Get total rows in poi.csv and calculate total chunks
        total_rows = sum(1 for _ in open(poi_file)) - 1  # Exclude header row
        total_chunks = total_rows // chunk_size + 1

        df_poi_chunk = pd.read_csv(
            poi_file, usecols=poi_required_cols, chunksize=chunk_size, encoding='utf-8')
    except Exception:
        df_poi_chunk = pd.read_csv(
            poi_file, usecols=poi_required_cols, chunksize=chunk_size, encoding='latin-1')

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating POIs using Pool with {cpu_cores} CPUs. Please wait...")

    poi_dict_final = {}

    with Pool(cpu_cores) as pool:
        # results = pool.map(_create_poi_from_dataframe, df_poi_chunk)
        results = list(
            tqdm(pool.imap(_create_poi_from_dataframe, df_poi_chunk), total=total_chunks))
        pool.close()
        pool.join()

    # results = process_map(_create_poi_from_dataframe, df_poi_chunk, max_workers=cpu_cores)

    for poi_dict in results:
        poi_dict_final.update(poi_dict)

    if verbose:
        print(f"  : Successfully loaded poi.csv: {len(poi_dict_final)} POIs loaded.")

    poi_dict_final = {k: dataclass_from_dict("POI", v) for k, v in poi_dict_final.items()}

    return poi_dict_final


@func_time
def read_zone_by_geometry(zone_file: str = "", cpu_cores: int = 1, verbose: bool = False) -> dict[int: Zone]:
    """Read zone.csv file and return a dict of Zones.

    Raises:
        FileNotFoundError: _description_
        FileNotFoundError: _description_

    Args:
        zone_file (str, optional): the input zone file path. Defaults to "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to 1.
        verbose (bool, optional): print processing information. Defaults to False.

    Returns:
        dict: the result dictionary of Zones. {zone_id: Zone}
    """

    # convert path to linux path
    zone_file = path2linux(zone_file)

    # check if zone_file exists
    if not os.path.exists(zone_file):
        raise FileNotFoundError(f"File: {zone_file} does not exist.")

    # load default settings for zone required fields and chunk size
    zone_required_cols = config_gmns["zone_geometry_fields"]
    chunk_size = config_gmns["data_chunk_size"]

    if verbose:
        print(f"  : Reading zone.csv with specified columns: {zone_required_cols} \
                \n   and chunksize {chunk_size} for iterations...")

    # check whether required fields are in zone.csv
    df_zone = pd.read_csv(zone_file, nrows=1)
    col_names = df_zone.columns.tolist()
    for col in zone_required_cols:
        if col not in col_names:
            raise FileNotFoundError(f"Required column: {col} is not in zone.csv. \
                Please make sure you have {zone_required_cols} in zone.csv.")

    # load zone.csv with specified columns and chunksize for iterations
    df_zone_chunk = pd.read_csv(
        zone_file, usecols=zone_required_cols, chunksize=chunk_size)

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating Zones using Pool with {cpu_cores} CPUs. Please wait...")

    zone_dict_final = {}

    with Pool(cpu_cores) as pool:
        results = pool.map(
            _create_zone_from_dataframe_by_geometry, df_zone_chunk)
        pool.close()
        pool.join()

    for zone_dict in results:
        zone_dict_final.update(zone_dict)

    if verbose:
        print(f"  : Successfully loaded zone.csv: {len(zone_dict_final)} Zones loaded.")

    zone_dict_final = {k: dataclass_from_dict("POI", v) for k, v in zone_dict_final.items()}

    return zone_dict_final


@func_time
def read_zone_by_centroid(zone_file: str = "", cpu_cores: int = 1, verbose: bool = False) -> dict[int: Zone]:
    """Read zone.csv file and return a dict of Zones.

    Args:
        zone_file (str, optional): the input zone file path. Defaults to "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to 1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: File: {zone_file} does not exist.
        FileNotFoundError: Required column: {col} is not in zone.csv. Please make sure zone_required_cols in zone.csv.

    Returns:
        dict: a dict of Zones.
    """

    # convert path to linux path
    zone_file = path2linux(zone_file)

    # check if zone_file exists
    if not os.path.exists(zone_file):
        raise FileNotFoundError(f"File: {zone_file} does not exist.")

    # load default settings for zone required fields and chunk size
    zone_required_cols = config_gmns["zone_centroid_fields"]
    chunk_size = config_gmns["data_chunk_size"]

    if verbose:
        print(f"  : Reading zone.csv with specified columns: {zone_required_cols} \
                \n   and chunksize {chunk_size} for iterations...")

    # check whether required fields are in zone.csv
    df_zone = pd.read_csv(zone_file, nrows=1)
    col_names = df_zone.columns.tolist()
    for col in zone_required_cols:
        if col not in col_names:
            raise FileNotFoundError(f"Required column: {col} is not in zone.csv. \
                Please make sure you have {zone_required_cols} in zone.csv.")

    # load zone.csv with specified columns and chunksize for iterations
    df_zone_chunk = pd.read_csv(
        zone_file, usecols=zone_required_cols, chunksize=chunk_size)

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating Zones using Pool with {cpu_cores} CPUs. Please wait...")

    zone_dict_final = {}

    with Pool(cpu_cores) as pool:
        results = pool.map(
            _create_zone_from_dataframe_by_centroid, df_zone_chunk)
        pool.close()
        pool.join()

    for zone_dict in results:
        zone_dict_final.update(zone_dict)

    if verbose:
        print(f"  : Successfully loaded zone.csv: {len(zone_dict_final)} Zones loaded.")

    zone_dict_final = {k: dataclass_from_dict("POI", v) for k, v in zone_dict_final.items()}

    return zone_dict_final


@func_time
@requires("tqdm", auto_install=True)
def read_link(link_file: str = "", cpu_cores: int = 1, verbose: bool = False) -> dict[int: Link]:
    """Read link.csv file and return a dict of Links.

    Args:
        link_file (str): The link.csv file path. default is "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to -1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: File: {link_file} does not exist.
        ValueError: cpu_cores should be integer, but got {type(cpu_cores)}

    Returns:
        dict: A dict of Links.

    Examples:
        >>> from pyufunc import gmns_read_link
        >>> link_dict = gmns_read_link(link_file = r"../dataset/ASU/link.csv")
        >>> link_dict[1]
        Link(id=1, name='A', from_node_id=1, to_node_id=2, length=0.0, lanes=1, dir_flag=1, free_speed=0.0,
        capacity=0.0, link_type=1, link_type_name='motorway', geometry='LINESTRING (0 0, 1 1)')
    """
    import_package("tqdm", verbose=False)
    from tqdm import tqdm

    # convert path to linux path
    link_file = path2linux(link_file)

    # check link file
    if not os.path.exists(link_file):
        raise FileNotFoundError(f"File: {link_file} does not exist.")

    # check cpu_cores
    if not isinstance(cpu_cores, int):
        raise ValueError(f"cpu_cores should be integer, but got {type(cpu_cores)}")

    if cpu_cores <= 0:
        cpu_cores = config_gmns["cpu_cores"]

    # Read link.csv with specified columns and chunksize for iterations
    link_required_cols = config_gmns["link_fields"]
    chunk_size = config_gmns["data_chunk_size"]

    if verbose:
        print(f"  : Reading link.csv with specified columns: {link_required_cols} \
                    \n    and chunksize {chunk_size} for iterations...")
    # Get total rows in poi.csv and calculate total chunks
    total_rows = sum(1 for _ in open(link_file)) - 1  # Exclude header row
    total_chunks = total_rows // chunk_size + 1
    try:
        df_link_chunk = pd.read_csv(
            link_file, usecols=link_required_cols, chunksize=chunk_size, encoding='utf-8')
    except Exception:
        df_link_chunk = pd.read_csv(
            link_file, usecols=link_required_cols, chunksize=chunk_size, encoding='latin-1')

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating Links using Pool with {cpu_cores} CPUs. Please wait...")

    link_dict_final = {}
    with Pool(cpu_cores) as pool:
        # results = pool.map(_create_link_from_dataframe, df_link_chunk)
        results = tqdm(pool.imap(_create_link_from_dataframe, df_link_chunk), total=total_chunks)
        pool.close()
        pool.join()

    for link_dict in results:
        print("link_dict: ", link_dict)
        link_dict_final.update(link_dict)

    if verbose:
        print(f"  : Successfully loaded link.csv: {len(link_dict_final)} Links loaded.")

    return link_dict_final


@func_time
def read_zone(zone_file: str = "", cpu_cores: int = -1, verbose: bool = False) -> dict[int: Zone]:
    """Read zone.csv file and return a dict of Zones.

    Args:
        zone_file (str, optional): the input zone file path. Defaults to "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to -1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: Error: File {zone_file} does not exist.
        ValueError: Error: cpu_cores must be an integer greater than 0.
        Exception: Error: Failed to read {zone_file}.

    Returns:
        dict: a dict of Zones.

    Examples:
        >>> from pyufunc import gmns_read_zone
        >>> zone_dict = gmns_read_zone(zone_file = r"../dataset/ASU/zone.csv")
        >>> zone_dict[1]
        Zone(id=1, name='1', centroid_x=0.0, centroid_y=0.0, centroid='POINT (0 0)', x_max=0.0,
        x_min=0.0, y_max=0.0, y_min=0.0, node_id_list=[], poi_id_list=[],
        production=0, attraction=0, production_fixed=0, attraction_fixed=0,
        geometry='POLYGON ((0 0, 1 1, 1 0, 0 0))')
    """

    # check zone_file, geometry or centroid?
    if not os.path.exists(zone_file):
        raise FileNotFoundError(f"Error: File {zone_file} does not exist.")

    # check inputs of cpu_cores
    if not isinstance(cpu_cores, int):
        raise ValueError("Error: cpu_cores must be an integer greater than 0.")

    # check available cpu cores
    if cpu_cores <= 0:
        cpu_cores = config_gmns["cpu_cores"]

    # load zone file column names
    zone_columns = []
    try:
        # 1 row, reduce memory and time
        zone_df = pd.read_csv(zone_file, nrows=1)
        zone_columns = zone_df.columns
    except Exception as e:
        raise Exception(f"Error: Failed to read {zone_file}.") from e

    # update geometry or centroid
    if set(config_gmns.get("zone_geometry_fields")).issubset(set(zone_columns)):
        zone_dict = read_zone_by_geometry(zone_file, cpu_cores, verbose)
    elif set(config_gmns.get("zone_centroid_fields")).issubset(set(zone_columns)):
        zone_dict = read_zone_by_centroid(zone_file, cpu_cores, verbose)
    else:
        zone_dict = {}
        print(f"Error: No valid zone fields in {zone_file}.", flush=True)
    return zone_dict
