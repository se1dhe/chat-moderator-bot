"""Moderation service: performs Telegram restrictions and writes the audit log."""
from __future__ import annotations

from datetime import datetime

from aiogram import Bot
from aiogram.types import ChatPermissions
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from . import trust

_MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
)
_UNMUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)


async def ban(
    bot: Bot, session: AsyncSession, *, chat_id: int, user_id: int, actor_id: int,
    until: datetime | None = None, reason: str | None = None,
) -> None:
    # A `until_date` in the past/near future or none == permanent ban (Telegram rule).
    await bot.ban_chat_member(chat_id, user_id, until_date=until)
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="ban", reason=reason,
        meta={"until": until.isoformat()} if until else {},
    )

    # Check if global ban is enabled
    settings = await session.scalar(
        sa.select(repo.ChatSettings).where(repo.ChatSettings.chat_telegram_id == chat_id)
    )
    if settings and (settings.data or {}).get("modes", {}).get("use_global_bans", False):
        # Insert or update GlobalBan
        from redqueen.db.models import GlobalBan
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        
        stmt = pg_insert(GlobalBan).values(
            admin_telegram_id=actor_id,
            user_telegram_id=user_id,
            reason=reason
        ).on_conflict_do_update(
            index_elements=['admin_telegram_id', 'user_telegram_id'],
            set_={'reason': reason}
        )
        await session.execute(stmt)
    await repo.set_member_state(session, chat_id, user_id, state="banned")
    await trust.adjust(session, user_id, trust.BAN)


async def unban(
    bot: Bot, session: AsyncSession, *, chat_id: int, user_id: int, actor_id: int
) -> None:
    await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="unban",
    )
    await repo.set_member_state(session, chat_id, user_id, state="active")


async def kick(
    bot: Bot, session: AsyncSession, *, chat_id: int, user_id: int, actor_id: int, reason: str | None = None
) -> None:
    # ban + immediate unban == kick (user may rejoin)
    await bot.ban_chat_member(chat_id, user_id)
    await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="kick", reason=reason,
    )
    await repo.set_member_state(session, chat_id, user_id, state="active")
    await trust.adjust(session, user_id, trust.KICK)


async def mute(
    bot: Bot, session: AsyncSession, *, chat_id: int, user_id: int, actor_id: int,
    until: datetime | None = None, reason: str | None = None,
) -> None:
    await bot.restrict_chat_member(
        chat_id, user_id, permissions=_MUTED_PERMISSIONS, until_date=until
    )
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="mute", reason=reason,
        meta={"until": until.isoformat()} if until else {},
    )
    if reason != "captcha_pending":  # procedural quarantine, not a behavioral penalty
        await repo.set_member_state(session, chat_id, user_id, state="muted", muted_until=until)
        await trust.adjust(session, user_id, trust.MUTE)


async def unmute(
    bot: Bot, session: AsyncSession, *, chat_id: int, user_id: int, actor_id: int
) -> None:
    await bot.restrict_chat_member(chat_id, user_id, permissions=_UNMUTED_PERMISSIONS)
    await repo.log_action(
        session, chat_telegram_id=chat_id, user_telegram_id=user_id, actor_id=actor_id,
        action="unmute",
    )
    await repo.set_member_state(session, chat_id, user_id, state="active", muted_until=None)
