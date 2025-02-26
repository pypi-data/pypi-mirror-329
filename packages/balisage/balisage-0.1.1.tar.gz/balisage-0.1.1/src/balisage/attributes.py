"""
Contains code related to HTML attributes.
"""

from typing import Any, Iterator, Self, TypeAlias

from .utilities import is_valid_class_name, split_preserving_quotes


class Classes:
    """Class for managing classes for HTML elements."""

    DEFAULT_REPLACEMENTS: dict[str, str] = {" ": "-"}

    def __init__(self, *names: str) -> None:
        """Initializes the Classes object."""

        # Initialize instance variables
        self._classes = dict()
        self.reset_replacements()

        # Set the classes
        self.set(*names)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Creates a Classes object from a string."""
        return cls(*string.split(" "))

    @property
    def classes(self) -> dict[str:str]:
        """Gets the stored classes as a dictionary.

        Keys are the original class names, values are the sanitized class names.
        """
        return self._classes

    @property
    def replacements(self) -> dict[str, str]:
        """Gets the replacements dictionary.

        The replacements dictionary controls the replacement of specifed
        characters in provided class names when they are sanitized.

        Keys are the characters to be replaced, values are the replacements.
        """
        return self._replacements

    @replacements.setter
    def replacements(self, replacements: dict[str, str]) -> None:
        """Sets the replacements dictionary."""
        self._replacements = replacements
        self.set(*self._classes.keys())

    def reset_replacements(self) -> None:
        """Resets the replacements dictionary to its default value."""
        self._replacements = self.DEFAULT_REPLACEMENTS

    def add(self, *names: str) -> None:
        """Adds classes to the list of classes.

        Note that duplicate classes will be ignored.
        """

        # Determine the existing sanitized names
        old_sanitized_names = list(self._classes.values())
        # Determine the new sanitized names
        new_original_names = names
        new_sanitized_names = [self._sanitize_name(name) for name in names]
        new_names = zip(new_original_names, new_sanitized_names)
        # Check that duplicate classes aren't being added
        filtered_names = {
            new_original_name: new_sanitized_name
            for new_original_name, new_sanitized_name in new_names
            if new_sanitized_name not in old_sanitized_names
        }
        # Update the classes
        self._classes.update(filtered_names)

    def set(self, *names: str) -> None:
        """Sets the list of classes."""
        method_name = self.set.__name__
        if not all(isinstance(i, str) for i in names):
            raise TypeError(f"Arguments passed to {method_name} must be strings")
        self._classes = {arg: self._sanitize_name(arg) for arg in names}

    def remove(self, name: str) -> tuple[str, str]:
        """Removes a class from the list of classes.

        Returns the removed class (if it exists) as a tuple, otherwise None.
        The tuple is in the form of (class name, sanitized class name).
        """

        # Try removing the class by its original name
        try:
            return name, self._classes.pop(name)
        except KeyError:
            pass
        # Try removing the class by its sanitized name
        for original_name, sanitized_name in self._classes.items():
            if sanitized_name == self._sanitize_name(name):
                return original_name, self._classes.pop(original_name)
        # If the class was not found, raise an exception
        raise KeyError(f"Class '{name}' not found")

    def clear(self) -> None:
        """Clears the list of classes."""
        self._classes.clear()

    def _sanitize_name(
        self,
        name: str,
        lower: bool = True,
        strip: bool = True,
    ) -> str:
        """Converts a class string into a valid class name."""
        original_name = name
        name = name.lower() if lower else name
        name = name.strip() if strip else name
        for k, v in self._replacements.items():
            name = name.replace(k, v)
        if not is_valid_class_name(name):
            raise ValueError(
                f"Class name '{original_name}' (sanitized to '{name}') is invalid"
            )
        return name

    def construct(self) -> str:
        """Generates the class string."""
        return " ".join(self._classes.values())

    def __eq__(self, other: Self) -> bool:
        """Determines whether two Classes objects are equal.

        Since keys are only kept for historical reasons, equality is determined
        by comparing the values (e.g., sanitized class names) of the classes.
        """
        if isinstance(other, self.__class__):
            return set(self._classes.values()) == set(other._classes.values())
        elif isinstance(other, dict):
            return set(self._classes.values()) == set(other.values())
        return False

    def __bool__(self) -> bool:
        """Determines whether the instance is empty."""
        return len(self._classes) > 0

    def __str__(self) -> str:
        """Gets the string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        arg_string = ", ".join(repr(c) for c in self._classes.keys())
        return f"{self.__class__.__name__}({arg_string})"


ClassesType: TypeAlias = Classes | str
AttributeValue: TypeAlias = str | bool | None
AttributeMap: TypeAlias = dict[str, AttributeValue]


class Attributes:
    """Class for managing attributes for HTML elements."""

    def __init__(self, attributes: AttributeMap | None = None) -> None:
        """Initializes the Attributes object."""

        # Initialize instance variables
        self._attributes: AttributeMap = {"class": Classes()}

        # Set the attributes
        if attributes is not None:
            self.set(attributes)

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Creates an Attributes object from a string."""
        attributes = dict()
        pairs = split_preserving_quotes(string)
        for pair in pairs:
            key, _, value = pair.partition("=")
            value = value.strip("'")
            if not value:
                value = True
            attributes[key] = value
        return cls(attributes)

    @property
    def attributes(self) -> AttributeMap:
        """Gets the stored attributes.

        Keys are the attribute names, values are the attribute values.
        """
        return self._attributes

    @property
    def classes(self) -> Classes:
        """Gets the stored classes."""
        return self._attributes["class"]

    @classes.setter
    def classes(self, classes: ClassesType) -> None:
        """Sets the stored classes.

        Valid data types for the classes property are:
        - A string
        - An instance of the Classes class
        Other data types will raise a TypeError.

        Note that a provided value with data type string will be assumed to be
        a class string, and thus the Classes.from_string method will be used
        to create the Classes object.
        """
        if isinstance(classes, str):
            classes = Classes.from_string(classes)
        elif not isinstance(classes, Classes):
            # Handle any invalid data types during conversion
            classes = Classes(classes)
        self._attributes["class"] = classes

    def add(self, attributes: AttributeMap) -> None:
        """Adds attributes to the list of attributes.

        Note that duplicate attributes will be ignored, and that the 'class'
        attribute will never be added since it is a special case (it will
        always exist).
        """
        self._attributes.update(
            {
                key: value
                for key, value in attributes.items()
                if key not in self._attributes
            }
        )

    def set(self, attributes: AttributeMap) -> None:
        """Sets the list of attributes."""
        if "class" in attributes and isinstance(attributes["class"], str):
            attributes["class"] = Classes.from_string(attributes["class"])
        elif "class" in attributes and attributes["class"] is None:
            attributes["class"] = Classes()
        elif "class" not in attributes:
            attributes["class"] = Classes()
        self._attributes = dict(attributes)

    def remove(self, name: str) -> None:
        """Removes attributes from the list of attributes.

        Will raise a KeyError if the attribute does not exist.
        """
        if name not in self._attributes:
            raise KeyError(f"Attribute '{name}' not found")
        elif name == "class":
            self._attributes["class"].clear()
        else:
            self._attributes.pop(name)

    def clear(self) -> None:
        """Clears the attributes of the HTML object."""
        self._attributes.clear()
        self._attributes["class"] = Classes()

    def construct(self) -> str:
        """Generates the attribute string."""
        pairs = []
        for key, value in self._attributes.items():
            # None and True values are boolean attributes, False will be ignored
            if (value is None) or (isinstance(value, bool) and value):
                pairs.append(f"{key}")
            elif isinstance(value, Classes) and not value:
                continue
            elif value:
                pairs.append(f"{key}='{value}'")
        return " ".join(pairs)

    def __getitem__(self, key: str) -> AttributeValue:
        """Gets an attribute from the Attributes object."""
        return self._attributes[key]

    def __setitem__(self, key: str, value: AttributeValue) -> None:
        """Sets an attribute in the Attributes object."""
        self._attributes[key] = value

    def __eq__(self, other: Self) -> bool:
        """Determines whether two Attributes objects are equal."""
        if isinstance(other, self.__class__):
            return self._attributes == other._attributes
        elif isinstance(other, dict):
            return self._attributes == other
        return False

    def __bool__(self) -> bool:
        """Determines whether the instance is empty."""
        has_added_attributes = len(self._attributes) > 1
        has_added_classes = bool(self.classes)
        return has_added_attributes or has_added_classes

    def __str__(self) -> str:
        """Gets the string version of the object."""
        return self.construct()

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        return f"{self.__class__.__name__}(attributes={self._attributes!r})"


AttributesType: TypeAlias = Attributes | AttributeMap
Element: TypeAlias = Any


class Elements:
    """Class for managing subelements of HTML elements."""

    def __init__(self, *elements: Element) -> None:
        """Initializes the Elements object."""

        # Initialize instance variables
        self._elements: list[Element] = []
        self._max_elements: int | None = None

        # Set the elements
        self.set(*elements)

    @property
    def elements(self) -> list[Element]:
        """Gets the stored elements."""
        return self._elements

    @property
    def max_elements(self) -> int | None:
        """Gets the maximum number of elements."""
        return self._max_elements

    @max_elements.setter
    def max_elements(self, value: int | None) -> None:
        """Sets the maximum number of elements."""
        is_integer = isinstance(value, int) and not isinstance(value, bool)
        is_none = value is None
        current_elements = len(self._elements)
        property_name = Elements.max_elements.fget.__name__
        if not is_integer and not is_none:
            raise TypeError(f"{property_name} must be an int or None")
        elif is_integer and value < 0:
            raise ValueError(f"{property_name} must be a positive integer")
        elif is_integer and value < current_elements:
            raise ValueError(
                f"{property_name} must be greater than or equal to the current "
                f"number of elements ({current_elements})"
            )
        self._max_elements = value

    def add(self, *elements: Element) -> None:
        """Adds elements to the list of elements."""
        self._raise_if_exceeds_max_elements(new_elements=len(elements))
        self._elements.extend(elements)

    def set(self, *elements: Element) -> None:
        """Sets the list of elements."""
        self._raise_if_exceeds_max_elements(
            new_elements=len(elements),
            ignore_current_elements=True,
        )
        self._elements = list(elements)

    def insert(self, index: int, element: Element) -> None:
        """Inserts the provided element at the specified index."""
        self._raise_if_exceeds_max_elements(new_elements=1)
        self._elements.insert(index, element)

    def update(self, index: int, element: Element) -> None:
        """Updates the provided element at the specified index."""
        self._elements[index] = element

    def remove(self, index: int) -> None:
        """Removes the element at the specified index."""
        del self._elements[index]

    def pop(self, index: int = -1) -> Element:
        """Pops and returns the element at the specified index."""
        return self._elements.pop(index)

    def clear(self) -> None:
        """Clears the list of elements."""
        self._elements.clear()

    def _raise_if_exceeds_max_elements(
        self,
        new_elements: int,
        ignore_current_elements: bool = False,
    ) -> None:
        """Determines whether the provided elements can be added."""

        if self.max_elements is None:
            return
        elif ignore_current_elements:
            # Check if the number of new elements exceeds the max elements
            proposed_elements = new_elements
        else:
            # Check if the total number of elements exceeds the max elements
            proposed_elements = len(self._elements) + new_elements
        exceeds_max_elements = proposed_elements > self.max_elements
        if exceeds_max_elements:
            proposed_string = "element" if proposed_elements == 1 else "elements"
            raise ValueError(
                f"{proposed_elements} {proposed_string} would exceed the "
                f"maximum number of elements ({self.max_elements})"
            )

    def __getitem__(self, index: int) -> Element:
        """Gets the element at the specified index."""
        return self._elements[index]

    def __setitem__(self, index: int, element: Element) -> None:
        """Sets the element at the specified index."""
        self.update(index, element)

    def __delitem__(self, index: int) -> None:
        """Deletes the element at the specified index."""
        self.remove(index)

    def __iter__(self) -> Iterator[Element]:
        """Iterates over the elements in the list."""
        return iter(self._elements)

    def __eq__(self, other: Self) -> bool:
        """Determines whether two Elements objects are equal."""
        if isinstance(other, self.__class__):
            return self._elements == other._elements
        elif isinstance(other, list):
            return self._elements == other
        return False

    def __bool__(self) -> bool:
        """Determines whether the instance is empty."""
        return len(self._elements) > 0

    def __len__(self) -> int:
        """Gets the number of elements in the list."""
        return len(self._elements)

    def __str__(self) -> str:
        """Gets the string version of the object."""
        return "".join(str(e) for e in self._elements)

    def __repr__(self) -> str:
        """Gets the string representation of the object."""
        contents = ", ".join(repr(e) for e in self._elements)
        return f"{self.__class__.__name__}({contents})"


ElementsType: TypeAlias = Elements | list[Element]
