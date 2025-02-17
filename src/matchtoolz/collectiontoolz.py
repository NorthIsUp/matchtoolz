from collections.abc import Container, Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Contains(Generic[T]):
    """
    Helper to enable containment pattern matching.

    `Contains` wraps the "case" side of the match statement allowing the match input to be a standard object.

    >>> class LotR:
    >>>     hobbits = Contains(["Frodo", "Sam", "Merry", "Pippin", "Gandalf", "Legolas", "Gimli"])
    >>>     dwarves = Contains(["Gimli", "Thorin", "Balin", "Dwalin", "Fili", "Kili", "Dori", "Nori"])
    >>>
    >>> match "Frodo":
    >>>     case LotR.hobbits:
    >>>         assert True
    >>>     case LotR.dwarves:
    >>>         assert False
    >>>     case _:
    >>>         assert False
    """

    items: Container[T]

    def __post_init__(self) -> None:
        # try to convert to a set if possible for faster lookups,
        # but not all Containers are Iterable or hashable
        try:
            if isinstance(self.items, Iterable):
                self.items = frozenset(self.items)
        except TypeError:
            pass

    def __eq__(self, elem: T) -> bool:
        return elem in self.items

    def __contains__(self, elem: T) -> bool:
        return elem in self.items


@dataclass
class IsIn(Generic[T]):
    """
    Helper to enable containment pattern matching.

    `IsIn` wraps the "match" input of the match statement, allowing the case side to be a standard collection.

    >>> class LotR:
    >>>     hobbits = ["Frodo", "Sam", "Merry", "Pippin", "Gandalf", "Legolas", "Gimli"]
    >>>     dwarves = ["Gimli", "Thorin", "Balin", "Dwalin", "Fili", "Kili", "Dori", "Nori"]
    >>>
    >>> match IsIn("Frodo"):
    >>>     case LotR.hobbits:
    >>>         assert True
    >>>     case LotR.dwarves:
    >>>         assert False
    """

    elem: T

    def __eq__(self, collection: Container[T]) -> bool:
        return self.elem in collection

    def __contains__(self, collection: Container[T]) -> bool:
        return self.elem in collection
