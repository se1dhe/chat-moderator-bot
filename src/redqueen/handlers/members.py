"""Passive member tracking: remember who the bot has seen, to power TMA search+actions.

Runs first in the message pipeline and always defers (SkipHandler) so every other
scanner still sees the message. Telegram gives no member list, so this roster is the
only way the Mini App can search members to act on."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo

router = Router(name="members")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message()
async def record(message: Message, session: AsyncSession) -> None:
    u = message.from_user
    if u and not u.is_bot:
        await repo.record_member(
            session, chat_telegram_id=message.chat.id, user_telegram_id=u.id,
            username=u.username, full_name=u.full_name,
        )
    raise SkipHandler
