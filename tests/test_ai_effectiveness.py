"""AI overhaul: trust-tuned thresholds, verdict cache, enriched rule fallback."""
from __future__ import annotations

import pytest

from redqueen.services import ai_cache, trust
from redqueen.services.ai.provider import Verdict
from redqueen.services.ai.rules import RuleProvider


def test_effective_threshold_neutral_trust_unchanged():
    assert trust.effective_threshold(80, 50) == 80


def test_effective_threshold_low_trust_easier_to_flag():
    # trust 0 → threshold lowered by the full swing
    assert trust.effective_threshold(80, 0) == 70


def test_effective_threshold_high_trust_harder_to_flag():
    assert trust.effective_threshold(80, 100) == 90


def test_effective_threshold_clamped():
    assert trust.effective_threshold(3, 0) == 0
    assert trust.effective_threshold(98, 100) == 100


@pytest.mark.asyncio
async def test_ai_cache_roundtrip(fake_redis):
    v = Verdict("scam", 91, "crypto lure")
    assert await ai_cache.get(fake_redis, 1, "Free crypto!") is None
    await ai_cache.put(fake_redis, 1, "Free crypto!", v)
    cached = await ai_cache.get(fake_redis, 1, "  free   CRYPTO! ")  # normalized match
    assert cached is not None
    assert cached.category == "scam" and cached.score == 91


@pytest.mark.asyncio
async def test_ai_cache_scoped_per_chat(fake_redis):
    await ai_cache.put(fake_redis, 1, "hello", Verdict("ok", 95, "-"))
    assert await ai_cache.get(fake_redis, 2, "hello") is None


@pytest.mark.asyncio
async def test_rules_detect_russian_scam():
    v = await RuleProvider().classify_text("Бесплатная крипта! заработай $500 в день, пиши в whatsapp +123456789")
    assert v.is_violation
    assert v.category in {"scam", "spam"}


@pytest.mark.asyncio
async def test_rules_detect_russian_toxicity():
    v = await RuleProvider().classify_text("ты полный идиот")
    assert v.category == "toxicity"


@pytest.mark.asyncio
async def test_rules_pass_clean_ukrainian():
    v = await RuleProvider().classify_text("доброго ранку, як справи?")
    assert not v.is_violation


@pytest.mark.asyncio
async def test_classify_image_uses_caption_when_no_vision():
    # No vision model → the caption is judged by the text rules.
    v = await RuleProvider().classify_image(b"\x89PNG...", caption="free crypto giveaway t.me/x")
    assert v.category in {"scam", "spam"}


@pytest.mark.asyncio
async def test_classify_image_without_caption_is_ok_offline():
    v = await RuleProvider().classify_image(b"\x89PNG...", caption=None)
    assert not v.is_violation


@pytest.mark.asyncio
async def test_ollama_image_falls_back_without_vision_model():
    from redqueen.services.ai.ollama import OllamaProvider
    prov = OllamaProvider("http://localhost:1", "qwen3:4b", RuleProvider(), vision_model="")
    v = await prov.classify_image(b"img", caption="ты идиот")  # no network: vision disabled
    assert v.category == "toxicity"
    await prov.close()
