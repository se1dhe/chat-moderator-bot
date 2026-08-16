"""handlers/modes.in_night_window: pure hour-range check (wraps past midnight)."""
from __future__ import annotations

from redqueen.handlers.modes import in_night_window


def test_same_day_window():
    assert in_night_window(2, 1, 5)
    assert not in_night_window(6, 1, 5)


def test_window_wraps_midnight():
    assert in_night_window(23, 23, 7)
    assert in_night_window(3, 23, 7)
    assert not in_night_window(10, 23, 7)


def test_equal_bounds_disables_window():
    assert not in_night_window(5, 5, 5)
