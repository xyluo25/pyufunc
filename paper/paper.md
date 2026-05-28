---
title: 'pyufunc: A Categorized Collection of Python Utility Functions'
tags:
  - Python
  - utilities
  - software reuse
  - packaging
  - documentation
authors:
  - name: Xiangyong Luo
    orcid: "0009-0003-1290-9983"
    affiliation: "1"
  - name: Xuesong Simon Zhou
    orcid: "0000-0002-9963-5369"
    affiliation: "1"
affiliations:
  - name: Arizona State University, United States
    index: 1
date: 28 May 2026
bibliography: paper.bib
---

# Summary

`pyufunc` is a Python package that collects utility functions for recurring
programming tasks, including path and file handling, date and time conversion,
data processing, testing helpers, image utilities, geographic helpers, and
selected wrappers around third-party utility packages. The package provides a
categorized public API so that users can inspect available helpers by category
or keyword before importing a specific function.

The current package design emphasizes documented, reviewable utility code
rather than novelty in a single algorithmic method. Version 0.5.1 exposes more
than 250 public utility entries, including optional wrappers for selected
packages whose source package, repository, documentation, and license are
recorded in function docstrings and repository-level third-party license
metadata.

# Statement of need

Small helper functions are common in research software. They are often copied
between projects, rewritten with minor differences, or hidden inside local
scripts where they are difficult to test and document consistently. This pattern
can make research code harder to maintain because behavior that appears simple,
such as path normalization, date conversion, dictionary traversal, file locking,
or retry logic, may still need clear inputs, errors, examples, and dependency
handling.

`pyufunc` addresses this maintenance problem by grouping selected helpers into a
single package with type hints, tests, and generated documentation. The target
users are Python developers and researchers who need small, reusable functions
while maintaining readable project code. The package is particularly relevant to
research workflows where scripts combine file operations, tabular data
preparation, time handling, image or geospatial preprocessing, and lightweight
testing utilities in the same project.

The project does not claim that every included function is widely used or that
the package improves runtime performance in general. Instead, package selection
is documented through public metadata, review tables, and exploratory
dependent-repository scans stored in the repository. These records define the
current evidence boundary for utility selection.

# State of the field

The Python ecosystem already includes mature packages that solve specialized
utility problems. Examples include `psutil` for system monitoring [@psutil],
`dateutil` for date and time extensions [@dateutil], `imutils` for image
processing convenience functions [@imutils], `pyhelpers` for data and path
helpers [@Fu_PyHelpers_2020], and `pyutil` for general helper functions
[@pyutil]. These packages remain the appropriate primary dependencies when a
project needs their broader APIs.

`pyufunc` was developed as a collection and documentation layer rather than as a
replacement for those projects. The build-versus-contribute decision follows
from the package scope: the objective is to expose a categorized, cross-domain
set of small helpers and thin optional wrappers under one namespace, while
preserving attribution to source packages and avoiding vendoring their code.
Contributing every selected helper to a single upstream package would not
address cross-domain API discovery, and contributing unrelated file, date,
image, testing, and system helpers to many separate projects would not provide a
common documentation and dependency-handling model for users.

# Software design

The package is organized by utility domain, with modules for categories such as
path input/output, data processing, datetime, images, geographic utilities,
testing, logging, networking, and third-party package wrappers. Public function
indexes are generated for category-based and keyword-based discovery, and the
Read the Docs API reference is generated from the same public API surface.

The `util_pkgs` subpackage contains thin wrappers around selected third-party
packages. These wrappers are intentionally narrow: they provide concise entry
points for common operations, retain source attribution in the docstrings, and
defer to the upstream package implementation at runtime. Third-party packages
are not vendored. Optional dependencies are also not installed automatically by
default; missing packages are reported to the user, and explicit installation is
left to the environment owner. This design avoids surprising network access in
continuous-integration or offline environments.

The main tradeoff is API size. A larger utility namespace can reduce repeated
local helper code, but it can also increase search and selection overhead.
`pyufunc` mitigates this through categorized indexes, keyword search helpers,
examples, tests, and clear dependency behavior. The package also carries
maintenance responsibilities for license attribution, compatibility with
upstream packages, and test coverage across multiple utility domains.

# Research impact statement

The current evidence for `pyufunc` is strongest as community-ready research
software infrastructure. The repository includes packaging metadata, tests,
continuous-integration configuration, generated API documentation, a changelog,
contribution guidance, third-party license notices, and package-selection
evidence. The package review table records metadata for 92 candidate packages
listed in the project guidance, including PyPI version badges, download badges
where available, GitHub latest-commit badges, repository links, license
metadata, and descriptions.

Exploratory dependent-usage datasets are stored under
`datasets/util_pkgs_dependents_func_usage`. In the current checked-in data,
`psutil.json` records 35 valid function references across 5 dependent
repositories, `pyhelpers.json` records 175 valid function references across 4
dependent repositories, and `pyutil.json` records 20 valid function references
across 13 dependent repositories. These scans are incomplete because GitHub
dependent pages are rate-limited, private repositories are not visible, and
static analysis does not capture every dynamic call. They are therefore used as
selection evidence, not as a complete frequency measurement.

The practical research contribution is a maintained utility layer that helps
research teams keep common helper behavior documented, tested, and attributable.
This is useful when utility code supports reproducible workflows but is not the
primary scientific method itself.

# AI usage disclosure

OpenAI Codex, based on GPT-5, was used during recent maintenance to assist with
code review, documentation updates, and manuscript editing. Human authors made
the project design decisions, reviewed and edited AI-assisted outputs, and
remain responsible for the correctness, licensing, and originality of the
submitted software and paper.

# Acknowledgements

This open-source package was supported by the National Science Foundation under
grant no. TIP-2303748, "POSE: Phase II: CONNECT: Consortium of Open-source
Planning Models for Next-generation Equitable and Efficient Communities and
Transportation."

Additional support was provided by the U.S. Department of Energy, Office of
Energy Efficiency and Renewable Energy, Vehicle Technologies Office. Any
opinions, findings, conclusions, or recommendations expressed in this material
are those of the authors and do not necessarily reflect the views of the U.S.
Department of Transportation, the U.S. Department of Energy, or the U.S.
Government.

# References
