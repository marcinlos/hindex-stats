import itertools
from typing import Iterable


def take(n: int, xs: Iterable) -> Iterable:
    return itertools.islice(xs, n)
