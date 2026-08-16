"""AI moderation listener + explainable quarantine decision cards."""
from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..db.models import AIVerdict
from ..services import ai_budget, moderation, trust
from ..services.ai import AIProvider
from ..services.config import get_config, save_section

log = logging.getLogger(__name__)

router = Router(name="ai_review")


class ReviewCB(CallbackData, prefix="rq"):
    action: str  # ban | approve | rule
    verdict_id: int


def _decision_kb(verdict_id: int, t: Callable[..., str]) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="\U0001F534 Ban", callback_data=ReviewCB(action="ban", verdict_id=verdict_id).pack()
        ),
        InlineKeyboardButton(
            text="✅ Approve",
            callback_data=ReviewCB(action="approve", verdict_id=verdict_id).pack(),
        ),
    )
    kb.row(
        InlineKeyboardButton(
            text=t("AI_RULE_BUTTON"),
            callback_data=ReviewCB(action="rule", verdict_id=verdict_id).pack(),
        ),
    )
    return kb


@router.message(F.chat.type.in_({"group", "supergroup"}) & F.text)
async def scan_message(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, ai_provider: AIProvider,
    ai_semaphore: asyncio.Semaphore, t: Callable[..., str],
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
        raise SkipHandler

    async with ai_semaphore:
        verdict = await ai_provider.classify_text(message.text or "")
    if not verdict.is_violation or verdict.score < settings.ai_threshold:
        raise SkipHandler

    row = AIVerdict(
        chat_telegram_id=message.chat.id,
        user_telegram_id=message.from_user.id,
        message_id=message.message_id,
        category=verdict.category,
        score=verdict.score,
        explanation=verdict.explanation,
        status="pending",
    )
    session.add(row)
    await session.flush()

    await repo.log_action(
        session, chat_telegram_id=message.chat.id, user_telegram_id=message.from_user.id,
        actor_id=None, action="ai_quarantine", reason=verdict.category,
        meta={"score": verdict.score},
    )

    if settings.ai_mode == "autoban":
        try:
            await moderation.ban(bot, session, chat_id=message.chat.id,
                                 user_id=message.from_user.id, actor_id=None,
                                 reason=f"AI:{verdict.category}")
            await message.delete()
        except Exception as exc:  # noqa: BLE001
            log.warning("autoban failed: %s", exc)
        row.status = "rejected"
        return

    # quarantine: hold the message for admin decision
    card = t(
        "AI_QUARANTINE_CARD",
        name=message.from_user.full_name,
        category=verdict.category,
        score=verdict.score / 100,
        reason=verdict.explanation,
    )
    await message.reply(card, reply_markup=_decision_kb(row.id, t).as_markup())


@router.callback_query(ReviewCB.filter())
async def on_decision(
    query: CallbackQuery, callback_data: ReviewCB, bot: Bot, session: AsyncSession, t: Callable[..., str]
) -> None:
    verdict = await session.scalar(
        select(AIVerdict).where(AIVerdict.id == callback_data.verdict_id)
    )
    if verdict is None:
        await query.answer(t("AI_VERDICT_NOT_FOUND"), show_alert=True)
        return

    # Only admins may decide.
    member = await bot.get_chat_member(verdict.chat_telegram_id, query.from_user.id)
    if member.status not in {"administrator", "creator"}:
        await query.answer(t("AI_ADMIN_REQUIRED"), show_alert=True)
        return

    if callback_data.action == "ban":
        await moderation.ban(bot, session, chat_id=verdict.chat_telegram_id,
                             user_id=verdict.user_telegram_id, actor_id=query.from_user.id,
                             reason=f"AI:{verdict.category}")
        verdict.status = "rejected"
        verdict.decided_by = query.from_user.id
        if verdict.message_id:
            try:
                await bot.delete_message(verdict.chat_telegram_id, verdict.message_id)
            except Exception:  # noqa: BLE001
                pass
        text = t("AI_CONFIRMED_BAN")
    elif callback_data.action == "rule":
        flagged_text = None
        if query.message and query.message.reply_to_message:
            flagged_text = query.message.reply_to_message.text or query.message.reply_to_message.caption
        if flagged_text:
            chat_settings = await repo.get_settings(session, verdict.chat_telegram_id)
            words = get_config(chat_settings)["filters"]["banned_words"]
            snippet = flagged_text.strip().lower()[:60]
            if snippet and snippet not in words:
                words.append(snippet)
                save_section(chat_settings, "filters", {"banned_words": words})
        await moderation.ban(bot, session, chat_id=verdict.chat_telegram_id,
                             user_id=verdict.user_telegram_id, actor_id=query.from_user.id,
                             reason=f"AI:{verdict.category}")
        verdict.status = "rejected"
        verdict.decided_by = query.from_user.id
        if verdict.message_id:
            try:
                await bot.delete_message(verdict.chat_telegram_id, verdict.message_id)
            except Exception:  # noqa: BLE001
                pass
        text = t("AI_RULE_CREATED")
    else:
        verdict.status = "approved"
        verdict.decided_by = query.from_user.id
        await trust.adjust(session, verdict.user_telegram_id, trust.AI_FALSE_POSITIVE)
        text = t("AI_APPROVED")

    if query.message:
        await query.message.edit_text(text)
    await query.answer()
