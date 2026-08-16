"""Warn service: issue warnings and apply the configured action at the limit."""
from __future__ import annotations

from dataclasses import dataclass

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from . import moderation


@dataclass
class WarnResult:
    count: int
    limit: int
    triggered: bool
    action: str | None = None  # action applied when limit hit


async def issue_warn(
    bot: Bot,
    session: AsyncSession,
    *,
    chat_id: int,
    user_id: int,
    actor_id: int,
    reason: str | None,
) -> WarnResult:
    settings = await repo.get_settings(session, chat_id)
    count = await repo.add_warn(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id,
        issued_by=actor_id, reason=reason,
    )
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="warn", reason=reason,
    )
    if count < settings.warn_limit:
        return WarnResult(count=count, limit=settings.warn_limit, triggered=False)

    action = settings.warn_action
    if action == "ban":
        await moderation.ban(bot, session, chat_id=chat_id, user_id=user_id, actor_id=None,
                             reason="warn limit reached")
    elif action == "kick":
        await moderation.kick(bot, session, chat_id=chat_id, user_id=user_id, actor_id=None,
                              reason="warn limit reached")
    else:
        await moderation.mute(bot, session, chat_id=chat_id, user_id=user_id, actor_id=None,
                              reason="warn limit reached")
    await repo.reset_warns(session, chat_id, user_id)
    return WarnResult(count=count, limit=settings.warn_limit, triggered=True, action=action)
