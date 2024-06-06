.. _install:

============
Installation
============

The easiest way to install pyufunc is to install it
as part of the `Anaconda <https://docs.continuum.io/free/anaconda/>`__ distribution, a
cross platform distribution for data analysis and scientific computing.
The `Conda <https://conda.io/en/latest/>`__ package manager is the
recommended installation method for most users.

.. _install.version:

Python version support
----------------------

Officially Python 3.9 or higher.

Installing pyufunc
------------------


Installing from PyPI
~~~~~~~~~~~~~~~~~~~~

pyufunc can be installed via pip from
`PyPI <https://pypi.org/project/pyufunc>`__.

.. code-block:: python

    pip install pyufunc

.. note::

    It is recommended to install and run pyufunc from a virtual environment, for example,
    using the Python standard library's `venv <https://docs.python.org/3/library/venv.html>`__

Handling ImportErrors
~~~~~~~~~~~~~~~~~~~~~

If you encounter an ``ImportError``, it usually means that Python couldn't find pyufunc in the list of available
libraries. Python internally has a list of directories it searches through, to find packages. You can
obtain these directories with.

.. code-block:: python

    import sys
    sys.path

One way you could be encountering this error is if you have multiple Python installations on your system
and you don't have pyufunc installed in the Python installation you're currently using.
In Linux/Mac you can run ``which python`` on your terminal and it will tell you which Python installation you're
using. If it's something like "/usr/bin/python", you're using the Python from the system, which is not recommended.

It is highly recommended to use ``conda``, for quick installation and for package and dependency updates.


Dependencies
------------


Required dependencies
~~~~~~~~~~~~~~~~~~~~~

pyufunc requires **no** dependencies.

updating...

.. ================================================================ ==========================
.. Package                                                          Minimum supported version
.. ================================================================ ==========================
.. `NumPy <https://numpy.org>`__                                    1.23.5
.. `python-dateutil <https://dateutil.readthedocs.io/en/stable/>`__ 2.8.2
.. `pytz <https://pypi.org/project/pytz/>`__                        2020.1
.. `tzdata <https://pypi.org/project/tzdata/>`__                    2022.7
.. ================================================================ ==========================
