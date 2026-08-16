"""Join-captcha: challenge generation, session persistence, and timeout sweeping."""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..db.models import CaptchaSession, Chat
from ..i18n import t as _t
from . import moderation

log = logging.getLogger(__name__)


@dataclass
class Challenge:
    kind: str  # button|math
    answer: int  # correct option value
    prompt_kwargs: dict = field(default_factory=dict)
    options: list[int] = field(default_factory=lambda: [1])


def build_challenge(mode: str) -> Challenge:
    if mode == "math":
        a, b = random.randint(1, 9), random.randint(1, 9)
        answer = a + b
        distractors: set[int] = set()
        while len(distractors) < 3:
            d = answer + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            if d > 0 and d != answer:
                distractors.add(d)
        options = [*distractors, answer]
        random.shuffle(options)
        return Challenge(kind="math", answer=answer, prompt_kwargs={"a": a, "b": b}, options=options)
    return Challenge(kind="button", answer=1, prompt_kwargs={}, options=[1])


async def create_session(
    session: AsyncSession,
    *,
    chat_id: int,
    user_id: int,
    challenge: Challenge,
    is_join_request: bool,
    timeout_seconds: int,
) -> CaptchaSession:
    row = CaptchaSession(
        chat_telegram_id=chat_id,
        user_telegram_id=user_id,
        kind=challenge.kind,
        answer=challenge.answer,
        is_join_request=is_join_request,
        status="pending",
        expires_at=datetime.now(UTC) + timedelta(seconds=timeout_seconds),
    )
    session.add(row)
    await session.flush()
    return row


async def sweep_expired(bot: Bot, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    """Kick/decline members whose captcha timed out.

    Driven by `expires_at` in the DB (not an in-memory timer), so a bot restart never
    loses track of a pending challenge. Call this periodically from the app lifecycle.
    """
    async with sessionmaker() as session:
        now = datetime.now(UTC)
        rows = (
            await session.scalars(
                select(CaptchaSession).where(
                    CaptchaSession.status == "pending", CaptchaSession.expires_at < now
                )
            )
        ).all()

        for row in rows:
            row.status = "expired"
            chat = await session.scalar(select(Chat).where(Chat.telegram_id == row.chat_telegram_id))
            lang = chat.lang if chat else None
            chat_name = chat.title if chat and chat.title else str(row.chat_telegram_id)
            try:
                if row.is_join_request:
                    await bot.decline_chat_join_request(row.chat_telegram_id, row.user_telegram_id)
                    await bot.send_message(
                        row.user_telegram_id,
                        _t(lang, "CAPTCHA_JOINREQUEST_DECLINED", chat=chat_name),
                    )
                else:
                    await moderation.kick(
                        bot, session, chat_id=row.chat_telegram_id, user_id=row.user_telegram_id,
                        actor_id=None, reason="captcha_timeout",
                    )
                    if row.prompt_message_id:
                        try:
                            await bot.delete_message(row.chat_telegram_id, row.prompt_message_id)
                        except Exception:  # noqa: BLE001
                            pass
                    await bot.send_message(
                        row.chat_telegram_id,
                        _t(lang, "CAPTCHA_FAILED_KICK", name=str(row.user_telegram_id)),
                    )
            except Exception as exc:  # noqa: BLE001
                log.warning("captcha sweep action failed for session %s: %s", row.id, exc)

        if rows:
            await session.commit()
