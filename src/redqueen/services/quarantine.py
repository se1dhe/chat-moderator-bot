"""Resolve an AI quarantine verdict — shared by the bot card and the Mini App API.

Keeps the domain effects (ban / approve / promote-to-rule, message deletion, trust
adjustment) in one place so both entry points behave identically.
"""
from __future__ import annotations

import logging

import aiogram
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..db.models import AIVerdict
from . import moderation, trust
from .config import get_config, save_section

log = logging.getLogger(__name__)

VALID_ACTIONS = ("approve", "ban", "rule")


async def decide(
    bot: Bot, session: AsyncSession, verdict: AIVerdict, *, actor_id: int | None, action: str
) -> str:
    """Apply `action` to `verdict`. Returns the action performed. No-op if not pending."""
    if action not in VALID_ACTIONS:
        raise ValueError(f"unknown action: {action}")
    if verdict.status != "pending":
        return verdict.status

    if action == "approve":
        verdict.status = "approved"
        verdict.decided_by = actor_id
        await trust.adjust(session, verdict.user_telegram_id, trust.AI_FALSE_POSITIVE)
        return action

    if action == "rule" and verdict.text:
        chat_settings = await repo.get_settings(session, verdict.chat_telegram_id)
        words = get_config(chat_settings)["filters"]["banned_words"]
        snippet = verdict.text.strip().lower()[:60]
        if snippet and snippet not in words:
            words.append(snippet)
            save_section(chat_settings, "filters", {"banned_words": words})

    # ban + rule both remove the member and delete the flagged message.
    await moderation.ban(
        bot, session, chat_id=verdict.chat_telegram_id, user_id=verdict.user_telegram_id,
        actor_id=actor_id, reason=f"AI:{verdict.category}",
    )
    verdict.status = "rejected"
    verdict.decided_by = actor_id
    if verdict.message_id:
        try:
            await bot.delete_message(verdict.chat_telegram_id, verdict.message_id)
        except aiogram.exceptions.TelegramAPIError as exc:
            log.debug("could not delete flagged message: %s", exc)
    return action
