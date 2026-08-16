"""Night / silent / slow mode enforcement + exemption management."""
from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..services import roles
from ..services.config import get_config, save_root, save_section
from ..utils.targets import resolve_target

router = Router(name="modes")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


def in_night_window(hour: int, start: int, end: int) -> bool:
    """Whether `hour` (0-23) falls in a [start, end) window that may wrap past midnight."""
    if start == end:
        return False
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


async def _set_night(session: AsyncSession, chat_id: int, **patch: object) -> dict:
    settings = await repo.get_settings(session, chat_id)
    night = get_config(settings)["modes"]["night"]
    night.update(patch)
    save_section(settings, "modes", {"night": night})
    return night


@router.message()
async def check_modes(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    if message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    settings = await repo.get_settings(session, message.chat.id)
    cfg = get_config(settings)["modes"]

    blocking = cfg["silent"]
    if not blocking and cfg["night"]["enabled"]:
        hour = datetime.now(UTC).hour
        blocking = in_night_window(hour, cfg["night"]["start"], cfg["night"]["end"])

    slow_hit = False
    if not blocking and cfg["slow_seconds"] > 0:
        key = f"rq:slow:{message.chat.id}:{message.from_user.id}"
        slow_hit = not await redis.set(key, "1", nx=True, ex=cfg["slow_seconds"])

    if not blocking and not slow_hit:
        raise SkipHandler

    if await roles.is_exempt(
        bot, redis, chat_id=message.chat.id, user_id=message.from_user.id, settings=settings
    ):
        raise SkipHandler

    try:
        await message.delete()
    except Exception:  # noqa: BLE001
        pass


@router.message(Command("nightmode"), IsChatAdmin())
async def cmd_nightmode(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split()
    if not parts or parts[0] not in {"on", "off"}:
        await message.reply(t("NIGHTMODE_USAGE"))
        return
    if parts[0] == "off":
        night = await _set_night(session, message.chat.id, enabled=False)
        await message.reply(t("NIGHTMODE_SET", state="off", start=night["start"], end=night["end"]))
        return
    if len(parts) < 3 or not parts[1].isdigit() or not parts[2].isdigit():
        await message.reply(t("NIGHTMODE_USAGE"))
        return
    start, end = int(parts[1]) % 24, int(parts[2]) % 24
    night = await _set_night(session, message.chat.id, enabled=True, start=start, end=end)
    await message.reply(t("NIGHTMODE_SET", state="on", start=night["start"], end=night["end"]))


@router.message(Command("silentmode"), IsChatAdmin())
async def cmd_silentmode(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    choice = (command.args or "").strip().lower()
    if choice not in {"on", "off"}:
        await message.reply(t("SILENTMODE_USAGE"))
        return
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "modes", {"silent": choice == "on"})
    await message.reply(t("SILENTMODE_SET", state=choice))


@router.message(Command("slowmode"), IsChatAdmin())
async def cmd_slowmode(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    arg = (command.args or "").strip()
    if not arg.isdigit():
        await message.reply(t("SLOWMODE_USAGE"))
        return
    seconds = max(0, min(3600, int(arg)))
    settings = await repo.get_settings(session, message.chat.id)
    save_section(settings, "modes", {"slow_seconds": seconds})
    await message.reply(t("SLOWMODE_SET", seconds=seconds))


@router.message(Command("exempt"), IsChatAdmin())
async def cmd_exempt(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    parts = (command.args or "").split(maxsplit=1)
    settings = await repo.get_settings(session, message.chat.id)
    exempt_ids: list[int] = get_config(settings)["exempt_user_ids"]

    if not parts or parts[0] not in {"add", "remove", "list"}:
        await message.reply(t("EXEMPT_USAGE"))
        return

    if parts[0] == "list":
        if not exempt_ids:
            await message.reply(t("EXEMPT_EMPTY"))
            return
        await message.reply(
            t("EXEMPT_LIST", count=len(exempt_ids), names="\n".join(f"• {i}" for i in exempt_ids))
        )
        return

    if len(parts) < 2:
        await message.reply(t("EXEMPT_USAGE"))
        return
    target = resolve_target(message, parts[1])
    if target is None:
        await message.reply(t("REPLY_OR_TARGET_REQUIRED"))
        return

    if parts[0] == "add":
        if target.user_id not in exempt_ids:
            exempt_ids.append(target.user_id)
        save_root(settings, "exempt_user_ids", exempt_ids)
        await message.reply(t("EXEMPT_ADDED", name=target.name))
    else:
        if target.user_id in exempt_ids:
            exempt_ids.remove(target.user_id)
        save_root(settings, "exempt_user_ids", exempt_ids)
        await message.reply(t("EXEMPT_REMOVED", name=target.name))
