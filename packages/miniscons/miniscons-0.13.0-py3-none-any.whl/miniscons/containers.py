from functools import reduce
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def unique(lst: list[T]) -> list[T]:
    empty = []  # type: list[T]
    return list(reduce(lambda acc, x: acc if x in acc else [*acc, x], lst, empty))


def flatten(ignore: list[T | list[T]]) -> list[T]:
    return list(sum(map(lambda x: x if isinstance(x, list) else [x], ignore), []))


def merge_maps(
    x: dict[T, list[U]], y: dict[T, list[U]], keys: list[T]
) -> dict[T, list[U]]:
    return {k: unique(x.get(k, []) + y.get(k, [])) for k in keys}
