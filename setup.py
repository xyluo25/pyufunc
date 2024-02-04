# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, July 12th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import pyufunc as uf
import setuptools

with open("README_pkg.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    # if have requirements.txt file inside the folder
    with open("requirements.txt", "r", encoding="utf-8") as f:
        modules_needed = [i.strip() for i in f.readlines()]
except Exception:
    modules_needed = []

setuptools.setup(
    name=uf.pkg_name,  # Replace with your own username
    version=uf.pkg_version,
    author=uf.pkg_author,
    author_email=uf.pkg_email,

    keywords=["utility functions", "utility", "functions", "common functions", "common utility functions"]
    description="A tool for generating zone-to-zone travel demand based on grid zones and gravity model",

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xyluo25/pyufunc",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
    python_requires='>=3.10',
    install_requires=modules_needed,

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.xls', '*.xlsx', '*.csv'],
                  "test_data": ['*.xls']},
    project_urls={
        'Homepage': "https://github.com/xyluo25/pyufunc",
        # 'Documentation': 'https://github.com/asu-trans-ai-lab/grid2demand',
        # 'Bug Tracker': '',
        # 'Source Code': '',
        # 'Download': '',
        # 'Publication': '',
        # 'Citation': '',
        # 'License': '',
        # 'Acknowledgement': '',
        # 'FAQs': '',
        # 'Contact': '',
    },
    platforms=["all"],
    license='Apache License 2.0',
)
