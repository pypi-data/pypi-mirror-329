from __future__ import annotations

import collections.abc

from .const import STRONG, STRONGEST, WEAK, WEAKEST
from .exception import NoMatch

try:
    from typing import Self  # type: ignore (py3.11+)
except ImportError:
    from typing_extensions import Self

PRIO_MAPPING = {
    (True, True): STRONGEST,
    (True, False): STRONG,
    (False, True): WEAK,
    (False, False): WEAKEST,
}


def split_items(items: str) -> collections.abc.Generator[str, None, None]:
    current = ''  # Current value being collected
    whitespace = ''  # Whitespace that might or might not be part of the value
    quote = None  # None: not inside a quoted string, otherwise the quote itself
    escape = False  # True: include next character unconditionally

    for c in items+',':
        if escape:
            # This character is escaped, so include it unconditionally
            escape = False
            current += c
        elif c == '\\':
            # Escape next character
            escape = True
        elif quote:
            # Inside a quoted string
            if c == quote:
                # End of string
                quote = None
            else:
                # Include any other character
                current += c
        elif c in (' ', '\t'):
            # Whitespace. Ignore leading whitespace, collect all other whitespace in a separate variable
            if current:
                whitespace += c
        elif c in ('"', "'"):
            # Start of a quoted string. Also include whitespace into current
            quote = c
            current += whitespace
            whitespace = ''
        elif c == ',':
            # Field separator. Ignore trailing whitespace, reset current value
            yield current
            current = ''
            whitespace = ''
        elif c == ':':
            # An unescaped colon is not allowed (See #3)
            raise ValueError("colons in items must be escaped")
        else:
            # Any other character. Include whitespace too if it was collected
            current += whitespace + c
            whitespace = ''

    if quote:
        # Unterminated quoted string
        raise ValueError("unmatched quotes")

    assert current == ''
    assert whitespace == ''


class ResourceItem:
    def __init__(self, value: str, required: bool, excluded: bool):
        if required and excluded:
            raise ValueError('cannot combine required and excluded flags')

        self.value = value
        self.required = required
        self.excluded = excluded

    @classmethod
    def _create_item(cls, value) -> Self:
        from .tag import Tag
        return Tag(value)

    @classmethod
    def create(cls, value: str | collections.abc.Iterable[str]) -> collections.abc.Iterable[Self]:
        if isinstance(value, str):
            for item in split_items(value):
                if item:
                    yield cls._create_item(item)
        else:
            for element in value:
                for item in split_items(element):
                    if item:
                        yield cls._create_item(item)

    def comparable(self, worker: Self) -> bool:
        return type(self) is type(worker)

    def compare(self, worker: Self) -> float | None:
        """
            +-----------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
            | . worker  | required                                             | optional                                           | excluded                                      |
            | task      |                                                      |                                                    |                                               |
            +-----------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
            | required  | :py:data:`~momotor.shared.resources.const.STRONGEST` | :py:data:`~momotor.shared.resources.const.STRONG`  | :py:class:`~momotor.shared.resources.NoMatch` |
            +-----------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
            | optional  | :py:data:`~momotor.shared.resources.const.WEAK`      | :py:data:`~momotor.shared.resources.const.WEAKEST` | :py:class:`~momotor.shared.resources.NoMatch` |
            +-----------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
            | excluded  | :py:class:`~momotor.shared.resources.NoMatch`        | :py:class:`~momotor.shared.resources.NoMatch`      |                                               |
            +-----------+------------------------------------------------------+----------------------------------------------------+-----------------------------------------------+
        """
        if self.comparable(worker):
            if self.excluded or worker.excluded:
                if self.excluded and worker.excluded:
                    return None
                else:
                    raise NoMatch

            return PRIO_MAPPING[(self.required, worker.required)]

        return None

    @classmethod
    def compare_missing(cls, worker: Self) -> float | None:
        """
            +----------+-----------------------------------------------+----------------------------------------------------+------------------------------------------------+
            | . worker | required                                      | optional                                           | excluded                                       |
            | task     |                                               |                                                    |                                                |
            +----------+-----------------------------------------------+----------------------------------------------------+------------------------------------------------+
            | `-`      | :py:class:`~momotor.shared.resources.NoMatch` |                                                    |                                                |
            +----------+-----------------------------------------------+----------------------------------------------------+------------------------------------------------+
        """
        if worker.required:
            raise NoMatch

        return None

    def as_str(self) -> str:
        if self.excluded:
            prefix = '~'
        elif self.required:
            prefix = ''
        else:
            prefix = '?'

        return prefix + self.value
    
    def __str__(self) -> str:
        return self.as_str()
    
    def __hash__(self) -> int:
        return hash((self.value, self.required, self.excluded))
    
    def __eq__(self, other: Self) -> bool:
        return self.value == other.value and self.required == other.required and self.excluded == other.excluded
    
    def __lt__(self, other: Self) -> bool:
        if self.value < other.value:
            return True
        elif self.value == other.value:
            return (self.excluded, self.required) > (other.excluded,other.required)

        return False
