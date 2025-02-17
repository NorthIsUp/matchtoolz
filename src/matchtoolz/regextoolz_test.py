from operator import eq, ne
from typing import Callable

import pytest

from matchtoolz.regextoolz import Regex, RegexBytes


@pytest.mark.parametrize(
    "pattern, op, string",
    [
        ("hello", eq, "hello"),
        ("hello", ne, "world"),
        ("hello", eq, "hel+o"),
        ("hello", eq, "(hello|world)"),
        ("world", ne, "hello"),
    ],
)
def test_regex_equal(pattern: str, op: Callable[[str, str], bool], string: str):
    assert op(Regex(pattern), string)


def test_example_bytes():
    assert RegexBytes(b"Something") == b"^S.*ing$"


def test_match_statement():
    match Regex("hello"):
        case r"world":
            assert False
        case r"hello":
            assert True
        case _:
            assert False


def test_match_statement_bytes():
    match RegexBytes(b"hello world"):
        case r"^h.?l+o .*d$":
            assert False
        case b"^h.?l+o .*d$":
            assert True
        case _:
            assert False
