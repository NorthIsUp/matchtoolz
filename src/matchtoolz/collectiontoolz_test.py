from collections import namedtuple

import pytest

from matchtoolz.collectiontoolz import Contains, IsIn


@pytest.fixture
def hobbits() -> list[str]:
    return ["Frodo", "Sam", "Merry", "Pippin", "Gandalf", "Legolas", "Gimli"]


@pytest.fixture
def dwarves() -> list[str]:
    return ["Gimli", "Thorin", "Balin", "Dwalin", "Fili", "Kili", "Dori", "Nori"]


Characters = namedtuple("Characters", ["hobbits", "dwarves"])


def test_is_in(hobbits: list[str], dwarves: list[str]) -> None:
    lotr = Characters(hobbits, dwarves)

    match IsIn("Frodo"):
        case lotr.hobbits:
            assert True
        case lotr.dwarves:
            assert False
        case _:
            assert False


def test_contains(hobbits: list[str], dwarves: list[str]) -> None:
    lotr = Characters(Contains(hobbits), Contains(dwarves))

    match "Frodo":
        case lotr.hobbits:
            assert True
        case lotr.dwarves:
            assert False
        case _:
            assert False
