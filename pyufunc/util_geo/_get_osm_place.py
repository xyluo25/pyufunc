# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, June 19th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import annotations
from pathlib import Path
from hashlib import sha1
from urllib.parse import urlparse
from json import JSONDecodeError
import socket
import json
from collections import OrderedDict
import time
import importlib
from pyufunc.util_common._dependency_requires_decorator import requires
from pyufunc.util_common._import_package import import_package
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import shapely
    import requests

# capture getaddrinfo function to use original later after mutating it
_original_getaddrinfo = socket.getaddrinfo

settings = {
    "cache_folder": "./cache",
    "doh_url_template": "https://8.8.8.8/resolve?name={hostname}",
    "http_accept_language": "en",
    "http_referer": "OSMnx Python package (https://github.com/gboeing/osmnx)",
    "http_user_agent": "OSMnx Python package (https://github.com/gboeing/osmnx)",
    "max_query_area_size": 50 * 1000 * 50 * 1000,
    "nominatim_key": None,
    "nominatim_url": "https://nominatim.openstreetmap.org/",

    "requests_kwargs": {},
    "requests_timeout": 180,
    "use_cache": False,
}


@requires("shapely", "requests", "urllib", verbose=False)
class OSMPlaceFinder:

    import_package("shapely", verbose=False)
    import_package("requests", verbose=False)
    import_package("urllib", verbose=False)
    import shapely
    import requests


    def __init__(self, place: str, verbose: bool = False):

        self.place = place
        self.verbose = verbose

    def _download_nominatim_element(self,
                                    query: str | dict[str, str],
                                    *,
                                    by_osmid: bool = False,
                                    limit: int = 50,
                                    polygon_geojson: bool = True,
                                    ) -> list[dict[str, Any]]:
        """
        Retrieve an OSM element from the Nominatim API.

        Parameters
        ----------
        query
            Query string or structured query dict.
        by_osmid
            If True, treat `query` as an OSM ID lookup rather than text search.
        limit
            Max number of results to return.
        polygon_geojson
            Whether to retrieve the place's geometry from the API.

        Returns
        -------
        response_json
        """
        # define the parameters
        params: OrderedDict[str, int | str] = OrderedDict()
        params["format"] = "json"
        params["polygon_geojson"] = int(polygon_geojson)  # bool -> int

        if by_osmid:
            # if querying by OSM ID, use the lookup endpoint
            if not isinstance(query, str):
                msg = "`query` must be a string if `by_osmid` is True."
                raise TypeError(msg)
            request_type = "lookup"
            params["osm_ids"] = query

        else:
            # if not querying by OSM ID, use the search endpoint
            request_type = "search"

            # prevent OSM from deduping so we get precise number of results
            params["dedupe"] = 0
            params["limit"] = limit

            if isinstance(query, str):
                params["q"] = query
            elif isinstance(query, dict):
                # add query keys in alphabetical order so URL is the same string
                # each time, for caching purposes
                for key in sorted(query):
                    params[key] = query[key]
            else:  # pragma: no cover
                # type: ignore[unreachable]
                msg = "Each query must be a dict or a string."
                raise TypeError(msg)

        # request the URL, return the JSON
        return self._nominatim_request(params=params, request_type=request_type)

    def _nominatim_request(self,
                           params: OrderedDict[str, int | str],
                           *,
                           request_type: str = "search",
                           pause: float = 1,
                           error_pause: float = 60) -> list[dict[str, Any]]:
        """
        Send a HTTP GET request to the Nominatim API and return response.

        Parameters
        ----------
        params
            Key-value pairs of parameters.
        request_type
            {"search", "reverse", "lookup"}
            Which Nominatim API endpoint to query.
        pause
            How long to pause before request, in seconds. Per the Nominatim usage
            policy: "an absolute maximum of 1 request per second" is allowed.
        error_pause
            How long to pause in seconds before re-trying request if error.

        Returns
        -------
        response_json
        """
        if request_type not in {"search", "reverse", "lookup"}:  # pragma: no cover
            msg = "Nominatim `request_type` must be 'search', 'reverse', or 'lookup'."
            raise ValueError(msg)

        # add nominatim API key to params if one has been provided in settings
        if settings["nominatim_key"] is not None:
            params["key"] = settings["nominatim_key"]

        # prepare Nominatim API URL and see if request already exists in cache
        url = settings["nominatim_url"].rstrip("/") + "/" + request_type
        prepared_url = str(requests.Request("GET", url, params=params).prepare().url)
        cached_response_json = self._retrieve_from_cache(prepared_url)
        if isinstance(cached_response_json, list):
            return cached_response_json

        # pause then request this URL
        domain = self._hostname_from_url(url)
        msg = f"Pausing {pause} second(s) before making HTTP GET request to {domain!r}"
        if self.verbose:
            print(f"  :{msg}")
        time.sleep(pause)

        # transmit the HTTP GET request
        msg = f"Get {prepared_url} with timeout={settings['requests_timeout']}"
        if self.verbose:
            print(f"  :{msg}")
        response = requests.get(
            url,
            params=params,
            timeout=settings["requests_timeout"],
            headers=self._get_http_headers(),
            **settings["requests_kwargs"],
        )

        # handle 429 and 504 errors by pausing then recursively re-trying request
        if response.status_code in {429, 504}:  # pragma: no cover
            msg = (
                f"{domain!r} responded {response.status_code} {response.reason}: "
                f"we'll retry in {error_pause} secs"
            )
            if self.verbose:
                print(f"  :{msg}")
            time.sleep(error_pause)
            return self._nominatim_request(
                params,
                request_type=request_type,
                pause=pause,
                error_pause=error_pause,
            )

        response_json = self._parse_response(response)
        if not isinstance(response_json, list):
            msg = "Nominatim API did not return a list of results."
            raise ValueError(msg)
        self._save_to_cache(prepared_url, response_json, response.ok)

        return response_json

    def get_osm_place(self,
                      query: str | dict[str, str],
                      which_result: int | None = None,
                      by_osmid: bool = False) -> dict:
        """
        Geocode a single place query to a GeoDataFrame.

        Parameters
        ----------
        query
            Query string or structured dict to geocode.
        which_result
            Which search result to return. If None, auto-select the first
            (Multi)Polygon or raise an error if OSM doesn't return one. To get
            the top match regardless of geometry type, set `which_result=1`.
            Ignored if `by_osmid=True`.
        by_osmid
            If True, treat query as an OSM ID lookup rather than text search.

        Returns
        -------
        dict
            Dictionary with the geocoding result.
        """

        limit = 50 if which_result is None else which_result
        results = self._download_nominatim_element(
            query, by_osmid=by_osmid, limit=limit)

        # choose the right result from the JSON response
        if len(results) == 0:
            # if no results were returned, raise error
            msg = f"Nominatim geocoder returned 0 results for query {query!r}."
            raise ValueError(msg)

        if by_osmid:
            # if searching by OSM ID, always take the first (ie, only) result
            result = results[0]

        elif which_result is None:
            # else, if which_result=None, auto-select the first (Multi)Polygon
            try:
                result = self.__get_first_polygon(results)
            except TypeError as e:
                msg = f"Nominatim did not geocode query {query!r} to a geometry of type (Multi)Polygon."
                raise TypeError(msg) from e

        elif len(results) >= which_result:
            # else, if we got at least which_result results, choose that one
            result = results[which_result - 1]

        else:  # pragma: no cover
            # else, we got fewer results than which_result, raise error
            msg = f"Nominatim returned {len(results)} result(s) but `which_result={which_result}`."
            raise ValueError(msg)

        # if we got a non (Multi)Polygon geometry type (like a point), log warning
        geom_type = result["geojson"]["type"]
        if geom_type not in {"Polygon", "MultiPolygon"}:
            msg = f"Nominatim geocoder returned a {geom_type} as the geometry for query {query!r}"
            if self.verbose:
                print(f"  :{msg}")

        # build the GeoJSON feature from the chosen result
        south, north, west, east = result["boundingbox"]
        feature = {
            "type": "Feature",
            "geometry": result["geojson"],
            "properties": {
                "bbox_north": north,
                "bbox_south": south,
                "bbox_east": east,
                "bbox_west": west,
            },
        }

        # add the other attributes we retrieved
        for attr in result:
            if attr not in {"address", "boundingbox", "geojson", "icon", "licence"}:
                feature["properties"][attr] = result[attr]

        place_dict = feature["properties"]
#         # create and return the GeoDataFrame
#         gdf = gpd.GeoDataFrame.from_features([feature])
#         cols = ["lat", "lon", "bbox_north",
#                 "bbox_south", "bbox_east", "bbox_west"]
#         gdf[cols] = gdf[cols].astype(float)
#
#         place_dict = gdf.to_dict(orient="records")[0]

        feature_coords = feature["geometry"]["coordinates"]

        try:
            place_dict["geometry"] = shapely.geometry.MultiPolygon(
                [shapely.geometry.Polygon(s[0]) for s in feature_coords])
        except Exception:
            place_dict["geometry"] = feature_coords
        return place_dict

    def __get_first_polygon(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Choose first result of geometry type (Multi)Polygon from list of results.

        Parameters
        ----------
        results
            Results from the Nominatim API.

        Returns
        -------
        result
            The chosen result.
        """
        polygon_types = {"Polygon", "MultiPolygon"}

        for result in results:
            if "geojson" in result and result["geojson"]["type"] in polygon_types:
                return result

        # if we never found a polygon, raise an error
        raise TypeError

    def _save_to_cache(self,
                       url: str,
                       response_json: dict[str, Any] | list[dict[str, Any]],
                       ok: bool) -> None:
        """
        Save a HTTP response JSON object to a file in the cache folder.

        This calculates the checksum of `url` to generate the cache file name. If
        the request was sent to server via POST instead of GET, then `url` should
        be a GET-style representation of the request. Response is only saved to a
        cache file if `settings.use_cache` is True, `response_json` is not None,
        and `ok` is True.

        Users should always pass OrderedDicts instead of dicts of parameters into
        request functions, so the parameters remain in the same order each time,
        producing the same URL string, and thus the same hash. Otherwise the cache
        will eventually contain multiple saved responses for the same request
        because the URL's parameters appeared in a different order each time.

        Parameters
        ----------
        url
            The URL of the request.
        response_json
            The JSON response from the server.
        ok
            A `requests.response.ok` value.

        Returns
        -------
        None
        """
        if settings["use_cache"]:
            if not ok:  # pragma: no cover
                msg = "Did not save to cache because HTTP status code is not OK"
                if self.verbose:
                    print(f"  :{msg}")
            else:
                # create the folder on the disk if it doesn't already exist
                cache_folder = Path(settings["cache_folder"])
                cache_folder.mkdir(parents=True, exist_ok=True)

                # hash the url to make the filename succinct but unique
                # sha1 digest is 160 bits = 20 bytes = 40 hexadecimal characters
                checksum = sha1(url.encode("utf-8")).hexdigest()  # noqa: S324
                cache_filepath = cache_folder / f"{checksum}.json"

                # dump to json, and save to file
                cache_filepath.write_text(json.dumps(
                    response_json), encoding="utf-8")
                msg = f"Saved response to cache file {str(cache_filepath)!r}"
                if self.verbose:
                    print(f"  :{msg}")

    def _url_in_cache(self, url: str) -> Path | None:
        """
        Determine if a URL's response exists in the cache.

        Calculates the checksum of `url` to determine the cache file's name.
        Returns None if it cannot be found in the cache.

        Parameters
        ----------
        url
            The URL to look for in the cache.

        Returns
        -------
        cache_filepath
            Path to cached response for `url` if it exists, otherwise None.
        """
        # hash the url to generate the cache filename
        checksum = sha1(url.encode("utf-8")).hexdigest()  # noqa: S324
        cache_filepath = Path(settings["cache_folder"]) / f"{checksum}.json"

        # if this file exists in the cache, return its full path
        return cache_filepath if cache_filepath.is_file() else None

    def _retrieve_from_cache(self, url: str) -> dict[str, Any] | list[dict[str, Any]] | None:
        """
        Retrieve a HTTP response JSON object from the cache if it exists.

        Returns None if there is a server remark in the cached response.

        Parameters
        ----------
        url
            The URL of the request.

        Returns
        -------
        response_json
            Cached response for `url` if it exists in the cache and does not
            contain a server remark, otherwise None.
        """
        # if the tool is configured to use the cache
        if settings["use_cache"]:
            # return cached response for this url if exists, otherwise return None
            cache_filepath = self._url_in_cache(url)
            if cache_filepath is not None:
                response_json: dict[str, Any] | list[dict[str, Any]] = json.loads(
                    cache_filepath.read_text(encoding="utf-8"),
                )

                # return None if there is a server remark in the cached response
                if isinstance(response_json, dict) and ("remark" in response_json):  # pragma: no cover
                    msg = (
                        f"Ignoring cache file {str(cache_filepath)!r} because "
                        f"it contains a remark: {response_json['remark']!r}"
                    )
                    if self.verbose:
                        print(f"  :{msg}")
                    return None

                msg = f"Retrieved response from cache file {str(cache_filepath)!r}"
                if self.verbose:
                    print(f"  :{msg}")
                return response_json

        return None

    def _get_http_headers(self,
                          *,
                          user_agent: str | None = None,
                          referer: str | None = None,
                          accept_language: str | None = None,
                          ) -> dict[str, str]:
        """
        Update the default requests HTTP headers with OSMnx information.

        Parameters
        ----------
        user_agent
            The user agent. If None, use `settings.http_user_agent` value.
        referer
            The referer. If None, use `settings.http_referer` value.
        accept_language
            The accept language. If None, use `settings.http_accept_language`
            value.

        Returns
        -------
        headers
        """
        if user_agent is None:
            user_agent = settings["http_user_agent"]
        if referer is None:
            referer = settings["http_referer"]
        if accept_language is None:
            accept_language = settings["http_accept_language"]

        info = {"User-Agent": user_agent, "referer": referer,
                "Accept-Language": accept_language}
        headers = dict(requests.utils.default_headers())
        headers.update(info)
        return headers

    def _resolve_host_via_doh(self, hostname: str) -> str:
        """
        Resolve hostname to IP address via Google's public DNS-over-HTTPS API.

        Necessary fallback as socket.gethostbyname will not always work when using
        a proxy. See https://developers.google.com/speed/public-dns/docs/doh/json
        If the user has set `settings.doh_url_template=None` or if resolution
        fails (e.g., due to local network blocking DNS-over-HTTPS) the hostname
        itself will be returned instead. Note that this means that server slot
        management may be violated: see `_config_dns` documentation for details.

        Parameters
        ----------
        hostname
            The hostname to consistently resolve the IP address of.

        Returns
        -------
        ip_address
            Resolved IP address of host, or hostname itself if resolution failed.
        """
        if settings["doh_url_template"] is None:
            if self.verbose:
                # if user has set the url template to None, return hostname itself
                msg = "User set `doh_url_template=None`, requesting host by name"
                print(f"  :{msg}")
            return hostname

        if self.verbose:
            err_msg = f"Failed to resolve {hostname!r} IP via DoH, requesting host by name"
            print(f"  :{err_msg}")
        try:
            url = settings["doh_url_template"].format(hostname=hostname)
            response = requests.get(url, timeout=settings["requests_timeout"])
            data = response.json()

        # if we cannot reach DoH server or resolve host, return hostname itself
        except requests.exceptions.RequestException:  # pragma: no cover
            return hostname

        # if there were no request exceptions, return
        else:
            if response.ok and data["Status"] == 0:
                # status 0 means NOERROR, so return the IP address
                ip_address: str = data["Answer"][0]["data"]
                return ip_address

            # otherwise, if we cannot reach DoH server or cannot resolve host
            # just return the hostname itself
            return hostname

    def _config_dns(self, url: str) -> None:
        """
        Force socket.getaddrinfo to use IP address instead of hostname.

        Resolves the URL's domain to an IP address so that we use the same server
        for both 1) checking the necessary pause duration and 2) sending the query
        itself even if there is round-robin redirecting among multiple server
        machines on the server-side. Mutates the getaddrinfo function so it uses
        the same IP address everytime it finds the hostname in the URL.

        For example, the server overpass-api.de just redirects to one of the other
        servers (currently gall.openstreetmap.de and lambert.openstreetmap.de). So
        if we check the status endpoint of overpass-api.de, we may see results for
        server gall, but when we submit the query itself it gets redirected to
        server lambert. This could result in violating server lambert's slot
        management timing.

        Parameters
        ----------
        url
            The URL to consistently resolve the IP address of.

        Returns
        -------
        None
        """
        hostname = self._hostname_from_url(url)
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:  # pragma: no cover
            # may occur when using a proxy, so instead resolve IP address via DoH
            msg = f"Encountered gaierror while trying to resolve {hostname!r}, trying again via DoH..."
            if self.verbose:
                print(f"  :{msg}")
            ip = self._resolve_host_via_doh(hostname)

        # mutate socket.getaddrinfo to map hostname -> IP address
        def _getaddrinfo(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            if args[0] == hostname:
                msg = f"Resolved {hostname!r} to {ip!r}"
                if self.verbose:
                    print(f"  :{msg}")
                return _original_getaddrinfo(ip, *args[1:], **kwargs)

            # otherwise
            return _original_getaddrinfo(*args, **kwargs)

        socket.getaddrinfo = _getaddrinfo

    def _hostname_from_url(self, url: str) -> str:
        """
        Extract the hostname (domain) from a URL.

        Parameters
        ----------
        url
            The url from which to extract the hostname.

        Returns
        -------
        hostname
            The extracted hostname (domain).
        """
        return urlparse(url).netloc.split(":")[0]

    def _parse_response(self, response: requests.Response) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Parse JSON from a requests response and log the details.

        Parameters
        ----------
        response
            The response object.

        Returns
        -------
        response_json
            Value will be a dict if the response is from the Google or Overpass
            APIs, and a list if the response is from the Nominatim API.
        """
        # log the response size and domain
        domain = self._hostname_from_url(response.url)
        size_kb = len(response.content) / 1000
        msg = f"Downloaded {size_kb:,.1f}kB from {domain!r} with status {response.status_code}"
        if self.verbose:
            print(f"  :{msg}")
        # parse the response to JSON and log/raise exceptions
        try:
            response_json: dict[str, Any] | list[dict[str, Any]] = response.json()
        except JSONDecodeError as e:  # pragma: no cover
            msg = f"{domain!r} responded: {response.status_code} {response.reason} {response.text}"
            if response.ok:
                raise ValueError(msg) from e
            raise ValueError(msg) from e

        # log any remarks if they exist
        if isinstance(response_json, dict) and "remark" in response_json:  # pragma: no cover
            msg = f"{domain!r} remarked: {response_json['remark']!r}"
            if self.verbose:
                print(f"  :{msg}")

        # log if the response status_code is not OK
        if not response.ok:
            msg = f"{domain!r} returned HTTP status code {response.status_code}"
            if self.verbose:
                print(f"  :{msg}")
        return response_json


@requires("shapely", "requests", "urllib", verbose=False)
def get_osm_place(place: str, verbose: bool = False) -> dict:
    """
    Geocode a place query to a GeoDataFrame.

    Parameters
    ----------
    place
        The place name or query string to geocode.
    verbose
        Whether to print out information about the geocoding process.

    Returns
    -------
    dict
        Dictionary with the geocoding result.
    """

    import_package("shapely", verbose=False)
    import_package("requests", verbose=False)
    import shapely
    import requests
    globals()["requests"] = importlib.import_module("requests")
    globals()["shapely"] = importlib.import_module("shapely")


    return OSMPlaceFinder(place, verbose).get_osm_place(place, None, False)
