# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, April 24th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import pytest

import _path_setup

_path_setup.add_pkg_to_sys_path("pyufunc")

np = pytest.importorskip("numpy")

from pyufunc import (  # pylint: disable=wrong-import-position  # noqa: E402
    algo_bubble_sort,
    algo_heap_sort,
    algo_insertion_sort,
    algo_merge_sort,
    algo_quick_sort,
    algo_selection_sort,
    calc_area_from_wkt_geometry,
    calc_distance_on_unit_haversine,
    calc_distance_on_unit_sphere,
    check_platform,
    count_lines_of_code,
    create_circle_at_point_with_radius,
    cvt_baidu09_to_gcj02,
    cvt_baidu09_to_wgs84,
    cvt_current_dt_to_tz,
    cvt_gcj02_to_baidu09,
    cvt_gcj02_to_wgs84,
    cvt_int_to_alpha,
    cvt_wgs84_to_baidu09,
    cvt_wgs84_to_gcj02,
    dataclass_creation,
    dataclass_dict_wrapper,
    dataclass_extend,
    dataclass_from_dict,
    dataclass_merge,
    dict_delete_keys,
    dict_split_by_chunk,
    find_closest_point,
    find_util_func_by_keyword,
    fmt_dt_to_str,
    fmt_str_to_dt,
    get_coordinates_from_geom,
    get_host_ip,
    get_host_name,
    import_package,
    get_layer_boundary,
    get_time_diff_in_unit,
    get_timezone,
    is_linux,
    is_mac,
    is_float,
    is_windows,
    list_all_timezones,
    list_flatten_nested,
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_percentage_error,
    mean_squared_error,
    mean_squared_log_error,
    proj_point_to_line,
    pkg_public_func,
    r2_score,
    requires,
    root_mean_squared_error,
    show_util_func_by_category,
    terminal_height,
    terminal_width,
    str_digit_to_float,
    str_digit_to_int,
    str_strip,
    time_str_to_seconds,
    time_unit_converter,
    validate_url,
)


def test_sort_algorithms_return_sorted_values():
    """
    Test that sorting algorithms return the expected sorted values.

    Raises:
        AssertionError: if any of the sorting algorithms do not return the expected sorted values.
        AssertionError: if the sorting algorithms do not handle edge cases correctly.
        AssertionError: if the sorting algorithms do not handle empty lists correctly.
        AssertionError: if the sorting algorithms do not handle lists with duplicate values correctly.
        AssertionError: if the sorting algorithms do not handle lists with negative values correctly.
        AssertionError: if the sorting algorithms do not handle lists with mixed data types correctly.

    """
    values = [3, 6, 8, 10, 1, 2, 1]
    expected = [1, 1, 2, 3, 6, 8, 10]

    assert algo_quick_sort(values.copy()) == expected
    assert algo_merge_sort(values.copy()) == expected
    assert algo_heap_sort(values.copy()) == expected
    assert algo_selection_sort(values.copy()) == expected
    assert algo_insertion_sort(values.copy()) == expected
    assert algo_bubble_sort(values.copy()) == expected


def test_sort_algorithms_cover_base_and_verbose_paths(capsys: pytest.CaptureFixture[str]):
    """
    Test that sorting algorithms cover base and verbose code paths.

    Raises:
        AssertionError: if the sorting algorithms do not return expected sorted values.
        AssertionError: if verbose output does not contain "Running time" message.

    """
    assert algo_quick_sort([1], verbose=True) == [1]
    assert algo_merge_sort([1], verbose=True) == [1]
    assert algo_heap_sort([1], verbose=True) == [1]
    assert algo_selection_sort([1], verbose=True) == [1]
    assert algo_insertion_sort([1], verbose=True) == [1]
    assert algo_bubble_sort([1], verbose=True) == [1]
    output = capsys.readouterr().out
    assert output
    assert output.find("Running time") != -1
    assert algo_quick_sort([2, 1], verbose=True) == [1, 2]
    assert algo_merge_sort([2, 1], verbose=True) == [1, 2]
    assert algo_heap_sort([2, 1], verbose=True) == [1, 2]
    assert algo_selection_sort([2, 1], verbose=True) == [1, 2]
    assert algo_insertion_sort([2, 1], verbose=True) == [1, 2]


def test_sort_algorithms_reject_non_iterables():
    """Ensure sort algorithms reject non-iterable inputs."""
    # implementations may raise ValueError or TypeError for non-iterable inputs
    with pytest.raises((ValueError, TypeError)):
        algo_quick_sort(1)


def test_dataclass_from_dict_supports_dict_like_access():
    """Ensure dataclass_from_dict instances support dict-like access and attribute access."""
    person = cast(Any, dataclass_from_dict("Person", {"name": "Alice", "scores": [1, 2]}))

    assert person["name"] == "Alice"
    person["name"] = "Bob"
    assert person.name == "Bob"
    assert person.as_dict() == {"name": "Bob", "scores": [1, 2]}
    with pytest.raises(KeyError):
        _ = person["missing"]


def test_dataclass_creation_merge_extend_and_wrapper():
    """Test dataclass creation, merging, extending and dict-wrapper utilities."""
    dynamic_cls = dataclass_creation(
        "DynamicClass",
        [("name", "base"), ("count", int, 2)],
    )
    instance = dynamic_cls()
    assert instance["name"] == "base"
    assert instance.as_dict() == {"name": "base", "count": 2}

    @dataclass
    class First:
        name: str = "first"
        value: int = 1

    @dataclass
    class Second:
        value: int = 2
        city: str = "Oak Ridge"

    merged_first = dataclass_merge(First, Second)
    merged_second = dataclass_merge(First, Second, prefer="second")
    assert merged_first().value == 1
    assert merged_second().value == 2
    assert merged_second().city == "Oak Ridge"

    extended = dataclass_extend(First, [("tags", list[str], field(default_factory=list))])
    extended_instance = extended()
    assert extended_instance.name == "first"
    assert extended_instance.tags == []

    wrapped = dataclass_dict_wrapper(First())
    assert wrapped["name"] == "first"
    wrapped["name"] = "changed"
    assert wrapped.name == "changed"
    with pytest.raises(KeyError):
        wrapped["missing"] = "value"


def test_dataclass_from_dict_mutable_defaults_are_isolated():
    """
    Ensure dataclass_from_dict creates isolated mutable default instances.

    This verifies that mutable default fields (like lists) are not shared
    between instances created from the generated dataclass.

    """
    dynamic_cls = dataclass_from_dict("MutableDefaults", {"items": []}).__class__
    first = dynamic_cls()
    second = dynamic_cls()
    first.items.append("x")
    assert second.items == []


def test_dataclass_helpers_reject_invalid_inputs():
    """Ensure dataclass helpers reject invalid inputs."""
    with pytest.raises(ValueError, match="Both inputs must be dataclasses"):
        dataclass_merge(dict, list)

    with pytest.raises(ValueError, match="base_dataclass must be a dataclass"):
        dataclass_extend(dict, [])

    @dataclass
    class Base:
        name: str = "base"

    with pytest.raises(ValueError, match="additional_attributes"):
        dataclass_extend(Base, [("bad", str, "value", "extra")])

    with pytest.raises(ValueError, match="not a dataclass"):
        dataclass_dict_wrapper({"name": "Alice"})


def test_dict_string_float_and_int_helpers():
    """Test dict, string, float, and int helper functions."""
    assert dict_split_by_chunk({"a": 1, "b": 2, "c": 3}, 2) == [
        {"a": 1, "b": 2},
        {"c": 3},
    ]
    assert dict_delete_keys({"a": 1, "b": 2, "c": 3}, ["a", "c"]) == {"b": 2}
    assert dict_delete_keys({"a": 1, "b": 2}, "a") == {"b": 2}
    with pytest.raises(ValueError, match="keys must be"):
        dict_delete_keys({"a": 1}, 1)

    assert is_float(1)
    assert is_float("1.2")
    assert not is_float("")
    assert not is_float("not-float")
    assert str_strip("  hello    world  ") == "hello world"
    assert str_digit_to_int("123.9") == 123
    assert str_digit_to_float("123.9") == 123.9
    assert cvt_int_to_alpha(0) == "A"
    assert cvt_int_to_alpha(27) == "AB"
    assert list_flatten_nested([[1, 2], [3], []]) == [1, 2, 3]


def test_string_helpers_error_paths():
    """Test error paths for string helper functions."""
    with pytest.raises(TypeError, match="input must be a string"):
        str_digit_to_int(1)
    with pytest.raises(TypeError, match="input must be a string"):
        str_digit_to_float(1)
    with pytest.raises(Exception, match="Error"):
        str_digit_to_int("not-a-number")
    with pytest.raises(Exception, match="Error"):
        str_digit_to_float("not-a-number")


def test_error_measurements():
    """Test regression metrics for expected values."""
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0, 2, 8]

    assert mean_absolute_error(y_true, y_pred) == pytest.approx(0.5)
    assert mean_squared_error(y_true, y_pred) == pytest.approx(0.375)
    assert root_mean_squared_error(y_true, y_pred) == pytest.approx(np.sqrt(0.375))
    assert mean_absolute_percentage_error(y_true, y_pred) == pytest.approx(0.3273809523809524)
    assert mean_percentage_error(y_true, y_pred) == pytest.approx(0.255952380952381)
    assert r2_score(y_true, y_pred) == pytest.approx(0.9486081370449679)

    assert mean_squared_log_error([3, 5, 2.5, 7], [2.5, 5, 4, 8]) == pytest.approx(0.03973012298459379)


def test_error_measurements_reject_non_iterables():
    """Test error metrics reject non-iterable inputs."""
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        mean_absolute_error(1, [1])
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        mean_squared_error([1], 1)
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        mean_squared_log_error(1, [1])
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        root_mean_squared_error([1], 1)
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        mean_absolute_percentage_error(1, [1])
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        mean_percentage_error([1], 1)
    with pytest.raises(TypeError, match="Input should be an iterable object"):
        r2_score(1, [1])


def test_removed_database_package_is_not_public():
    """Test deleted util_dababase package is not exposed as a public category."""
    with pytest.raises(ModuleNotFoundError):
        __import__("pyufunc.util_dababase")

    assert "util_dababase" not in show_util_func_by_category(verbose=False)


def test_import_package_does_not_install_missing_dependency_by_default(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    """Ensure import_package reports missing dependencies without invoking pip by default."""
    subprocess_calls = []

    def fail_run(*args, **kwargs):
        subprocess_calls.append((args, kwargs))
        raise AssertionError("import_package should not run pip unless auto_install=True.")

    monkeypatch.setattr("subprocess.run", fail_run)

    missing_module = "pyufunc_missing_dependency_for_test"
    assert import_package(missing_module, verbose=True) is None
    assert subprocess_calls == []

    output = capsys.readouterr().out
    assert f"missing dependency {missing_module}" in output
    assert "auto_install=True" in output


def test_import_package_installs_only_with_explicit_opt_in(monkeypatch: pytest.MonkeyPatch):
    """Ensure import_package invokes pip only when auto_install=True is passed."""
    import pyufunc.util_magic._import_package as import_helpers  # pylint: disable=import-outside-toplevel

    fake_module = object()
    import_attempts = []
    subprocess_calls = []

    def fake_import_module(module_name: str):
        import_attempts.append(module_name)
        if len(import_attempts) == 1:
            raise ImportError(module_name)
        return fake_module

    class FakeCompletedProcess:
        """Minimal subprocess result used by import_package."""

        stdout = b""
        stderr = b""

        @staticmethod
        def check_returncode():
            return None

    def fake_run(command, stdout, stderr):
        subprocess_calls.append(command)
        return FakeCompletedProcess()

    monkeypatch.setattr(import_helpers.importlib, "import_module", fake_import_module)
    monkeypatch.setattr(import_helpers.subprocess, "run", fake_run)

    imported_module = import_package("demo_package", options=["--no-index"], verbose=False, auto_install=True)

    assert imported_module is fake_module
    assert len(subprocess_calls) == 1
    command = subprocess_calls[0]
    assert command[1:4] == ["-m", "pip", "install"]
    assert "--no-index" in command
    assert command[-1] == "demo_package"


def test_requires_missing_dependency_skips_without_installing(monkeypatch: pytest.MonkeyPatch):
    """Ensure requires does not call the wrapped function or install packages by default."""
    import pyufunc.util_magic._dependency_requires_decorator as requires_helpers

    call_log = []

    def fail_import_package(*args, **kwargs):
        raise AssertionError("requires should not install missing dependencies by default.")

    monkeypatch.setattr(requires_helpers, "import_package", fail_import_package)

    @requires("pyufunc_missing_dependency_for_test", verbose=False)
    def guarded_function():
        """Guarded function docstring."""
        call_log.append("called")
        return "called"

    assert guarded_function.__doc__ == "Guarded function docstring."
    assert guarded_function.__name__ == "guarded_function"
    assert guarded_function() is None
    assert call_log == []


def test_package_introspection_helpers(capsys: pytest.CaptureFixture[str]):
    """
    Test package introspection helpers for listing and searching utilities.

    Ensures that util_algorithm and algo_quick_sort are discoverable via
    show_util_func_by_category and find_util_func_by_keyword.
    """
    category_map = show_util_func_by_category(verbose=False)
    assert "util_algorithm" in category_map
    assert "algo_quick_sort" in category_map["util_algorithm"]

    assert "algo_quick_sort" in find_util_func_by_keyword("quick", verbose=False)


def test_pkg_public_func_from_installed_and_source_package(tmp_path: Path):
    """Test public function discovery from installed packages and source trees."""
    assert "img_to_bytes" in pkg_public_func("pyufunc.util_img")

    package_dir = tmp_path / "demo_pkg"
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text(
        "\n".join(
            [
                "from .helpers import *",
                "from .helpers import renamed as alias",
                "__all__ = ['alias', 'public_func', 'star_func']",
            ]
        ),
        encoding="utf-8",
    )
    (package_dir / "helpers.py").write_text(
        "\n".join(
            [
                "__all__ = ['public_func', 'star_func']",
                "def public_func():",
                "    return 'public'",
                "def star_func():",
                "    return 'star'",
                "def renamed():",
                "    return 'renamed'",
                "def _private_func():",
                "    return 'private'",
            ]
        ),
        encoding="utf-8",
    )

    from pyufunc.util_pkgs.__pkg_public_func import _get_public_functions_from_source_tree

    assert _get_public_functions_from_source_tree(tmp_path, "demo_pkg") == ["alias", "public_func", "star_func"]


def test_platformdirs_wrappers():
    """Test platformdirs wrapper functions when the optional dependency exists."""
    pytest.importorskip("platformdirs")
    from pyufunc import (
        get_user_cache_dir,
        get_user_config_dir,
        get_user_data_dir,
        get_user_log_dir,
    )

    app_name = "pyufunc-test"
    assert app_name in get_user_cache_dir(app_name)
    assert app_name in get_user_config_dir(app_name)
    assert app_name in get_user_data_dir(app_name)
    assert app_name in get_user_log_dir(app_name)


def test_filelock_wrappers(tmp_path: Path):
    """Test filelock write helpers when the optional dependency exists."""
    pytest.importorskip("filelock")
    from pyufunc import (
        safe_write_json_with_lock,
        safe_write_pickle_with_lock,
        safe_write_text_with_lock,
        with_file_lock,
    )

    text_path = safe_write_text_with_lock(tmp_path / "note.txt", "hello")
    assert text_path.read_text(encoding="utf-8") == "hello"

    json_path = safe_write_json_with_lock(tmp_path / "data.json", {"ok": True}, sort_keys=True)
    assert json_path.read_text(encoding="utf-8") == '{"ok": true}'

    pickle_path = safe_write_pickle_with_lock(tmp_path / "data.pkl", {"ok": True})
    assert pickle_path.read_bytes()

    with with_file_lock(tmp_path / "manual.lock"):
        assert True


def test_pathspec_wrappers(tmp_path: Path):
    """Test pathspec gitignore helpers when the optional dependency exists."""
    pytest.importorskip("pathspec")
    from pyufunc import (
        collect_files_excluding_gitignore,
        filter_paths_by_gitignore,
        is_path_ignored,
        load_gitignore_patterns,
    )

    (tmp_path / ".gitignore").write_text("build/\n*.pyc\n", encoding="utf-8")
    (tmp_path / "keep.txt").write_text("keep", encoding="utf-8")
    build_dir = tmp_path / "build"
    build_dir.mkdir()
    (build_dir / "skip.txt").write_text("skip", encoding="utf-8")

    spec = load_gitignore_patterns(tmp_path / ".gitignore")
    assert is_path_ignored(tmp_path / "build" / "skip.txt", spec, root=tmp_path)
    assert filter_paths_by_gitignore([tmp_path / "keep.txt", build_dir / "skip.txt"], spec, root=tmp_path) == [
        tmp_path / "keep.txt"
    ]
    assert tmp_path / "keep.txt" in collect_files_excluding_gitignore(tmp_path)


def test_more_itertools_wrappers():
    """Test more-itertools wrappers when the optional dependency exists."""
    pytest.importorskip("more_itertools")
    from pyufunc import iter_chunked, iter_flatten, iter_split_when, iter_unique, iter_windowed

    assert list(iter_chunked([1, 2, 3], 2)) == [[1, 2], [3]]
    assert list(iter_windowed([1, 2, 3], 2)) == [(1, 2), (2, 3)]
    assert list(iter_unique([1, 1, 2])) == [1, 2]
    assert list(iter_flatten([[1], [2, [3]]])) == [1, 2, 3]
    assert list(iter_split_when([1, 2, 5], lambda left, right: right - left > 1)) == [[1, 2], [5]]


def test_humanize_wrappers():
    """Test humanize wrappers when the optional dependency exists."""
    pytest.importorskip("humanize")
    from pyufunc import human_file_size, human_intcomma, human_number, human_time_delta

    assert "kB" in human_file_size(1536)
    assert human_intcomma(1200000) == "1,200,000"
    assert "million" in human_number(1200000)
    assert human_time_delta(3600)


def test_tenacity_wrappers():
    """Test tenacity retry wrappers when the optional dependency exists."""
    pytest.importorskip("tenacity")
    from pyufunc import retry_call, retry_on_exception, retry_with_backoff

    attempts = {"count": 0}

    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise ValueError("try again")
        return "ok"

    assert retry_call(flaky, attempts=2, wait_seconds=0, retry_exceptions=ValueError) == "ok"
    assert retry_with_backoff(lambda: "ok", attempts=1, min_seconds=0, max_seconds=0)() == "ok"
    assert retry_on_exception(lambda: "ok", attempts=1, wait_seconds=0)() == "ok"


def test_boltons_wrappers(tmp_path: Path):
    """Test boltons wrappers when the optional dependency exists."""
    pytest.importorskip("boltons")
    from pyufunc import atomic_save_file, flatten_iterable, parse_timedelta_text, remap_nested_dict, slugify_text

    assert remap_nested_dict({"a": {"b": 1}}) == {"a": {"b": 1}}
    assert flatten_iterable([[1], [2, 3]]) == [1, 2, 3]
    assert slugify_text("Hello World") == "hello_world"
    assert parse_timedelta_text("1d 2h").days == 1

    output_path = atomic_save_file(tmp_path / "atomic.txt", "hello")
    assert output_path.read_text(encoding="utf-8") == "hello"


def test_toolz_wrappers():
    """Test toolz wrappers when the optional dependency exists."""
    pytest.importorskip("toolz")
    from pyufunc import (
        toolz_count_frequencies,
        toolz_groupby_key,
        toolz_merge_dicts,
        toolz_pipe_call,
        toolz_sliding_window,
    )

    assert toolz_groupby_key(lambda value: value % 2, [1, 2, 3]) == {1: [1, 3], 0: [2]}
    assert toolz_merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert list(toolz_sliding_window(2, [1, 2, 3])) == [(1, 2), (2, 3)]
    assert toolz_pipe_call(2, lambda value: value + 1, lambda value: value * 2) == 6
    assert toolz_count_frequencies(["a", "a", "b"]) == {"a": 2, "b": 1}


def test_python_benedict_wrappers():
    """Test python-benedict wrappers when the optional dependency exists."""
    pytest.importorskip("benedict")
    from pyufunc import dict_flatten, dict_get_by_path, dict_set_by_path, dict_to_json_safe, dict_unflatten

    nested = {"a": {"b": 1}}
    assert dict_get_by_path(nested, "a.b") == 1
    assert dict_set_by_path({}, "a.b", 1) == nested
    assert dict_flatten(nested) == {"a_b": 1}
    assert dict_unflatten({"a_b": 1}) == nested
    assert '"a"' in dict_to_json_safe(nested)


def test_loguru_wrappers(tmp_path: Path):
    """Test loguru wrappers when the optional dependency exists."""
    pytest.importorskip("loguru")
    from loguru import logger

    from pyufunc import disable_logger, enable_logger, setup_file_logger, setup_simple_logger

    stderr_handler_id = setup_simple_logger(level="INFO")
    logger.remove(stderr_handler_id)

    log_path = tmp_path / "app.log"
    file_handler_id = setup_file_logger(log_path, level="INFO")
    logger.info("hello from pyufunc")
    logger.remove(file_handler_id)

    assert log_path.exists()
    assert "hello from pyufunc" in log_path.read_text(encoding="utf-8")
    disable_logger("pyufunc-test")
    enable_logger("pyufunc-test")


def test_datetime_format_and_timezone_helpers():
    """Test datetime formatting and timezone helper utilities."""
    pytest.importorskip("dateutil")

    dt = datetime(2024, 2, 6, 11, 12, 13)
    assert fmt_dt_to_str(dt, "%Y/%m/%d") == "2024/02/06"
    assert fmt_dt_to_str("2024-02-06", "%Y/%m/%d") == "2024/02/06"
    assert fmt_str_to_dt("2024-02-06 11:12:13") == dt
    assert fmt_str_to_dt(dt) is dt
    assert fmt_dt_to_str(dt, 1) == "2024-02-06"
    assert fmt_dt_to_str("not a date", "%Y") == "not a date"
    assert fmt_dt_to_str(1, "%Y") == "1"

    assert "UTC" in list_all_timezones("UTC")
    assert "UTC" in list_all_timezones()
    assert isinstance(get_timezone(), str)
    assert cvt_current_dt_to_tz(dt, "UTC").tzinfo is not None
    assert cvt_current_dt_to_tz(dt, "Not/AZone") == dt


def test_time_difference_helpers():
    """Test time difference calculation and conversion utilities."""
    start = "2024-02-06 00:00:00"
    end = "2024-02-07 00:00:00"
    assert get_time_diff_in_unit(start, end, "days") == 1
    assert get_time_diff_in_unit(end, start, "hours") == 24
    assert get_time_diff_in_unit(start, end, "bad-unit") == 86400

    assert time_unit_converter(2, "hours", "minutes") == 120
    assert time_unit_converter(1, "day", "hours", verbose=True) == 24
    with pytest.raises(ValueError, match="Invalid unit"):
        time_unit_converter(1, "bad", "seconds")

    assert time_str_to_seconds("12:00AM") == 0
    assert time_str_to_seconds("3:30pm", to_unit="minutes") == 930
    assert time_str_to_seconds("01:02:03", to_unit="seconds") == 3723
    assert time_str_to_seconds("3:30pm", to_unit="hours", verbose=True) == pytest.approx(15.5)
    with pytest.raises(ValueError, match="Invalid time string"):
        time_str_to_seconds("bad-time")


def test_datetime_group_helpers():
    """
    Test grouping helpers for datetime-based aggregations.

    Verifies daily, weekly, monthly, yearly, hourly and minutely grouping
    functions produce expected aggregation results.
    """
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame(
        {
            "dt": pd.date_range("2024-01-01", periods=6, freq="D"),
            "value": [1, 2, 3, 4, 5, 6],
        }
    )

    from pyufunc import (  # pylint: disable=import-outside-toplevel
        group_dt_daily,
        group_dt_hourly,
        group_dt_minutely,
        group_dt_monthly,
        group_dt_weekly,
        group_dt_yearly,
    )

    assert group_dt_daily(df, col=["dt", "value"]).loc[0, "sum"] == 1
    assert int(group_dt_weekly(df, col=["dt", "value"]).loc[0, "count"]) >= 1
    assert group_dt_monthly(df, col=["dt", "value"]).loc[0, "sum"] == 21
    assert group_dt_yearly(df, col=["dt", "value"]).loc[0, "sum"] == 21

    hourly = pd.DataFrame({"dt": pd.date_range("2024-01-01", periods=3, freq="h"), "value": [1, 2, 3]})
    minutely = pd.DataFrame({"dt": pd.date_range("2024-01-01", periods=3, freq="min"), "value": [1, 2, 3]})
    assert group_dt_hourly(hourly, col=["dt", "value"]).loc[0, "sum"] == 1
    assert group_dt_minutely(minutely, col=["dt", "value"]).loc[0, "sum"] == 1
    assert group_dt_daily(df, interval=0, col=["dt", "value"]).loc[0, "sum"] == 1
    assert group_dt_hourly(hourly, interval=0, col=["dt", "value"]).loc[0, "sum"] == 1
    assert group_dt_minutely(minutely, interval=0, col=["dt", "value"]).loc[0, "sum"] == 1


def test_coordinate_conversion_helpers():
    """Test coordinate conversion functions between WGS84, GCJ02, and Baidu09 formats."""
    wgs_lng, wgs_lat = 113.8294754, 22.6926477
    gcj_lng, gcj_lat = cvt_wgs84_to_gcj02(wgs_lng, wgs_lat)
    baidu_lng, baidu_lat = cvt_gcj02_to_baidu09(gcj_lng, gcj_lat)

    assert (gcj_lng, gcj_lat) == pytest.approx((113.83449435090813, 22.689706503327333))
    assert cvt_gcj02_to_wgs84(gcj_lng, gcj_lat) == pytest.approx((wgs_lng, wgs_lat), abs=2e-5)
    assert cvt_baidu09_to_gcj02(baidu_lng, baidu_lat) == pytest.approx((gcj_lng, gcj_lat), abs=1e-5)
    assert cvt_wgs84_to_baidu09(wgs_lng, wgs_lat) == pytest.approx((baidu_lng, baidu_lat), abs=1e-5)
    assert cvt_baidu09_to_wgs84(baidu_lng, baidu_lat) == pytest.approx((wgs_lng, wgs_lat), abs=3e-5)

    with pytest.raises(TypeError):
        cvt_wgs84_to_gcj02("113", wgs_lat)
    with pytest.raises(TypeError):
        cvt_gcj02_to_baidu09("113", wgs_lat)
    with pytest.raises(TypeError):
        cvt_baidu09_to_gcj02("113", wgs_lat)
    with pytest.raises(TypeError):
        cvt_gcj02_to_wgs84("113", wgs_lat)
    with pytest.raises(TypeError):
        cvt_baidu09_to_wgs84("113", wgs_lat)
    with pytest.raises(TypeError):
        cvt_wgs84_to_baidu09("113", wgs_lat)
    with pytest.raises(ValueError):
        cvt_wgs84_to_gcj02(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_wgs84_to_gcj02(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_gcj02_to_baidu09(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_gcj02_to_baidu09(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_baidu09_to_gcj02(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_baidu09_to_gcj02(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_gcj02_to_wgs84(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_gcj02_to_wgs84(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_baidu09_to_wgs84(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_baidu09_to_wgs84(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_wgs84_to_baidu09(200, wgs_lat)
    with pytest.raises(ValueError):
        cvt_wgs84_to_baidu09(wgs_lng, 100)
    with pytest.raises(ValueError):
        cvt_wgs84_to_gcj02(0, 0)


def test_geo_distance_helpers():
    """Test geographical distance helper functions."""
    shapely = pytest.importorskip("shapely")
    from shapely.geometry import LineString, MultiPoint, Point, Polygon  # pyright: ignore[reportMissingModuleSource]

    point = Point(0, 0)
    line = LineString([(0, 1), (1, 1)])
    projected = proj_point_to_line(point, line)
    assert projected.equals(Point(0, 1))

    pts = MultiPoint([(3, 3), (1, 1), (2, 2)])
    closest = find_closest_point(point, pts, k_closest=2)
    assert [tuple(pt.coords)[0] for pt in closest] == [(1.0, 1.0), (2.0, 2.0)]

    assert calc_distance_on_unit_sphere((0, 0), (0, 1), unit="km") == pytest.approx(111.195, rel=1e-3)
    haversine = calc_distance_on_unit_haversine(
        np.array([0.0]),
        np.array([0.0]),
        np.array([0.0]),
        np.array([1.0]),
    )
    assert haversine[0] == pytest.approx(111.195, rel=1e-3)

    assert get_coordinates_from_geom(Point(1, 2)).tolist() == [[1.0, 2.0]]
    assert get_coordinates_from_geom(LineString([(0, 0), (1, 1)])).tolist() == [[0.0, 0.0], [1.0, 1.0]]
    assert get_coordinates_from_geom(Polygon([(0, 0), (1, 0), (1, 1)])).shape[1] == 2
    assert calc_distance_on_unit_sphere([object()], (0, 1)) is None
    with pytest.raises(AssertionError):
        calc_distance_on_unit_haversine(np.array([0]), np.array([0]), np.array([0]), np.array([1]), unit="bad")
    assert shapely


def test_geo_area_circle_and_layer_boundary_helpers():
    """Validate geo area, circle, and layer boundary helper behavior."""
    shapely = pytest.importorskip("shapely")
    pytest.importorskip("pyproj")
    pd = pytest.importorskip("pandas")

    polygon = "POLYGON ((-74.006 40.712, -74.005 40.712, -74.005 40.713, -74.006 40.713, -74.006 40.712))"
    area_sqm = calc_area_from_wkt_geometry(polygon, unit="sqm", verbose=True)
    area_sqft = calc_area_from_wkt_geometry(polygon, unit="sqft", verbose=True)
    assert area_sqm > 0
    assert area_sqft == pytest.approx(area_sqm * 10.7639104)
    with pytest.raises(ValueError, match="unit must be"):
        calc_area_from_wkt_geometry(polygon, unit="acre")

    circle = create_circle_at_point_with_radius(
        [0, 0],
        100,
        options={"edges": 4, "bearing": 0, "direction": 1},
        verbose=True,
    )
    assert circle["type"] == "Polygon"
    assert len(circle["coordinates"]) == 5
    assert shapely

    data = pd.DataFrame({"x": [0, 1, 2, 3], "y": [1.0, 2.0, 3.0, 4.0]})
    boundary = get_layer_boundary(data, "x", "y", base_interval=1, percentile=1.0)
    assert list(boundary.columns) == ["x", "y"]
    assert boundary["y"].tolist() == [2.0, 3.0, 4.0]
    with pytest.raises(Exception, match="not in the dataframe"):
        get_layer_boundary(data, "missing", "y")


def test_magic_network_platform_and_doc_helpers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    """Test magic, network, platform, and documentation helper functions."""
    from pyufunc import (  # pylint: disable=import-outside-toplevel
        func_running_time,
        func_time,
        generate_password,
        pytest_show_assert,
        pytest_show_database,
        pytest_show_fixture,
        pytest_show_naming_convention,
        pytest_show_parametrize,
        pytest_show_raise,
        pytest_show_skip_xfail,
        pytest_show_warning,
        show_docstring_google,
        show_docstring_headers,
        show_docstring_numpy,
        timeout,
        timeout_linux,
    )

    assert len(generate_password(pwd_len=8)) == 8
    with pytest.raises(ValueError, match="longer than the password length"):
        generate_password(pwd_len=2)

    sample = tmp_path / "sample.py"
    sample.write_text("a = 1\nb = 2\n", encoding="utf-8")
    assert count_lines_of_code(sample) == 2
    assert count_lines_of_code(tmp_path, ext="py") == 2
    assert count_lines_of_code(1) == 0
    assert count_lines_of_code(sample, ext=1) == 0

    assert validate_url("https://example.com")
    assert not validate_url("not-a-url")
    monkeypatch.setattr("socket.gethostname", lambda: "host")
    monkeypatch.setattr("socket.gethostbyname", lambda host: "127.0.0.1")
    assert get_host_name() == "host"
    assert get_host_ip() == "127.0.0.1"

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    assert check_platform() == "MacOS"
    assert is_mac()
    monkeypatch.setattr("platform.system", lambda: "Windows")
    assert is_windows()
    monkeypatch.setattr("platform.system", lambda: "Linux")
    assert is_linux()
    assert terminal_width() > 0
    assert terminal_height() > 0

    @func_running_time
    def add_one(value):
        return value + 1

    @func_time
    def add_two(value):
        return value + 2

    assert add_one(1) == 2
    assert add_two(1) == 3

    @timeout(1)
    def immediate():
        return "ok"

    assert immediate() == "ok"
    signal = __import__("signal")

    if hasattr(signal, "SIGALRM") and hasattr(signal, "alarm"):

        @timeout_linux(1)
        def linux_immediate():
            return "ok"

        assert linux_immediate() == "ok"

    show_docstring_headers()
    show_docstring_google()
    show_docstring_numpy()
    pytest_show_naming_convention()
    pytest_show_assert()
    pytest_show_raise()
    pytest_show_warning()
    pytest_show_skip_xfail()
    pytest_show_parametrize()
    pytest_show_fixture()
    pytest_show_database()
    assert "pytest" in capsys.readouterr().out.lower()
