"""
Contains code for all table-related HTML elements.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterator, Self

from ..attributes import AttributesType, Classes, ClassesType, Elements
from ..core import HTMLBuilder
from ..utilities import requires_modules

# Import optional dependencies
try:
    import numpy as np
except ImportError:
    pass

try:
    import pandas as pd
except ImportError:
    pass


class Data(HTMLBuilder):
    """Constructs an HTML table data."""

    def __init__(
        self,
        data: Any | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
        is_header: bool = False,
    ) -> None:
        """Initializes the Data object."""

        # Initialize the builder
        super().__init__(
            elements=None,
            attributes=attributes,
            classes=classes,
        )
        self.tag = "td" if not is_header else "th"

        self.elements.max_elements = 1

        # Store instance variables
        self._is_header = is_header

        # Set the data
        if data is not None:
            self.set(data)

    @property
    def data(self) -> str:
        """Gets the data."""
        return self.elements[0] if self.elements else None

    def set(self, data: str) -> None:
        """Convenience wrapper for the self.elements.set method."""
        self.elements.set(data)

    def clear(self) -> None:
        """Convenience wrapper for the self.elements.clear method."""
        self.elements.clear()

    @property
    def is_header(self) -> bool:
        """Gets the is_header property."""
        return self._is_header

    @is_header.setter
    def is_header(self, value: bool) -> None:
        """Sets the is_header property."""
        self.tag = "td" if not value else "th"
        self._is_header = value

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return super().construct()


class Row(HTMLBuilder):
    """Constructs an HTML table row."""

    def __init__(
        self,
        data: list[Data] | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Row object."""

        # Initialize the builder
        super().__init__(
            elements=Elements(*data) if data else Elements(),
            attributes=attributes,
            classes=classes,
        )
        self.tag = "tr"

        # Set the data
        if data is not None:
            self.set(*data)

    def add(self, *data: Data) -> None:
        """Convenience wrapper for the self.elements.add method."""
        self.elements.add(*data)

    def set(self, *data: Data) -> None:
        """Convenience wrapper for the self.elements.set method."""
        self.elements.set(*data)

    def insert(self, index: int, data: Data) -> None:
        """Convenience wrapper for the self.elements.insert method."""
        self.elements.insert(index, data)

    def update(self, index: int, data: Data) -> None:
        """Convenience wrapper for the self.elements.update method."""
        self.elements.update(index, data)

    def remove(self, index: int) -> None:
        """Convenience wrapper for the self.elements.remove method."""
        self.elements.remove(index)

    def pop(self, index: int = -1) -> Data:
        """Convenience wrapper for the self.elements.pop method."""
        return self.elements.pop(index)

    def clear(self) -> None:
        """Convenience wrapper for the self.elements.clear method."""
        self.elements.clear()

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return super().construct()

    def __iter__(self) -> Iterator[Data]:
        """Iterates over the stored data."""
        return iter(self.elements)


class Header(Row):
    """Constructs an HTML table header row.

    Convenience wrapper around the Row class that will change any Data being
    added or modified to be header data.
    """

    def __init__(
        self,
        data: list[Data] | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Header object."""

        # Convert all data to header data
        if data is not None:
            for d in range(len(data)):
                try:
                    data[d].is_header = True
                except AttributeError:
                    raise TypeError(
                        f"Expected {Data.__name__} object, got {type(data[d]).__name__}"
                    )

        # Initialize the builder
        super().__init__(
            data=Elements(*data) if data else Elements(),
            attributes=attributes,
            classes=classes,
        )

    def add(self, *data: Data) -> None:
        """Convenience wrapper for the self.elements.add method."""
        for d in data:
            d.is_header = True
        self.elements.add(*data)

    def set(self, *data: Data) -> None:
        """Convenience wrapper for the self.elements.set method."""
        for d in data:
            d.is_header = True
        self.elements.set(*data)

    def insert(self, index: int, data: Data) -> None:
        """Convenience wrapper for the self.elements.insert method."""
        data.is_header = True
        self.elements.insert(index, data)

    def update(self, index: int, data: Data) -> None:
        """Convenience wrapper for the self.elements.update method."""
        data.is_header = True
        self.elements.update(index, data)


class Table(HTMLBuilder):
    """Constructs an HTML table."""

    def __init__(
        self,
        rows: list[Row] | None = None,
        header: Header | None = None,
        attributes: AttributesType | None = None,
        classes: ClassesType | None = None,
    ) -> None:
        """Initializes the Table object."""

        # Initialize the builder
        super().__init__(
            elements=Elements(*rows) if rows else Elements(),
            attributes=attributes,
            classes=classes,
        )
        self.tag = "table"

        # Set header and rows
        if rows is not None:
            self.set_rows(*rows)
        if header is not None:
            self.set_header(header)

    def _header_exists(self) -> bool:
        """Determines whether or not a header exists in the stored elements."""
        return bool(self.elements) and isinstance(self.elements[0], Header)

    @property
    def header(self) -> Header | Row | None:
        """Gets the header if one exists."""
        return self.elements[0] if self._header_exists() else None

    @header.setter
    def header(self, value: Header | Row | None) -> None:
        """Sets the header row."""
        self.set_header(value)

    @property
    def rows(self) -> list[Row]:
        """Gets the rows."""
        if self._header_exists():
            return self.elements[1:]
        return self.elements

    @rows.setter
    def rows(self, rows: list[Row]) -> None:
        """Sets the rows."""
        self.set_rows(*rows)

    def set_header(self, header: Header) -> None:
        """Sets the header row."""
        self._raise_if_incorrect_type(header, expected_type=Header)
        if self._header_exists() and self.elements:
            self.elements.update(0, header)
        else:
            self.elements.insert(0, header)

    def clear_header(self) -> None:
        """Clears the header row."""
        if self._header_exists():
            self.elements.remove(0)

    def add_rows(self, *rows: Row) -> None:
        """Adds rows to the table."""
        for row in rows:
            self._raise_if_incorrect_type(row, expected_type=Row)
            row.is_header = False
        self.elements.add(*rows)

    def set_rows(self, *rows: Row) -> None:
        """Sets rows for the table."""
        for row in rows:
            self._raise_if_incorrect_type(row, expected_type=Row)
            row.is_header = False
        elements = [self.header] if self._header_exists() else []
        elements.extend(rows)
        self.elements.set(*elements)

    def clear_rows(self) -> None:
        """Clears the rows."""
        old_header = self.header
        self.elements.clear()
        if old_header is not None:
            self.set_header(old_header)

    def clear(self) -> None:
        """Clears both the header and the rows."""
        self.clear_header()
        self.clear_rows()

    def construct(self) -> str:
        """Generates HTML from the stored elements."""
        return super().construct()

    def _raise_if_incorrect_type(
        self,
        value: Any,
        expected_type: Any,
    ) -> None:
        """Determines whether the input is of the expected type."""
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Expected {expected_type.__name__} object, got {type(value).__name__}"
            )

    @classmethod
    @requires_modules("pandas", "numpy")
    def from_df(
        cls,
        df: pd.DataFrame,
        table_classes: ClassesType | None = None,
        header_classes: ClassesType | None = None,
        body_classes: ClassesType | None = None,
        attributes: AttributesType | None = None,
        alternating_rows: bool = True,
        columns_as_classes: bool = True,
    ) -> Self:
        """Creates an HTMLTable object from a pandas dataframe.

        Setting alternating_rows to True will add alternating classes to each
        row (excluding the header) for styling purposes. Even-numbered rows
        will have the class 'even' added and odd-numbered rows will have the
        class 'odd' added.
        """

        # Reset the index for the dataframe
        if alternating_rows:
            df.index = np.arange(1, len(df) + 1)

        # Create the body
        body: list[Row] = []
        for r, row in df.iterrows():
            data: list[Data] = []
            for i, item in enumerate(row):
                data_classes = Classes()
                if columns_as_classes:
                    data_classes.add(row.index[i])
                data.append(Data(item, classes=data_classes))
            html_row = Row(data, classes=deepcopy(body_classes))
            if alternating_rows:
                html_row.classes.add("odd" if r % 2 else "even")
            body.append(html_row)

        # Create the header
        header = Header(
            [Data(c) for c in df.columns],
            classes=deepcopy(header_classes),
        )

        # Create an instance with the results and return
        return cls(
            rows=body,
            header=header,
            attributes=attributes,
            classes=deepcopy(table_classes),
        )
