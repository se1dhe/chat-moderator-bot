"""i18n lookup: locale resolution and fallback."""
from __future__ import annotations

from redqueen.i18n import SUPPORTED_LANGS, resolve_lang, t


def test_resolve_lang_supported():
    assert resolve_lang("ru") == "ru"
    assert resolve_lang("UK") == "uk"
    assert resolve_lang("ru-RU") == "ru"


def test_resolve_lang_unsupported_falls_back_to_english():
    assert resolve_lang("xx") == "en"
    assert resolve_lang(None) == "en"
    assert resolve_lang("") == "en"


def test_t_formats_with_kwargs():
    assert t("en", "WARNLIMIT_SET", limit=5) == "Warn limit set to <b>5</b>."
    assert "5" in t("ru", "WARNLIMIT_SET", limit=5)


def test_t_unknown_key_falls_back_to_key_itself():
    assert t("en", "NOT_A_REAL_KEY") == "NOT_A_REAL_KEY"


def test_all_supported_locales_define_every_english_key():
    from redqueen.locales import en

    en_keys = {k for k in vars(en) if k.isupper()}
    for lang in SUPPORTED_LANGS:
        module = __import__(f"redqueen.locales.{lang}", fromlist=["_"])
        module_keys = {k for k in vars(module) if k.isupper()}
        missing = en_keys - module_keys
        assert not missing, f"{lang} is missing keys: {missing}"
