"""Bot and Dispatcher factory."""
from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import Settings
from .db.base import get_sessionmaker
from .handlers import setup_routers
from .middlewares import DbSessionMiddleware
from .services.ai import AIProvider, build_provider


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_dispatcher(settings: Settings) -> Dispatcher:
    dp = Dispatcher()

    provider: AIProvider = build_provider(settings)
    dp["ai_provider"] = provider
    dp["settings"] = settings

    session_mw = DbSessionMiddleware(get_sessionmaker())
    dp.message.middleware(session_mw)
    dp.callback_query.middleware(session_mw)

    setup_routers(dp)
    return dp
