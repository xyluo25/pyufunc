# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import argparse
import inspect
import functools
import sys
import atexit


def with_argparse(func_or_class: object):
    """Decorator to add argparse support to a function or class.

    Example:
        >>> # in script.py
        >>> from pyufunc import with_argparse
        >>>
        >>> @with_argparse
        >>> def example_function(name: str, age: int = 30):
        >>>     print(f'Name: {name}, Age: {age}')
        >>>     return None
        >>> # in terminal
        >>> python script.py --name "John" --age 25

        >>> # in script_1.py
        >>> from pyufunc import with_argparse
        >>> @with_argparse
        >>> def example_function(name: str, age: int = 30):
        >>>     print(f'Name: {name}, Age: {age}')
        >>>     return None

        >>> # for class with main method (the main method is required for the class to work with with_argparse)
        >>> @with_argparse
        >>> class NewClass:
        >>>     def __init__(self, name: str):
        >>>         self.name = name
        >>>     def main(self, age: int = 30):
        >>>         print(f'Name: {self.name}, Age: {age}')
        >>>         return None
        >>> # in terminal
        >>> $ python script_1.py NewClass --name "John" --age 25
    """

    @functools.wraps(func_or_class)
    def wrapper(*args, **kwargs):
        script_name = sys.argv[0] if sys.argv else "script.py"
        subcommand_name = getattr(func_or_class, "__name__", "")
        parser = argparse.ArgumentParser(
            description=func_or_class.__doc__,
            prog=f"{script_name} {subcommand_name}" if subcommand_name else script_name,
        )

        # Check if we are dealing with a class
        if inspect.isclass(func_or_class):
            cls_instance = func_or_class
            init_sig = inspect.signature(cls_instance.__init__)
            main_method = getattr(cls_instance, 'main', None)
            if not main_method:
                raise ValueError(
                    "Class must have a 'main' method to use with_argparse.")
            main_sig = inspect.signature(main_method)

            # Skip 'self'
            for name, param in list(init_sig.parameters.items())[1:]:
                parser.add_argument(
                    f'--{name}',
                    type=(param.annotation if param.annotation != inspect._empty else str),
                    required=param.default == inspect._empty,
                )

            # Skip 'self'
            for name, param in list(main_sig.parameters.items())[1:]:
                parser.add_argument(
                    f'--{name}',
                    type=(param.annotation if param.annotation != inspect._empty else str),
                    required=param.default == inspect._empty,
                )

            parsed_args = parser.parse_args()
            init_args = {name: getattr(parsed_args, name) for name in list(
                init_sig.parameters.keys())[1:]}  # Skip 'self'
            main_args = {name: getattr(parsed_args, name) for name in list(
                main_sig.parameters.keys())[1:]}  # Skip 'self'

            instance = cls_instance(**init_args)
            return instance.main(**main_args)

        # Otherwise, we are dealing with a function
        else:
            func = func_or_class
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                parser.add_argument(f'--{name}',
                                    type=param.annotation if param.annotation != inspect._empty else str,
                                    required=param.default == inspect._empty)

            parsed_args = parser.parse_args()
            func_args = {name: getattr(parsed_args, name)
                         for name in sig.parameters.keys()}

            return func(**func_args)

    # Mark wrapped target so available subcommands can be discovered.
    setattr(wrapper, "_with_argparse_subcommand", True)

    def _emit_direct_style_warning_once():
        main_module = sys.modules.get("__main__")
        if not main_module:
            return
        if getattr(main_module, "_with_argparse_subcommand_executed", False):
            return
        if getattr(main_module, "_with_argparse_direct_style_warned", False):
            return
        if len(sys.argv) <= 1 or not sys.argv[1].startswith("-"):
            return

        setattr(main_module, "_with_argparse_direct_style_warned", True)
        script_name = sys.argv[0] if sys.argv else "script.py"
        available = sorted(set(getattr(main_module, "_with_argparse_available_functions", [])))
        print("  :Info: direct style is not supported.")
        print("  :Use subcommand style instead:"
              f" python {script_name} <function_name> [arguments]")
        if available:
            print(f"  :Available functions: {', '.join(available)}")

    # Automatically handle execution when the decorated target is defined
    # in the script that is executed directly.
    if getattr(func_or_class, "__module__", None) == "__main__":
        main_module = sys.modules.get("__main__")
        if main_module and inspect.isfunction(func_or_class):
            available = getattr(main_module, "_with_argparse_available_functions", [])
            available.append(getattr(func_or_class, "__name__", ""))
            setattr(main_module, "_with_argparse_available_functions", available)

        if main_module and not getattr(main_module, "_with_argparse_exit_hook_registered", False):
            setattr(main_module, "_with_argparse_exit_hook_registered", True)
            atexit.register(_emit_direct_style_warning_once)

        # Support subcommand style only:
        #   python script.py my_func --name Roy --age 20
        if len(sys.argv) > 1 and sys.argv[1] == getattr(func_or_class, "__name__", ""):
            if main_module:
                setattr(main_module, "_with_argparse_subcommand_executed", True)
            sys.argv.pop(1)
            wrapper()
    return wrapper
