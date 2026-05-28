## Message From pyufunc Developers

This document is a generated category index for the public utility functions exposed by pyufunc. It is intended to help users inspect the package API by subpackage and identify candidate functions for a specific task.

The list is an API-discovery aid, not a claim that every function is widely used or performance-improving. Evidence about reviewed source packages and exploratory dependent-usage scans is tracked separately in `PACKAGE_CLAIMS.md`, `docs/md_files/utility_function_pkg_review.md`, and `datasets/util_pkgs_dependents_func_usage`.

## Existing Utility Functions by Category

Note: we may not update available functions in time, please run code below to check latest available functions.

```python
pyufunc.show_util_func_by_category()
```

Available utility functions in pyUFunc (253):

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

- util_magic:
  - count_lines_of_code
  - cvt_py_to_dll
  - end_of_life
  - func_running_time
  - func_time
  - generate_password
  - get_active_python_env
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
  - dataclass_creation
  - dataclass_dict_wrapper
  - dataclass_extend
  - dataclass_from_dict
  - dataclass_merge
  - dict_delete_keys
  - dict_split_by_chunk
  - get_layer_boundary
  - is_float
  - list_flatten_nested
  - list_split_by_equal_sublist
  - list_split_by_fixed_length
  - str_digit_to_float
  - str_digit_to_int
  - str_strip

- util_datetime:
  - cvt_current_dt_to_tz
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
  - time_str_to_seconds
  - time_unit_converter

- util_geo:
  - calc_area_from_wkt_geometry
  - calc_distance_on_unit_haversine
  - calc_distance_on_unit_sphere
  - create_circle_at_point_with_radius
  - cvt_baidu09_to_gcj02
  - cvt_baidu09_to_wgs84
  - cvt_gcj02_to_baidu09
  - cvt_gcj02_to_wgs84
  - cvt_wgs84_to_baidu09
  - cvt_wgs84_to_gcj02
  - download_elevation_tif_by
  - extract_bbox_coordinates
  - find_closest_point
  - find_k_nearest_points
  - get_coordinates_from_geom
  - get_osm_by_bbox
  - get_osm_by_relation_id
  - get_osm_place
  - gmns_Agent
  - gmns_Link
  - gmns_Node
  - gmns_POI
  - gmns_read_link
  - gmns_read_node
  - gmns_read_poi
  - gmns_read_zone
  - gmns_Zone
  - proj_point_to_line

- util_git_pypi:
  - github_file_downloader
  - github_get_status
  - github_private_file_downloader
  - pypi_downloads

- util_img:
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
  - is_CV_img
  - is_PIL_img

- util_log:
  - add_date_in_filename
  - generate_dir_with_date

- util_network:
  - get_host_ip
  - get_host_name
  - validate_url

- util_office:
  - is_valid_email
  - printer_file
  - send_email

- util_pathio:
  - add_dir_to_env
  - add_pkg_to_sys_path
  - check_file_existence
  - check_filename
  - check_files_in_dir
  - check_platform
  - create_tempfile
  - create_unique_filename
  - file_delete
  - file_remove
  - find_duplicate_files
  - find_executable_from_PATH_on_win
  - find_fname_from_PATH_on_win
  - generate_unique_filename
  - get_dir_size
  - get_file_size
  - get_filenames_by_ext
  - get_files_by_ext
  - is_linux
  - is_mac
  - is_windows
  - path2linux
  - path2uniform
  - pickle_load
  - pickle_save
  - remove_duplicate_files
  - show_dir_in_tree
  - size_of_dir
  - size_of_file
  - terminal_height
  - terminal_width
  - with_argparse

- util_test:
  - pytest_show_assert
  - pytest_show_database
  - pytest_show_fixture
  - pytest_show_naming_convention
  - pytest_show_parametrize
  - pytest_show_raise
  - pytest_show_skip_xfail
  - pytest_show_warning

- util_pkgs:
  - atomic_save_file
  - auto_canny
  - boot_time
  - cd
  - collect_files_excluding_gitignore
  - confirmed
  - cpu_count
  - cpu_freq
  - cpu_percent
  - cpu_times
  - dict_flatten
  - dict_get_by_path
  - dict_set_by_path
  - dict_to_json_safe
  - dict_unflatten
  - disable_logger
  - disk_io_counters
  - disk_usage
  - enable_logger
  - fake_requests_headers
  - filter_paths_by_gitignore
  - find_similar_str
  - flatten_iterable
  - get_user_cache_dir
  - get_user_config_dir
  - get_user_data_dir
  - get_user_log_dir
  - getloadavg
  - grab_contours
  - human_file_size
  - human_intcomma
  - human_number
  - human_time_delta
  - is_cv2
  - is_cv3
  - is_cv4
  - is_path_ignored
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
  - pkg_dependents_func_usage
  - pkg_public_func
  - precondition
  - Process
  - process_iter
  - remap_nested_dict
  - remove_punctuation
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
  - sensor_battery
  - sensor_fans
  - sensor_temperatures
  - sensors_temperatures
  - setup_file_logger
  - setup_simple_logger
  - show_public_func
  - skeletonize
  - slugify_text
  - swap_memory
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
  - with_file_lock

- pkg_utils:
  - find_util_func_by_keyword
  - show_util_func_by_category
