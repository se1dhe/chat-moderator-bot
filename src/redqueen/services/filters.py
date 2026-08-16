"""Pure content-filter evaluation: banned words, links, forwards, mentions, media.

No aiogram side effects here — `evaluate()` only inspects a `Message` and returns
what, if anything, violates the chat's configured filters. The caller decides what
to do about it (delete, log, notify).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from aiogram.types import Message

_URL_RE = re.compile(r"(https?://|t\.me/|www\.)\S+", re.IGNORECASE)
_MENTION_RE = re.compile(r"(?<!\w)@\w{4,}")
_LINK_ENTITY_TYPES = {"url", "text_link"}
_MENTION_ENTITY_TYPES = {"mention", "text_mention"}


@dataclass
class FilterHit:
    kind: str    # banned_word | link | forward | mention | media
    reason: str  # short machine-readable reason, stored on the ModAction row


def evaluate(message: Message, cfg: dict[str, Any]) -> FilterHit | None:
    text = message.text or message.caption or ""
    low = text.lower()

    for word in cfg["banned_words"]:
        if word and word.lower() in low:
            return FilterHit(kind="banned_word", reason=f"banned word: {word}")

    if cfg["block_links"] and (_URL_RE.search(text) or _has_entity(message, _LINK_ENTITY_TYPES)):
        return FilterHit(kind="link", reason="link")

    if cfg["block_forwards"] and message.forward_origin is not None:
        return FilterHit(kind="forward", reason="forwarded message")

    if cfg["block_mentions"] and (
        _MENTION_RE.search(text) or _has_entity(message, _MENTION_ENTITY_TYPES)
    ):
        return FilterHit(kind="mention", reason="mention")

    media_kind = _media_kind(message)
    if media_kind and media_kind in cfg["blocked_media"]:
        return FilterHit(kind="media", reason=f"blocked media: {media_kind}")

    return None


def _has_entity(message: Message, types: set[str]) -> bool:
    entities = list(message.entities or []) + list(message.caption_entities or [])
    return any(e.type in types for e in entities)


def _media_kind(message: Message) -> str | None:
    if message.sticker:
        return "sticker"
    if message.animation:
        return "animation"
    if message.voice:
        return "voice"
    if message.video_note:
        return "video_note"
    return None
