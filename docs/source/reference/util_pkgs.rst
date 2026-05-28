.. _api.util_pkgs:

=========
util_pkgs
=========

pyufunc includes selected wrappers around third-party utility packages. These
packages are maintained by their original projects; pyufunc documents source
package, repository, documentation, and license information in wrapper
docstrings. The wrappers are included as convenience APIs and should not be read
as a claim that every wrapped function is widely used or performance-improving.
Users should evaluate optional dependencies and project-specific tradeoffs before
using a wrapper in production code.


psutil
------
.. currentmodule:: pyufunc

CPU, memory, disk related utility functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   cpu_count
   cpu_percent
   cpu_times
   virtual_memory
   swap_memory
   disk_usage
   sensor_temperatures
   sensor_fans
   sensor_battery


pyhelpers
---------
.. currentmodule:: pyufunc

Common filesystem, serialization, string, and dictionary helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   cd
   confirmed
   fake_requests_headers
   find_similar_str
   load_data
   load_pickle
   merge_dicts
   osgb36_to_wgs84
   remove_punctuation
   resolve_dir
   save_data
   save_pickle
   update_dict_keys
   wgs84_to_osgb36


pyutil
------
.. currentmodule:: pyufunc

General-purpose helpers from pyutil
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   Version
   log_ceil
   pad_size
   precondition


imutils
-------
.. currentmodule:: pyufunc

Image and OpenCV convenience helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   auto_canny
   grab_contours
   is_cv2
   is_cv3
   is_cv4
   opencv2matplotlib
   resize
   rotate
   rotate_bound
   skeletonize
   translate
   url_to_image


platformdirs
------------
.. currentmodule:: pyufunc

Platform-specific application directories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   get_user_cache_dir
   get_user_config_dir
   get_user_data_dir
   get_user_log_dir


filelock
--------
.. currentmodule:: pyufunc

File locking and safe writes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   safe_write_json_with_lock
   safe_write_pickle_with_lock
   safe_write_text_with_lock
   with_file_lock


pathspec
--------
.. currentmodule:: pyufunc

Gitignore-style pattern matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   collect_files_excluding_gitignore
   filter_paths_by_gitignore
   is_path_ignored
   load_gitignore_patterns


more-itertools
--------------
.. currentmodule:: pyufunc

Iterable recipes and grouping helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   iter_chunked
   iter_flatten
   iter_split_when
   iter_unique
   iter_windowed


humanize
--------
.. currentmodule:: pyufunc

Human-readable formatting helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   human_file_size
   human_intcomma
   human_number
   human_time_delta


tenacity
--------
.. currentmodule:: pyufunc

Retry helpers
~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   retry_call
   retry_on_exception
   retry_with_backoff


boltons
-------
.. currentmodule:: pyufunc

Nested data, atomic file, string, and time helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   atomic_save_file
   flatten_iterable
   parse_timedelta_text
   remap_nested_dict
   slugify_text


toolz
-----
.. currentmodule:: pyufunc

Functional data helpers
~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   toolz_count_frequencies
   toolz_groupby_key
   toolz_merge_dicts
   toolz_pipe_call
   toolz_sliding_window


python-benedict
---------------
.. currentmodule:: pyufunc

Nested dictionary key-path helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   dict_flatten
   dict_get_by_path
   dict_set_by_path
   dict_to_json_safe
   dict_unflatten


loguru
------
.. currentmodule:: pyufunc

Logger setup helpers
~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   disable_logger
   enable_logger
   setup_file_logger
   setup_simple_logger


Package inspection
------------------
.. currentmodule:: pyufunc

Package public-function discovery and dependent usage helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autosummary::
   :toctree: api/

   pkg_dependents_func_usage
   pkg_public_func
   save_dict_to_json
