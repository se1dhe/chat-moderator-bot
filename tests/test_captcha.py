"""services/captcha.build_challenge: button/math challenge generation."""
from __future__ import annotations

from redqueen.services.captcha import build_challenge


def test_button_challenge():
    c = build_challenge("button")
    assert c.kind == "button"
    assert c.answer == 1
    assert c.options == [1]


def test_math_challenge_has_correct_answer_among_four_unique_options():
    c = build_challenge("math")
    assert c.kind == "math"
    assert c.answer == c.prompt_kwargs["a"] + c.prompt_kwargs["b"]
    assert len(c.options) == 4
    assert len(set(c.options)) == 4
    assert c.answer in c.options
    assert all(o > 0 for o in c.options)
