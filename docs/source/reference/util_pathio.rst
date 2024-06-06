{{ header }}

.. _api.util_pathio:

===========
util_pathio
===========
.. currentmodule:: pyufunc

path
~~~~
.. autosummary::
   :toctree: api/

   path2linux
   path2uniform
   get_filenames_by_ext
   get_files_by_ext
   check_files_in_dir
   check_filename
   check_file_existence
   generate_unique_filename
   create_unique_filename
   show_dir_in_tree

io
~~~
.. autosummary::
   :toctree: api/

   get_file_size
   get_dir_size
   create_tempfile
   remove_file
   add_dir_to_env
   pickle_save
   pickle_load

platform
~~~~~~~~
.. autosummary::
   :toctree: api/

   check_platform
   is_windows
   is_linux
   is_mac
   get_terminal_width
   get_terminal_height
