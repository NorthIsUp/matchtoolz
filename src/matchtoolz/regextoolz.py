import re
from dataclasses import dataclass, field
from typing import AnyStr, Generic, TypeVar

T = TypeVar("T")


@dataclass
class RegexBase(Generic[AnyStr]):
    string: AnyStr
    flags: int = re.NOFLAG
    strict: bool = True
    _match: re.Match | None = field(init=False, default=None)

    def __getitem__(self, group: int | str) -> AnyStr:
        if self._match is None:
            raise ValueError("No match found")

        return self._match[group]

    @property
    def match(self) -> re.Match:
        if self._match is None:
            raise ValueError("No match found")

        return self._match

    def group(self, group: int | str) -> AnyStr:
        return self[group]

    def groups(self) -> tuple[AnyStr, ...]:
        if self._match is None:
            raise ValueError("No match found")

        return self._match.groups()

    def groupdict(self) -> dict[str, AnyStr]:
        if self._match is None:
            raise ValueError("No match found")

        return self._match.groupdict()

    def clear_match(self) -> None:
        self._match = None


def __re_eq__(self: RegexBase, pattern: AnyStr | re.Pattern) -> bool:
    self._match = re.search(pattern, self.string, self.flags)
    return self._match is not None


@dataclass
class Regex(str, RegexBase[str]):
    """
    Helper to enable regex structural pattern matching.

    >>> match Regex("hello world"):
    >>>   case r"world":
    >>>     assert False
    >>>   case r"^h.?l+o .*d$":
    >>>     assert True
    >>>   case _:
    >>>     assert False

    "as" can be used to check capture groups:

    >>> match Regex("hello world"):
    >>>   case r"^h(?P<a>.)l+o .*d$" as match:
    >>>     assert match.a == "e"
    >>>   case _:
    >>>     assert False
    """

    def __eq__(self, pattern: AnyStr | re.Pattern) -> bool:
        match pattern:
            case str():
                return __re_eq__(self, pattern)
            case bytes():
                return False if self.strict else __re_eq__(self, pattern.decode())
            case _:
                raise ValueError("Invalid pattern")


@dataclass
class RegexBytes(bytes, RegexBase[bytes]):
    """
    Same as Regex but for bytes.
    """

    def __eq__(self, pattern: AnyStr | re.Pattern) -> bool:
        match pattern:
            case bytes():
                return __re_eq__(self, pattern)
            case str():
                return False if self.strict else __re_eq__(self, pattern.encode())
            case _:
                raise ValueError("Invalid pattern")
