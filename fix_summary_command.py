with open('src/redqueen/handlers/summary.py', 'r') as f:
    text = f.read()

# I will just remove the cmd_summary function entirely.
# The store_history function will remain.
new_text = """\"\"\"AI Summarizer: Keeps a rolling buffer of chat history in Redis and generates summaries.\"\"\"
from __future__ import annotations

import json
from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import Message
from redis.asyncio import Redis

router = Router(name="summary")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

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
"""
with open('src/redqueen/handlers/summary.py', 'w') as f:
    f.write(new_text)

