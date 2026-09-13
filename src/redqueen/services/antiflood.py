"""Antiflood: Redis fixed-window message counter. Pure logic, no aiogram/Telegram I/O."""
from __future__ import annotations

from redis.asyncio import Redis


async def register_hit(redis: Redis, *, chat_id: int, user_id: int, window_seconds: int) -> int:
    """Increment the message counter for this chat/user window; return the new count."""
    key = f"rq:af:{chat_id}:{user_id}"
    pipe = redis.pipeline()
    pipe.incr(key)
    pipe.expire(key, window_seconds)
    results = await pipe.execute()
    count = results[0]
    return count


async def is_flooding(
    redis: Redis, *, chat_id: int, user_id: int, limit: int, window_seconds: int
) -> bool:
    count = await register_hit(redis, chat_id=chat_id, user_id=user_id, window_seconds=window_seconds)
    return count > limit
