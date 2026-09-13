import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

# Send to log channel if configured
old_notify = """    # 2. Send the quarantine card to the registered TMA moderators in PM
    async def _notify_admins():
        try:
            from redqueen.db.repo import get_chat_moderators
            mods = await get_chat_moderators(session, message.chat.id)
            for mod, _ in mods:
                try:
                    await bot.send_message(mod.user_telegram_id, f"<b>Chat: {message.chat.title}</b>\\n\\n" + card, reply_markup=markup)
                    await asyncio.sleep(0.1)  # Prevent FloodWait
                except TelegramAPIError:
                    pass  # Moderator hasn't started the bot in PM, ignore
        except Exception as exc:
            log.warning("Could not send quarantine card to moderators: %s", exc)

    asyncio.create_task(_notify_admins())"""

new_notify = """    # 2. Send to Log Channel (AI Tribunal) or TMA moderators in PM
    async def _notify_admins():
        log_channel_id = get_config(settings).get("log_channel_id")
        if log_channel_id:
            try:
                await bot.send_message(log_channel_id, f"<b>Chat: {message.chat.title}</b>\\n\\n" + card, reply_markup=markup)
                return
            except Exception as exc:
                log.warning("Could not send to log channel %s: %s", log_channel_id, exc)
                # Fallback to PMs if log channel fails
        
        try:
            from redqueen.db.repo import get_chat_moderators
            mods = await get_chat_moderators(session, message.chat.id)
            for mod, _ in mods:
                try:
                    await bot.send_message(mod.user_telegram_id, f"<b>Chat: {message.chat.title}</b>\\n\\n" + card, reply_markup=markup)
                    await asyncio.sleep(0.1)  # Prevent FloodWait
                except TelegramAPIError:
                    pass
        except Exception as exc:
            log.warning("Could not send quarantine card to moderators: %s", exc)

    asyncio.create_task(_notify_admins())"""
text = text.replace(old_notify, new_notify)

# Allow TMA mods to click button
old_click = """    # Only admins may decide.
    member = await bot.get_chat_member(verdict.chat_telegram_id, query.from_user.id)
    if member.status not in {"administrator", "creator"}:
        await query.answer(t("AI_ADMIN_REQUIRED"), show_alert=True)
        return"""

new_click = """    # Only admins or TMA moderators may decide.
    member = await bot.get_chat_member(verdict.chat_telegram_id, query.from_user.id)
    is_admin = member.status in {"administrator", "creator"}
    if not is_admin:
        from redqueen.db.repo import is_chat_moderator
        is_mod = await is_chat_moderator(session, verdict.chat_telegram_id, query.from_user.id)
        if not is_mod:
            await query.answer(t("AI_ADMIN_REQUIRED"), show_alert=True)
            return"""
text = text.replace(old_click, new_click)

with open('src/redqueen/handlers/ai_review.py', 'w') as f:
    f.write(text)

