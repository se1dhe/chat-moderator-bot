"""Chat settings commands: /settings, /warnlimit, /aimode."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin

router = Router(name="settings")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

_AI_MODES = {"off", "quarantine", "autoban"}


@router.message(Command("settings"), IsChatAdmin())
async def cmd_settings(message: Message, session: AsyncSession) -> None:
    s = await repo.get_settings(session, message.chat.id)
    await message.reply(
        "<b>RedQueen protocols for this chat</b>\n"
        f"• Warn limit: <b>{s.warn_limit}</b>\n"
        f"• Warn action: <b>{s.warn_action}</b>\n"
        f"• AI mode: <b>{s.ai_mode}</b>\n"
        f"• AI threshold: <b>{s.ai_threshold}%</b>\n\n"
        "Change with /warnlimit N, /warnaction mute|kick|ban, /aimode off|quarantine|autoban"
    )


@router.message(Command("warnlimit"), IsChatAdmin())
async def cmd_warnlimit(message: Message, command: CommandObject, session: AsyncSession) -> None:
    if not command.args or not command.args.strip().isdigit():
        await message.reply("Usage: /warnlimit N (e.g. /warnlimit 3)")
        return
    limit = max(1, min(20, int(command.args.strip())))
    s = await repo.get_settings(session, message.chat.id)
    s.warn_limit = limit
    await message.reply(f"Warn limit set to <b>{limit}</b>.")


@router.message(Command("warnaction"), IsChatAdmin())
async def cmd_warnaction(message: Message, command: CommandObject, session: AsyncSession) -> None:
    action = (command.args or "").strip().lower()
    if action not in {"mute", "kick", "ban"}:
        await message.reply("Usage: /warnaction mute|kick|ban")
        return
    s = await repo.get_settings(session, message.chat.id)
    s.warn_action = action
    await message.reply(f"Warn action set to <b>{action}</b>.")


@router.message(Command("aimode"), IsChatAdmin())
async def cmd_aimode(message: Message, command: CommandObject, session: AsyncSession) -> None:
    mode = (command.args or "").strip().lower()
    if mode not in _AI_MODES:
        await message.reply("Usage: /aimode off|quarantine|autoban")
        return
    s = await repo.get_settings(session, message.chat.id)
    s.ai_mode = mode
    await message.reply(f"AI moderation mode set to <b>{mode}</b>.")
