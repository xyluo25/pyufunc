## Message From PyUFunc Developers

This document serves as a curated compendium of existing utility functions, meticulously organized by keywords to facilitate ease of navigation and application for developers across various disciplines. By categorizing these functions, we aim to provide a structured overview that not only simplifies the discovery process but also encourages the exploration of new methods and techniques that may have been previously overlooked. This categorization is intended to serve as a bridge, connecting developers with the tools they need to optimize their code, improve functionality, and innovate within their projects.

The categories outlined in this document span a wide range of functionalities, each category is accompanied by a brief description, followed by a list of utility functions that fall under its umbrella, this comprehensive approach aims to arm developers with a robust toolkit, enabling them to select the most appropriate utility functions for their specific needs. Whether you are working on a complex application requiring advanced data manipulation or a simple project needing basic string operations, this guide endeavors to provide a valuable resource that enhances your development process and leads to more efficient, effective, and elegant coding solutions.

## Existing Utility Functions by Category

Note: we may not update available functions in time, please run code below to check latest available functions.

```python
pyufunc.show_util_func_by_category()
```

Available utility functions in pyUFunc (53):

- util_common:
  - show_docstring_headers
  - show_docstring_google
  - show_docstring_numpy
  - generate_password

- util_data_processing:
  - split_dict_by_chunk
  - cvt_int_to_alpha
  - split_list_by_equal_sublist
  - split_list_by_fixed_length

- util_datetime:
  - fmt_dt_to_str
  - list_all_timezones
  - get_timezone
  - cvt_dt_to_tz
  - get_time_diff_in_unit
  - group_dt_yearly
  - group_dt_monthly
  - group_dt_weekly
  - group_dt_daily
  - group_dt_hourly
  - group_dt_minutely

- util_geo:
  - create_circle_at_point_with_radius
  - proj_point_to_line
  - calc_distance_on_unit_sphere
  - find_closest_point
  - get_coordinates_from_geom
  - find_k_nearest_points
  - gmns_geo

- util_git_pypi:
  - github_file_downloader
  - pypi_downloads
  - github_get_status

- util_network:
  - get_host_ip
  - validate_url

- util_pathio:
  - get_file_size
  - get_dir_size
  - path2linux
  - path2uniform
  - get_filenames_by_ext
  - check_files_existence
  - check_filename
  - generate_unique_filename
  - check_platform
  - is_windows
  - is_linux
  - is_mac

- pkg_utils:
  - import_package
  - requires
  - func_running_time
  - func_time
  - run_parallel
  - get_user_defined_func
  - is_user_defined_func
  - is_module_importable
  - show_util_func_by_category
  - show_util_func_by_keyword
