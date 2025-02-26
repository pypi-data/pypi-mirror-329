"""
Contains code for all formatting-related HTML elements.
"""

from ..attributes import AttributesType, ClassesType, Element, ElementsType
from ..core import HTMLBuilder


class LineBreak(HTMLBuilder):
    """Constructs an HTML line break."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the LineBreak object."""

        # Initialize the builder
        super().__init__(
            elements=None,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "br"

        self.elements.max_elements = 0

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        attributes_string = f" {self.attributes}" if self.attributes else ""
        return f"<{self.tag}{attributes_string}>"


class HorizontalRule(LineBreak):
    """Constructs an HTML horizontal rule."""

    def __init__(
        self,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the HorizontalRule object."""

        # Initialize the builder
        super().__init__(
            attributes=attributes,
            classes=classes,
        )
        self.tag = "hr"


class Div(HTMLBuilder):
    """Constructs an HTML div."""

    def __init__(
        self,
        elements: ElementsType | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Div object."""

        # Initialize the builder
        super().__init__(
            elements=elements,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "div"

    def add(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.add method."""
        self.elements.add(*elements)

    def set(self, *elements: Element) -> None:
        """Convenience wrapper for the self.elements.set method."""
        self.elements.set(*elements)

    def insert(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.insert method."""
        self.elements.insert(index, element)

    def update(self, index: int, element: Element) -> None:
        """Convenience wrapper for the self.elements.update method."""
        self.elements.update(index, element)

    def remove(self, index: int) -> None:
        """Convenience wrapper for the self.elements.remove method."""
        self.elements.remove(index)

    def pop(self, index: int = -1) -> Element:
        """Convenience wrapper for the self.elements.pop method."""
        return self.elements.pop(index)

    def clear(self) -> None:
        """Convenience wrapper for the self.elements.clear method."""
        self.elements.clear()

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return super().construct()
