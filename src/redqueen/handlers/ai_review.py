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
from ..services import ai_budget, ai_cache, billing, quarantine, trust
from ..services.ai import AIProvider
from ..services.config import get_config

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
    ai_semaphore: asyncio.Semaphore, t: Callable[..., str], lang: str,
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    text = message.text or ""
    ai_cfg = get_config(settings)["ai"]

    # Cache first: raids repeat identical text, so classify each distinct message once
    # per window instead of paying for the model (and a queue slot) every time.
    verdict = await ai_cache.get(redis, message.chat.id, text)
    if verdict is None:
        if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
            raise SkipHandler
        context = message.reply_to_message.text if message.reply_to_message else None
        async with ai_semaphore:
            verdict = await ai_provider.classify_text(text, context=context, lang=lang)
        await ai_cache.put(redis, message.chat.id, text, verdict)

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=text)


async def _act_on_verdict(message, bot, session, settings, verdict, t, *, flagged_text) -> None:
    """Shared tail for text & image scans: threshold check → quarantine card / autoban."""
    if not verdict.is_violation:
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    # Per-category threshold (falls back to the chat default), then nudged by the
    # author's trust score: suspicious members are flagged more readily.
    base = ai_cfg["thresholds"].get(verdict.category, settings.ai_threshold)
    score_now = await trust.get_score(session, message.from_user.id)
    if verdict.score < trust.effective_threshold(base, score_now):
        raise SkipHandler

    row = AIVerdict(
        chat_telegram_id=message.chat.id,
        user_telegram_id=message.from_user.id,
        message_id=message.message_id,
        category=verdict.category,
        score=verdict.score,
        explanation=verdict.explanation,
        text=flagged_text,
        status="pending",
    )
    session.add(row)
    await session.flush()

    await repo.log_action(
        session, chat_telegram_id=message.chat.id, user_telegram_id=message.from_user.id,
        actor_id=None, action="ai_quarantine", reason=verdict.category,
        meta={"score": verdict.score},
    )

    # Auto-ban is a Pro capability; free chats fall back to the quarantine card.
    if settings.ai_mode == "autoban" and await billing.is_pro(session, message.chat.id):
        try:
            await quarantine.decide(bot, session, row, actor_id=None, action="ban")
        except Exception as exc:  # noqa: BLE001
            log.warning("autoban failed: %s", exc)
        return

    card = t(
        "AI_QUARANTINE_CARD",
        name=message.from_user.full_name,
        category=verdict.category,
        score=verdict.score / 100,
        reason=verdict.explanation,
    )
    await message.reply(card, reply_markup=_decision_kb(row.id, t).as_markup())


@router.message(F.chat.type.in_({"group", "supergroup"}) & F.photo)
async def scan_photo(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, ai_provider: AIProvider,
    ai_semaphore: asyncio.Semaphore, t: Callable[..., str], lang: str,
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler
    # Multimodal anti-scam (image analysis) is a Pro capability.
    if not await billing.is_pro(session, message.chat.id):
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
        raise SkipHandler

    try:
        buf = await bot.download(message.photo[-1])  # largest size
        image = buf.read()
    except Exception as exc:
        log.warning("photo download failed: %s", exc)
        raise SkipHandler from exc

    async with ai_semaphore:
        verdict = await ai_provider.classify_image(image, caption=message.caption, lang=lang)

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=message.caption)


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

    await quarantine.decide(
        bot, session, verdict, actor_id=query.from_user.id, action=callback_data.action
    )
    text = {
        "ban": t("AI_CONFIRMED_BAN"),
        "rule": t("AI_RULE_CREATED"),
        "approve": t("AI_APPROVED"),
    }.get(callback_data.action, t("AI_APPROVED"))

    if query.message:
        await query.message.edit_text(text)
    await query.answer()


# Re-scan edits: a common evasion is to post clean text, then edit in a scam/insult.
router.edited_message.register(scan_message, F.chat.type.in_({"group", "supergroup"}) & F.text)
