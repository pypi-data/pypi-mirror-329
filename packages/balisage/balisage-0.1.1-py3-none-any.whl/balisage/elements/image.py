"""
Contains code for all formatting-related HTML elements.
"""

from ..attributes import AttributesType, ClassesType
from ..core import HTMLBuilder


class Image(HTMLBuilder):
    """Constructs an HTML image."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Image object."""

        # Initialize the builder
        super().__init__(
            elements=None,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "img"

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        attributes_string = f" {self.attributes}" if self.attributes else ""
        return f"<{self.tag}{attributes_string}>"
