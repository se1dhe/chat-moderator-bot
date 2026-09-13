"""Per-chat AI-classification call budget (Redis fixed window).

Keeps a runaway chat (or an attacker flooding ambiguous text) from monopolizing the
shared Ollama concurrency slots. When the budget is exhausted, callers should just
skip classification for that message rather than blocking or erroring.
"""
from __future__ import annotations

from redis.asyncio import Redis


async def allow(redis: Redis, *, chat_id: int, limit: int, window_seconds: int = 60) -> bool:
    key = f"rq:aicalls:{chat_id}"
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, window_seconds)
    results = await pipe.execute()
    count = results[0]
    return count <= limit
