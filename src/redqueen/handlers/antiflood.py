"""Antiflood: per-message rate check (auto-mute/kick/ban) + chat config commands."""
from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..services import antiflood, moderation, roles
from ..services.config import get_config, save_section
from ..utils.duration import until_from_now

router = Router(name="antiflood")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

_ACTION_WORDS = {"ban": "banned", "kick": "removed", "mute": "silenced"}


@router.message()
async def check_flood(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    if message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    settings = await repo.get_settings(session, message.chat.id)
    cfg = get_config(settings)["antiflood"]
    if not cfg["enabled"]:
        raise SkipHandler

    if await roles.is_exempt(
        bot, redis, chat_id=message.chat.id, user_id=message.from_user.id, settings=settings
    ):
        raise SkipHandler

    flooding = await antiflood.is_flooding(
        redis, chat_id=message.chat.id, user_id=message.from_user.id,
        limit=cfg["limit"], window_seconds=cfg["window"],
    )
    if not flooding:
        raise SkipHandler

    action = cfg["action"]
    if action == "ban":
        await moderation.ban(bot, session, chat_id=message.chat.id, user_id=message.from_user.id,
                             actor_id=None, reason="antiflood")
    elif action == "kick":
        await moderation.kick(bot, session, chat_id=message.chat.id, user_id=message.from_user.id,
                              actor_id=None, reason="antiflood")
    else:
        until = until_from_now(timedelta(seconds=cfg["mute_seconds"]))
        await moderation.mute(bot, session, chat_id=message.chat.id, user_id=message.from_user.id,
                              actor_id=None, until=until, reason="antiflood")

    try:
        await message.delete()
    except Exception:  # noqa: BLE001
        pass

    await message.answer(
        t("ANTIFLOOD_TRIGGERED", name=message.from_user.full_name, action=_ACTION_WORDS[action])
    )


@router.message(Command("antiflood"), IsChatAdmin())
async def cmd_antiflood(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split()
    settings = await repo.get_settings(session, message.chat.id)

    if parts and parts[0] == "off":
        save_section(settings, "antiflood", {"enabled": False})
        await message.reply(t("ANTIFLOOD_DISABLED"))
        return

    if len(parts) < 3 or parts[0] != "on" or not parts[1].isdigit() or not parts[2].isdigit():
        await message.reply(t("ANTIFLOOD_USAGE"))
        return

    limit = max(2, min(50, int(parts[1])))
    window = max(2, min(300, int(parts[2])))
    section = save_section(settings, "antiflood", {"enabled": True, "limit": limit, "window": window})
    await message.reply(t("ANTIFLOOD_SET", limit=limit, window=window, action=section["action"]))


@router.message(Command("antifloodaction"), IsChatAdmin())
async def cmd_antifloodaction(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    action = (command.args or "").strip().lower()
    if action not in {"mute", "kick", "ban"}:
        await message.reply(t("ANTIFLOOD_USAGE"))
        return
    settings = await repo.get_settings(session, message.chat.id)
    section = save_section(settings, "antiflood", {"action": action})
    await message.reply(t("ANTIFLOOD_SET", limit=section["limit"], window=section["window"], action=action))
