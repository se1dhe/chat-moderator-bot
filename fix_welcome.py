import re

with open('src/redqueen/handlers/welcome.py', 'r') as f:
    text = f.read()

# Make sure func is imported
text = text.replace("from sqlalchemy import select", "from sqlalchemy import select, func")

old_global = """            # Check if user is in GlobalBans of any admin
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
                    asyncio.create_task(delete_later(sent, 60))
                except Exception:
                    pass
                raise SkipHandler  # Stop processing welcome if banned"""

new_global = """            # 1. Personal Network Ban (Current Admins)
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
                raise SkipHandler  # Stop processing welcome if banned"""

text = text.replace(old_global, new_global)

with open('src/redqueen/handlers/welcome.py', 'w') as f:
    f.write(text)

