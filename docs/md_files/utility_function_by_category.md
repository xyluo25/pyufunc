## Message From PyUFunc Developers

This document serves as a curated compendium of existing utility functions, meticulously organized by keywords to facilitate ease of navigation and application for developers across various disciplines. By categorizing these functions, we aim to provide a structured overview that not only simplifies the discovery process but also encourages the exploration of new methods and techniques that may have been previously overlooked. This categorization is intended to serve as a bridge, connecting developers with the tools they need to optimize their code, improve functionality, and innovate within their projects.

The categories outlined in this document span a wide range of functionalities, each category is accompanied by a brief description, followed by a list of utility functions that fall under its umbrella, this comprehensive approach aims to arm developers with a robust toolkit, enabling them to select the most appropriate utility functions for their specific needs. Whether you are working on a complex application requiring advanced data manipulation or a simple project needing basic string operations, this guide endeavors to provide a valuable resource that enhances your development process and leads to more efficient, effective, and elegant coding solutions.

## Existing Utility Functions by Category

Note: we may not update available functions in time, please run code below to check latest available functions.

```python
pyufunc.show_util_func_by_category()
```

Available utility functions in pyUFunc (119):

- util_ai:
  - mean_absolute_error
  - mean_absolute_percentage_error
  - mean_percentage_error
  - mean_squared_error
  - mean_squared_log_error
  - r2_score
  - root_mean_squared_error

- util_algorithm:
  - algo_bubble_sort
  - algo_heap_sort
  - algo_insertion_sort
  - algo_merge_sort
  - algo_quick_sort
  - algo_selection_sort

- util_common:
  - count_lines_of_code
  - end_of_life
  - func_running_time
  - func_time
  - generate_password
  - get_user_defined_func
  - get_user_defined_module
  - get_user_imported_module
  - import_package
  - is_module_importable
  - is_user_defined_func
  - requires
  - run_parallel
  - show_docstring_google
  - show_docstring_headers
  - show_docstring_numpy
  - timeout
  - timeout_linux

- util_data_processing:
  - cvt_int_to_alpha
  - delete_dict_keys
  - dict_delete_keys
  - dict_split_by_chunk
  - is_float
  - split_dict_by_chunk
  - split_list_by_equal_sublist
  - split_list_by_fixed_length
  - str_strip

- util_datetime:
  - cvt_dt_to_tz
  - fmt_dt_to_str
  - fmt_str_to_dt
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
  - cvt_baidu09_to_gcj02
  - cvt_baidu09_to_wgs84
  - cvt_gcj02_to_baidu09
  - cvt_gcj02_to_wgs84
  - cvt_wgs84_to_baidu09
  - cvt_wgs84_to_gcj02
  - find_closest_point
  - find_k_nearest_points
  - get_coordinates_from_geom
  - gmns_geo
  - GMNSAgent
  - GMNSLink
  - GMNSNode
  - GMNSPOI
  - GMNSZone
  - proj_point_to_line

- util_git_pypi:
  - github_file_downloader
  - github_get_status
  - pypi_downloads

- util_img:
  - img_bytes_to_PIL
  - img_CV_to_PIL
  - img_PIL_to_bytes
  - img_PIL_to_CV
  - img_resize
  - img_rotate
  - img_rotate_bound
  - img_show
  - img_to_bytes
  - img_translate
  - is_CV_img
  - is_PIL_img

- util_log:
  - add_date_in_filename
  - generate_dir_with_date
  - log_logger
  - log_writer

- util_network:
  - get_host_ip
  - validate_url

- util_office:
  - is_valid_email
  - send_email

- util_pathio:
  - add_dir_to_env
  - check_file_existence
  - check_filename
  - check_files_in_dir
  - check_platform
  - create_tempfile
  - create_unique_filename
  - generate_unique_filename
  - get_dir_size
  - get_file_size
  - get_filenames_by_ext
  - get_files_by_ext
  - get_terminal_height
  - get_terminal_width
  - is_linux
  - is_mac
  - is_windows
  - path2linux
  - path2uniform
  - pickle_load
  - pickle_save
  - remove_file
  - show_dir_in_tree

- pkg_utils:
  - find_util_func_by_keyword
  - show_util_func_by_category
  - show_util_func_by_keyword
