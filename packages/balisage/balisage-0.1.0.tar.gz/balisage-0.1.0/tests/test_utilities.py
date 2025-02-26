"""
Contains tests for the utilities module.
"""

from unittest.mock import patch

import pytest

from balisage.utilities import (
    is_valid_class_name,
    module_exists,
    requires_modules,
    split_preserving_quotes,
)


def test_module_exists() -> None:
    """Tests the module_exists function."""

    # Test with built-in modules
    assert module_exists("sys") is True
    assert module_exists("os") is True

    # Test with non-existent modules
    assert module_exists("does_not_exist") is False

    # Test with a third-party module
    try:
        import pandas  # noqa: F401

        pandas_installed = True
    except ImportError:
        pandas_installed = False
    assert module_exists("pandas") is (True if pandas_installed else False)

    # Simulate an Import or ModuleNotFound error
    with patch("importlib.import_module", side_effect=ImportError):
        assert module_exists("balisage") is False
    with patch("importlib.import_module", side_effect=ModuleNotFoundError):
        assert module_exists("balisage") is False


def test_requires_modules() -> None:
    """Tests the requires_modules decorator."""

    # Verify normal execution when all modules are present
    @requires_modules("sys", "os")
    def test_function() -> str:
        return "Success"

    assert test_function() == "Success"

    # Verify error when some modules are missing
    with patch("balisage.utilities.module_exists") as mock:
        mock.side_effect = lambda module: module != "does_not_exist"

        @requires_modules("sys", "does_not_exist")
        def test_function() -> str:
            return "Success"

        for error in [ImportError, ModuleNotFoundError]:
            with pytest.raises(error):
                test_function()

    # Verify error when all modules are missing
    with patch("balisage.utilities.module_exists", return_value=False):

        @requires_modules("does_not_exist_1", "does_not_exist_2")
        def test_function() -> str:
            return "Success"

        for error in [ImportError, ModuleNotFoundError]:
            with pytest.raises(error):
                test_function()


def test_split_preserving_quotes() -> None:
    """Tests the split_preserving_quotes function."""

    # Test with only boolean attributes
    string = "required disabled itemscope"
    expected = ["required", "disabled", "itemscope"]
    assert split_preserving_quotes(string) == expected

    # Test with only non-boolean attributes
    string = "id='test' class='class1 class2' width='50'"
    expected = ["id='test'", "class='class1 class2'", "width='50'"]
    assert split_preserving_quotes(string) == expected

    # Test with boolean and non-boolean attributes
    string = "id='test' required disabled class='class1 class2' width='50' itemscope"
    expected = [
        "id='test'",
        "required",
        "disabled",
        "class='class1 class2'",
        "width='50'",
        "itemscope",
    ]
    assert split_preserving_quotes(string) == expected


def test_is_valid_class_name() -> None:
    """Tests the is_valid_class_name function."""

    # Test with valid class names
    valid_classes = [
        "class",  # Purely alphabetic, same case
        "Class",  # Purely alphabetic, mixed case
        "_class",  # Starts with an underscore
        "-class",  # Starts with a hyphen
        "-_class",  # Character following hyphen is underscore or letter
        "c",  # Too short
    ]
    for valid_class in valid_classes:
        assert is_valid_class_name(valid_class) is True

    # Test with invalid class names
    invalid_classes = [
        "1234567890",  # Purely numeric
        "$class",  # Starts with an invalid character
        "class!",  # Contains an invalid character
        "test class",  # Contains a space
        "--class",  # Character following hyphen is hyphen
        "-!class",  # Character following hyphen is invalid character
        "-",  # Starts with a hyphen but not 2 characters long
    ]
    for invalid_class in invalid_classes:
        assert is_valid_class_name(invalid_class) is False
