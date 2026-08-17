"""Smoke tests for framework-agnostic logic (no Telegram / DB required)."""
from __future__ import annotations

from datetime import timedelta

import pytest

from redqueen.services.ai.rules import RuleProvider
from redqueen.utils.duration import humanize, parse_duration
from redqueen.utils.targets import target_from_arg


def test_parse_duration_variants():
    assert parse_duration("30m") == timedelta(minutes=30)
    assert parse_duration("2h") == timedelta(hours=2)
    assert parse_duration("1d") == timedelta(days=1)
    assert parse_duration("1w") == timedelta(weeks=1)
    assert parse_duration("") is None
    assert parse_duration("banana") is None


def test_humanize():
    assert "30 minutes" in humanize(timedelta(minutes=30))
    assert humanize(None) == ""


def test_humanize_english_plural():
    assert humanize(timedelta(hours=1)) == " for 1 hour"
    assert humanize(timedelta(hours=2)) == " for 2 hours"


def test_humanize_localized():
    # Russian: one/few/many forms after "на".
    assert humanize(timedelta(hours=1), "ru") == " на 1 час"
    assert humanize(timedelta(hours=2), "ru") == " на 2 часа"
    assert humanize(timedelta(hours=5), "ru") == " на 5 часов"
    assert humanize(timedelta(minutes=21), "ru") == " на 21 минуту"  # ..1 but not 11 → one
    # Ukrainian.
    assert humanize(timedelta(hours=1), "uk") == " на 1 годину"
    assert humanize(timedelta(hours=3), "uk") == " на 3 години"
    assert humanize(timedelta(hours=11), "uk") == " на 11 годин"
    # Unknown language falls back to English; permanent stays empty.
    assert humanize(timedelta(minutes=5), "de") == " for 5 minutes"
    assert humanize(None, "ru") == ""


def test_target_from_arg():
    assert target_from_arg("12345").user_id == 12345
    assert target_from_arg("@12345").user_id == 12345
    assert target_from_arg("@name") is None
    assert target_from_arg(None) is None


@pytest.mark.asyncio
async def test_rule_provider_flags_scam():
    v = await RuleProvider().classify_text("Free crypto giveaway, join t.me/scam now!")
    assert v.is_violation
    assert v.category in {"scam", "spam"}


@pytest.mark.asyncio
async def test_rule_provider_passes_clean_text():
    v = await RuleProvider().classify_text("Good morning everyone, how are you?")
    assert not v.is_violation
    assert v.category == "ok"
