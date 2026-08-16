"""Locale lookup: `t(lang, key, **kwargs)` resolves a persona string for a chat/user."""
from __future__ import annotations

from .locales import en, ru, uk

_LOCALES = {"en": en, "ru": ru, "uk": uk}
SUPPORTED_LANGS = tuple(_LOCALES)
DEFAULT_FALLBACK = "en"


def resolve_lang(lang: str | None) -> str:
    """Normalize a language code to a supported locale, falling back to English."""
    if lang:
        code = lang.lower().split("-")[0]
        if code in _LOCALES:
            return code
    return DEFAULT_FALLBACK


def t(lang: str | None, key: str, **kwargs: object) -> str:
    module = _LOCALES[resolve_lang(lang)]
    template = getattr(module, key, None) or getattr(en, key, key)
    return template.format(**kwargs) if kwargs else template
