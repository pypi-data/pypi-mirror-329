"""
Contains core functionality for the package.
"""

from abc import ABC, abstractmethod
from typing import Any, Self

from .attributes import (
    Attributes,
    AttributesType,
    Classes,
    ClassesType,
    Elements,
    ElementsType,
)
from .utilities import requires_modules

# Import optional dependencies
try:
    from bs4 import BeautifulSoup
    from bs4.formatter import HTMLFormatter
except ImportError:
    pass


class HTMLBuilder(ABC):
    """Base class for HTML Builder objects."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the HTMLTable object."""

        # Initialize instance variables
        self._elements = elements if elements else Elements()
        self._attributes = attributes if attributes else Attributes()

        # Set the classes if any were provided
        if classes is not None:
            self._attributes.classes = classes

    @abstractmethod
    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        attributes_string = f" {self.attributes}" if self.attributes else ""
        html = f"<{self.tag}{attributes_string}>"
        for element in self.elements:
            html += f"{element}"
        html += f"</{self.tag}>"
        return html

    @requires_modules("bs4", "bs4.formatter")
    def prettify(self, indent: int = 2) -> str:
        """Generates HTML from the stored elements."""
        formatter = HTMLFormatter(void_element_close_prefix="", indent=indent)
        soup = BeautifulSoup(self.construct(), "html.parser")
        return soup.prettify(formatter=formatter)

    def save(self, filepath: str, prettify: bool = False) -> None:
        """Saves the HTML data to the specified filepath."""
        with open(filepath, "w", encoding="utf-8") as f:
            if not prettify:
                f.write(self.construct())
            else:
                try:
                    f.write(self.prettify())
                except ModuleNotFoundError:
                    f.write(self.construct())

    @property
    def elements(self) -> list[Any]:
        """Gets the stored elements."""
        return self._elements

    @property
    def attributes(self) -> Attributes:
        """Gets the stored attributes."""
        return self._attributes

    @property
    def classes(self) -> Classes | None:
        """Gets the stored classes."""
        return self._attributes.classes

    def __eq__(self, other: Self) -> bool:
        """Determines whether two HTMLBuilder objects are equal."""
        if isinstance(other, self.__class__):
            attributes_equal = self.attributes == other.attributes
            elements_equal = self.elements == other.elements
            return attributes_equal and elements_equal
        return False

    def __str__(self) -> str:
        """Gets a string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets a string representation of the object."""
        return f"{self.__class__.__name__}(attributes={self._attributes!r})"
