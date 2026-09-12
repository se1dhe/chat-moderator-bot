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
    "antiflood": {"enabled": False, "limit": 5, "window": 10, "action": "mute",
                  "mute_seconds": 600, "ban_seconds": 0},
    # Duration of the penalty applied when the warn limit is hit (0 == permanent).
    # Used only when `warn_action` is "mute" or "ban" respectively.
    "warns": {"mute_seconds": 3600, "ban_seconds": 0},
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
    # `thresholds`: optional per-category overrides (0..100), e.g. {"scam": 60}.
    # Empty → the chat's global `ai_threshold` column applies to every category.
    "ai": {"max_per_minute": 20, "thresholds": {}},
    "raid": {
        "enabled": False,
        "join_threshold": 5,
        "window_seconds": 30,
        "lock_seconds": 600,
        "locked_until": None,  # epoch seconds, or None when not locked
    },
    "auto_comment": {
        "enabled": False,
        "text": "",
        "media_url": "",
    },
    "onboarding": {
        "setup_completed": False,
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


# ---------------------------------------------------------------------------
# Merged view + validated patch — the single contract the Mini App API speaks.
# Keeps all range/enum validation in one pure place so the HTTP layer stays thin.
# ---------------------------------------------------------------------------

from .ai.provider import CATEGORIES

_VIOLATION_CATEGORIES = tuple(c for c in CATEGORIES if c != "ok")
_MEDIA_TYPES = {"sticker", "animation", "voice", "video_note"}
_WARN_ACTIONS = {"mute", "kick", "ban"}
_AI_MODES = {"off", "quarantine", "autoban"}
_CAPTCHA_MODES = {"button", "math"}


def _clamp(value: Any, lo: int, hi: int, default: int) -> int:
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default


def _as_bool(value: Any, default: bool) -> bool:
    return bool(value) if isinstance(value, bool) else default


# Penalty durations in seconds: 0 means permanent, otherwise 30s..365d.
_MAX_PENALTY_SECONDS = 365 * 86400


def _duration(value: Any, default: int) -> int:
    try:
        v = int(value)
    except (TypeError, ValueError):
        return default
    if v <= 0:
        return 0  # permanent
    return max(30, min(_MAX_PENALTY_SECONDS, v))


def full_view(settings: ChatSettings) -> dict[str, Any]:
    """Everything the Mini App shows for a chat: core columns + JSONB sections."""
    cfg = get_config(settings)
    return {
        "core": {
            "warn_limit": settings.warn_limit,
            "warn_action": settings.warn_action,
            "ai_mode": settings.ai_mode,
            "ai_threshold": settings.ai_threshold,
            "ai_provider": getattr(settings, "ai_provider", "ollama"),
            "ai_model": getattr(settings, "ai_model", ""),
            "ai_has_key": bool(getattr(settings, "ai_api_key_encrypted", None)),
        },
        "warns": cfg["warns"],
        "captcha": cfg["captcha"],
        "antiflood": cfg["antiflood"],
        "filters": cfg["filters"],
        "modes": cfg["modes"],
        "ai": cfg["ai"],
        "raid": {k: v for k, v in cfg["raid"].items() if k != "locked_until"}
        | {"locked": bool(cfg["raid"].get("locked_until"))},
        "auto_comment": cfg["auto_comment"],
        "onboarding": cfg["onboarding"],
        "exempt_user_ids": cfg["exempt_user_ids"],
    }


def apply_patch(settings: ChatSettings, patch: dict[str, Any]) -> dict[str, Any]:
    """Validate & apply a (possibly partial) settings patch from the Mini App.

    Unknown keys are ignored; every value is clamped to its allowed range/enum so the
    HTTP layer can forward request bodies without trusting them. Returns `full_view`.
    """
    cfg = get_config(settings)

    core = patch.get("core", {})
    if "warn_limit" in core:
        settings.warn_limit = _clamp(core["warn_limit"], 1, 20, settings.warn_limit)
    if core.get("warn_action") in _WARN_ACTIONS:
        settings.warn_action = core["warn_action"]
    if core.get("ai_mode") in _AI_MODES:
        settings.ai_mode = core["ai_mode"]
    if "ai_threshold" in core:
        settings.ai_threshold = _clamp(core["ai_threshold"], 0, 100, settings.ai_threshold)
    if "ai_provider" in core and core["ai_provider"] in {"ollama", "openai", "gemini", "claude"}:
        settings.ai_provider = core["ai_provider"]
    if "ai_model" in core:
        settings.ai_model = str(core["ai_model"])[:64]

    if "warns" in patch:
        w, cur = patch["warns"], cfg["warns"]
        cfg["warns"] = {
            "mute_seconds": _duration(w.get("mute_seconds"), cur["mute_seconds"]),
            "ban_seconds": _duration(w.get("ban_seconds"), cur["ban_seconds"]),
        }

    if "captcha" in patch:
        c, cur = patch["captcha"], cfg["captcha"]
        cfg["captcha"] = {
            "enabled": _as_bool(c.get("enabled"), cur["enabled"]),
            "mode": c["mode"] if c.get("mode") in _CAPTCHA_MODES else cur["mode"],
            "timeout_seconds": _clamp(c.get("timeout_seconds"), 60, 1800, cur["timeout_seconds"]),
        }

    if "antiflood" in patch:
        a, cur = patch["antiflood"], cfg["antiflood"]
        cfg["antiflood"] = {
            "enabled": _as_bool(a.get("enabled"), cur["enabled"]),
            "limit": _clamp(a.get("limit"), 2, 50, cur["limit"]),
            "window": _clamp(a.get("window"), 2, 300, cur["window"]),
            "action": a["action"] if a.get("action") in _WARN_ACTIONS else cur["action"],
            "mute_seconds": _clamp(a.get("mute_seconds"), 30, 86400, cur["mute_seconds"]),
            "ban_seconds": _duration(a.get("ban_seconds"), cur.get("ban_seconds", 0)),
        }

    if "filters" in patch:
        f, cur = patch["filters"], cfg["filters"]
        words = cur["banned_words"]
        if isinstance(f.get("banned_words"), list):
            words = _clean_words(f["banned_words"])
        media = cur["blocked_media"]
        if isinstance(f.get("blocked_media"), list):
            media = sorted({m for m in f["blocked_media"] if m in _MEDIA_TYPES})
        cfg["filters"] = {
            "banned_words": words,
            "block_links": _as_bool(f.get("block_links"), cur["block_links"]),
            "block_forwards": _as_bool(f.get("block_forwards"), cur["block_forwards"]),
            "block_mentions": _as_bool(f.get("block_mentions"), cur["block_mentions"]),
            "blocked_media": media,
        }

    if "modes" in patch:
        m, cur = patch["modes"], cfg["modes"]
        night = cur["night"]
        if isinstance(m.get("night"), dict):
            night = {
                "enabled": _as_bool(m["night"].get("enabled"), night["enabled"]),
                "start": _clamp(m["night"].get("start"), 0, 23, night["start"]),
                "end": _clamp(m["night"].get("end"), 0, 23, night["end"]),
            }
        cfg["modes"] = {
            "night": night,
            "silent": _as_bool(m.get("silent"), cur["silent"]),
            "slow_seconds": _clamp(m.get("slow_seconds"), 0, 3600, cur["slow_seconds"]),
        }

    if "ai" in patch:
        a, cur = patch["ai"], cfg["ai"]
        thresholds = cur.get("thresholds", {})
        if isinstance(a.get("thresholds"), dict):
            thresholds = {
                cat: _clamp(val, 0, 100, 80)
                for cat, val in a["thresholds"].items()
                if cat in _VIOLATION_CATEGORIES
            }
        cfg["ai"] = {
            "max_per_minute": _clamp(a.get("max_per_minute"), 1, 600, cur["max_per_minute"]),
            "thresholds": thresholds,
        }

    if "raid" in patch:
        r, cur = patch["raid"], cfg["raid"]
        cfg["raid"] = {
            **cur,
            "enabled": _as_bool(r.get("enabled"), cur["enabled"]),
            "join_threshold": _clamp(r.get("join_threshold"), 2, 100, cur["join_threshold"]),
            "window_seconds": _clamp(r.get("window_seconds"), 5, 600, cur["window_seconds"]),
            "lock_seconds": _clamp(r.get("lock_seconds"), 60, 86400, cur["lock_seconds"]),
        }
        # The Mini App may only *clear* an active lock, never set one.
        if r.get("locked") is False:
            cfg["raid"]["locked_until"] = None

    if "auto_comment" in patch:
        ac, cur = patch["auto_comment"], cfg["auto_comment"]
        cfg["auto_comment"] = {
            "enabled": _as_bool(ac.get("enabled"), cur["enabled"]),
            "text": str(ac.get("text", cur["text"]))[:4000],
            "media_url": str(ac.get("media_url", cur["media_url"]))[:1000],
        }

    if "onboarding" in patch:
        ob, cur = patch["onboarding"], cfg["onboarding"]
        cfg["onboarding"] = {
            "setup_completed": _as_bool(ob.get("setup_completed"), cur["setup_completed"]),
        }

    if isinstance(patch.get("exempt_user_ids"), list):
        cleaned: list[int] = []
        for uid in patch["exempt_user_ids"]:
            try:
                cleaned.append(int(uid))
            except (TypeError, ValueError):
                continue
        cfg["exempt_user_ids"] = cleaned

    settings.data = cfg
    return full_view(settings)


def _clean_words(words: list) -> list[str]:
    out: list[str] = []
    for w in words:
        if not isinstance(w, str):
            continue
        w = w.strip().lower()[:60]
        if w and w not in out:
            out.append(w)
        if len(out) >= 500:
            break
    return out
