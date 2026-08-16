"""Bot and Dispatcher factory."""
from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis, from_url

from .config import Settings
from .db.base import get_sessionmaker
from .handlers import setup_routers
from .middlewares import DbSessionMiddleware, LangMiddleware
from .services.ai import AIProvider, build_provider

# Update types whose handlers need a DB session / resolved chat language.
_DB_SCOPED_OBSERVERS = ("message", "callback_query", "chat_member", "chat_join_request", "my_chat_member")


def create_bot(settings: Settings) -> Bot:
    return Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_redis(settings: Settings) -> Redis:
    return from_url(settings.redis_url, decode_responses=True)


def create_dispatcher(settings: Settings, redis: Redis) -> Dispatcher:
    dp = Dispatcher()

    provider: AIProvider = build_provider(settings)
    dp["ai_provider"] = provider
    dp["settings"] = settings
    dp["redis"] = redis

    session_mw = DbSessionMiddleware(get_sessionmaker())
    lang_mw = LangMiddleware(settings.default_lang)
    for name in _DB_SCOPED_OBSERVERS:
        observer = getattr(dp, name)
        observer.middleware(session_mw)
        observer.middleware(lang_mw)

    setup_routers(dp)
    return dp
