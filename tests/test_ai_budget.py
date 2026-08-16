"""services/ai_budget: per-chat Redis call budget for AI classification."""
from __future__ import annotations

import pytest

from redqueen.services.ai_budget import allow


@pytest.mark.asyncio
async def test_allow_within_limit(fake_redis):
    for _ in range(3):
        assert await allow(fake_redis, chat_id=1, limit=3)


@pytest.mark.asyncio
async def test_allow_blocks_over_limit(fake_redis):
    for _ in range(3):
        await allow(fake_redis, chat_id=1, limit=3)
    assert not await allow(fake_redis, chat_id=1, limit=3)


@pytest.mark.asyncio
async def test_allow_counts_separately_per_chat(fake_redis):
    for _ in range(5):
        await allow(fake_redis, chat_id=1, limit=3)
    assert await allow(fake_redis, chat_id=2, limit=3)
