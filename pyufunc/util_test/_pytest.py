# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


# show different scenarios of using pytest
def pytest_show_naming_convention() -> None:
    """Show pytest naming convention.

    References:
        source https://docs.pytest.org/en/latest/goodpractices.html
        source https://docs.pytest.org/en/latest/example/pythoncollection.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_naming_convention()

    """
    print("*** This is a general header for pytest naming convention.***\n")
    print("For file names:")
    print("""   test_*.py or *_test.py""")
    print()
    print("For class names:")
    print("""   Test*""")
    print()
    print("For method names:")
    print("""   test_* or *_test""")

    print()
    print("You can also change naming convention by using pytest.ini file.")
    print("For example (in pytest.ini file):")
    print("""[pytest]
          python_files = check_*.py
          python_classes = Check*
          python_functions = check_* or *_check""")
    print("pytest will then only consider files matching the pattern check_*.py\n",
          " classes with names starting with Check and,\n",
          " functions with names starting with check_ or ending with _check.")
    print()

    return None


def pytest_show_assert() -> None:
    """Show pytest assert.

    References:
        source https://docs.pytest.org/en/latest/assert.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_assert()

    """
    pytest_assert = """The python code example of pytest assert:

    # directly use assert statement
    def test_something():
        a = 3
        b = 4
        assert a + b == 7
        assert a + 1 == 4

    # running func to verify the result
    def func():
        return 3

    def test_func():
        assert func() == 3
        assert func() == 4

    """
    print(pytest_assert)
    return None


def pytest_show_raise() -> None:
    """Show pytest raise.

    References:
        source https://docs.pytest.org/en/latest/assert.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_raise()

    """
    pytest_raise = """The python code example of pytest raise:

    def func():
        raise Exception("Error message: This is an exception.")

    def test_func():
        with pytest.raises(Exception) as exc_info:
            func()
        assert str(exc_info.value) == "Error message: This is an exception."

    """
    print(pytest_raise)
    return None


def pytest_show_warning() -> None:
    """Show pytest warning.

    References:
        source https://docs.pytest.org/en/latest/warnings.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_warning()

    """
    pytest_warning = """The python code example of pytest warning:

    import warnings

    def func():
        warnings.warn("This is a warning message.")
        return 0

    def test_func():
        with pytest.warns() as record:
            func()
        assert len(record) == 1
        assert str(record[0].message) == "This is a warning message."

    # user can filter the warning message

    @pytest.mark.filterwarnings("ignore:This is a warning message.")
    def test_func():
        with pytest.warns(None) as record:
            func()
        assert len(record) == 0
        assert str(record[0].message) == "This is a warning message."

    """
    print(pytest_warning)
    return None


def pytest_show_skip_xfail() -> None:
    """Show pytest skip and xfail.

    References:
        source https://docs.pytest.org/en/latest/skipping.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_skip_xfail()

    """
    pytest_skip_xfail = """The python code example of pytest skip and xfail:

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_func():
        pass

    @pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
    def test_func():
        pass

    @pytest.mark.xfail
    def test_func():
        assert False

    @pytest.mark.xfail(sys.version_info < (3.10), reason="this test is expected to fail")
    def test_func():
        assert False

    """
    print(pytest_skip_xfail)
    return None


def pytest_show_parametrize() -> None:
    """Show pytest parametrize.

    References:
        source https://docs.pytest.org/en/latest/parametrize.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_parametrize()

    """
    pytest_parametrize = """The python code example of pytest parametrize:

    import pytest

    @pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_eval(test_input, expected):
        assert eval(test_input) == expected

    @pytest.mark.parametrize("n, expected", [(1, 2), (2, 3), (3, 4)])
    class TestClass:
        def test_simple(self, n, expected):
            assert n + 1 == expected

        def test_simple2(self, n, expected):
            assert (n * 1) + 1 == expected

    """
    print(pytest_parametrize)
    return None


def pytest_show_fixture() -> None:
    """Show pytest fixture.

    References:
        source https://docs.pytest.org/en/latest/fixture.html

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_fixture()

    """
    pytest_fixture = """The python code example of pytest fixture:

    import pytest

    @pytest.fixture
    def input_value():
        return 39

    def test_divisible_by_3(input_value):
        assert input_value % 3 == 0

    def test_divisible_by_6(input_value):
        assert input_value % 6 == 0

    """
    print(pytest_fixture)
    return None


def pytest_show_database() -> None:
    """Show pytest database connection and testing

    Examples:
        >>> import pyufunc as pf
        >>> pf.pytest_show_database()

    """
    pytest_database = """The python code example of pytest database:

    import pytest

    @pytest.fixture()
    def db_con():
        print("connecting to database")
        db = DB_connection()  # create a database connection
        yield db
        print("closing database connection")

    def test_db(db_con):
        with pytest.raises(Exception) as exc_info:
            db_con.query("SELECT * FROM table")

        assert "Error message: This is an exception." in str(exc_info.value)

    def test_db2(db_con):
        with pytest.warns(None) as record:
            db_con.query("SELECT * FROM table")
        assert len(record) == 1
        assert "This is a warning message." in str(record[0].message)

    """
    print(pytest_database)
    return None