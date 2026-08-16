"""Common commands: /start, /help, /panel (open the Mini App)."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import Settings

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message, t: Callable[..., str]) -> None:
    await message.answer(t("START"))


@router.message(Command("help"))
async def cmd_help(message: Message, t: Callable[..., str]) -> None:
    await message.answer(t("HELP"))


@router.message(Command("panel"))
async def cmd_panel(
    message: Message, settings: Settings, t: Callable[..., str], bot_username: str | None = None
) -> None:
    if not settings.webapp_url:
        await message.reply(t("PANEL_UNCONFIGURED"))
        return
    kb = InlineKeyboardBuilder()
    if message.chat.type == "private":
        # WebApp buttons open the Mini App inline; allowed in private chats.
        kb.button(text=t("PANEL_BUTTON"), web_app=WebAppInfo(url=settings.webapp_url))
    else:
        # In groups, deep-link to the bot's Mini App carrying this chat id as start_param.
        url = (
            f"https://t.me/{bot_username}?startapp={message.chat.id}"
            if bot_username else settings.webapp_url
        )
        kb.button(text=t("PANEL_BUTTON"), url=url)
    await message.reply(t("PANEL_PROMPT"), reply_markup=kb.as_markup())
