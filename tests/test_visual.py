"""handlers.ai_review._visual_source: pick a downloadable image from photo/sticker/GIF."""
from __future__ import annotations

from types import SimpleNamespace

from redqueen.handlers.ai_review import _visual_source


def _msg(**kw):
    base = {"photo": None, "sticker": None, "animation": None}
    base.update(kw)
    return SimpleNamespace(**base)


def test_photo_uses_largest_size():
    m = _msg(photo=["small", "medium", "large"])
    assert _visual_source(m) == "large"


def test_sticker_uses_thumbnail():
    m = _msg(sticker=SimpleNamespace(thumbnail="sticker_thumb"))
    assert _visual_source(m) == "sticker_thumb"


def test_animation_uses_thumbnail():
    m = _msg(animation=SimpleNamespace(thumbnail="gif_thumb"))
    assert _visual_source(m) == "gif_thumb"


def test_nothing_visual_returns_none():
    assert _visual_source(_msg()) is None
