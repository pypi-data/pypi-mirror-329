from __future__ import annotations

import collections.abc
import itertools
import typing

from .exception import NoMatch
from .item import ResourceItem
from .utils import escape_str, quote_str, unique_everseen

try:
    from typing import Self  # type: ignore (py3.11+)
except ImportError:
    from typing_extensions import Self

UNSAFE_CHARS = {',', ':', ';', '"', "'"}


def quote_item(item: str) -> str:
    if item.startswith(' ') or item.endswith(' ') or '\t' in item or '\n' in item:
        return quote_str(item)

    return escape_str(item, UNSAFE_CHARS)


def combine_item(left: float | None, right: float | None) -> float | None:
    """ Combine item values

    Returns the **strongest** match, ie. the lower numeric value.
    If one value is ``None``, returns the other value.
    """
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)


class ResourceGroup:
    """ A group of :py:class:`~momotor.shared.resources`.
    """
    _items: tuple[ResourceItem, ...]
    
    def __init__(self, items: collections.abc.Iterable[ResourceItem] | None = None):
        self._items = tuple(items) if items is not None else ()

    # Factories

    @classmethod
    def create(cls, value: str | collections.abc.Iterable[str]) -> Self:
        return cls(ResourceItem.create(value))

    @classmethod
    def union(cls, *groups: Self) -> Self:
        """ Merge multiple resource groups into a new one """
        return cls(unique_everseen(itertools.chain(*(group.items for group in groups))))
    
    @classmethod
    def difference(cls, *groups: Self) -> Self:
        """ Return a new resource group with items that are in the first group but not in the others """
        if not groups:
            return cls()
        
        return cls(
            item for item in groups[0].items 
            if item not in cls.union(*groups[1:]).items
        )
    
    # Implementation

    def __len__(self):
        return len(self._items)

    @property
    def items(self) -> tuple[ResourceItem, ...]:
        return self._items

    def match(self, worker_group: Self | None) -> float | None:
        """ Returns the match between this resource group and the provided worker's resource group

        :param worker_group: The worker's resource group
        :return: match value, the lower the value, the better the match is (ranges from
                 :py:data:`-inf <math.inf>` to :py:data:`+inf <math.inf>`)
        :raises: :py:exc:`~momotor.shared.resources.NoMatch` if there are missing or excluded tags
        """
        match = None
        unmatched = frozenset(worker_group.items) if worker_group is not None else frozenset()
        for task_resource in self.items:
            matched = set()
            for worker_resource in unmatched:
                if task_resource.comparable(worker_resource):
                    matched.add(worker_resource)
                    match = combine_item(match, task_resource.compare(worker_resource))

            # If no tag matched, but the task tag is required, it's no match
            if not matched and task_resource.required:
                raise NoMatch

            unmatched -= matched

        # process resources defined on the worker but not the task
        for worker_resource in unmatched:
            match = combine_item(match, worker_resource.compare_missing(worker_resource))

        return match

    def as_str_tuple(self) -> tuple[str, ...]:
        return tuple(item.as_str() for item in self._items)

    def as_str(self) -> str:
        return ','.join(quote_item(item) for item in self.as_str_tuple())
