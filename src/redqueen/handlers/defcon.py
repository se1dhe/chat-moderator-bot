"""Auto-DEFCON: Dynamic Raid Shield & Spam Velocity Tracker."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import UTC, datetime

from aiogram import Bot, F, Router
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, CommandObject
from aiogram.filters.chat_member_updated import JOIN_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message, ChatPermissions
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo
from ..db.models import RaidEvent
from ..filters import IsChatAdmin
from ..services import billing, roles, moderation
from ..services.config import get_config, save_section

router = Router(name="defcon")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


def is_active(cfg: dict) -> bool:
    active_until = cfg["defcon"]["active_until"]
    return bool(active_until) and datetime.now(UTC).timestamp() < active_until

async def _notify_mods(bot: Bot, session: AsyncSession, chat_id: int, chat_title: str, text: str):
    try:
        from redqueen.db.repo import get_chat_moderators
        mods = await get_chat_moderators(session, chat_id)
        for mod, _ in mods:
            try:
                await bot.send_message(mod.user_telegram_id, f"<b>Chat: {chat_title}</b>\n\n" + text)
                await asyncio.sleep(0.1)
            except Exception:
                pass
    except Exception:
        pass


async def _record_velocity(
    bot: Bot, session: AsyncSession, redis: Redis, chat_id: int, chat_title: str, user_id: int, weight: int
) -> None:
    settings = await repo.get_settings(session, chat_id)
    cfg = get_config(settings)
    if not cfg["defcon"]["enabled"] or is_active(cfg):
        return
    
    if not await billing.is_pro(session, chat_id):
        return

    key = f"rq:defcon:vel:{chat_id}"
    count = await redis.incrby(key, weight)
    if count == weight:
        await redis.expire(key, 60) # 1 minute rolling window

    if count >= cfg["defcon"]["threshold"]:
        # TRIGGER DEFCON
        until = datetime.now(UTC).timestamp() + cfg["defcon"]["lock_seconds"]
        save_section(settings, "defcon", {"active_until": until})
        
        # Log event
        session.add(RaidEvent(
            chat_telegram_id=chat_id, join_count=count,
            window_seconds=60,
            locked_until=datetime.fromtimestamp(until, UTC),
        ))
        await repo.log_action(
            session, chat_telegram_id=chat_id, action="defcon_on",
            reason=f"Velocity {count} exceeded threshold {cfg['defcon']['threshold']}",
        )
        
        minutes = max(1, cfg["defcon"]["lock_seconds"] // 60)
        action_name = cfg["defcon"]["action"]
        text = f"🚨 <b>DEFCON ACTIVATED</b>\n\nHigh spam/join velocity detected. Action: <b>{action_name}</b> for {minutes} minutes."
        await _notify_mods(bot, session, chat_id, chat_title, text)
        try:
            await bot.send_message(chat_id, text)
        except Exception:
            pass


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_join_defcon(
    event: ChatMemberUpdated, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    # 1. Track velocity (weight 2 for joins)
    await _record_velocity(bot, session, redis, event.chat.id, event.chat.title, event.new_chat_member.user.id, 2)
    
    # 2. Enforce active DEFCON
    settings = await repo.get_settings(session, event.chat.id)
    cfg = get_config(settings)
    if is_active(cfg):
        if await roles.is_exempt(bot, redis, chat_id=event.chat.id, user_id=event.new_chat_member.user.id, settings=settings):
            return
            
        action = cfg["defcon"]["action"]
        if action == "read_only":
            until = datetime.now(UTC) + __import__("datetime").timedelta(seconds=cfg["defcon"]["lock_seconds"])
            await moderation.mute(bot, session, chat_id=event.chat.id, user_id=event.new_chat_member.user.id, actor_id=0, until=until, reason="Auto-DEFCON Read-Only")
        elif action == "captcha":
            # Handled by captcha.py integration if needed, or we can just restrict them here
            # For simplicity, if captcha is enabled, captcha.py will see them anyway. 
            # If not, we just mute them.
            pass


@router.message()
async def on_message_defcon(
    message: Message, bot: Bot, session: AsyncSession, redis: Redis, t: Callable[..., str]
) -> None:
    if message.from_user is None or message.from_user.is_bot:
        raise SkipHandler

    # 1. Track velocity (weight 1 for messages)
    if not await roles.is_admin(bot, redis, chat_id=message.chat.id, user_id=message.from_user.id):
        await _record_velocity(bot, session, redis, message.chat.id, message.chat.title, message.from_user.id, 1)

    # 2. Enforce active DEFCON strict mode
    settings = await repo.get_settings(session, message.chat.id)
    cfg = get_config(settings)
    if is_active(cfg) and cfg["defcon"]["action"] == "strict":
        if await roles.is_exempt(bot, redis, chat_id=message.chat.id, user_id=message.from_user.id, settings=settings):
            raise SkipHandler
            
        # Strict mode: If it has media, links, or forwards, quarantine immediately
        has_media = bool(message.photo or message.video or message.document or message.audio or message.animation or message.sticker)
        has_links = False
        if message.entities:
            has_links = any(e.type in ("url", "text_link", "mention") for e in message.entities)
        if message.caption_entities:
            has_links = has_links or any(e.type in ("url", "text_link", "mention") for e in message.caption_entities)
            
        is_forward = bool(message.forward_origin)
        
        if has_media or has_links or is_forward:
            try:
                await message.delete()
                # We could send to quarantine here, but just deleting it is safer during a massive raid to save DB load
            except Exception:
                pass
            return # Block it

    raise SkipHandler

@router.message(Command("defcon"), IsChatAdmin())
async def cmd_defcon(
    message: Message, command: CommandObject, session: AsyncSession, t: Callable[..., str]
) -> None:
    choice = (command.args or "").strip().lower()
    settings = await repo.get_settings(session, message.chat.id)
    if choice == "off":
        save_section(settings, "defcon", {"active_until": None, "enabled": False})
        await message.reply("DEFCON deactivated and disabled.")
    elif choice == "on":
        save_section(settings, "defcon", {"enabled": True})
        await message.reply("DEFCON armed.")
    else:
        await message.reply("Usage: /defcon on | off")
