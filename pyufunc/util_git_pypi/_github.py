# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, February 20th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import annotations
import contextlib
import re
import os
import json
import sys
import html.parser
import copy
import importlib
import secrets
import random
import shutil
from urllib.parse import urlparse
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING
from pyufunc.util_magic import requires, import_package

path_user_agent_strings = Path(__file__).parent.joinpath("static/user-agent-strings.json")

with open(path_user_agent_strings, mode='r', encoding='utf-8') as f:
    _web_agent_str = f.read()
_USER_AGENT_STRINGS = json.loads(_web_agent_str)

#  https://stackoverflow.com/questions/61384752/how-to-type-hint-with-an-optional-import
if TYPE_CHECKING:
    import requests
    from requests import Session
    import urllib3


class _FakeUserAgentParser(html.parser.HTMLParser):

    def __init__(self, browser_name):
        super().__init__()
        self.reset()
        self.recording = 0
        self.data = []
        self.browser_name = browser_name

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return

        if self.recording:
            self.recording += 1
            return

        if tag == 'a':
            for name, link in attrs:
                if name == 'href' and link.startswith(f'/{self.browser_name}') and link.endswith('.php'):
                    break
                else:
                    return
            self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'a' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data.strip())


@requires('requests', "urllib3", verbose=False)
class GitHubFileDownloader:
    """
    Download files on GitHub from a given repository URL.
    """
    import_package('requests', verbose=False)
    import_package("urllib3", verbose=False)
    import requests
    import urllib3

    def __init__(self, repo_url: str, flatten_files: bool = False, output_dir: str | None = None) -> None:
        """
        Initialize a GitHubFileDownloader object.

        Args:
            repo_url (str): URL of a GitHub repository to download from;
                it can be a ``blob`` or tree path
            flatten_files (bool, optional): Whether to pull the contents of all subdirectories into the root folder.
                Defaults to False.
            output_dir (str, optional): an output directory where the downloaded files will be saved,
                when ``output_dir=None``, it defaults to ``None``

        Returns:
            None

        Raises:
            ValueError: if the input URL is not valid

        """

        self.dir_out = None
        self.repo_url = repo_url
        self.flatten = flatten_files
        self.output_dir = "./" if output_dir is None else output_dir

        # Create a URL that is compatible with GitHub's REST API
        try:
            self.api_url, self.download_dirs = self.create_url(self.repo_url)
        except Exception as e:
            raise ValueError(f"Error: the input URL is not valid. {e}") from e

        # Initialize the total number of files under the given directory
        self.total_files = 0

        # Set user agent in default
        opener = urllib.request.build_opener()
        opener.addheaders = list(self.fake_requests_headers().items())
        urllib.request.install_opener(opener)

    @staticmethod
    def create_url(url: str) -> tuple[str, str]:
        """
        From the given url, produce a URL that is compatible with GitHub's REST API.
        It can handle ``blob`` or tree paths.

        Args:
            url (str): a URL of a GitHub repository to download from

        Returns:
            tuple: a tuple of two strings, the first string is the API URL, and the second string is the download path

        """

        repo_only_url = re.compile(
            r"https://github\.com/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}/[a-zA-Z0-9]+$")
        re_branch = re.compile("/(tree|blob)/(.+?)/")

        # Check if the given url is a complete url to a GitHub repo.
        if re.match(repo_only_url, url):
            print(
                "Given url is a complete repository, "
                "please use 'git clone' to download the repository")
            sys.exit()

        # Extract the branch name from the given url (e.g. master)
        branch = re_branch.search(url)
        download_paths = url[branch.end():]

        api_url = (
            f'{url[: branch.start()].replace("github.com", "api.github.com/repos", 1)}/'
            f'contents/{download_paths}?ref={branch[2]}')

        return (api_url, download_paths)

    def init_requests_session(self, url: str,
                              max_retries: int = 5,
                              backoff_factor: float = 0.1,
                              retry_status: str = 'default',
                              **kwargs) -> Session:
        # sourcery skip: dict-assign-update-to-union
        """Initialize a session for making HTTP requests.

        Args:
            url (_type_): a valid URL
            max_retries (int, optional): maximum number of retries. Defaults to 5.
            backoff_factor (float, optional): ``backoff_factor`` of `urllib3.util.retry.Retry`_. Defaults to 0.1.
            retry_status (str, optional): a list of HTTP status codes that force to retry downloading,
                inherited from ``status_forcelist`` of `urllib3.util.retry.Retry`_;
                when ``retry_status='default'``, the list defaults to ``[429, 500, 502, 503, 504]``.
                Defaults to 'default'.

        Returns:
            requests.Session:
        """

        if retry_status == 'default':
            codes_for_retries = [429, 500, 502, 503, 504]
        else:
            codes_for_retries = copy.copy(retry_status)

        kwargs.update({'backoff_factor': backoff_factor,
                       'status_forcelist': codes_for_retries})
        retries = urllib3.util.retry.Retry(total=max_retries, **kwargs)

        session = requests.Session()

        # noinspection HttpUrlsUsage
        session.mount(
            prefix='https://' if url.startswith('https:') else 'http://',
            adapter=requests.adapters.HTTPAdapter(max_retries=retries))

        return session

    def _user_agent_strings(self, browser_names: list = None, dump_dat: bool = True) -> dict:
        """Get a dictionary of user-agent strings for popular browsers.

        Args:
            browser_names (list, optional): names of a list of popular browsers. Defaults to None.
            dump_dat (bool, optional): _description_. Defaults to True.

        Returns:
            dict: a dictionary of user-agent strings for popular browsers
        """

        if browser_names is None:
            browser_names_ = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Internet Explorer', 'Opera']
        else:
            browser_names_ = browser_names.copy()

        resource_url = 'https://useragentstring.com/pages/useragentstring.php'

        user_agent_strings = {}
        for browser_name in browser_names_:
            # url = resource_url.replace('useragentstring.php', browser_name.replace(" ", "+") + '/')
            url = resource_url + f'?name={browser_name.replace(" ", "+")}'
            response = requests.get(url=url)
            fua_parser = _FakeUserAgentParser(browser_name=browser_name)
            fua_parser.feed(response.text)
            user_agent_strings[browser_name] = list(set(fua_parser.data))

        if dump_dat and all(user_agent_strings.values()):
            path_to_uas = importlib.resources.files(__package__).joinpath("data/user-agent-strings.json")
            with path_to_uas.open(mode='w') as f:
                f.write(json.dumps(user_agent_strings, indent=4))

        return user_agent_strings

    def load_user_agent_strings(self,
                                shuffled: bool = False,
                                flattened: bool = False,
                                update: bool = False,
                                verbose: bool = False) -> list:
        """
        Load user-agent strings of popular browsers.

        The current version collects a partially comprehensive list of user-agent strings for
        `Chrome`_, `Firefox`_, `Safari`_, `Edge`_, `Internet Explorer`_ and `Opera`_.

        Args:
            shuffled (bool, optional): whether to shuffle the user-agent strings of each browser. Defaults to False.
            flattened (bool, optional): whether to flatten the user-agent strings of all browsers into a single list.
                Defaults to False.
            update (bool, optional): whether to update the backup data of user-agent strings. Defaults to False.
            verbose (bool, optional): whether to print relevant information in console. Defaults to False.

        Returns:
            list: a list of user-agent strings of popular browsers

        See also:
            .. _`Chrome`: https://useragentstring.com/pages/useragentstring.php?name=Chrome
            .. _`Firefox`: https://useragentstring.com/pages/useragentstring.php?name=Firefox
            .. _`Safari`: https://useragentstring.com/pages/useragentstring.php?name=Safari
            .. _`Edge`: https://useragentstring.com/pages/useragentstring.php?name=Edge
            .. _`Internet Explorer`: https://useragentstring.com/pages/useragentstring.php?name=Internet+Explorer
            .. _`Opera`: https://useragentstring.com/pages/useragentstring.php?name=Opera


        Notes:
            The order of the elements in ``uas_list`` may be different every time we run the example
            as ``shuffled=True``.
        """

        if not update:
            # path_to_json = pkg_resources.resource_filename(__name__, "data\\user-agent-strings.json")
            # json_in = open(path_to_json, mode='r')
            # user_agent_strings = json.loads(json_in.read())
            user_agent_strings = _USER_AGENT_STRINGS.copy()

        else:
            if verbose:
                print("Updating the backup data of user-agent strings", end=" ... ")

            try:
                user_agent_strings = self._user_agent_strings(dump_dat=True)

                importlib.reload(sys.modules.get('pyhelpers._cache'))

                if verbose:
                    print("Done.")

            except Exception as e:
                if verbose:
                    print(f"Failed. {e}")
                user_agent_strings = self.load_user_agent_strings(update=False, verbose=False)

        if shuffled:
            for browser_name, ua_str in user_agent_strings.items():
                random.shuffle(ua_str)
                user_agent_strings.update({browser_name: ua_str})

        if flattened:
            user_agent_strings = [x for v in user_agent_strings.values() for x in v]

        return user_agent_strings

    def get_user_agent_string(self, fancy: str = None, **kwargs) -> str:
        """
        Get a random user-agent string of a certain browser.

        Args:
            fancy (str, optional): a name of a popular browser. Defaults to None.
            kwargs: [optional] parameters of the function

        Returns:
            str: a random user-agent string of a certain browser


        Notes:
            In the above examples, the returned user-agent string is random and may be different
            every time of running the function.
        """

        if fancy is not None:
            browser_names = {'Chrome', 'Firefox', 'Safari', 'Edge', 'Internet Explorer', 'Opera'}
            assert fancy in browser_names, f"`fancy` must be one of {browser_names}."

            kwargs['flattened'] = False
            user_agent_strings_ = self.load_user_agent_strings(**kwargs)

            user_agent_strings = user_agent_strings_[fancy]

        else:
            kwargs['flattened'] = True
            user_agent_strings = self.load_user_agent_strings(**kwargs)

        user_agent_string = secrets.choice(user_agent_strings)

        return user_agent_string

    def fake_requests_headers(self, randomized: bool = True, **kwargs) -> dict:
        """
        Make a fake HTTP headers for `requests.get
        <https://requests.readthedocs.io/en/master/user/advanced/#request-and-response-objects>`_.

        Args:
            randomized (bool, optional): whether to use a random user-agent string. Defaults to True.
            kwargs: [optional] parameters of the function :func:`pyhelpers.ops.get_user_agent_string`

        Returns:
            dict: a fake HTTP headers for `requests.get`

        Notes:
            - ``fake_headers_1`` may also be different every time we run the example.
            This is because the returned result is randomly chosen from a limited set of candidate
            user-agent strings, even though ``randomized`` is (by default) set to be ``False``.
            - By setting ``randomized=True``, the function returns a random result from among
            all available user-agent strings of several popular browsers.
        """

        if not randomized:
            kwargs['fancy'] = 'Chrome'

        user_agent_string = self.get_user_agent_string(**kwargs)

        fake_headers = {'user-agent': user_agent_string}

        return fake_headers

    @requires('tqdm', verbose=False)
    def _download_file_from_url(self, response, path_to_file):
        """
        Download an object from a valid URL (and save it as a file).

        """

        # import tqdm if it is available, otherwise, install and import it
        tqdm_ = import_package('tqdm', verbose=False)

        file_size = int(response.headers.get('content-length'))  # Total size in bytes

        unit_divisor = 1024
        block_size = unit_divisor ** 2
        chunk_size = block_size if file_size >= block_size else unit_divisor

        total_iter = file_size // chunk_size

        pg_args = {
            'desc': f'"{path_to_file}"',
            'total': total_iter,
            'unit': 'B',
            'unit_scale': True,
            'unit_divisor': unit_divisor,
        }
        with tqdm_.tqdm(**pg_args) as progress:

            contents = response.iter_content(chunk_size=chunk_size, decode_unicode=True)

            with open(file=path_to_file, mode='wb') as f:
                written = 0
                for data in contents:
                    if data:
                        try:
                            f.write(data)
                        except TypeError:
                            f.write(data.encode())
                        progress.update(len(data))
                        written += len(data)

        if file_size != 0 and written != file_size:
            print("ERROR! Something went wrong!")

    def download_file_from_url(self, url: str,
                               path_to_file: str,
                               if_exists: str = 'replace',
                               max_retries: str = 5,
                               random_header: bool = True,
                               verbose: bool = False,
                               requests_session_args=None,
                               fake_headers_args: dict = None,
                               **kwargs):
        """
        Download an object available at a valid URL.

        See also:
            [`OPS-DFFU-1`_] and [`OPS-DFFU-2`_].

            .. _OPS-DFFU-1: https://stackoverflow.com/questions/37573483/
            .. _OPS-DFFU-2: https://stackoverflow.com/questions/15431044/

        Args:
            url (str): a valid URL
            path_to_file (str): a path to the file to be saved
            if_exists (str, optional): whether to replace or skip the file if it already exists.
                Defaults to 'replace'.
            max_retries (str, optional): maximum number of retries. Defaults to 5.
            random_header (bool, optional): whether to use a random user-agent string. Defaults to True.
            verbose (bool, optional): whether to print relevant information in console. Defaults to False.
            requests_session_args (dict, optional): parameters of the function
            fake_headers_args (dict, optional): parameters of the function
            kwargs: [optional] parameters of the function :func:`requests.Session.get`

        .. _`requests.Session.get()`:
            https://docs.python-requests.org/en/master/_modules/requests/sessions/#Session.get

        Notes:

            - When ``verbose=True``, the function requires `tqdm`_.

            .. _`tqdm`: https://pypi.org/project/tqdm/
        """

        path_to_dir = os.path.dirname(path_to_file)
        if path_to_dir == "":
            path_to_file_ = os.path.join(os.getcwd(), path_to_file)
            path_to_dir = os.path.dirname(path_to_file_)
        else:
            path_to_file_ = copy.copy(path_to_file)

        if os.path.exists(path_to_file_) and if_exists != 'replace':
            if verbose:
                print(f"The destination already has a file named: {os.path.basename(path_to_file_)}, \
                      the download is cancelled.")

        else:
            if requests_session_args is None:
                requests_session_args = {}
            session = self.init_requests_session(url=url, max_retries=max_retries, **requests_session_args)

            if fake_headers_args is None:
                fake_headers_args = {}
            fake_headers = self.fake_requests_headers(randomized=random_header, **fake_headers_args)

            # Streaming, so we can iterate over the response
            with session.get(url=url, stream=True, headers=fake_headers, **kwargs) as response:

                if not os.path.exists(path_to_dir):
                    os.makedirs(path_to_dir)

                if verbose:
                    self._download_file_from_url(response=response, path_to_file=path_to_file_)

                else:
                    with open(file=path_to_file_, mode='wb') as f:
                        shutil.copyfileobj(fsrc=response.raw, fdst=f)

                    if os.stat(path=path_to_file_).st_size == 0:
                        print("ERROR! Something went wrong! Check if the URL is downloadable.")

    def download_single_file(self, file_url: str, dir_out: str):
        # Download the file
        _, _ = urllib.request.urlretrieve(file_url, dir_out)

        if self.flatten:
            if self.output_dir == "./":
                print(f"Downloaded to: ./{dir_out.split('/')[-1]}")
            else:
                print(
                    f"Downloaded to: {self.output_dir}/{dir_out.split('/')[-1]}")
        else:
            print(f"Downloaded to: {dir_out}")

    def download(self, api_url: str | None = None):
        # Update api_url if it is not specified
        api_url_local = self.api_url if api_url is None else api_url

        # Update output directory if flatten is not specified
        if self.flatten:
            self.dir_out = self.output_dir
        elif len(self.download_dirs.split(".")) == 0:
            self.dir_out = os.path.join(self.output_dir, self.download_dirs)
        else:
            self.dir_out = os.path.join(
                self.output_dir, "/".join(self.download_dirs.split("/")[:-1]))

        # Make a directory with the name which is taken from the actual repo
        os.makedirs(self.dir_out, exist_ok=True)

        # Get response from GutHub response
        try:
            response = urllib.request.urlretrieve(api_url_local)
        except KeyboardInterrupt:
            print(
                "Can not get response from GitHub API, please check the url again or try later.")

        # Download files according to the response
        with open(response[0], "r") as f:
            data = json.load(f)

        # If the data is a file, download it as one.
        if isinstance(data, dict) and data["type"] == "file":
            try:
                # Download the file
                self.download_single_file(
                    data["download_url"], "/".join([self.dir_out, data["name"]]))
                self.total_files += 1
                return self.total_files
            except KeyboardInterrupt as e:
                print(f"Error: Got interrupted for {e}")

        # If the data is a directory, download all files in it.
        for file in data:
            file_url = file["download_url"]
            file_path = file["path"]
            path = os.path.basename(file_path) if self.flatten else file_path
            path = "/".join([self.output_dir, path])

            dirname = os.path.dirname(path)

            # Create a directory if it does not exist
            if dirname != '':
                os.makedirs(os.path.dirname(path), exist_ok=True)

            # Download the file if it is not a directory
            if file_url is not None:
                # file_name = file["name"]
                try:
                    self.download_single_file(file_url, path)
                    self.total_files += 1
                except KeyboardInterrupt:
                    print("Got interrupted")

            # If the file is a directory, recursively download it
            else:
                try:
                    self.api_url, self.download_dirs = self.create_url(
                        file["html_url"])
                    self.download(self.api_url)
                except Exception:
                    print(
                        f"Error: {file['html_url']} is not a file or a directory")

        return self.total_files


def github_file_downloader(repo_url: str, output_dir: str | None = None, flatten: bool = False) -> int:
    """Download files from a GitHub repository.

    Args:
        url (str): URL of a GitHub repository to download from;
            it can be a ``blob`` or tree path
        output_dir (str): an output directory where the downloaded files will be saved,
            when ``output_dir=None``, it defaults to ``None``
        flatten (bool, optional): Whether to pull the contents of all subdirectories into the root folder.
            Defaults to False.

    Returns:
        int: total number of files downloaded
    """

    return GitHubFileDownloader(repo_url, flatten_files=flatten, output_dir=output_dir).download()


@requires('requests', verbose=False)
def github_get_status(usr_name, repo_name=None) -> list[dict]:
    """
    Fetches GitHub repository status including stars, forks, issues, and pull requests.
    If the repository is forked, also fetches the star count of the original repository.
    If repo_name is not specified, returns details for all repositories under the user.

    Args:
        usr_name (str): GitHub username
        repo_name (str, optional): Name of the repository. Defaults to None.

    Returns:
        list: A list of dictionaries containing the status of the repositories.

    Example:
        >>> from pyufunc import github_get_status
        >>> github_get_status("xyluo25", "pyufunc")
        [{'name': 'pyufunc',
        'stars': 1,
        'forks': 0,
        'issues': 0,
        'pull_requests': 0,
        'original_stars': None}]

    """
    import_package('requests', verbose=False)
    import requests

    print(f"  Collecting {usr_name} GitHub repository status...")
    base_url = "https://api.github.com/users"
    repo_details = []

    def get_repo_info(repo_url):
        """
        Helper function to fetch repository information including the star count of the original repository if forked.
        """

        repo_response = requests.get(repo_url)
        repo = repo_response.json()
        repo_url = repo['url']  # Using the URL directly from the repo data
        prs_count = get_pull_requests_count(repo_url)
        repo_info = {
            "name": repo['name'],
            "stars": repo.get('stargazers_count', 0),
            "forks": repo.get('forks_count', 0),
            "issues": repo.get('open_issues_count', 0),
            "pull_requests": prs_count,
            "original_stars": None  # Default value
        }

        if repo['fork']:
            # Fetch the original repository's star count
            with contextlib.suppress(Exception):
                original_repo_url = repo['source']['url']
                original_repo_response = requests.get(original_repo_url)
                original_repo_data = original_repo_response.json()
                repo_info['original_stars'] = original_repo_data.get('stargazers_count', 0)
        return repo_info

    def get_pull_requests_count(repo_url):
        """
        Helper function to fetch the count of open pull requests for a repository.

        Parameters:
        - repo_url: URL of the repository

        Returns:
        The count of open pull requests.
        """
        prs_url = f"{repo_url}/pulls?state=open"
        prs_response = requests.get(prs_url)
        prs_data = prs_response.json()
        return len(prs_data)

    if repo_name:
        try:
            # Fetch details for a specific repository
            repo_url = f"https://api.github.com/repos/{usr_name}/{repo_name}"
            repo_details.append(get_repo_info(repo_url))
        except Exception as e:
            print(f"Error: {e}")
    else:
        # Fetch all repositories for the user
        try:
            user_repos_url = f"{base_url}/{usr_name}/repos?page=1&per_page=1000"
            repos_response = requests.get(user_repos_url)
            repos_data = repos_response.json()
            repo_url_all = [repo['url'] for repo in repos_data]

            for repo_url_single in repo_url_all:
                repo_details.append(get_repo_info(repo_url_single))
        except Exception as e:
            print(f"Error: {e}")

    return repo_details


def github_private_file_downloader(raw_url: str, token: str, dest_path: str) -> bool:
    """
    Download a file (e.g. a ZIP) from a private GitHub repository given its
    raw/blob URL, using a personal access token for authentication.

    Args:
        raw_url (str): Either a raw.githubusercontent.com URL:
                       https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}
                       or a GitHub blob URL:
                       https://github.com/{owner}/{repo}/blob/{ref}/{path}
        token (str):  Personal access token with `repo` scope.
        dest_path (str): Local path where the file will be written.
    """
    # parse URL
    parsed = urlparse(raw_url)
    parts = parsed.path.strip("/").split("/")
    if parsed.netloc == "github.com":
        # blob URL: /{owner}/{repo}/blob/{ref}/{path…}
        owner, repo, blob, ref = parts[:4]
        if blob != "blob":
            raise ValueError("Expected a /blob/ URL")
        file_path = "/".join(parts[4:])
    elif parsed.netloc == "raw.githubusercontent.com":
        # raw URL: /{owner}/{repo}/{ref}/{path…}
        owner, repo, ref = parts[:3]
        file_path = "/".join(parts[3:])
    else:
        raise ValueError(
            "URL must be raw.githubusercontent.com or github.com blob URL")

    # construct Contents API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"  # <-- ask for raw file bytes
    }
    params = {"ref": ref}

    # stream download
    with requests.get(api_url, headers=headers, params=params, stream=True) as r:
        r.raise_for_status()  # will surface 404 / 401 / etc.
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
    return True
