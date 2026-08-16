"""Human-friendly duration parsing: '30m', '2h', '1d', '1w'."""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
_PATTERN = re.compile(r"^(\d+)\s*([smhdw])$", re.IGNORECASE)


def parse_duration(text: str | None) -> timedelta | None:
    """Return a timedelta, or None if text is empty/permanent/invalid."""
    if not text:
        return None
    m = _PATTERN.match(text.strip())
    if not m:
        return None
    value, unit = int(m.group(1)), m.group(2).lower()
    return timedelta(seconds=value * _UNITS[unit])


def until_from_now(delta: timedelta | None) -> datetime | None:
    if delta is None:
        return None
    return datetime.now(timezone.utc) + delta


def humanize(delta: timedelta | None) -> str:
    if delta is None:
        return ""
    secs = int(delta.total_seconds())
    for unit, size, name in (
        ("w", 604800, "week"),
        ("d", 86400, "day"),
        ("h", 3600, "hour"),
        ("m", 60, "minute"),
        ("s", 1, "second"),
    ):
        if secs >= size:
            n = secs // size
            return f" for {n} {name}{'s' if n != 1 else ''}"
    return ""
