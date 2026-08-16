"""Resolve the chat/user language and inject `lang` + `t` into handler data."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..i18n import resolve_lang
from ..i18n import t as _t

_CHAT_SCOPED_TYPES = {"group", "supergroup", "channel"}


class LangMiddleware(BaseMiddleware):
    """Groups/channels use `Chat.lang`; private chats fall back to the user's
    Telegram `language_code`. Must run after `DbSessionMiddleware`."""

    def __init__(self, default_lang: str) -> None:
        self.default_lang = default_lang

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        lang = self.default_lang
        tg_chat = getattr(event, "chat", None)
        if tg_chat is None:
            inner = getattr(event, "message", None)
            tg_chat = getattr(inner, "chat", None) if inner else None

        session: AsyncSession | None = data.get("session")

        if tg_chat is not None and tg_chat.type in _CHAT_SCOPED_TYPES and session is not None:
            chat_row = await repo.get_or_create_chat(
                session, tg_chat.id, type_=tg_chat.type, title=tg_chat.title
            )
            lang = chat_row.lang or self.default_lang
        else:
            user = getattr(event, "from_user", None)
            if user is not None and user.language_code:
                lang = user.language_code

        lang = resolve_lang(lang)
        data["lang"] = lang
        data["t"] = lambda key, **kw: _t(lang, key, **kw)
        return await handler(event, data)
