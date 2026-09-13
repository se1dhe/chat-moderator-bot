import re

with open('src/redqueen/services/moderation.py', 'r') as f:
    text = f.read()

old_stmt = """        stmt = pg_insert(GlobalBan).values(
            admin_telegram_id=actor_id,
            user_telegram_id=user_id,
            reason=reason
        ).on_conflict_do_update(
            index_elements=['admin_telegram_id', 'user_telegram_id'],
            set_={'reason': reason}
        )"""

new_stmt = """        safe_actor = actor_id if actor_id is not None else 0
        stmt = pg_insert(GlobalBan).values(
            admin_telegram_id=safe_actor,
            user_telegram_id=user_id,
            reason=reason
        ).on_conflict_do_update(
            index_elements=['admin_telegram_id', 'user_telegram_id'],
            set_={'reason': reason}
        )"""

text = text.replace(old_stmt, new_stmt)

with open('src/redqueen/services/moderation.py', 'w') as f:
    f.write(text)

