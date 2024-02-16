# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, April 24th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from pyufunc.pkg_utils import requires


@requires("requests", "bs4")
def pypi_downloads(pkg_name: str) -> dict:
    """Get the total downloads of a package from PyPI.

    Args:
        package (str): The name of the package.

    Returns:
        dict: A dictionary containing the total downloads of the package.

    Examples:
        >>> pypi_downloads("pandas")  # package is found
        {'pandas': {'Total downloads': 4051345849.0}}

        >>> pypi_downloads("pandas123")  # package is not found
        {'pandas123': 0}
    """

    # import packages required for this function
    import requests
    from bs4 import BeautifulSoup

    # prepare the url and get the response
    # url = 'https://api.pepy.tech/api/projects/' + package_name
    url = f"https://www.pepy.tech/projects/{pkg_name}"
    print(f"..Getting data from {url}")

    try:
        # get data from url
        response = requests.get(url)

        # convert the response to a dictionary
        # content_dict = json.loads(response.content.decode("utf-8"))
        web_content = BeautifulSoup(response.content, "html.parser")
        total_downloads_str_list = web_content.find_all(string=lambda t: "Total downloads" in t.text)

        # if the package is not found, return 0
        if len(total_downloads_str_list) == 0:
            print(f"Error: {pkg_name} not found. returning 0 instead.")
            return {pkg_name: 0}

        # get the total downloads and save it to a dictionary
        downloads_dict = {}
        for total_downloads_str in total_downloads_str_list:
            download_str = web_content.find(string=total_downloads_str).parent.find_next("div").text
            download_float = float(download_str.replace(",", ""))
            downloads_dict[total_downloads_str] = download_float

        # return the dictionary containing the total downloads of the package
        return {pkg_name: downloads_dict}
    except Exception:
        print(f"Error: {pkg_name} not found. returning 0 instead.")
        return {pkg_name: 0}
