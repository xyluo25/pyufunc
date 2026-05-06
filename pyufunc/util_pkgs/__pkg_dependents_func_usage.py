# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 6th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
###############################################################

from __future__ import annotations

import ast
import builtins
import os
import re
import time
import base64
import warnings
from typing import Dict, Set, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
from pathlib import Path

from pyufunc.util_magic import requires

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from requests import Session, Response  # pyright: ignore[reportMissingModuleSource]
    from bs4 import BeautifulSoup  # pyright: ignore[reportMissingImports]


_PYTHON_BUILTIN_FUNCTION_NAMES = {
    name for name in dir(builtins) if callable(getattr(builtins, name))
}


@requires("requests", ("beautifulsoup4", "bs4"), "tqdm")
def pkg_dependents_func_usage(github_link: str, *, GITHUB_TOKEN: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Collect public GitHub dependents of a repository and detect which functions
    from the target package are used by each dependent.

    Args:
        github_link: URL of the target GitHub repository.
        GITHUB_TOKEN: Optional GitHub token for authenticated requests. Can also
            be set via the GITHUB_TOKEN environment variable.

    Notes:
        - This function relies on GitHub's web UI for dependents collection, which
          may be subject to change and rate limits. Use a token to increase the
          rate limit if you have many dependents.
          unauthorized requests have very low rate limits (60 requests per hour)
          authenticated requests can have much higher limits (up to 5000 requests per hour).
        - The function usage detection is based on static analysis of Python files
          in the dependent repositories. It may not be 100% accurate but should
          give a good indication of which functions are used.
        - This function targets Python packages and Python dependent repositories.
        - GitHub does not provide a stable official REST API for dependents, so
            the dependents page is scraped.
        - Set environment variable GITHUB_TOKEN for better rate limits:
            Windows PowerShell:
                $env:GITHUB_TOKEN="ghp_xxx"
            Linux/macOS:
                export GITHUB_TOKEN="ghp_xxx"
        - For very popular packages, scanning all dependents can be slow.

    Example:
        >>> github_url = ""
        >>> github_token = "" # Optional
        >>> result = pkg_dependents_func_usage(github_url, GITHUB_TOKEN=github_token)

    Returns:
        dict: A dictionary mapping each dependent repository (in "owner/repo" format)
            to a list of function names from the target package that are used in that dependent.
            If there was an error processing a dependent, the list will contain an error message. Dict[str, List[str]]:
            {
                "dependent_owner/dependent_repo": ["func_a", "module.func_b", ...],
                ...
            }

    """
    import requests
    from tqdm import tqdm

    token = GITHUB_TOKEN or os.getenv("GITHUB_TOKEN")
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    )
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})

    owner, repo = _parse_github_repo(github_link)
    package_name = _infer_python_package_name(session, owner, repo) or repo.replace("-", "_")

    dependents = _collect_dependents_from_github_ui(
        session=session,
        owner=owner,
        repo=repo,
        max_pages=20,
        sleep_seconds=1.0,
    )

    result: Dict[str, list[str]] = {}

    for dep_full_name in tqdm(dependents,
                              desc="Processing dependents"):
        dep_owner, dep_repo = dep_full_name.split("/", 1)

        try:
            python_files = _get_python_files_from_repo(
                session=session,
                owner=dep_owner,
                repo=dep_repo,
                max_files=300,
                max_file_size=300_000,
            )

            used_functions: list[str] = []

            for file_path, source_code in python_files:
                used_functions.extend(
                    _extract_used_functions_from_source(
                        source_code=source_code,
                        package_name=package_name,
                    )
                )

            result[dep_full_name] = used_functions

        except Exception as exc:
            # Keep the dependent in the result so the user knows it was found.
            result[dep_full_name] = [f"__ERROR__: {type(exc).__name__}: {exc}"]

    return result


def _parse_github_repo(github_link: str) -> Tuple[str, str]:
    parsed = urlparse(github_link.rstrip("/"))

    if parsed.netloc.lower() != "github.com":
        raise ValueError("The input must be a GitHub repository URL.")

    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) < 2:
        raise ValueError(
            "Invalid GitHub repository URL. Expected format: "
            "https://github.com/{owner}/{repo}"
        )

    owner, repo = parts[0], parts[1]
    repo = repo.removesuffix(".git")
    return owner, repo


def _github_get(session: Session, url: str, **kwargs) -> Response:
    headers = kwargs.pop("headers", {})
    if url.startswith("https://api.github.com/"):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            **headers,
        }

    response = session.get(url, timeout=30, headers=headers, **kwargs)

    if response.status_code == 403:
        raise RuntimeError(
            "GitHub returned 403. You may be rate limited. "
            "Set GITHUB_TOKEN to increase the rate limit."
        )

    if response.status_code == 404:
        raise RuntimeError(f"GitHub returned 404 for: {url}")

    response.raise_for_status()
    return response


def _github_get_html(session: Session, url: str, **kwargs) -> Response:
    headers = kwargs.pop("headers", {})
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        **headers,
    }
    return _github_get(session, url, headers=headers, **kwargs)


def _infer_python_package_name(
    session: Session,
    owner: str,
    repo: str,
) -> Optional[str]:
    """
    Try to infer the import package name from pyproject.toml or setup.py.
    Falls back to repository name outside this function.
    """
    candidates = [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
    ]

    for path in candidates:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

        try:
            response = _github_get(session, url)
            if response.status_code != 200:
                continue

            data = response.json()
            content = data.get("content")
            encoding = data.get("encoding")

            if not content or encoding != "base64":
                continue

            text = base64.b64decode(content).decode("utf-8", errors="replace")

            if path == "pyproject.toml":
                match = re.search(r'(?m)^\s*name\s*=\s*["\']([^"\']+)["\']', text)
                if match:
                    return match.group(1).replace("-", "_")

            if path == "setup.py":
                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', text)
                if match:
                    return match.group(1).replace("-", "_")

            if path == "setup.cfg":
                match = re.search(r'(?m)^\s*name\s*=\s*([A-Za-z0-9_.-]+)', text)
                if match:
                    return match.group(1).replace("-", "_")

        except Exception:
            continue

    return None


@requires(("beautifulsoup4", "bs4"))
def _collect_dependents_from_github_ui(
    session: Session,
    owner: str,
    repo: str,
    max_pages: int = 20,
    sleep_seconds: float = 1.0,
) -> List[str]:
    """
    Scrape GitHub's /network/dependents page.

    GitHub may change this page structure. This function uses multiple fallback
    selectors to make the scraper more robust.
    """
    from bs4 import BeautifulSoup  # pyright: ignore[reportMissingImports]

    start_url = f"https://github.com/{owner}/{repo}/network/dependents"
    current_url = start_url

    dependents: List[str] = []
    seen = set()

    for _ in range(max_pages):
        response = _github_get_html(session, current_url)
        soup = BeautifulSoup(response.text, "html.parser")

        page_dependents = _extract_repo_links_from_dependents_page(
            soup=soup,
            target_owner=owner,
            target_repo=repo,
        )

        for full_name in page_dependents:
            if full_name not in seen:
                seen.add(full_name)
                dependents.append(full_name)

        next_url = _find_next_page_url(soup, current_url)

        if not next_url:
            break

        current_url = next_url
        time.sleep(sleep_seconds)

    return dependents


def _extract_repo_links_from_dependents_page(
    soup: BeautifulSoup,
    target_owner: str,
    target_repo: str,
) -> List[str]:
    repo_pattern = re.compile(r"^/([^/\s]+)/([^/\s]+)$")

    dependents = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        match = repo_pattern.match(href)

        if not match:
            continue

        owner, repo = match.group(1), match.group(2)

        # Skip the original target repository.
        if owner.lower() == target_owner.lower() and repo.lower() == target_repo.lower():
            continue

        # Skip GitHub internal or non-repository paths.
        if owner in {"features", "marketplace", "topics", "collections", "settings"}:
            continue

        full_name = f"{owner}/{repo}"

        # The dependents page usually contains repeated repo links.
        if full_name not in dependents:
            dependents.append(full_name)

    return dependents


def _find_next_page_url(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """
    Find GitHub pagination next URL.
    """
    link_tag = soup.find("a", rel="next")
    if link_tag and link_tag.get("href"):
        return urljoin(current_url, link_tag["href"])

    # Fallback for GitHub pagination button text.
    for a_tag in soup.find_all("a", href=True):
        text = a_tag.get_text(strip=True).lower()
        if text == "next":
            return urljoin(current_url, a_tag["href"])

    return None


def _get_python_files_from_repo(
    session: Session,
    owner: str,
    repo: str,
    max_files: int = 300,
    max_file_size: int = 300_000,
) -> List[Tuple[str, str]]:
    """
    Use GitHub API to recursively list repository files and download Python files.
    """
    repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_info = _github_get(session, repo_api_url).json()

    default_branch = repo_info.get("default_branch", "main")

    tree_url = (
        f"https://api.github.com/repos/{owner}/{repo}/git/trees/"
        f"{default_branch}?recursive=1"
    )
    tree_data = _github_get(session, tree_url).json()

    files = []
    tree = tree_data.get("tree", [])

    py_items = [
        item
        for item in tree
        if item.get("type") == "blob"
        and item.get("path", "").endswith(".py")
        and item.get("size", 0) <= max_file_size
    ]

    for item in py_items[:max_files]:
        path = item["path"]
        raw_url = (
            f"https://raw.githubusercontent.com/"
            f"{owner}/{repo}/{default_branch}/{path}"
        )

        try:
            response = session.get(raw_url, timeout=30)
            if response.status_code == 200:
                files.append((path, response.text))
        except Exception:
            continue

    return files


def _extract_used_functions_from_source(
    source_code: str,
    package_name: str,
) -> Set[str]:
    """
    Extract functions from the target package used in a Python source file.

    Supported patterns:
        import package
        import package as pkg
        import package.module
        from package import func
        from package.module import func
        package.func()
        package.module.func()
        alias.func()
        imported_func()
    """
    used_functions: Set[str] = set()

    try:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r".*invalid escape sequence.*",
                category=SyntaxWarning,
            )
            tree = ast.parse(source_code)
    except SyntaxError:
        return used_functions

    package_aliases: Set[str] = set()
    module_aliases: Dict[str, str] = {}
    imported_functions: Dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name

                if name == package_name:
                    package_aliases.add(alias.asname or package_name)

                elif name.startswith(package_name + "."):
                    local_name = alias.asname or name.split(".")[-1]
                    module_path = name
                    module_aliases[local_name] = module_path

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""

            if module == package_name:
                for alias in node.names:
                    local_name = alias.asname or alias.name
                    imported_functions[local_name] = alias.name

            elif module.startswith(package_name + "."):
                for alias in node.names:
                    local_name = alias.asname or alias.name
                    imported_functions[local_name] = f"{module}.{alias.name}".replace(
                        package_name + ".", ""
                    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func

            # Case 1: imported_func()
            if isinstance(func, ast.Name):
                if func.id in imported_functions:
                    _add_used_function(
                        used_functions=used_functions,
                        function_name=imported_functions[func.id],
                    )

            # Case 2: package.func(), package.module.func(), alias.func()
            elif isinstance(func, ast.Attribute):
                full_attr = _ast_attribute_to_string(func)

                if not full_attr:
                    continue

                root_name = full_attr.split(".", 1)[0]

                if root_name in package_aliases:
                    _add_used_function(
                        used_functions=used_functions,
                        function_name=full_attr.split(".", 1)[1],
                    )

                elif root_name in module_aliases:
                    module_path = module_aliases[root_name]
                    cleaned_module_path = module_path.replace(package_name + ".", "")
                    _add_used_function(
                        used_functions=used_functions,
                        function_name=(
                            f"{cleaned_module_path}.{full_attr.split('.', 1)[1]}"
                        ),
                    )

    return used_functions


def _add_used_function(used_functions: Set[str], function_name: str) -> None:
    short_name = function_name.rsplit(".", 1)[-1]

    if short_name in _PYTHON_BUILTIN_FUNCTION_NAMES:
        return

    used_functions.add(function_name)


def _ast_attribute_to_string(node: ast.AST) -> Optional[str]:
    """
    Convert an AST attribute chain to a dotted string.

    Example:
        package.module.func -> "package.module.func"

    """
    parts = []

    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value

    if isinstance(node, ast.Name):
        parts.append(node.id)
    else:
        return None

    return ".".join(reversed(parts))


def save_dict_to_json(filename: str, data: Dict, *, output_dir: str = ".") -> None:
    """
    Save a dictionary to a JSON file with pretty formatting.

    Args:
        filename (str): The name of the output JSON file.
        data (Dict): The dictionary to save.
        output_dir (str): The directory where the JSON file will be saved.

    """
    import json

    # Check if filename is a github url, if so, extract the repo name and use it as filename
    if re.match(r"https?://github\.com/[^/\s]+/[^/\s]+", filename):
        filename = filename.rstrip("/").split("/")[-1]

    # Check if .json extension is present, if not add it
    if not Path(filename).suffix == ".json":
        filename += ".json"

    file_path = Path(output_dir) / filename

    # Ensure the directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    github_url = "https://github.com/mikeqfu/pyhelpers"
    result = pkg_dependents_func_usage(github_url)
    save_dict_to_json(filename="pyhelpers",
                      data=result,
                      output_dir="datasets/util_pkgs_dependents_func_usage")

    for dependent, functions in result.items():
        print(dependent, functions)