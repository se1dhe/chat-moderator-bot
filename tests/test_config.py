"""services/config: default-merged view over ChatSettings.data (JSONB)."""
from __future__ import annotations

from redqueen.db.models import ChatSettings
from redqueen.services.config import get_config, save_root, save_section


def test_get_config_returns_defaults_when_empty():
    cs = ChatSettings(data={})
    cfg = get_config(cs)
    assert cfg["captcha"]["enabled"] is False
    assert cfg["antiflood"]["limit"] == 5
    assert cfg["exempt_user_ids"] == []


def test_get_config_merges_stored_overrides():
    cs = ChatSettings(data={"captcha": {"enabled": True}})
    cfg = get_config(cs)
    assert cfg["captcha"]["enabled"] is True
    assert cfg["captcha"]["mode"] == "button"  # untouched default preserved


def test_get_config_does_not_mutate_defaults_between_calls():
    cs = ChatSettings(data={})
    cfg = get_config(cs)
    cfg["captcha"]["enabled"] = True
    assert get_config(cs)["captcha"]["enabled"] is False


def test_save_section_persists_and_keeps_sibling_defaults():
    cs = ChatSettings(data={})
    section = save_section(cs, "antiflood", {"enabled": True, "limit": 10})
    assert section == {"enabled": True, "limit": 10, "window": 10, "action": "mute", "mute_seconds": 600}
    assert cs.data["antiflood"]["enabled"] is True


def test_save_root_persists():
    cs = ChatSettings(data={})
    save_root(cs, "exempt_user_ids", [1, 2, 3])
    assert cs.data["exempt_user_ids"] == [1, 2, 3]
