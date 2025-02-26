"""
Contains miscellaneous code such as utility functions.
"""

import importlib
import re
from functools import wraps
from typing import Any, Callable


def module_exists(module_name: str) -> bool:
    """Determines whether or not a module exists."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def requires_modules(*dependencies: str) -> Callable[[Callable], Callable]:
    """Raises an exception if any of the specified modules are not installed.

    Module names should be passed as separate string arguments.
    """

    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            # Check if all required dependencies are installed
            if missing := [d for d in dependencies if not module_exists(d)]:
                module_string = "module" if len(missing) == 1 else "modules"
                raise ModuleNotFoundError(
                    f"Function {function.__name__} requires the missing "
                    f"optional {module_string}: {', '.join(missing)}"
                )
            return function(*args, **kwargs)

        return wrapper

    return decorator


def split_preserving_quotes(string: str) -> list[str]:
    """Splits an attribute string into a list of strings, preserving quotes."""
    return re.findall(r"[^'\s]+='[^']*'|\S+", string)


def is_valid_class_name(name: str) -> bool:
    """Determines whether a string is a valid HTML/CSS class name."""
    return re.match(r"^-?[_a-zA-Z]+[_a-zA-Z0-9-]*$", name) is not None
