"""Bot and Dispatcher factory."""
from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis, from_url

from .config import Settings
from .db.base import get_sessionmaker
from .handlers import setup_routers
from .middlewares import DbSessionMiddleware, LangMiddleware
from .services.ai import AIProvider, build_provider
from .services.asr import Transcriber

# Update types whose handlers need a DB session / resolved chat language.
_DB_SCOPED_OBSERVERS = (
    "message", "edited_message", "callback_query",
    "chat_member", "chat_join_request", "my_chat_member",
)


def create_bot(settings: Settings, token: str | None = None) -> Bot:
    return Bot(
        token=token or settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def create_redis(settings: Settings) -> Redis:
    return from_url(settings.redis_url, decode_responses=True)


def create_dispatcher(
    settings: Settings, redis: Redis, *,
    provider: AIProvider | None = None,
    semaphore: asyncio.Semaphore | None = None,
    transcriber: Transcriber | None = None,
) -> Dispatcher:
    """Build a dispatcher. AI deps can be shared across bots (orchestrator) or built here."""
    dp = Dispatcher()

    dp["ai_provider"] = provider or build_provider(settings)
    dp["settings"] = settings
    dp["redis"] = redis
    dp["ai_semaphore"] = semaphore or asyncio.Semaphore(settings.ai_max_concurrency)
    dp["transcriber"] = transcriber or Transcriber(
        settings.whisper_model, device=settings.whisper_device, compute_type=settings.whisper_compute
    )

    session_mw = DbSessionMiddleware(get_sessionmaker(), redis)
    lang_mw = LangMiddleware(settings.default_lang)
    for name in _DB_SCOPED_OBSERVERS:
        observer = getattr(dp, name)
        observer.middleware(session_mw)
        observer.middleware(lang_mw)

    setup_routers(dp)
    return dp
