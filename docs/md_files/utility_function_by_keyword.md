<!--
 *  Created Date: Friday, February 16th 2024
 *  Contact Info: luoxiangyong01@gmail.com
 *  Author/Copyright: Mr. Xiangyong Luo
-->

## Message From pyufunc Developers

This document is a generated keyword index for the public utility functions exposed by pyufunc. The keyword groups are derived from function names and are intended to support API discovery.

The keyword index should not be interpreted as evidence that a function is widely used, frequently used, or faster than an alternative implementation. Evidence about reviewed packages and exploratory dependent-usage scans is tracked separately in `PACKAGE_CLAIMS.md`, `docs/md_files/utility_function_pkg_review.md`, and `datasets/util_pkgs_dependents_func_usage`.

## Existing Utility Functions by Keywords

Available utility functions in pyufunc:

Note: we may not update available functions in time, please run code below to check latest available functions.

```python
pyufunc.find_util_func_by_keyword("keyword")
```

Available utility functions in pyUFunc (253):

- non-keywords:
  - add_date_in_filename
  - add_dir_to_env
  - add_pkg_to_sys_path
  - atomic_save_file
  - auto_canny
  - boot_time
  - cd
  - collect_files_excluding_gitignore
  - confirmed
  - count_lines_of_code
  - cpu_count
  - cpu_freq
  - cpu_percent
  - cpu_times
  - dataclass_creation
  - dataclass_dict_wrapper
  - dataclass_extend
  - dataclass_from_dict
  - dataclass_merge
  - dict_delete_keys
  - dict_flatten
  - dict_get_by_path
  - dict_set_by_path
  - dict_split_by_chunk
  - dict_to_json_safe
  - dict_unflatten
  - disable_logger
  - disk_io_counters
  - disk_usage
  - download_elevation_tif_by
  - enable_logger
  - end_of_life
  - extract_bbox_coordinates
  - fake_requests_headers
  - file_delete
  - file_remove
  - filter_paths_by_gitignore
  - flatten_iterable
  - func_running_time
  - func_time
  - getloadavg
  - grab_contours
  - human_file_size
  - human_intcomma
  - human_number
  - human_time_delta
  - import_package
  - iter_chunked
  - iter_flatten
  - iter_split_when
  - iter_unique
  - iter_windowed
  - load_data
  - load_gitignore_patterns
  - load_pickle
  - log_ceil
  - merge_dicts
  - net_io_counters
  - opencv2matplotlib
  - osgb36_to_wgs84
  - pad_size
  - parse_timedelta_text
  - path2linux
  - path2uniform
  - pickle_load
  - pickle_save
  - pkg_dependents_func_usage
  - pkg_public_func
  - precondition
  - printer_file
  - Process
  - process_iter
  - r2_score
  - remap_nested_dict
  - remove_duplicate_files
  - remove_punctuation
  - requires
  - resize
  - resolve_dir
  - retry_call
  - retry_on_exception
  - retry_with_backoff
  - rotate
  - rotate_bound
  - safe_write_json_with_lock
  - safe_write_pickle_with_lock
  - safe_write_text_with_lock
  - save_data
  - save_dict_to_json
  - save_pickle
  - send_email
  - sensor_battery
  - sensor_fans
  - sensor_temperatures
  - sensors_temperatures
  - setup_file_logger
  - setup_simple_logger
  - size_of_dir
  - size_of_file
  - skeletonize
  - slugify_text
  - str_digit_to_float
  - str_digit_to_int
  - str_strip
  - swap_memory
  - terminal_height
  - terminal_width
  - time_str_to_seconds
  - time_unit_converter
  - timeout
  - timeout_linux
  - toolz_count_frequencies
  - toolz_groupby_key
  - toolz_merge_dicts
  - toolz_pipe_call
  - toolz_sliding_window
  - translate
  - update_dict_keys
  - url_to_image
  - Version
  - virtual_memory
  - wgs84_to_osgb36
  - with_argparse
  - with_file_lock

- show:
  - show_dir_in_tree
  - show_docstring_google
  - show_docstring_headers
  - show_docstring_numpy
  - show_public_func
  - show_util_func_by_category

- get:
  - get_active_python_env
  - get_coordinates_from_geom
  - get_dir_size
  - get_file_size
  - get_filenames_by_ext
  - get_files_by_ext
  - get_host_ip
  - get_host_name
  - get_layer_boundary
  - get_osm_by_bbox
  - get_osm_by_relation_id
  - get_osm_place
  - get_time_diff_in_unit
  - get_timezone
  - get_user_cache_dir
  - get_user_config_dir
  - get_user_data_dir
  - get_user_defined_func
  - get_user_defined_module
  - get_user_imported_module
  - get_user_log_dir

- generate:
  - generate_dir_with_date
  - generate_password
  - generate_unique_filename

- create:
  - create_circle_at_point_with_radius
  - create_tempfile
  - create_unique_filename

- find:
  - find_closest_point
  - find_duplicate_files
  - find_executable_from_PATH_on_win
  - find_fname_from_PATH_on_win
  - find_k_nearest_points
  - find_similar_str
  - find_util_func_by_keyword

- calc:
  - calc_area_from_wkt_geometry
  - calc_distance_on_unit_haversine
  - calc_distance_on_unit_sphere

- run:
  - run_parallel

- group:
  - group_dt_daily
  - group_dt_hourly
  - group_dt_minutely
  - group_dt_monthly
  - group_dt_weekly
  - group_dt_yearly

- check:
  - check_file_existence
  - check_filename
  - check_files_in_dir
  - check_platform

- validate:
  - validate_url

- list:
  - list_all_timezones
  - list_flatten_nested
  - list_split_by_equal_sublist
  - list_split_by_fixed_length

- img:
  - img_bytes_to_CV
  - img_bytes_to_PIL
  - img_CV_to_bytes
  - img_CV_to_PIL
  - img_PIL_to_bytes
  - img_PIL_to_CV
  - img_resize
  - img_rotate
  - img_rotate_bound
  - img_show
  - img_to_bytes
  - img_translate

- fmt:
  - fmt_dt_to_str
  - fmt_str_to_dt

- cvt:
  - cvt_baidu09_to_gcj02
  - cvt_baidu09_to_wgs84
  - cvt_current_dt_to_tz
  - cvt_gcj02_to_baidu09
  - cvt_gcj02_to_wgs84
  - cvt_int_to_alpha
  - cvt_py_to_dll
  - cvt_wgs84_to_baidu09
  - cvt_wgs84_to_gcj02

- is:
  - is_cv2
  - is_cv3
  - is_cv4
  - is_CV_img
  - is_float
  - is_linux
  - is_mac
  - is_module_importable
  - is_path_ignored
  - is_PIL_img
  - is_user_defined_func
  - is_valid_email
  - is_windows

- proj:
  - proj_point_to_line

- github:
  - github_file_downloader
  - github_get_status
  - github_private_file_downloader

- pypi:
  - pypi_downloads

- error:
  - mean_absolute_error
  - mean_absolute_percentage_error
  - mean_percentage_error
  - mean_squared_error
  - mean_squared_log_error
  - root_mean_squared_error

- algo:
  - algo_bubble_sort
  - algo_heap_sort
  - algo_insertion_sort
  - algo_merge_sort
  - algo_quick_sort
  - algo_selection_sort

- gmns:
  - gmns_Agent
  - gmns_Link
  - gmns_Node
  - gmns_POI
  - gmns_read_link
  - gmns_read_node
  - gmns_read_poi
  - gmns_read_zone
  - gmns_Zone

- pytest:
  - pytest_show_assert
  - pytest_show_database
  - pytest_show_fixture
  - pytest_show_naming_convention
  - pytest_show_parametrize
  - pytest_show_raise
  - pytest_show_skip_xfail
  - pytest_show_warning
