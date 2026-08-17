"""Role/exemption checks shared by antiflood, content filters, and mode enforcement."""
from __future__ import annotations

import logging

from aiogram import Bot
from redis.asyncio import Redis

from ..db.models import ChatSettings
from .config import get_config

log = logging.getLogger(__name__)

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

    try:
        admins = await bot.get_chat_administrators(chat_id)
    except Exception as exc:  # noqa: BLE001
        # Bot not in the chat / no access / channel without admin list → treat as non-admin.
        log.debug("get_chat_administrators(%s) failed: %s", chat_id, exc)
        return False
    ids = [str(admin.user.id) for admin in admins]
    if ids:
        await redis.sadd(key, *ids)
        await redis.expire(key, _ADMIN_CACHE_TTL)
    return str(user_id) in ids
