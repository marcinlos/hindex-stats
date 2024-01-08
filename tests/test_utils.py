import pytest

import hindex_stats.utils as utils


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
