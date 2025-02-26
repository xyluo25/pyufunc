'''
##############################################################
# Created Date: Wednesday, January 15th 2025
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
'''
from typing import TYPE_CHECKING

from pyufunc.util_magic import requires, import_package

if TYPE_CHECKING:
    import requests

# import requests
from datetime import datetime


@requires("requests", verbose=False)
def download_elevation_tif_by(bbox: tuple | list, output_file: str) -> None:
    """
    Download elevation data (TIFF) from USGS National Map based on a bounding box.

    Args:
        bbox (tuple): Bounding box (min_lon, min_lat, max_lon, max_lat).
        output_file (str): Path to save the downloaded TIFF file.

    Location:
        pyufunc.util_geo._geo_tif.download_elevation_tif_by

    Note:
        UGSG National Map API: https://tnmaccess.nationalmap.gov/api/v1/products
        USGS Elevation Data: https://apps.nationalmap.gov/downloader/#/elevation
        Dataset: National Elevation Dataset (NED) 1/3 arc-second
        Available products: 1 arc-second, 1/3 arc-second, 1/9 arc-second, 1 meter

    Example:
        >>> from pyufunc import download_elevation_tif_by
        >>> bbox = (-122.5, 37.5, -122.0, 38.0)
        >>> output_file = "elevation.tif"
        >>> download_elevation_tif_by(bbox, output_file)
            :Downloading GeoTIFF file from: https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/n38w123/USGS_1_n38w123.tif
            Total file size: 1.00 MB
            :Downloaded: 1.00 MB
            :GeoTIFF file saved as: elevation.tif

    Returns:
        None
    """

    # TDD: check input parameters
    if not isinstance(bbox, (tuple, list)):
        raise ValueError("Bounding box must be a tuple or list.")

    if len(bbox) != 4:
        raise ValueError("Bounding box must contain 4 coordinates (min_lon, min_lat, max_lon, max_lat).")

    # check if bounding box coordinates are valid numeric values
    if not all(isinstance(coord, (int, float)) for coord in bbox):
        raise ValueError("Bounding box coordinates must be numeric.")

    # check if longitude and latitude values are within valid range
    if not (-180 <= bbox[0] <= 180) or not (-180 <= bbox[2] <= 180):
        raise ValueError("Longitude values must be within the range [-180, 180].")

    if not (-90 <= bbox[1] <= 90) or not (-90 <= bbox[3] <= 90):
        raise ValueError("Latitude values must be within the range [-90, 90].")

    # check whether the output file with .tif extension
    if not output_file.endswith(".tif"):
        raise ValueError("Output file must be a TIFF file.")

    # Download elevation data from USGS National Map

    # USGS Elevation Data API endpoint
    usgs_api_url = "https://tnmaccess.nationalmap.gov/api/v1/products"

    # API parameters
    params = {
        "datasets": "National Elevation Dataset (NED) 1/3 arc-second",
        "bbox": ",".join(map(str, bbox)),
        "outputFormat": "json",
        "extentType": "bbox"
    }

    # Make a request to the API
    response = requests.get(usgs_api_url, params=params)

    # Check for a successful response
    if response.status_code != 200:
        print(f"  :Failed to query USGS API: {response.status_code} {response.text}")
        return None
    # Parse the response
    data = response.json()
    if not data.get("items"):
        print("  :No data available for the specified bounding box.")
        return None

    # Download the first available GeoTIFF file
    # tiff_url = data["items"][0]["downloadURL"]
    tiff_url_list = list({item["downloadURL"] for item in data["items"]})

    # Extract date from each URL
    def extract_date(url):
        try:
            date_str = url.split('_')[-1].split('.')[0]
            return datetime.strptime(date_str, '%Y%m%d')
        except Exception:
            return None

    # Find the URL with the latest date
    latest_url = max(tiff_url_list, key=lambda url: extract_date(url))
    print(f"  :Downloading GeoTIFF file from: {latest_url}")

    # Download the TIFF file
    tiff_response = requests.get(latest_url, stream=True)
    if tiff_response.status_code == 200:
        # Get the total file size in MB
        total_size = int(tiff_response.headers.get('content-length', 0))
        total_size_mb = total_size / (1024 * 1024)
        print(f"  Total file size: {total_size_mb:.2f} MB")

        downloaded_size = 0
        with open(output_file, "wb") as file:
            # 1 MB chunks
            for chunk in tiff_response.iter_content(chunk_size=1024 * 1024):
                if chunk:  # Filter out keep-alive chunks
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    downloaded_mb = downloaded_size / (1024 * 1024)
                    print(f"  :Downloaded: {downloaded_mb:.2f} MB", end="\r")

        print(f"\n  :GeoTIFF file saved as: {output_file}")
    else:
        print(f"  :Failed to download GeoTIFF file: {tiff_response.status_code} {tiff_response.text}")

    return None
