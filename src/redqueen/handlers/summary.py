"""AI Summarizer: Keeps a rolling buffer of chat history in Redis and generates summaries."""
from __future__ import annotations

import json
from collections.abc import Callable
from datetime import UTC, datetime

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command
from aiogram.types import Message
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..filters import IsChatAdmin
from ..services.ai import build_provider
from ..config import Settings

router = Router(name="summary")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


@router.message(Command("summary"), IsChatAdmin())
async def cmd_summary(
    message: Message, bot: Bot, redis: Redis, session: AsyncSession, t: Callable[..., str]
) -> None:
    key = f"rq:history:{message.chat.id}"
    raw_msgs = await redis.lrange(key, 0, -1)
    if not raw_msgs:
        await message.reply(t("SUMMARY_EMPTY") if hasattr(t, "SUMMARY_EMPTY") else "Недостаточно истории сообщений для дайджеста.")
        return

    lines = []
    for raw in reversed(raw_msgs):
        try:
            d = json.loads(raw)
            lines.append(f"{d['author']}: {d['text']}")
        except Exception:
            pass

    if len(lines) < 5:
        await message.reply(t("SUMMARY_EMPTY") if hasattr(t, "SUMMARY_EMPTY") else "Недостаточно истории сообщений для дайджеста.")
        return
        
    chat_settings = await repo.get_settings(session, message.chat.id)

    text_to_summarize = "\n".join(lines)
    prompt = "Составь краткую выжимку (дайджест) следующих сообщений из чата в 3-5 буллитах. Выдели главные темы и решения. Пиши коротко и по делу.\n\n" + text_to_summarize
    
    status = await message.reply("⏳ Генерирую дайджест...")
    
    try:
        provider = message.bot.dispatcher.get("ai_provider")
        if not provider or not hasattr(provider, "generate_text"):
            await status.edit_text("❌ AI Summarizer is not available on this provider.")
            return
            
        summary = await provider.generate_text(prompt, chat_settings=chat_settings)
        await status.edit_text(f"📊 **Дайджест чата:**\n\n{summary}", parse_mode="Markdown")
    except Exception as exc:
        await status.edit_text(f"❌ Ошибка генерации: {exc}")


@router.message()
async def store_history(
    message: Message, bot: Bot, redis: Redis
) -> None:
    # 1. Store only text messages
    if message.text and not message.from_user.is_bot:
        key = f"rq:history:{message.chat.id}"
        data = json.dumps({
            "author": message.from_user.full_name or message.from_user.first_name,
            "text": message.text[:500]
        })
        # Push to the left
        await redis.lpush(key, data)
        # Keep only the last 300 messages
        await redis.ltrim(key, 0, 299)
        # Expire the whole list in 24 hours
        await redis.expire(key, 86400)
    
    # 2. Always let the pipeline continue!
    raise SkipHandler
