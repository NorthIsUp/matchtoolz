# matchtoolz

utilities for structural pattern matching

## `re.match`

The `Regex` helper provides a convenient way to use regular expressions in Python's structural pattern matching. It allows you to match strings against regex patterns within match statements. There is als `RegexBytes` for bytes based regular expressions.

Example:

```python
match Regex("hello"):
    case r"world":
        assert False
    case r"^h.?l+o$":
        assert True
    case _:
        assert False
```

## `__contains__`

The `IsIn` and `Contains` helpers assist in membership tests.


### `IsIn` is the "match" side helper

The `IsIn` helper is probably the easier to use for most use cases, but it may be less performat than `Contains`. `IsIn` checks for membership in the collection without modification, so you may be looking at `O(1)` for lookups.

```
lotr = Characters(hobbits, dwarves)

match IsIn("Frodo"):
    case lotr.hobbits:
        assert True
    case lotr.dwarves:
        assert False
    case _:
        assert False
```

### `Contains` is the "case" side helper

`Contains` attempts to conver the collection to a `frozenset`, so for re-used lookups this will be more performant, but you have to build the set, so it isn't worth it unless the collection will be matched multiple times.

```
lotr = Characters(Contains(hobbits), Contains(dwarves))

match "Frodo":
    case lotr.hobbits:
        assert True
    case lotr.dwarves:
        assert False
    case _:
        assert False
```
