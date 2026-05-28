# Third-Party License Information

pyufunc is licensed under the MIT License. See [LICENSE](LICENSE).

This file summarizes third-party packages that pyufunc wraps or uses for optional utility functions. These packages are not vendored in pyufunc and are not installed automatically by pyufunc. Most wrappers import the source package at runtime only when the related function is called.

The license values below are based on upstream package metadata and repository license information checked on 2026-05-28. Users with redistribution or compliance requirements should verify the current upstream license before redistributing third-party packages.

## Optional Wrapper and Runtime Packages

| Package | Used by | License | Upstream / License Source |
| --- | --- | --- | --- |
| `psutil` | `pyufunc.util_pkgs._psutil` | BSD-3-Clause | https://github.com/giampaolo/psutil |
| `pyhelpers` | `pyufunc.util_pkgs._pyhelpers` | MIT | https://github.com/mikeqfu/pyhelpers |
| `pyutil` | `pyufunc.util_pkgs._pyutil` | GPL-2.0-or-later | https://github.com/tpltnt/pyutil |
| `imutils` | `pyufunc.util_pkgs._imutils` | MIT | https://github.com/PyImageSearch/imutils |
| `opencv-python` | Runtime dependency for `imutils` image helpers | Apache-2.0 | https://github.com/opencv/opencv-python |
| `platformdirs` | `pyufunc.util_pkgs._platformdirs` | MIT | https://github.com/tox-dev/platformdirs |
| `filelock` | `pyufunc.util_pkgs._filelock` | MIT | https://github.com/tox-dev/py-filelock |
| `pathspec` | `pyufunc.util_pkgs._pathspec` | MPL-2.0 | https://github.com/cpburnz/python-pathspec |
| `more-itertools` | `pyufunc.util_pkgs._more_itertools` | MIT | https://github.com/more-itertools/more-itertools |
| `humanize` | `pyufunc.util_pkgs._humanize` | MIT | https://github.com/python-humanize/humanize |
| `tenacity` | `pyufunc.util_pkgs._tenacity` | Apache-2.0 | https://github.com/jd/tenacity |
| `boltons` | `pyufunc.util_pkgs._boltons` | BSD | https://github.com/mahmoud/boltons |
| `toolz` | `pyufunc.util_pkgs._toolz` | BSD | https://github.com/pytoolz/toolz |
| `python-benedict` | `pyufunc.util_pkgs._python_benedict` | MIT | https://github.com/fabiocaccamo/python-benedict |
| `loguru` | `pyufunc.util_pkgs._loguru` | MIT | https://github.com/Delgan/loguru |
| `requests` | `pkg_dependents_func_usage` optional helper | Apache-2.0 | https://github.com/psf/requests |
| `beautifulsoup4` | `pkg_dependents_func_usage` optional helper | MIT | https://www.crummy.com/software/BeautifulSoup/bs4/ |
| `tqdm` | `pkg_dependents_func_usage` optional helper | MPL-2.0 AND MIT | https://github.com/tqdm/tqdm |

## Notes

- `pyutil` is GPL-2.0-or-later. pyufunc does not vendor `pyutil` implementation code; the related wrappers import `pyutil` at runtime only when the optional package is installed.
- `pathspec` is MPL-2.0. pyufunc does not vendor `pathspec` implementation code; the related wrappers import `pathspec` at runtime only when the optional package is installed.
- If future changes copy third-party implementation code into pyufunc, the copied code must keep the required upstream copyright and license notices.
- If any attribution or license entry is inaccurate, please open an issue or contact the maintainers so the notice can be corrected.
