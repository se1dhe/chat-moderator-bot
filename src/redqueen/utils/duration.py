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


# Unit sizes, largest first — the first unit the duration reaches is the one shown.
_SIZES = (("w", 604800), ("d", 86400), ("h", 3600), ("m", 60), ("s", 1))

# Prefix + pluralized unit names per language. English has 2 forms (one/other),
# Russian & Ukrainian have 3 (one/few/many) selected by `_slavic_plural`.
_PREFIX = {"en": " for ", "ru": " на ", "uk": " на "}
_UNIT_NAMES = {
    "en": {  # (singular, plural)
        "w": ("week", "weeks"), "d": ("day", "days"), "h": ("hour", "hours"),
        "m": ("minute", "minutes"), "s": ("second", "seconds"),
    },
    "ru": {  # accusative after "на": (one, few, many)
        "w": ("неделю", "недели", "недель"), "d": ("день", "дня", "дней"),
        "h": ("час", "часа", "часов"), "m": ("минуту", "минуты", "минут"),
        "s": ("секунду", "секунды", "секунд"),
    },
    "uk": {  # accusative after "на": (one, few, many)
        "w": ("тиждень", "тижні", "тижнів"), "d": ("день", "дні", "днів"),
        "h": ("годину", "години", "годин"), "m": ("хвилину", "хвилини", "хвилин"),
        "s": ("секунду", "секунди", "секунд"),
    },
}


def _slavic_plural(n: int) -> int:
    """Index into a (one, few, many) tuple for Russian/Ukrainian plural forms."""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return 0
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return 1
    return 2


def humanize(delta: timedelta | None, lang: str = "en") -> str:
    """A localized ' for 2 hours' / ' на 2 часа' suffix (leading space), '' if permanent."""
    if delta is None:
        return ""
    code = lang.lower().split("-")[0] if lang else "en"
    if code not in _UNIT_NAMES:
        code = "en"
    secs = int(delta.total_seconds())
    for unit, size in _SIZES:
        if secs >= size:
            n = secs // size
            forms = _UNIT_NAMES[code][unit]
            name = forms[0 if n == 1 else 1] if code == "en" else forms[_slavic_plural(n)]
            return f"{_PREFIX[code]}{n} {name}"
    return ""
