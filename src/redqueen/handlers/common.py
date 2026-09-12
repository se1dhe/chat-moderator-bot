"""Common commands: /start, /help, /panel (open the Mini App)."""
from __future__ import annotations

from collections.abc import Callable

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

from ..config import Settings
from ..db import repo
from ..i18n import t as _t
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="common")


async def _send_welcome(
    message: Message | CallbackQuery,
    lang: str,
    settings: Settings,
    bot_username: str | None = None,
) -> None:
    def t(key: str, **kw: object) -> str:
        return _t(lang, key, **kw)
        
    kb = InlineKeyboardBuilder()
    if settings.webapp_url:
        kb.button(text=t("PANEL_BUTTON"), web_app=WebAppInfo(url=settings.webapp_url))
        
    logo = FSInputFile("webapp/dist/logo.jpg")
    
    if lang == "ru":
        desc = "Продвинутая система модерации и аналитики Telegram-сообществ."
        prompt = "Нажмите на кнопку ниже, чтобы открыть панель управления и добавить бота в свои чаты."
    elif lang == "uk":
        desc = "Просунута система модерації та аналітики Telegram-спільнот."
        prompt = "Натисніть на кнопку нижче, щоб відкрити панель керування та додати бота у свої чати."
    else:
        desc = "Advanced Telegram moderation SaaS and analytics."
        prompt = "Click the button below to open the dashboard and add the bot to your chats."

    text = (
        f"👑 *RedQueen Security*\n\n"
        f"_{desc}_\n\n"
        f"{prompt}"
    )
    
    msg = message if isinstance(message, Message) else message.message
    await msg.answer_photo(
        photo=logo,
        caption=text,
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    session: AsyncSession,
    settings: Settings,
    bot_username: str | None = None,
) -> None:
    # Check if user already exists in DB
    user = await repo.get_user(session, message.from_user.id)
    if user and user.lang:
        await _send_welcome(message, user.lang, settings, bot_username)
        return

    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇸 English", callback_data="lang:en")
    kb.button(text="🇷🇺 Русский", callback_data="lang:ru")
    kb.button(text="🇺🇦 Українська", callback_data="lang:uk")
    kb.adjust(1)
    
    await message.answer(
        "👋 Welcome to RedQueen Security!\nПожалуйста, выберите ваш язык / Please choose your language:",
        reply_markup=kb.as_markup()
    )


@router.callback_query(F.data.startswith("lang:"))
async def on_lang_selected(
    call: CallbackQuery,
    session: AsyncSession,
    settings: Settings,
    bot_username: str | None = None,
) -> None:
    lang = call.data.split(":")[1]
    
    # Save user language, creating user if it doesn't exist
    await repo.upsert_user(
        session,
        call.from_user.id,
        username=call.from_user.username,
        full_name=call.from_user.full_name,
        lang=lang
    )
    await session.commit()
    
    await call.message.delete()
    await _send_welcome(call, lang, settings, bot_username)


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
