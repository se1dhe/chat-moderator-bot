"""services/antiflood: Redis fixed-window counter logic."""
from __future__ import annotations

import pytest

from redqueen.services.antiflood import is_flooding, register_hit


@pytest.mark.asyncio
async def test_register_hit_increments(fake_redis):
    assert await register_hit(fake_redis, chat_id=1, user_id=2, window_seconds=10) == 1
    assert await register_hit(fake_redis, chat_id=1, user_id=2, window_seconds=10) == 2


@pytest.mark.asyncio
async def test_is_flooding_triggers_over_limit(fake_redis):
    for _ in range(3):
        assert not await is_flooding(fake_redis, chat_id=1, user_id=2, limit=3, window_seconds=10)
    assert await is_flooding(fake_redis, chat_id=1, user_id=2, limit=3, window_seconds=10)


@pytest.mark.asyncio
async def test_is_flooding_counts_separately_per_user(fake_redis):
    for _ in range(5):
        await is_flooding(fake_redis, chat_id=1, user_id=1, limit=3, window_seconds=10)
    assert not await is_flooding(fake_redis, chat_id=1, user_id=2, limit=3, window_seconds=10)
