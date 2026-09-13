"""Welcome new members and enforce Cross-Chat Blacklists."""
import asyncio
import logging
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from redqueen.db.models import ChatSettings, GlobalBan
from redqueen.db.repo import get_or_create_chat
from redqueen.i18n import t

log = logging.getLogger(__name__)
router = Router(name=__name__)


@router.chat_member(F.new_chat_member.status == "member")
async def on_user_join(event: ChatMemberUpdated, session: AsyncSession) -> None:
    user = event.new_chat_member.user
    if user.is_bot:
        return
        
    chat, _ = await get_or_create_chat(session, event.chat.id, event.chat.title)
    
    # Reload settings
    settings = await session.scalar(select(ChatSettings).where(ChatSettings.chat_telegram_id == event.chat.id))
    if not settings:
        return
        
    data = settings.data or {}
    use_global_bans = data.get("use_global_bans", False)
    welcome_message = data.get("welcome_message", "")
    
    # 1. Global Ban Check
    if use_global_bans:
        # Get chat admins
        admins = await event.chat.get_administrators()
        admin_ids = [a.user.id for a in admins]
        
        # Check if user is in GlobalBans of any admin
        ban = await session.scalar(
            select(GlobalBan).where(
                GlobalBan.user_telegram_id == user.id,
                GlobalBan.admin_telegram_id.in_(admin_ids)
            ).limit(1)
        )
        if ban:
            log.info(f"User {user.id} banned globally by admin {ban.admin_telegram_id}")
            await event.chat.ban(user.id)
            if ban.reason:
                msg = t(chat.lang, "GLOBAL_BANNED_REASON", name=user.full_name, reason=ban.reason)
            else:
                msg = t(chat.lang, "GLOBAL_BANNED", name=user.full_name)
            
            try:
                sent = await event.bot.send_message(event.chat.id, msg, parse_mode="HTML")
                # Auto delete after 1 minute
                asyncio.create_task(delete_later(sent, 60))
            except Exception:
                pass
            return  # Stop processing welcome if banned

    # 2. Welcome Message
    if welcome_message:
        text = welcome_message.format(
            name=user.full_name,
            chat=event.chat.title
        )
        try:
            sent = await event.bot.send_message(event.chat.id, text, parse_mode="HTML")
            # Auto delete after 5 minutes to keep chat clean
            asyncio.create_task(delete_later(sent, 300))
        except Exception:
            pass


async def delete_later(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass
