"""
Contains code for all text-related HTML elements.
"""

from enum import Enum

from ..attributes import AttributesType, ClassesType
from ..core import HTMLBuilder


class TextType(Enum):
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"


class Text(HTMLBuilder):
    """Constructs HTML text."""

    def __init__(
        self,
        text: str | None = None,
        tag: TextType = TextType.P,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Text object."""

        # Initialize the builder
        super().__init__(
            elements=None,
            attributes=attributes,
            classes=classes,
        )
        self.tag = tag.value

        self.elements.max_elements = 1

        # Set the text
        if text is not None:
            self.set(text)

    @property
    def text(self) -> str:
        """Gets the text."""
        return self.elements[0] if self.elements else ""

    def set(self, text: str) -> None:
        """Convenience wrapper for the self.elements.set method."""
        self.elements.set(text)

    def clear(self) -> None:
        """Convenience wrapper for the self.elements.clear method."""
        self.elements.clear()

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return super().construct()


class Paragraph(Text):
    """Constructs an HTML paragraph."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Paragraph object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.P,
            attributes=attributes,
            classes=classes,
        )


class Heading1(Text):
    """Constructs an HTML heading (size 1)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading1 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H1,
            attributes=attributes,
            classes=classes,
        )


class Heading2(Text):
    """Constructs an HTML heading (size 2)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading2 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H2,
            attributes=attributes,
            classes=classes,
        )


class Heading3(Text):
    """Constructs an HTML heading (size 3)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading3 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H3,
            attributes=attributes,
            classes=classes,
        )


class Heading4(Text):
    """Constructs an HTML heading (size 4)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading4 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H4,
            attributes=attributes,
            classes=classes,
        )


class Heading5(Text):
    """Constructs an HTML heading (size 5)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading5 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H5,
            attributes=attributes,
            classes=classes,
        )


class Heading6(Text):
    """Constructs an HTML heading (size 6)."""

    def __init__(
        self,
        text: str,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Heading6 object."""

        # Initialize the builder
        super().__init__(
            text,
            TextType.H6,
            attributes=attributes,
            classes=classes,
        )
