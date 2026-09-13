"""Custom Commands & Auto-Replies."""
import re
import logging
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from redqueen.db.models import ChatTrigger

log = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(F.text)
async def check_triggers(message: Message, session: AsyncSession) -> None:
    text = message.text
    chat_id = message.chat.id
    
    triggers = await session.scalars(
        select(ChatTrigger).where(ChatTrigger.chat_telegram_id == chat_id)
    )
    
    for trigger in triggers:
        match_found = False
        if trigger.is_regex:
            try:
                if re.search(trigger.trigger_word, text, re.IGNORECASE):
                    match_found = True
            except re.error:
                pass
        else:
            if trigger.trigger_word.lower() in text.lower():
                match_found = True
                
        if match_found:
            try:
                # Reply to the message
                await message.reply(trigger.reply_text, parse_mode="HTML")
            except Exception as e:
                log.warning(f"Failed to send trigger reply: {e}")
            break  # Stop checking other triggers to prevent spam

