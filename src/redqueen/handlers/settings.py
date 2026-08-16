"""Chat settings commands: /settings, /lang, /warnlimit, /warnaction, /aimode."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..i18n import SUPPORTED_LANGS
from ..services.config import get_config

router = Router(name="settings")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

_AI_MODES = {"off", "quarantine", "autoban"}


def _state(enabled: bool) -> str:
    return "on" if enabled else "off"


@router.message(Command("settings"), IsChatAdmin())
async def cmd_settings(message: Message, session: AsyncSession, t: Callable[..., str], lang: str) -> None:
    s = await repo.get_settings(session, message.chat.id)
    cfg = get_config(s)
    await message.reply(
        t(
            "SETTINGS_CARD",
            lang=lang,
            warn_limit=s.warn_limit,
            warn_action=s.warn_action,
            ai_mode=s.ai_mode,
            ai_threshold=s.ai_threshold,
            captcha=_state(cfg["captcha"]["enabled"]),
            antiflood=_state(cfg["antiflood"]["enabled"]),
            banned_words_count=len(cfg["filters"]["banned_words"]),
            block_links=_state(cfg["filters"]["block_links"]),
            block_forwards=_state(cfg["filters"]["block_forwards"]),
            block_mentions=_state(cfg["filters"]["block_mentions"]),
            night_mode=_state(cfg["modes"]["night"]["enabled"]),
            silent_mode=_state(cfg["modes"]["silent"]),
            slow_mode=_state(cfg["modes"]["slow_seconds"] > 0),
        )
    )


@router.message(Command("lang"), IsChatAdmin())
async def cmd_lang(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    choice = (command.args or "").strip().lower()
    if choice not in SUPPORTED_LANGS:
        await message.reply(t("LANG_USAGE"))
        return
    chat = await repo.get_or_create_chat(session, message.chat.id, type_=message.chat.type,
                                         title=message.chat.title)
    chat.lang = choice
    await message.reply(t("LANG_SET", lang=choice))


@router.message(Command("warnlimit"), IsChatAdmin())
async def cmd_warnlimit(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    if not command.args or not command.args.strip().isdigit():
        await message.reply(t("WARNLIMIT_USAGE"))
        return
    limit = max(1, min(20, int(command.args.strip())))
    s = await repo.get_settings(session, message.chat.id)
    s.warn_limit = limit
    await message.reply(t("WARNLIMIT_SET", limit=limit))


@router.message(Command("warnaction"), IsChatAdmin())
async def cmd_warnaction(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    action = (command.args or "").strip().lower()
    if action not in {"mute", "kick", "ban"}:
        await message.reply(t("WARNACTION_USAGE"))
        return
    s = await repo.get_settings(session, message.chat.id)
    s.warn_action = action
    await message.reply(t("WARNACTION_SET", action=action))


@router.message(Command("aimode"), IsChatAdmin())
async def cmd_aimode(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    mode = (command.args or "").strip().lower()
    if mode not in _AI_MODES:
        await message.reply(t("AIMODE_USAGE"))
        return
    s = await repo.get_settings(session, message.chat.id)
    s.ai_mode = mode
    await message.reply(t("AIMODE_SET", mode=mode))
