# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, April 24th 2026
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from dataclasses import dataclass, field
from datetime import datetime
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
    r2_score,
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
    values = [3, 6, 8, 10, 1, 2, 1]
    expected = [1, 1, 2, 3, 6, 8, 10]

    assert algo_quick_sort(values.copy()) == expected
    assert algo_merge_sort(values.copy()) == expected
    assert algo_heap_sort(values.copy()) == expected
    assert algo_selection_sort(values.copy()) == expected
    assert algo_insertion_sort(values.copy()) == expected
    assert algo_bubble_sort(values.copy()) == expected


def test_sort_algorithms_cover_base_and_verbose_paths(capsys):
    assert algo_quick_sort([1], verbose=True) == [1]
    assert algo_merge_sort([1], verbose=True) == [1]
    assert algo_heap_sort([1], verbose=True) == [1]
    assert algo_selection_sort([1], verbose=True) == [1]
    assert algo_insertion_sort([1], verbose=True) == [1]
    assert algo_bubble_sort([1], verbose=True) == [1]
    assert "Running time" in capsys.readouterr().out
    assert algo_quick_sort([2, 1], verbose=True) == [1, 2]
    assert algo_merge_sort([2, 1], verbose=True) == [1, 2]
    assert algo_heap_sort([2, 1], verbose=True) == [1, 2]
    assert algo_selection_sort([2, 1], verbose=True) == [1, 2]
    assert algo_insertion_sort([2, 1], verbose=True) == [1, 2]


def test_sort_algorithms_reject_non_iterables():
    with pytest.raises(ValueError, match="Input should be iterable"):
        algo_quick_sort(1)


def test_dataclass_from_dict_supports_dict_like_access():
    person = cast(Any, dataclass_from_dict("Person", {"name": "Alice", "scores": [1, 2]}))

    assert person["name"] == "Alice"
    person["name"] = "Bob"
    assert person.name == "Bob"
    assert person.as_dict() == {"name": "Bob", "scores": [1, 2]}
    with pytest.raises(KeyError):
        _ = person["missing"]


def test_dataclass_creation_merge_extend_and_wrapper():
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
    dynamic_cls = dataclass_from_dict("MutableDefaults", {"items": []}).__class__
    first = dynamic_cls()
    second = dynamic_cls()
    first.items.append("x")
    assert second.items == []


def test_dataclass_helpers_reject_invalid_inputs():
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
    with pytest.raises(TypeError, match="input must be a string"):
        str_digit_to_int(1)
    with pytest.raises(TypeError, match="input must be a string"):
        str_digit_to_float(1)
    with pytest.raises(Exception, match="Error"):
        str_digit_to_int("not-a-number")
    with pytest.raises(Exception, match="Error"):
        str_digit_to_float("not-a-number")


def test_error_measurements():
    y_true = [3, -0.5, 2, 7]
    y_pred = [2.5, 0, 2, 8]

    assert mean_absolute_error(y_true, y_pred) == pytest.approx(0.5)
    assert mean_squared_error(y_true, y_pred) == pytest.approx(0.375)
    assert root_mean_squared_error(y_true, y_pred) == pytest.approx(np.sqrt(0.375))
    assert mean_absolute_percentage_error(y_true, y_pred) == pytest.approx(0.3273809523809524)
    assert mean_percentage_error(y_true, y_pred) == pytest.approx(0.255952380952381)
    assert r2_score(y_true, y_pred) == pytest.approx(0.9486081370449679)

    assert mean_squared_log_error([3, 5, 2.5, 7], [2.5, 5, 4, 8]) == pytest.approx(
        0.03973012298459379
    )


def test_error_measurements_reject_non_iterables():
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


def test_util_database_package_imports():
    import pyufunc.util_dababase as util_dababase  # pylint: disable=import-outside-toplevel

    assert util_dababase.__all__ == []


def test_package_introspection_helpers(capsys):
    category_map = show_util_func_by_category(verbose=False)
    assert "util_algorithm" in category_map
    assert "algo_quick_sort" in category_map["util_algorithm"]

    assert "algo_quick_sort" in find_util_func_by_keyword("quick", verbose=False)


def test_datetime_format_and_timezone_helpers():
    dateutil = pytest.importorskip("dateutil")
    assert dateutil

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
    shapely = pytest.importorskip("shapely")
    pytest.importorskip("pyproj")
    pd = pytest.importorskip("pandas")

    polygon = (
        "POLYGON ((-74.006 40.712, -74.005 40.712, -74.005 40.713, "
        "-74.006 40.713, -74.006 40.712))"
    )
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


def test_magic_network_platform_and_doc_helpers(tmp_path, monkeypatch, capsys):
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
    if hasattr(signal, "SIGALRM"):
        @timeout_linux(1)
        def linux_immediate():
            return "ok"

        assert linux_immediate() == "ok"

    for func in [
        show_docstring_headers,
        show_docstring_google,
        show_docstring_numpy,
        pytest_show_naming_convention,
        pytest_show_assert,
        pytest_show_raise,
        pytest_show_warning,
        pytest_show_skip_xfail,
        pytest_show_parametrize,
        pytest_show_fixture,
        pytest_show_database,
    ]:
        func()
    assert "pytest" in capsys.readouterr().out.lower()
