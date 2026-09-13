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
from aiogram.exceptions import TelegramAPIError

from ..db import repo
from ..db.models import AIVerdict
from ..services import ai_budget, ai_cache, billing, quarantine, trust
from ..services.ai import AIProvider
from ..services.asr import Transcriber
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
        try:
            # wait_for wrapper protects both the semaphore acquisition queue and the AI call.
            # If the queue is stuck (e.g. Ollama hung), this times out in 5 seconds and falls back to rule mode.
            verdict = await asyncio.wait_for(
                _classify_with_semaphore(ai_semaphore, ai_provider, text, context, lang, settings),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            log.warning(f"AI timeout for chat {message.chat.id}, falling back to rules")
            # fallback to rule provider directly
            verdict = await ai_provider.fallback.classify_text(text, context=context, lang=lang) if hasattr(ai_provider, "fallback") else Verdict("ok", 50, "timeout fallback")

        await ai_cache.put(redis, message.chat.id, text, verdict)

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=text)

async def _classify_with_semaphore(sem, provider, text, context, lang, settings):
    async with sem:
        return await provider.classify_text(text, context=context, lang=lang, chat_settings=settings)

async def _classify_image_with_semaphore(sem, provider, image, caption, lang, settings):
    async with sem:
        return await provider.classify_image(image, caption=caption, lang=lang, chat_settings=settings)


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

    # 1. Hide the offending message immediately
    try:
        await message.delete()
    except (TelegramAPIError, asyncio.TimeoutError) as exc:
        log.warning("Could not delete flagged message: %s", exc)

    # Auto-ban is a Pro capability; free chats fall back to the quarantine card.
    if settings.ai_mode == "autoban" and await billing.is_pro(session, message.chat.id):
        try:
            await quarantine.decide(bot, session, row, actor_id=None, action="ban")
        except (TelegramAPIError, asyncio.TimeoutError) as exc:  # noqa: BLE001
            log.warning("autoban failed: %s", exc)
        return

    card = t(
        "AI_QUARANTINE_CARD",
        name=message.from_user.full_name,
        category=verdict.category,
        score=verdict.score / 100,
        reason=verdict.explanation,
    )
    markup = _decision_kb(row.id, t).as_markup()

    # 2. Send the quarantine card to the admins in PM instead of spamming the group
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        for admin in admins:
            if admin.user.is_bot:
                continue
            try:
                await bot.send_message(admin.user.id, f"<b>Chat: {message.chat.title}</b>\n\n" + card, reply_markup=markup)
            except TelegramAPIError:
                pass  # Admin hasn't started the bot in PM, ignore
    except (TelegramAPIError, asyncio.TimeoutError) as exc:
        log.warning("Could not fetch admins to send quarantine card: %s", exc)


def _visual_source(message: Message):
    """Return a downloadable image for photos, stickers and GIFs/animations.

    Photos use the full-res size; stickers and animations use their thumbnail (animated
    stickers/videos aren't still images, but their preview frame is enough to catch
    scam posters, QR lures and NSFW content)."""
    if message.photo:
        return message.photo[-1]
    if message.sticker:
        return message.sticker.thumbnail
    if message.animation:
        return message.animation.thumbnail
    return None


@router.message(F.chat.type.in_({"group", "supergroup"}) & (F.photo | F.sticker | F.animation))
async def scan_visual(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, ai_provider: AIProvider,
    ai_semaphore: asyncio.Semaphore, t: Callable[..., str], lang: str,
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler
    # Multimodal anti-scam (image analysis) is a Pro capability.
    if not await billing.is_pro(session, message.chat.id):
        raise SkipHandler

    source = _visual_source(message)
    if source is None:
        raise SkipHandler
        
    if source.file_size is None or source.file_size > 5_000_000:
        log.info(f"Skipping large or unknown size visual media: {source.file_size} bytes")
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
        raise SkipHandler

    try:
        buf = await asyncio.wait_for(bot.download(source), timeout=10.0)
        image = buf.read()
    except (TelegramAPIError, asyncio.TimeoutError) as exc:
        log.warning("visual download failed: %s", exc)
        raise SkipHandler from exc

    try:
        verdict = await asyncio.wait_for(
            _classify_image_with_semaphore(ai_semaphore, ai_provider, image, message.caption, lang, settings),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        verdict = await ai_provider.fallback.classify_image(image, caption=message.caption, lang=lang) if hasattr(ai_provider, "fallback") else Verdict("ok", 50, "timeout")

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=message.caption)


_TEXT_MIMES = {
    "text/plain", "text/markdown", "text/csv", "application/csv", "application/json",
}
_MAX_DOC_BYTES = 100_000


@router.message(F.chat.type.in_({"group", "supergroup"}) & F.document)
async def scan_document(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, ai_provider: AIProvider,
    ai_semaphore: asyncio.Semaphore, t: Callable[..., str], lang: str,
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler
    # Document/URL anti-scam is a Pro capability.
    if not await billing.is_pro(session, message.chat.id):
        raise SkipHandler

    doc = message.document
    parts = [message.caption or "", doc.file_name or ""]
    # Read the body of small, text-like attachments; everything else is judged by its
    # caption + filename (which is where scam links/lures usually live anyway).
    if doc.mime_type in _TEXT_MIMES and doc.file_size is not None and doc.file_size <= _MAX_DOC_BYTES:
        try:
            buf = await asyncio.wait_for(bot.download(doc), timeout=10.0)
            parts.append(buf.read().decode("utf-8", "ignore")[:4000])
        except (TelegramAPIError, asyncio.TimeoutError) as exc:  # noqa: BLE001
            log.debug("document download failed: %s", exc)

    combined = "\n".join(p for p in parts if p).strip()
    if not combined:
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
        raise SkipHandler
    try:
        verdict = await asyncio.wait_for(
            _classify_with_semaphore(ai_semaphore, ai_provider, combined, None, lang, settings),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        verdict = await ai_provider.fallback.classify_text(combined, lang=lang) if hasattr(ai_provider, "fallback") else Verdict("ok", 50, "timeout")

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=combined[:500])


@router.message(F.chat.type.in_({"group", "supergroup"}) & (F.voice | F.video_note))
async def scan_voice(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, ai_provider: AIProvider,
    ai_semaphore: asyncio.Semaphore, transcriber: Transcriber, t: Callable[..., str], lang: str,
) -> None:
    settings = await repo.get_settings(session, message.chat.id)
    if settings.ai_mode == "off" or message.from_user is None or message.from_user.is_bot:
        raise SkipHandler
    # Voice anti-scam (ASR) is a Pro capability and needs a configured Whisper model.
    if not transcriber.enabled or not await billing.is_pro(session, message.chat.id):
        raise SkipHandler

    ai_cfg = get_config(settings)["ai"]
    if not await ai_budget.allow(redis, chat_id=message.chat.id, limit=ai_cfg["max_per_minute"]):
        raise SkipHandler

    media = message.voice or message.video_note
    if media.file_size is None or media.file_size > 5_000_000:
        log.info(f"Skipping large or unknown size voice/video note: {media.file_size} bytes")
        raise SkipHandler

    try:
        buf = await asyncio.wait_for(bot.download(media), timeout=10.0)
        audio = buf.read()
    except (TelegramAPIError, asyncio.TimeoutError) as exc:
        log.warning("voice download failed: %s", exc)
        raise SkipHandler from exc

    try:
        text = await asyncio.wait_for(transcriber.transcribe(audio), timeout=15.0)
    except asyncio.TimeoutError:
        log.warning("transcription timed out")
        raise SkipHandler
    if not text:
        raise SkipHandler
    try:
        verdict = await asyncio.wait_for(
            _classify_with_semaphore(ai_semaphore, ai_provider, text, None, lang, settings),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        verdict = await ai_provider.fallback.classify_text(text, lang=lang) if hasattr(ai_provider, "fallback") else Verdict("ok", 50, "timeout")

    await _act_on_verdict(message, bot, session, settings, verdict, t, flagged_text=text)


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
