"""Role/exemption checks shared by antiflood, content filters, and mode enforcement."""
from __future__ import annotations

from aiogram import Bot
from redis.asyncio import Redis

from ..db.models import ChatSettings
from .config import get_config

_ADMIN_CACHE_TTL = 300  # seconds; a chat always has >=1 admin (the creator)


async def is_exempt(
    bot: Bot, redis: Redis, *, chat_id: int, user_id: int, settings: ChatSettings
) -> bool:
    """Whether `user_id` should bypass automated moderation (antiflood/filters/modes)."""
    config = get_config(settings)
    if user_id in config["exempt_user_ids"]:
        return True
    return await is_admin(bot, redis, chat_id=chat_id, user_id=user_id)


async def is_admin(bot: Bot, redis: Redis, *, chat_id: int, user_id: int) -> bool:
    key = f"rq:admins:{chat_id}"
    cached = await redis.smembers(key)
    if cached:
        return str(user_id) in cached

    admins = await bot.get_chat_administrators(chat_id)
    ids = [str(admin.user.id) for admin in admins]
    if ids:
        await redis.sadd(key, *ids)
        await redis.expire(key, _ADMIN_CACHE_TTL)
    return str(user_id) in ids
