"""handlers/raid.is_locked: pure lock-expiry check over the config snapshot."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from redqueen.handlers.raid import is_locked
from redqueen.services.config import DEFAULT_DATA


def _cfg(locked_until):
    return {"raid": {**DEFAULT_DATA["raid"], "locked_until": locked_until}}


def test_not_locked_when_unset():
    assert not is_locked(_cfg(None))


def test_locked_when_future_timestamp():
    future = (datetime.now(UTC) + timedelta(minutes=5)).timestamp()
    assert is_locked(_cfg(future))


def test_not_locked_when_timestamp_in_past():
    past = (datetime.now(UTC) - timedelta(minutes=5)).timestamp()
    assert not is_locked(_cfg(past))
