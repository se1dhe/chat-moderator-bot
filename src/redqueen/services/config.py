"""Typed view over `ChatSettings.data` (JSONB) with defaults for M2 features.

Kept as plain dicts (not extra columns) since these are chat-configurable toggles
that grow over releases; each new M2 feature reads/writes its own sub-key.
"""
from __future__ import annotations

import copy
from typing import Any

from ..db.models import ChatSettings

DEFAULT_DATA: dict[str, Any] = {
    "captcha": {"enabled": False, "mode": "button", "timeout_seconds": 300},
    "antiflood": {"enabled": False, "limit": 5, "window": 10, "action": "mute", "mute_seconds": 600},
    "filters": {
        "banned_words": [],
        "block_links": False,
        "block_forwards": False,
        "block_mentions": False,
        "blocked_media": [],
    },
    "modes": {
        "night": {"enabled": False, "start": 23, "end": 7},
        "silent": False,
        "slow_seconds": 0,
    },
    "ai": {"max_per_minute": 20},
    "raid": {
        "enabled": False,
        "join_threshold": 5,
        "window_seconds": 30,
        "lock_seconds": 600,
        "locked_until": None,  # epoch seconds, or None when not locked
    },
    "exempt_user_ids": [],
}


def _deep_update(base: dict, override: dict) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value


def get_config(settings: ChatSettings) -> dict[str, Any]:
    """Defaults deep-merged with the stored data. Does not mutate `settings.data`."""
    merged = copy.deepcopy(DEFAULT_DATA)
    _deep_update(merged, settings.data or {})
    return merged


def save_section(settings: ChatSettings, section: str, patch: dict[str, Any]) -> dict[str, Any]:
    """Merge `patch` into `data[section]` and persist (reassigns `.data` so the ORM
    detects the change). Returns the section's new value."""
    config = get_config(settings)
    config[section].update(patch)
    settings.data = config
    return config[section]


def save_root(settings: ChatSettings, key: str, value: Any) -> None:
    """Set a top-level key (e.g. `exempt_user_ids`) and persist."""
    config = get_config(settings)
    config[key] = value
    settings.data = config
