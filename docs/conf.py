# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, June 30th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import sys
from pathlib import Path

home_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(home_dir))
# sys.path.insert(0, str(home_dir / 'my_readthedocs'))
from multiproject.utils import get_project

# -- Project information -----------------------------------------------------
project = 'pyufunc Guide'
copyright = '2023-, Xiangyong Luo'
author = 'Xiangyong Luo'

# The full version, including alpha/beta/rc tags
release = '0.1.3'


# 'sphinx.ext.napoleon'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    "hoverxref.extension",
    "multiproject",
    "myst_parser",
    "notfound.extension",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_search.extension",
    "sphinx_tabs.tabs",
    "sphinx-prompt",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.httpdomain",
    "sphinxcontrib.video",
    "sphinxemoji.sphinxemoji",
    "sphinxext.opengraph"]


multiproject_projects = {
    "user": {
        "use_config_file": False,
        "config": {
            "project": "Read the Docs user documentation",
            "html_title": "Read the Docs user documentation",
        },
    },
    "dev": {
        "use_config_file": False,
        "config": {
            "project": "Read the Docs developer documentation",
            "html_title": "Read the Docs developer documentation",
        },
    },
}
root_doc = 'index'
language = 'en'
source_suffix = {'.rst': 'restructuredtext'}


# Add any paths that contain templates here, relative to this directory.
templates_path = []
html_static_path = []

# html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = 'footnote'
