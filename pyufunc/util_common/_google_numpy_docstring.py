# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, February 4th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


def show_docstring_headers() -> None:
    """Show supported docstring header.

    See Also:
        show_google_docstring_style
        show_numpy_docstring_style

    References:
        source https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

    """

    print("**** This is a general header for google and numpy docstring. ****")
    print("""
        Args (alias of Parameters)
        Arguments (alias of Parameters)
        Attributes
        Example
        Examples
        Keyword Args (alias of Keyword Arguments)
        Keyword Arguments
        Methods
        Note
        Notes
        Other Parameters
        Parameters
        Return (alias of Returns)
        Returns
        Raises
        References
        See Also
        Todo
        Warning
        Warnings (alias of Warning)
        Warns
        Yield (alias of Yields)
        Yields

        """)
    return None


def show_docstring_google() -> None:
    """Show google docstring style.

    References:
        source https://sphinxcontrib-napoleon.readthedocs.io/en/latest/
    """

    print("Google style with Python 3 type annotations:")

    print_str = """
    def func(arg1, arg2):
        \"""Summary line.
        Extended description of function.

        Args:
            arg1 (int): Description of arg1
            arg2 (str): Description of arg2

        Returns:
            bool: Description of return value

        \"""
        return True

        """
    print(print_str)
    print()
    return None


def show_docstring_numpy() -> None:
    """Show numpy docstring style.

    References:
        source https://sphinxcontrib-napoleon.readthedocs.io/en/latest/
    """

    print("Numpy style annotation:")

    print_str = """
    def func(arg1, arg2):
        \"""Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        bool
            Description of return value

        \"""
        return True

    """
    print(print_str)
    return None