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


@router.message(CommandStart())
async def cmd_start(message: Message, t: Callable[..., str]) -> None:
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
    bot_username: str | None = None
) -> None:
    lang = call.data.split(":")[1]
    
    # Save user language
    user = await repo.get_user(session, call.from_user.id)
    if user:
        user.lang = lang
        await session.commit()
    
    def t(key: str, **kw: object) -> str:
        return _t(lang, key, **kw)
        
    kb = InlineKeyboardBuilder()
    if settings.webapp_url:
        kb.button(text=t("PANEL_BUTTON"), web_app=WebAppInfo(url=settings.webapp_url))
        
    logo = FSInputFile("webapp/public/logo.jpg")
    
    text = (
        f"👑 *{t('app.title', default='RedQueen Security')}*\n\n"
        f"{t('app.subtitle', default='Advanced Telegram moderation SaaS.')}\n\n"
        f"{t('ONBOARDING_WELCOME', default='Нажмите кнопку ниже, чтобы открыть панель управления.')}"
    )
    
    await call.message.delete()
    await call.message.answer_photo(
        photo=logo,
        caption=text,
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )


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
