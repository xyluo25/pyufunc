.. _getting_started:
.. If you update this toctree, also update the manual toctree in the
   main index.rst.template

.. toctree::
    :maxdepth: 2
    :hidden:

    install
    overview


===============
Getting started
===============

Installation
------------

.. grid:: 1 2 2 2
    :gutter: 4

    .. grid-item-card:: Prefer pip?
        :class-card: install-card
        :columns: 12 12 6 6
        :padding: 3

        pyufunc can be installed via pip from `PyPI <https://pypi.org/project/pyufunc>`__.

        ++++

        .. code-block:: bash

            pip install pyufunc

    .. grid-item-card:: In-depth instructions?
        :class-card: install-card
        :columns: 12
        :padding: 3

        Installing a specific version? Installing from source? Check the advanced
        installation page.

        +++

        .. button-ref:: install
            :ref-type: ref
            :click-parent:
            :color: secondary
            :expand:

            Learn more



Intro to pyufunc
----------------

pyufunc is a Python package that collects small helper functions for common
programming tasks. These helpers cover areas such as string cleanup, list
processing, date and time conversion, path and file handling, testing helpers,
image utilities, and selected wrappers around third-party packages.

Most functions are available directly from the top-level package:

.. code-block:: python

    import pyufunc as pf

    cleaned_text = pf.str_strip("  Hello     Python   ")
    print(cleaned_text)

You can think of pyufunc as a toolbox. You still choose the tool that fits your
task, but pyufunc gives you one place to look for common helpers.


Tutorials
---------

These tutorials are written for entry-level Python users. Each example can be
copied into a Python file and run from the terminal.

If you are new to Python packages, start with this pattern:

1. Install the package with ``pip``.
2. Import the package in Python.
3. Call one function.
4. Save the return value in a variable or print it.

Tutorial 1: install, import, and check the version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install pyufunc from PyPI:

.. code-block:: bash

    pip install pyufunc

Create a file named ``my_first_pyufunc.py`` and add:

.. code-block:: python

    import pyufunc as pf

    print(pf.__version__)

Run the file:

.. code-block:: bash

    python my_first_pyufunc.py

If Python prints a version number, pyufunc is installed and ready to use.


Tutorial 2: find a function before using it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pyufunc contains functions in different categories. You can inspect those
categories from Python.

.. code-block:: python

    import pyufunc as pf

    categories = pf.show_util_func_by_category(verbose=False)

    print(categories.keys())
    print(categories["util_data_processing"][:5])

You can also search by a word in the function name:

.. code-block:: python

    import pyufunc as pf

    time_functions = pf.find_util_func_by_keyword("time", verbose=False)
    print(time_functions)

Use this when you know the task, such as working with time, files, paths, or
lists, but do not know the exact function name yet.


Tutorial 3: clean text and convert simple values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example starts with messy text and a number stored as a string.

.. code-block:: python

    import pyufunc as pf

    message = "  Hello     Python   "
    clean_message = pf.str_strip(message)

    user_input = "42.9"
    user_number = pf.str_digit_to_int(user_input)

    print(clean_message)
    print(user_number)
    print(pf.is_float("3.14"))

Expected output:

.. code-block:: text

    Hello Python
    42
    True

This is useful when reading values from forms, text files, spreadsheets, or
command-line input.


Tutorial 4: convert text into a date and time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dates often begin as text, especially when they come from a CSV file or user
input. ``fmt_str_to_dt`` converts a text value into a Python ``datetime`` object.

.. code-block:: python

    import pyufunc as pf

    meeting_time = pf.fmt_str_to_dt("2026-05-28 09:30:00")

    print(meeting_time.year)
    print(meeting_time.month)
    print(meeting_time.day)
    print(meeting_time.hour)

Expected output:

.. code-block:: text

    2026
    5
    28
    9

After conversion, you can use normal Python date and time attributes such as
``year``, ``month``, ``day``, and ``hour``.


Tutorial 5: work with files safely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example creates a small text file, checks whether it exists, and asks
pyufunc for a safe filename to use if another file with the same name already
exists.

.. code-block:: python

    from pathlib import Path

    import pyufunc as pf

    note = Path("tutorial_note.txt")
    note.write_text("hello", encoding="utf-8")

    print(pf.check_filename(note))

    safe_name = pf.generate_unique_filename(note)
    print(safe_name.endswith("tutorial_note(1).txt"))

    note.unlink()

Expected output:

.. code-block:: text

    True
    True

The last line, ``note.unlink()``, deletes the small tutorial file after the
example runs.


Tutorial 6: split and flatten lists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists are one of the most common Python data structures. pyufunc includes helpers
for list cleanup and grouping.

.. code-block:: python

    import pyufunc as pf

    nested_numbers = [[1, 2], [3, 4], [5]]
    flat_numbers = pf.list_flatten_nested(nested_numbers)

    groups = list(pf.list_split_by_fixed_length(flat_numbers, fixed_length=2))

    print(flat_numbers)
    print(groups)

Expected output:

.. code-block:: text

    [1, 2, 3, 4, 5]
    [[1, 2], [3, 4], [5]]


Tutorial 7: understand optional dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pyufunc does not automatically install missing optional packages. This avoids
unexpected package installation in CI, offline, or security-sensitive
environments.

Some helper functions wrap third-party packages. If the package is not installed,
install it yourself before using that helper.

.. code-block:: python

    import pyufunc as pf

    humanize = pf.import_package("humanize")

    if humanize is None:
        print("Install the optional package with: pip install humanize")
    else:
        print(pf.human_file_size(1536))

This pattern is useful when sharing code with other users because it gives a
clear message when an optional package is missing.


Next steps
~~~~~~~~~~

- Use :ref:`api` when you want the full list of public functions.
- Use :ref:`api.util_pkgs` when you want helpers that wrap selected third-party
  utility packages.
- Use the `GitHub issue tracker <https://github.com/xyluo25/pyufunc/issues>`__
  to report unclear documentation or request a tutorial for a specific task.


