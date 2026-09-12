"""Inject a per-update SQLAlchemy session into handler data."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: async_sessionmaker, redis) -> None:
        self.sessionmaker = sessionmaker
        self.redis = redis

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            session.info["redis"] = self.redis
            data["session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except SkipHandler:
                await session.commit()
                raise
            except Exception:
                await session.rollback()
                raise
