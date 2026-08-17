"""config.token_list / brand_list — the white-label orchestrator's bot fleet."""
from __future__ import annotations

from redqueen.config import Settings


def _s(**over) -> Settings:
    s = Settings(_env_file=None)
    for k, v in over.items():
        setattr(s, k, v)
    return s


def test_single_bot_falls_back_to_bot_token():
    s = _s(bot_token="111:AAA", bot_brand="RedQueen")
    assert s.token_list == ["111:AAA"]
    assert s.brand_list == ["RedQueen"]


def test_multiple_tokens_and_brands():
    s = _s(bot_token="x", bot_tokens="111:AAA, 222:BBB", bot_brands="Red, Blue")
    assert s.token_list == ["111:AAA", "222:BBB"]
    assert s.brand_list == ["Red", "Blue"]


def test_brands_padded_with_default_when_shorter():
    s = _s(bot_tokens="111:AAA,222:BBB,333:CCC", bot_brands="Red", bot_brand="RedQueen")
    assert s.brand_list == ["Red", "RedQueen", "RedQueen"]


def test_newline_separated_tokens():
    s = _s(bot_tokens="111:AAA\n222:BBB")
    assert s.token_list == ["111:AAA", "222:BBB"]


def test_empty_everything_is_empty_list():
    s = _s(bot_token="", bot_tokens="")
    assert s.token_list == []
