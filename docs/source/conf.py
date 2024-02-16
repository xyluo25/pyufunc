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


# -- Project information -----------------------------------------------------
project = 'pyufunc Guide'
copyright = '2023-, Xiangyong Luo'
author = 'Xiangyong Luo'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# 'sphinx.ext.napoleon'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
root_doc = 'index'
language = 'en'
source_suffix = {'.rst': 'restructuredtext'}


# Add any paths that contain templates here, relative to this directory.
templates_path = []
html_static_path = []

# html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = 'footnote'
