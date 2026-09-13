"""Welcome new members and enforce Cross-Chat Blacklists."""
import asyncio
import logging
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from aiogram.dispatcher.event.bases import SkipHandler
from sqlalchemy import select, func
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
        raise SkipHandler
        
    chat = await get_or_create_chat(session, event.chat.id, title=event.chat.title)
    
    # Reload settings
    settings = await session.scalar(select(ChatSettings).where(ChatSettings.chat_telegram_id == event.chat.id))
    if not settings:
        raise SkipHandler
        
    data = settings.data or {}
    use_global_bans = data.get("modes", {}).get("use_global_bans", False)
    welcome_message = data.get("onboarding", {}).get("welcome_message", "")
    
    # 1. Global Ban Check
    if use_global_bans:
        # Get chat admins
        try:
            admins = await event.chat.get_administrators()
            admin_ids = [a.user.id for a in admins]
            
            # 1. Personal Network Ban (Current Admins)
            ban = await session.scalar(
                select(GlobalBan).where(
                    GlobalBan.user_telegram_id == user.id,
                    GlobalBan.admin_telegram_id.in_(admin_ids)
                ).limit(1)
            )
            
            # 2. Network of Trust Ban (Cross-ecosystem)
            not_bans = await session.scalar(
                select(func.count(func.distinct(GlobalBan.admin_telegram_id))).where(
                    GlobalBan.user_telegram_id == user.id,
                    GlobalBan.admin_telegram_id.notin_(admin_ids)
                )
            ) or 0
            
            if ban or not_bans >= 3:
                log.info(f"User {user.id} banned globally (Personal: {bool(ban)}, NoT: {not_bans})")
                await event.chat.ban(user.id)
                if ban and ban.reason:
                    msg = t(chat.lang, "GLOBAL_BANNED_REASON", name=user.full_name, reason=ban.reason)
                elif ban:
                    msg = t(chat.lang, "GLOBAL_BANNED", name=user.full_name)
                else:
                    msg = t(chat.lang, "NOT_BANNED", name=user.full_name, count=not_bans)
                
                try:
                    sent = await event.bot.send_message(event.chat.id, msg, parse_mode="HTML")
                    asyncio.create_task(delete_later(sent, 60))
                except Exception:
                    pass
                raise SkipHandler  # Stop processing welcome if banned
        except Exception as e:
            log.error(f"Error checking global ban: {e}")

    welcome_text = data.get("welcome_text", "")
    welcome_file_id = data.get("welcome_file_id", "")

    # 2. Welcome Message
    if welcome_text:
        # Escape user name and chat title for MarkdownV2
        import re
        def esc(text: str) -> str:
            return re.sub(r'([_*\[\]()~`>#\+\-=|{}.!])', r'\\\1', text)
            
        text = welcome_text.format(
            name=esc(user.full_name),
            chat=esc(event.chat.title)
        )
        try:
            if welcome_file_id:
                try:
                    sent = await event.bot.send_photo(event.chat.id, welcome_file_id, caption=text, parse_mode="MarkdownV2")
                except Exception:
                    try:
                        sent = await event.bot.send_video(event.chat.id, welcome_file_id, caption=text, parse_mode="MarkdownV2")
                    except Exception:
                        sent = await event.bot.send_document(event.chat.id, welcome_file_id, caption=text, parse_mode="MarkdownV2")
            else:
                sent = await event.bot.send_message(event.chat.id, text, parse_mode="MarkdownV2")
            
            # Auto delete after 5 minutes to keep chat clean
            asyncio.create_task(delete_later(sent, 300))
        except Exception as e:
            log.warning(f"Failed to send welcome message: {e}")

    raise SkipHandler


async def delete_later(message, delay: int):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass
