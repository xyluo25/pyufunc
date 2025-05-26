'''
##############################################################
# Created Date: Thursday, March 27th 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''

import json
import os
import sys
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    import shapely
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.fs as fs
    import geopandas as gpd
    from geopandas import GeoDataFrame

from pyufunc.util_magic import requires, import_package


def download_overture_map(bbox: list[float] = None,
                          map_type: str = "buildings",
                          output_fmt: str = "geojson",
                          output_fname: str = ""):
    """
    Download Overture map data within a specified bounding box and theme type and save it in the specified format.

    Args:
        bbox (list[float]): Bounding box coordinates in the format [min_lon, min_lat, max_lon, max_lat].
        map_type (str): Type of map data to download. Options include
            'address', 'bathymetry', 'building', 'building_part', 'division', 'division_area',
            'division_boundary', 'place', 'segment', 'connector', 'infrastructure', 'land',
            'land_cover', 'land_use', 'water'
        output_fmt (str): Format of the output file. Options include "geojson", "geojsonseq" and "geoparquet".
        output_fname (str): Name of the output file. If not provided, a default name will be generated.

    Note:
        This function is adopted and modified from the Overture CLI tool: https://github.com/OvertureMaps/overturemaps-py

    See Also:
        overturemaps-py CLI tool for more details on the available map types and their usage.
        https://github.com/OvertureMaps/overturemaps-py

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame containing the Overture map data.
    """

    # check input parameters
    if not isinstance(bbox, (tuple, list)):
        raise ValueError("Bounding box must be a tuple or list.")

    if len(bbox) != 4:
        raise ValueError("Bounding box must contain 4 coordinates (min_lon, min_lat, max_lon, max_lat).")

    # check if output file name is provided, if not, return none
    if not output_fname:
        output_fname = sys.stdout

    reader = record_batch_reader(map_type, bbox)
    if reader is None:
        return

    with get_writer(output_fmt, output_fname, schema=reader.schema) as writer:
        while True:
            try:
                batch = reader.read_next_batch()
            except StopIteration:
                break
            if batch.num_rows > 0:
                writer.write_batch(batch)


@requires("pyarrow", verbose=False)
def get_writer(output_format, path, schema):

    import_package("pyarrow", verbose=False)
    import pyarrow.parquet as pq

    if output_format == "geojson":
        writer = GeoJSONWriter(path)
    elif output_format == "geojsonseq":
        writer = GeoJSONSeqWriter(path)
    elif output_format == "geoparquet":
        # Update the geoparquet metadata to remove the file-level bbox which
        # will no longer apply to this file. Since we cannot write the field at
        # the end, just remove it as it's optional. Let the per-row bounding
        # boxes do all the work.
        metadata = schema.metadata
        # extract geo metadata
        geo = json.loads(metadata[b"geo"])
        # the spec allows for multiple geom columns
        geo_columns = geo["columns"]
        if len(geo_columns) > 1:
            raise IOError("Expected single geom column but encountered multiple.")
        for geom_col_vals in geo_columns.values():
            # geom level extents "bbox" is optional - remove if present
            # since extracted data will have different extents
            if "bbox" in geom_col_vals:
                geom_col_vals.pop("bbox")
            # add "covering" if there is a row level "bbox" column
            # this facilitates spatial filters e.g. geopandas read_parquet
            if "bbox" in schema.names:
                geom_col_vals["covering"] = {
                    "bbox": {
                        "xmin": ["bbox", "xmin"],
                        "ymin": ["bbox", "ymin"],
                        "xmax": ["bbox", "xmax"],
                        "ymax": ["bbox", "ymax"],
                    }
                }
        metadata[b"geo"] = json.dumps(geo).encode("utf-8")
        schema = schema.with_metadata(metadata)
        writer = pq.ParquetWriter(path, schema)
    return writer


@requires("shapely", verbose=False)
class BaseGeoJSONWriter:
    """
    A base feature writer that manages either a file handle
    or output stream. Subclasses should implement write_feature()
    and finalize() if needed
    """
    import_package("shapely", verbose=False)
    import shapely.wkb

    def __init__(self, where):
        self.file_handle = None
        if isinstance(where, str):
            self.file_handle = open(os.path.expanduser(where), "w")
            self.writer = self.file_handle
        else:
            self.writer = where
        self.is_open = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        self.close()

    def close(self):
        if not self.is_open:
            return
        self.finalize()
        if self.file_handle:
            self.file_handle.close()
        self.is_open = False

    def write_batch(self, batch):
        if batch.num_rows == 0:
            return

        for row in batch.to_pylist():
            feature = self.row_to_feature(row)
            self.write_feature(feature)

    def write_feature(self, feature):
        pass

    def finalize(self):
        pass

    def row_to_feature(self, row):
        geometry = shapely.wkb.loads(row.pop("geometry"))
        row.pop("bbox")

        # This only removes null values in the top-level dictionary but will leave in
        # nulls in sub-properties
        properties = {k: v for k, v in row.items() if k != "bbox" and v is not None}
        return {
            "type": "Feature",
            "geometry": geometry.__geo_interface__,
            "properties": properties,
        }


class GeoJSONSeqWriter(BaseGeoJSONWriter):
    def write_feature(self, feature):
        self.writer.write(json.dumps(feature, separators=(",", ":")))
        self.writer.write("\n")


class GeoJSONWriter(BaseGeoJSONWriter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_written_feature = False

        self.writer.write('{"type": "FeatureCollection", "features": [\n')

    def write_feature(self, feature):
        if self._has_written_feature:
            self.writer.write(",\n")
        self.writer.write(json.dumps(feature, separators=(",", ":")))
        self._has_written_feature = True

    def finalize(self):
        self.writer.write("]}")


@requires("pyarrow", verbose=False)
def record_batch_reader(overture_type: str, bbox=None) -> Optional[pa.RecordBatchReader]:
    """Return a pyarrow RecordBatchReader for the desired bounding box and s3 path

    Args:
        overture_type (str): The type of Overture map data to load. Options include
            'address', 'bathymetry', 'building', 'building_part', 'division', 'division_area',
            'division_boundary', 'place', 'segment', 'connector', 'infrastructure', 'land',
            'land_cover', 'land_use', 'water'
        bbox (tuple[float, float, float, float]): Bounding box for filtering data.
            Format is (xmin, ymin, xmax, ymax). Defaults to None.

    """
    import_package("pyarrow", verbose=False)
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.fs as fs

    path = _dataset_path(overture_type)

    if bbox:
        xmin, ymin, xmax, ymax = bbox
        filter_ = (
            (pc.field("bbox", "xmin") < xmax)
            & (pc.field("bbox", "xmax") > xmin)
            & (pc.field("bbox", "ymin") < ymax)
            & (pc.field("bbox", "ymax") > ymin)
        )
    else:
        filter_ = None

    dataset = ds.dataset(path, filesystem=fs.S3FileSystem(anonymous=True, region="us-west-2"))
    batches = dataset.to_batches(filter=filter_)

    # to_batches() can yield many batches with no rows. I've seen
    # this cause downstream crashes or other negative effects. For
    # example, the ParquetWriter will emit an empty row group for
    # each one bloating the size of a parquet file. Just omit
    # them so the RecordBatchReader only has non-empty ones. Use
    # the generator syntax so the batches are streamed out
    non_empty_batches = (b for b in batches if b.num_rows > 0)

    geoarrow_schema = geoarrow_schema_adapter(dataset.schema)
    return pa.RecordBatchReader.from_batches(geoarrow_schema, non_empty_batches)


@requires("geopandas", verbose=False)
def geodataframe(overture_type: str, bbox: tuple[float, float, float, float] = None) -> GeoDataFrame:
    """ Loads geoparquet for specified type into a geopandas dataframe

    Args:
        overture_type (str): The type of Overture map data to load. Options include
                'address', 'bathymetry', 'building', 'building_part', 'division', 'division_area',
                'division_boundary', 'place', 'segment', 'connector', 'infrastructure', 'land',
                'land_cover', 'land_use', 'water'
        bbox: optional bounding box for data fetch (xmin, ymin, xmax, ymax)

    Returns:
        GeoDataFrame with the optionally filtered theme data

    """
    import_package("geopandas", verbose=False)
    import geopandas as gpd

    reader = record_batch_reader(overture_type, bbox)
    return gpd.GeoDataFrame.from_arrow(reader)


def geoarrow_schema_adapter(schema: pa.Schema) -> pa.Schema:
    """
    Convert a geoarrow-compatible schema to a proper geoarrow schema

    This assumes there is a single "geometry" column with WKB formatting

    Parameters
    ----------
    schema: pa.Schema

    Returns
    -------
    pa.Schema
    A copy of the input schema with the geometry field replaced with
    a new one with the proper geoarrow ARROW:extension metadata

    """
    geometry_field_index = schema.get_field_index("geometry")
    geometry_field = schema.field(geometry_field_index)
    geoarrow_geometry_field = geometry_field.with_metadata(
        {b"ARROW:extension:name": b"geoarrow.wkb"}
    )

    return schema.set(geometry_field_index, geoarrow_geometry_field)


type_theme_map = {
    "address": "addresses",
    "bathymetry": "base",
    "building": "buildings",
    "building_part": "buildings",
    "division": "divisions",
    "division_area": "divisions",
    "division_boundary": "divisions",
    "place": "places",
    "segment": "transportation",
    "connector": "transportation",
    "infrastructure": "base",
    "land": "base",
    "land_cover": "base",
    "land_use": "base",
    "water": "base",
}


def _dataset_path(overture_type: str) -> str:
    """
    Returns the s3 path of the Overture dataset to use. This assumes overture_type has
    been validated, e.g. by the CLI

    """
    # Map of sub-partition "type" to parent partition "theme" for forming the
    # complete s3 path. Could be discovered by reading from the top-level s3
    # location but this allows to only read the files in the necessary partition.
    theme = type_theme_map[overture_type]
    return f"overturemaps-us-west-2/release/2025-03-19.0/theme={theme}/type={overture_type}/"


def get_all_overture_types() -> List[str]:
    return list(type_theme_map.keys())
