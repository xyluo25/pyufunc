## Message From PyUFunc Developers

This document serves as a curated compendium of existing utility functions, meticulously organized by keywords to facilitate ease of navigation and application for developers across various disciplines. By categorizing these functions, we aim to provide a structured overview that not only simplifies the discovery process but also encourages the exploration of new methods and techniques that may have been previously overlooked. This categorization is intended to serve as a bridge, connecting developers with the tools they need to optimize their code, improve functionality, and innovate within their projects.

The categories outlined in this document span a wide range of functionalities, each category is accompanied by a brief description, followed by a list of utility functions that fall under its umbrella, this comprehensive approach aims to arm developers with a robust toolkit, enabling them to select the most appropriate utility functions for their specific needs. Whether you are working on a complex application requiring advanced data manipulation or a simple project needing basic string operations, this guide endeavors to provide a valuable resource that enhances your development process and leads to more efficient, effective, and elegant coding solutions.

## Existing Utility Functions by Category

Note: we may not update available functions in time, please run code below to check latest available functions.

```python
pyufunc.show_util_func_by_category()
```

Available utility functions in pyUFunc (81):

- util_ai:
  - mean_absolute_error
  - mean_absolute_percentage_error
  - mean_percentage_error
  - mean_squared_error
  - mean_squared_log_error
  - r2_score
  - root_mean_squared_error

- util_algorithm:
  - bubble_sort
  - quick_sort
  - selection_sort

- util_common:
  - generate_password
  - show_docstring_google
  - show_docstring_headers
  - show_docstring_numpy

- util_data_processing:
  - cvt_int_to_alpha
  - split_dict_by_chunk
  - split_list_by_equal_sublist
  - split_list_by_fixed_length

- util_datetime:
  - cvt_dt_to_tz
  - fmt_dt_to_str
  - get_time_diff_in_unit
  - get_timezone
  - group_dt_daily
  - group_dt_hourly
  - group_dt_minutely
  - group_dt_monthly
  - group_dt_weekly
  - group_dt_yearly
  - list_all_timezones

- util_geo:
  - calc_distance_on_unit_sphere
  - create_circle_at_point_with_radius
  - find_closest_point
  - find_k_nearest_points
  - get_coordinates_from_geom
  - gmns_geo
  - proj_point_to_line

- util_git_pypi:
  - github_file_downloader
  - github_get_status
  - pypi_downloads

- util_img:
  - cvt_img_bytes_to_PIL_img
  - cvt_img_CV_to_PIL
  - cvt_img_PIL_to_CV
  - cvt_img_to_bytes
  - cvt_PIL_img_to_bytes
  - img_resize
  - img_rotate
  - img_rotate_bound
  - img_show
  - img_translate
  - is_CV_img
  - is_PIL_img

- util_network:
  - get_host_ip
  - validate_url

- util_office:
  - is_valid_email
  - send_email

- util_pathio:
  - add_dir_to_env
  - check_filename
  - check_files_existence
  - check_platform
  - create_tempfile
  - generate_unique_filename
  - get_dir_size
  - get_file_size
  - get_filenames_by_ext
  - is_linux
  - is_mac
  - is_windows
  - path2linux
  - path2uniform
  - remove_file

- pkg_utils:
  - find_util_func_by_keyword
  - func_running_time
  - func_time
  - get_user_defined_func
  - import_package
  - is_module_importable
  - is_user_defined_func
  - requires
  - run_parallel
  - show_util_func_by_category
  - show_util_func_by_keyword
