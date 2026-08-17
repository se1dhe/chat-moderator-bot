"""services/config: merged full_view + validated apply_patch (Mini App contract)."""
from __future__ import annotations

from redqueen.db.models import ChatSettings
from redqueen.services.config import apply_patch, full_view


def _cs() -> ChatSettings:
    return ChatSettings(warn_limit=3, warn_action="mute", ai_mode="off", ai_threshold=80, data={})


def test_full_view_shape():
    view = full_view(_cs())
    assert set(view) == {"core", "warns", "captcha", "antiflood", "filters", "modes", "ai", "raid",
                         "exempt_user_ids"}
    assert view["core"]["warn_limit"] == 3
    # raid never leaks the internal locked_until timestamp; only a boolean.
    assert "locked_until" not in view["raid"]
    assert view["raid"]["locked"] is False


def test_apply_patch_core_clamps_and_validates():
    cs = _cs()
    view = apply_patch(cs, {"core": {"warn_limit": 999, "warn_action": "nonsense", "ai_mode": "quarantine"}})
    assert view["core"]["warn_limit"] == 20      # clamped
    assert view["core"]["warn_action"] == "mute"  # invalid enum ignored
    assert view["core"]["ai_mode"] == "quarantine"


def test_apply_patch_unknown_keys_ignored():
    cs = _cs()
    view = apply_patch(cs, {"bogus": {"x": 1}, "captcha": {"enabled": True, "mode": "hack"}})
    assert view["captcha"]["enabled"] is True
    assert view["captcha"]["mode"] == "button"  # invalid mode falls back to default


def test_apply_patch_ai_thresholds_filtered():
    cs = _cs()
    view = apply_patch(cs, {"ai": {"thresholds": {"scam": 150, "ok": 10, "bogus": 5}}})
    assert view["ai"]["thresholds"] == {"scam": 100}  # clamped; ok/bogus dropped


def test_apply_patch_penalty_durations():
    cs = _cs()
    # 0/negative == permanent; positive values below 30s are floored to 30s.
    view = apply_patch(cs, {"warns": {"mute_seconds": 7200, "ban_seconds": 0},
                            "antiflood": {"ban_seconds": 5}})
    assert view["warns"]["mute_seconds"] == 7200
    assert view["warns"]["ban_seconds"] == 0        # permanent
    assert view["antiflood"]["ban_seconds"] == 30   # floored
    # Over-long durations are capped at 365 days.
    view = apply_patch(cs, {"warns": {"ban_seconds": 999_999_999}})
    assert view["warns"]["ban_seconds"] == 365 * 86400


def test_apply_patch_banned_words_normalized():
    cs = _cs()
    view = apply_patch(cs, {"filters": {"banned_words": ["  SPAM ", "spam", 5, ""]}})
    assert view["filters"]["banned_words"] == ["spam"]


def test_apply_patch_can_only_clear_raid_lock():
    cs = _cs()
    apply_patch(cs, {"raid": {"enabled": True}})
    # simulate an active lock, then clear it via the API contract
    from redqueen.services.config import save_section
    save_section(cs, "raid", {"locked_until": 9999999999})
    view = apply_patch(cs, {"raid": {"locked": False}})
    assert view["raid"]["locked"] is False
