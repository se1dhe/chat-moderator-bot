"""Raid shield: detect a coordinated join surge and auto-lock the chat."""
from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.filters.chat_member_updated import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..db.models import RaidEvent
from ..filters import IsChatAdmin
from ..services import roles
from ..services.config import get_config, save_section

router = Router(name="raid")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


def is_locked(cfg: dict) -> bool:
    locked_until = cfg["raid"]["locked_until"]
    return bool(locked_until) and datetime.now(UTC).timestamp() < locked_until


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_join_watch(
    event: ChatMemberUpdated, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)
    if not cfg["raid"]["enabled"] or is_locked(cfg):
        return

    key = f"rq:raidjoin:{event.chat.id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, cfg["raid"]["window_seconds"])
    if count < cfg["raid"]["join_threshold"]:
        return

    until = datetime.now(UTC).timestamp() + cfg["raid"]["lock_seconds"]
    save_section(settings, "raid", {"locked_until": until})
    session.add(RaidEvent(
        chat_telegram_id=event.chat.id, join_count=count,
        window_seconds=cfg["raid"]["window_seconds"],
        locked_until=datetime.fromtimestamp(until, UTC),
    ))
    await repo.log_action(
        session, chat_telegram_id=event.chat.id, action="raid_lock",
        reason=f"{count} joins in {cfg['raid']['window_seconds']}s",
    )
    minutes = max(1, cfg["raid"]["lock_seconds"] // 60)
    await bot.send_message(event.chat.id, t("RAID_LOCKED", count=count, minutes=minutes))


@router.message()
async def enforce_lock(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    if message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    settings = await repo.get_settings(session, message.chat.id)
    cfg = get_config(settings)
    if not is_locked(cfg):
        raise SkipHandler

    if await roles.is_exempt(
        bot, redis, chat_id=message.chat.id, user_id=message.from_user.id, settings=settings
    ):
        raise SkipHandler

    try:
        await message.delete()
    except Exception:  # noqa: BLE001
        pass


@router.message(Command("raidshield"), IsChatAdmin())
async def cmd_raidshield(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    choice = (command.args or "").strip().lower()
    if choice not in {"on", "off"}:
        await message.reply(t("RAIDSHIELD_USAGE"))
        return
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "raid", {"enabled": choice == "on"})
    await message.reply(t("RAIDSHIELD_ENABLED" if choice == "on" else "RAIDSHIELD_DISABLED"))


@router.message(Command("raidconfig"), IsChatAdmin())
async def cmd_raidconfig(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split()
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        await message.reply(t("RAIDCONFIG_USAGE"))
        return
    threshold = max(2, min(100, int(parts[0])))
    window = max(5, min(600, int(parts[1])))
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "raid", {"join_threshold": threshold, "window_seconds": window})
    await message.reply(t("RAIDCONFIG_SET", threshold=threshold, window=window))


@router.message(Command("unlock"), IsChatAdmin())
async def cmd_unlock(message: Message, session: AsyncSession, t: Callable[..., str]) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "raid", {"locked_until": None})
    await message.reply(t("RAID_UNLOCKED"))
