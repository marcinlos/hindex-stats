import itertools
from functools import reduce
from operator import or_
from typing import Callable, Iterable


def take(n: int, xs: Iterable) -> Iterable:
    """
    Generates n first elements of xs, or fewer if xs generates less than
    n elements.
    """
    return itertools.islice(xs, n)


class SkipOnce:
    """
    A callable object that does nothing the first time it is called. Each
    subsequent call is forwarded to a stored callable.

    Intended use case: actions that should be preformed between loop
    iterations, but not before/after.
    """

    def __init__(self, action: Callable):
        self.action = action
        self.first = True

    def __call__(self):
        """
        First call: does nothing
        Subsequent calls: calls the stored action
        """
        if not self.first:
            self.action()
        else:
            self.first = False


def flag_union(flags: Iterable, init):
    """
    Computes the union of given flags and the init flag.
    """
    return reduce(or_, flags, init)
