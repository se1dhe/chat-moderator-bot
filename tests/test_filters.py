"""services/filters.evaluate: pure content-filter checks (no aiogram I/O)."""
from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

from redqueen.services.config import DEFAULT_DATA
from redqueen.services.filters import evaluate


@dataclass
class FakeMessage:
    text: str | None = None
    caption: str | None = None
    entities: list | None = None
    caption_entities: list | None = None
    forward_origin: object | None = None
    sticker: object | None = None
    animation: object | None = None
    voice: object | None = None
    video_note: object | None = None


def _cfg(**overrides):
    cfg = {k: (list(v) if isinstance(v, list) else v) for k, v in DEFAULT_DATA["filters"].items()}
    cfg.update(overrides)
    return cfg


def test_clean_message_passes():
    assert evaluate(FakeMessage(text="good morning everyone"), _cfg()) is None


def test_banned_word_hit():
    hit = evaluate(FakeMessage(text="this is SPAMWORD here"), _cfg(banned_words=["spamword"]))
    assert hit is not None
    assert hit.kind == "banned_word"


def test_link_blocked_by_regex():
    hit = evaluate(FakeMessage(text="check https://evil.example/x"), _cfg(block_links=True))
    assert hit is not None
    assert hit.kind == "link"


def test_link_blocked_by_entity_when_text_hides_it():
    entity = SimpleNamespace(type="text_link")
    hit = evaluate(FakeMessage(text="click here", entities=[entity]), _cfg(block_links=True))
    assert hit is not None
    assert hit.kind == "link"


def test_links_allowed_when_not_configured():
    assert evaluate(FakeMessage(text="https://example.com"), _cfg(block_links=False)) is None


def test_forward_blocked():
    hit = evaluate(FakeMessage(text="hi", forward_origin=object()), _cfg(block_forwards=True))
    assert hit is not None
    assert hit.kind == "forward"


def test_mention_blocked():
    hit = evaluate(FakeMessage(text="hey @someone check this"), _cfg(block_mentions=True))
    assert hit is not None
    assert hit.kind == "mention"


def test_blocked_media_type():
    hit = evaluate(FakeMessage(sticker=object()), _cfg(blocked_media=["sticker"]))
    assert hit is not None
    assert hit.kind == "media"


def test_media_not_in_blocklist_passes():
    assert evaluate(FakeMessage(sticker=object()), _cfg(blocked_media=["voice"])) is None
