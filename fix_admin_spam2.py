import re

with open('src/redqueen/handlers/ai_review.py', 'r') as f:
    text = f.read()

old_code = """    # 2. Send the quarantine card to the admins in PM instead of spamming the group
    async def _notify_admins():
        try:
            admins = await bot.get_chat_administrators(message.chat.id)
            for admin in admins:
                if admin.user.is_bot:
                    continue
                try:
                    await bot.send_message(admin.user.id, f"<b>Chat: {message.chat.title}</b>\\n\\n" + card, reply_markup=markup)
                    await asyncio.sleep(0.1)  # Prevent FloodWait
                except TelegramAPIError:
                    pass  # Admin hasn't started the bot in PM, ignore
        except Exception as exc:
            log.warning("Could not send quarantine card to admins: %s", exc)"""

new_code = """    # 2. Send the quarantine card to the registered TMA moderators in PM
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
            log.warning("Could not send quarantine card to moderators: %s", exc)"""

text = text.replace(old_code, new_code)

with open('src/redqueen/handlers/ai_review.py', 'w') as f:
    f.write(text)

