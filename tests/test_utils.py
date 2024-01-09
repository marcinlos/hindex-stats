import pytest

import hindex_stats.utils as utils


def test_without_none_no_nones():
    """
    If no None values are present, nothing is removed.
    """
    xs = [1, 2, "a", 8, "asdf"]
    assert list(utils.without_none(xs)) == xs


def test_witout_none_all_nones():
    """
    If only None values are present, resulting iterable is empty.
    """
    xs = [None, None]
    assert not list(utils.without_none(xs))


def test_without_none_multiple():
    """
    Present None values are all removed, while non-None elements
    are preserved.
    """
    xs = [0, 1, None, None, 2, 3, None, 4]
    expected = [0, 1, 2, 3, 4]
    assert list(utils.without_none(xs)) == expected


def test_without_none_falses_are_preserved():
    """
    Values that are considered False in a boolean context are not removed.
    """
    xs = [0, 1, None, None, 2, 3, None, 4, [], 5, (), ""]
    expected = [0, 1, 2, 3, 4, [], 5, (), ""]
    assert list(utils.without_none(xs)) == expected


@pytest.fixture()
def call_counter():
    return CallCounter()


class CallCounter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1


def test_skip_once_skips_first_call(call_counter):
    """
    First call on SkipOnce object should be ignored.
    """
    action = utils.SkipOnce(call_counter)

    action()
    assert call_counter.count == 0


def test_skip_once_forwards_subsequent_calls(call_counter):
    """
    After the first call to SkipOnce, subsequent calls should be
    forwarded to the wrapped callable object.
    """
    action = utils.SkipOnce(call_counter)

    # skipped
    action()

    action()
    assert call_counter.count == 1

    action()
    assert call_counter.count == 2
