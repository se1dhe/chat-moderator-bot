import logging
from aiogram import Router, F, Bot
from aiogram.types import Message
from ..db.models import ChatSettings
from ..services.config import get_config

log = logging.getLogger(__name__)

router = Router(name="auto_comment")

@router.message(F.is_automatic_forward == True)
async def handle_automatic_forward(message: Message, settings: ChatSettings, bot: Bot):
    """Automatically posts a comment under newly forwarded posts from linked channels."""
    config = get_config(settings)
    ac = config.get("auto_comment", {})
    
    if not ac.get("enabled"):
        return
        
    text = ac.get("text")
    if not text:
        return
        
    media_url = ac.get("media_url")
    
    try:
        if media_url:
            if media_url.startswith("animation:"):
                await message.reply_animation(animation=media_url.split(":", 1)[1], caption=text, parse_mode="HTML")
            elif media_url.startswith("photo:"):
                await message.reply_photo(photo=media_url.split(":", 1)[1], caption=text, parse_mode="HTML")
            elif media_url.endswith(".mp4") or media_url.endswith(".gif"):
                await message.reply_animation(animation=media_url, caption=text, parse_mode="HTML")
            else:
                await message.reply_photo(photo=media_url, caption=text, parse_mode="HTML")
        else:
            await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)
            
        log.info(f"Auto-comment posted in chat {message.chat.id} for message {message.message_id}")
    except Exception as e:
        log.error(f"Failed to post auto-comment in {message.chat.id}: {e}")
