
# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, September 4th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
# GMNS: General Modeling Network Specification
##############################################################
from __future__ import annotations
from typing import TYPE_CHECKING
import os
from dataclasses import dataclass, field, asdict
from multiprocessing import Pool
from pyufunc.util_common._func_time_decorator import func_time
from pyufunc.util_pathio._path import path2linux
from pyufunc.util_common._dependency_requires_decorator import requires
from pyufunc.util_common._import_package import import_package
from pyufunc.pkg_configs import config_gmns

if TYPE_CHECKING:
    import pandas as pd
    import shapely

__all__ = ['Node', 'Link', 'POI', 'Zone', 'Agent',
           'read_node', 'read_poi', 'read_zone_by_geometry', 'read_zone_by_centroid']


@dataclass
class Node:
    """A node in the network.

    Args:
        id: The node ID.
        x_coord: The x coordinate of the node.
        y_coord: The y coordinate of the node.
        production: The production of the node.
        attraction: The attraction of the node.
        boundary_flag: The boundary flag of the node. = 1 (current node is boundary node)
        zone_id: The zone ID. default == -1, only three conditions to become an activity node
                1) POI node, 2) is_boundary node(freeway),  3) residential in activity_type
        poi_id: The POI ID of the node. default = -1; to be assigned to a POI ID after reading poi.csv
        activity_type: The activity type of the node. provided from osm2gmns such as motoway, residential, ...
        activity_location_tab: The activity location tab of the node.
        geometry: The geometry of the node. based on wkt format.
        as_dict: The method to convert the node to a dictionary.
        to_networkx: The method to convert the node to a networkx node tuple format. (id, attr_dict)
        _zone_id: store the zone_id for the node, default = -1,
            to be assigned if field zone_id exists in the node.csv and it is not empty
    """
    id: int = 0
    x_coord: float = 0
    y_coord: float = 0
    production: float = 0
    attraction: float = 0
    boundary_flag: int = 0
    zone_id: int = -1
    poi_id: int = -1
    activity_type: str = ''
    activity_location_tab: str = ''
    geometry: str = ''
    _zone_id: int = -1

    def as_dict(self):
        return asdict(self)
        # return self.__dict__

    def to_networkx(self) -> tuple:
        # covert to networkx node
        # networkx.add_nodes_from([(id, attr_dict), ])
        return (self.id, self.as_dict())


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
        capacity: The capacity of the link.
        link_type: The type of the link.
        link_type_name: The name of the link type.
        geometry: The geometry of the link. based on wkt format.
        as_dict: The method to convert the link to a dictionary.
        to_networkx: The method to convert the link to a networkx edge tuple format. (from_node_id, to_node_id, attr_dict)

    """

    id: int = 0
    name: str = ""
    from_node_id: int = -1
    to_node_id: int = -1
    length: float = -1
    lanes: int = -1
    dir_flag: int = 1
    free_speed: float = -1
    capacity: float = -1
    link_type: int = -1
    link_type_name: str = ""
    geometry: str = ""
    allowed_uses: str = ""
    from_biway: int = 1
    is_link: bool = True

    def as_dict(self):
        return asdict(self)
        # return self.__dict__

    def to_networkx(self) -> tuple:
        # convert to networkx edge
        # networkx.add_edges_from([(from_node_id, to_node_id, attr_dict), ])
        return (self.from_node_id, self.to_node_id, {**self.as_dict(), **{"weight": self.length}})


@dataclass
class POI:
    """A POI in the network.

    Args:
        id: The POI ID.
        x_coord: The x coordinate of the POI.
        y_coord: The y coordinate of the POI.
        count: The count of the POI. Total POI values for this POI node or POI zone
        area: The area of the POI. Total area of polygon for this POI zone. unit is square meter
        poi_type: The type of the POI. Default is empty string
        geometry: The polygon of the POI. based on wkt format. Default is empty string
        zone_id: The zone ID. mapping from zone
        as_dict: The method to convert the POI to a dictionary.
        to_networkx: The method to convert the POI to a networkx node tuple format. (id, attr_dict)
    """

    id: int = 0
    x_coord: float = 0
    y_coord: float = 0
    count: int = 1
    area: list = field(default_factory=list)
    poi_type: str = ''
    trip_rate: dict = field(default_factory=dict)
    geometry: str = ''
    zone_id: int = -1

    def as_dict(self):
        return asdict(self)
        # return self.__dict__

    def to_networkx(self) -> tuple:
        # convert to networkx node
        # networkx.add_nodes_from([(id, attr_dict), ])
        return (self.id, self.as_dict())


@dataclass
class Zone:
    """A zone in the network.

    Args:
        id: The zone ID.
        name: The name of the zone.
        centroid_x: The centroid x coordinate of the zone.
        centroid_y: The centroid y coordinate of the zone.
        centroid: The centroid of the zone. (x, y) based on wkt format
        x_max: The max x coordinate of the zone.
        x_min: The min x coordinate of the zone.
        y_max: The max y coordinate of the zone.
        y_min: The min y coordinate of the zone.
        node_id_list: Node IDs which belong to this zone.
        poi_id_list: The POIs which belong to this zone.
        production: The production of the zone.
        attraction: The attraction of the zone.
        production_fixed: The fixed production of the zone (implement different models).
        attraction_fixed: The fixed attraction of the zone (implement different models).
        geometry: The geometry of the zone. based on wkt format
        as_dict: The method to convert the zone to a dictionary.
    """

    id: int = 0
    name: str = ''
    centroid_x: float = 0
    centroid_y: float = 0
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

    def as_dict(self):
        return asdict(self)
        # return self.__dict__


@dataclass
class Agent:
    """An agent in the network.

    Args:
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
        as_dict: The method to convert the agent to a dictionary.
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

    def as_dict(self):
        return asdict(self)
        # return self.__dict__

# todo: read node, link and zone


def _create_node_from_dataframe(df_node: pd.DataFrame) -> dict[int, Node]:
    """Create Node from df_node.

    Args:
        df_node (pd.DataFrame): the dataframe of node from node.csv

    Returns:
        dict[int, Node]: a dict of nodes.{node_id: Node}
    """
    # Reset index to avoid index error
    df_node = df_node.reset_index(drop=True)

    print("df_node: ", df_node.head())

    node_dict = {}
    for i in range(len(df_node)):
        try:
            # check activity location tab
            activity_type = df_node.loc[i, 'activity_type']
            boundary_flag = df_node.loc[i, 'is_boundary']
            if activity_type in ["residential", "poi"]:
                activity_location_tab = activity_type
            elif boundary_flag == 1:
                activity_location_tab = "boundary"
            else:
                activity_location_tab = ''

            # check whether zone_id field in node.csv or not
            # if zone_id field exists and is not empty, assign it to __zone_id
            try:
                _zone_id = df_node.loc[i, 'zone_id']

                # check if _zone is none or empty, assign -1
                if pd.isna(_zone_id) or not _zone_id:
                    _zone_id = -1

            except Exception:
                _zone_id = -1

            node = Node(
                id=df_node.loc[i, 'node_id'],
                activity_type=activity_type,
                activity_location_tab=activity_location_tab,
                ctrl_type=df_node.loc[i, 'ctrl_type'],
                x_coord=df_node.loc[i, 'x_coord'],
                y_coord=df_node.loc[i, 'y_coord'],
                poi_id=df_node.loc[i, 'poi_id'],
                boundary_flag=boundary_flag,
                geometry=shapely.Point(df_node.loc[i, 'x_coord'], df_node.loc[i, 'y_coord']),
                _zone_id=_zone_id
            )
            node_dict[df_node.loc[i, 'node_id']] = node
        except Exception as e:
            print(f"  : Unable to create node: {df_node.loc[i, 'node_id']}, error: {e}")
    return node_dict


def _create_poi_from_dataframe(df_poi: pd.DataFrame) -> dict[int, POI]:
    """Create POI from df_poi.

    Args:
        df_poi (pd.DataFrame): the dataframe of poi from poi.csv

    Returns:
        dict[int, POI]: a dict of POIs.{poi_id: POI}
    """

    df_poi = df_poi.reset_index(drop=True)
    poi_dict = {}

    for i in range(len(df_poi)):
        try:
            centroid = shapely.from_wkt(df_poi.loc[i, 'centroid'])
            area = df_poi.loc[i, 'area']
            if area > 90000:
                area = 0
            poi = POI(
                id=df_poi.loc[i, 'poi_id'],
                x_coord=centroid.x,
                y_coord=centroid.y,
                area=[area, area * 10.7639104],  # square meter and square feet
                poi_type=df_poi.loc[i, 'building'] or "",
                geometry=df_poi.loc[i, "geometry"]
            )
            poi_dict[df_poi.loc[i, 'poi_id']] = poi
        except Exception as e:
            print(f"  : Unable to create poi: {df_poi.loc[i, 'poi_id']}, error: {e}")
    return poi_dict


def _create_zone_from_dataframe_by_geometry(df_zone: pd.DataFrame) -> dict[int, Zone]:
    """Create Zone from df_zone.

    Args:
        df_zone (pd.DataFrame): the dataframe of zone from zone.csv, the required fields are: [zone_id, geometry]

    Returns:
        dict[int, Zone]: a dict of Zones.{zone_id: Zone}
    """
    df_zone = df_zone.reset_index(drop=True)
    zone_dict = {}

    for i in range(len(df_zone)):
        try:
            zone_id = df_zone.loc[i, 'zone_id']
            zone_geometry = df_zone.loc[i, 'geometry']

            zone_geometry_shapely = shapely.from_wkt(zone_geometry)
            centroid_wkt = zone_geometry_shapely.centroid.wkt
            centroid_x = zone_geometry_shapely.centroid.x
            centroid_y = zone_geometry_shapely.centroid.y
            zone = Zone(
                id=zone_id,
                name=zone_id,
                centroid_x=centroid_x,
                centroid_y=centroid_y,
                centroid=centroid_wkt,
                x_max=zone_geometry_shapely.bounds[2],
                x_min=zone_geometry_shapely.bounds[0],
                y_max=zone_geometry_shapely.bounds[3],
                y_min=zone_geometry_shapely.bounds[1],
                node_id_list=[],
                poi_id_list=[],
                production=0,
                attraction=0,
                production_fixed=0,
                attraction_fixed=0,
                geometry=zone_geometry
            )

            zone_dict[zone_id] = zone
        except Exception as e:
            print(f"  : Unable to create zone: {zone_id}, error: {e}")
    return zone_dict


def _create_zone_from_dataframe_by_centroid(df_zone: pd.DataFrame) -> dict[int, Zone]:
    """Create Zone from df_zone.

    Args:
        df_zone (pd.DataFrame): the dataframe of zone from zone.csv, the required fields are: [zone_id, geometry]

    Returns:
        dict[int, Zone]: a dict of Zones.{zone_id: Zone}
    """
    df_zone = df_zone.reset_index(drop=True)
    zone_dict = {}

    for i in range(len(df_zone)):
        try:
            zone_id = df_zone.loc[i, 'zone_id']
            centroid_x = df_zone.loc[i, 'x_coord']
            centroid_y = df_zone.loc[i, 'y_coord']

            zone_centroid_shapely = shapely.Point(centroid_x, centroid_y)
            centroid_wkt = zone_centroid_shapely.wkt

            zone = Zone(
                id=zone_id,
                name=zone_id,
                centroid_x=centroid_x,
                centroid_y=centroid_y,
                centroid=centroid_wkt,
                node_id_list=[],
                poi_id_list=[],
                production=0,
                attraction=0,
                production_fixed=0,
                attraction_fixed=0,
            )

            zone_dict[zone_id] = zone
        except Exception as e:
            print(f"  : Unable to create zone: {zone_id}, error: {e}")
    return zone_dict


# main functions for reading node, poi, zone files and network

@func_time
@requires("pandas", "shapely")
def read_node(node_file: str = "", cpu_cores: int = -1, verbose: bool = False) -> dict[int: Node]:
    """Read node.csv file and return a dict of nodes.

    Args:
        node_file (str, optional): node file path. Defaults to "".
        cpu_cores (int, optional): number of cpu cores for parallel processing. Defaults to -1.
        verbose (bool, optional): print processing information. Defaults to False.

    Raises:
        FileNotFoundError: File: {node_file} does not exist.

    Returns:
        dict: a dict of nodes.

    Examples:
        >>> node_dict = read_node(node_file = r"../dataset/ASU/node.csv")
        >>> node_dict[1]
        Node(id=1, zone_id=0, x_coord=0.0, y_coord=0.0, boundary_flag=0, geometry='POINT (0 0)',...)

        # if node_file does not exist, raise error
        >>> node_dict = read_node(node_file = r"../dataset/ASU/node.csv")
        FileNotFoundError: File: ../dataset/ASU/node.csv does not exist.
    """

    import_package("pandas", verbose=False)
    import_package("shapely", verbose=False)
    import pandas as pd
    import shapely

    if verbose:
        print("  :Running on parallel processing, make sure you are running under if __name__ == '__main__': \n")

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

    if "zone_id" in col_names:
        node_required_cols.append("zone_id")

    if verbose:
        print(f"  : Reading node.csv with specified columns: {node_required_cols} \
                    \n    and chunksize {chunk_size} for iterations...")

    df_node_chunk = pd.read_csv(node_file, usecols=node_required_cols, chunksize=chunk_size)

    if verbose:
        print(f"  : Parallel creating Nodes using Pool with {cpu_cores} CPUs. Please wait...")
    node_dict_final = {}

    # Parallel processing using Pool
    with Pool(cpu_cores) as pool:
        results = pool.map(_create_node_from_dataframe, df_node_chunk)

    for node_dict in results:
        node_dict_final.update(node_dict)

    if verbose:
        print(f"  : Successfully loaded node.csv: {len(node_dict_final)} Nodes loaded.")
    return node_dict_final


@func_time
@requires("pandas", "shapely")
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
    import_package("pandas", verbose=False)
    import_package("shapely", verbose=False)
    import pandas as pd
    import shapely

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
        df_poi_chunk = pd.read_csv(poi_file, usecols=poi_required_cols, chunksize=chunk_size, encoding='utf-8')
    except Exception:
        df_poi_chunk = pd.read_csv(poi_file, usecols=poi_required_cols, chunksize=chunk_size, encoding='latin-1')

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating POIs using Pool with {cpu_cores} CPUs. Please wait...")
    poi_dict_final = {}

    with Pool(cpu_cores) as pool:
        results = pool.map(_create_poi_from_dataframe, df_poi_chunk)

    for poi_dict in results:
        poi_dict_final.update(poi_dict)

    if verbose:
        print(f"  : Successfully loaded poi.csv: {len(poi_dict_final)} POIs loaded.")

    return poi_dict_final


@func_time
@requires("pandas", "shapely")
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
        _type_: _description_
    """

    import_package("pandas", verbose=False)
    import_package("shapely", verbose=False)
    import pandas as pd
    import shapely

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
    df_zone_chunk = pd.read_csv(zone_file, usecols=zone_required_cols, chunksize=chunk_size)

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating Zones using Pool with {cpu_cores} CPUs. Please wait...")
    zone_dict_final = {}

    with Pool(cpu_cores) as pool:
        results = pool.map(_create_zone_from_dataframe_by_geometry, df_zone_chunk)

    for zone_dict in results:
        zone_dict_final.update(zone_dict)

    if verbose:
        print(f"  : Successfully loaded zone.csv: {len(zone_dict_final)} Zones loaded.")

    return zone_dict_final


@func_time
@requires("pandas", "shapely")
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

    import_package("pandas", verbose=False)
    import_package("shapely", verbose=False)
    import pandas as pd
    import shapely

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
    df_zone_chunk = pd.read_csv(zone_file, usecols=zone_required_cols, chunksize=chunk_size)

    # Parallel processing using Pool
    if verbose:
        print(f"  : Parallel creating Zones using Pool with {cpu_cores} CPUs. Please wait...")

    zone_dict_final = {}

    with Pool(cpu_cores) as pool:
        results = pool.map(_create_zone_from_dataframe_by_centroid, df_zone_chunk)

    for zone_dict in results:
        zone_dict_final.update(zone_dict)

    if verbose:
        print(f"  : Successfully loaded zone.csv: {len(zone_dict_final)} Zones loaded.")

    return zone_dict_final