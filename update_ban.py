import sys

filename = "src/redqueen/services/moderation.py"
with open(filename, "r") as f:
    lines = f.readlines()

new_lines = []
in_ban = False
for line in lines:
    new_lines.append(line)
    if "async def ban(" in line:
        in_ban = True
    if in_ban and "await repo.set_member_state(" in line:
        # inject code before this
        new_lines.insert(-1, """
    # Check if global ban is enabled
    settings = await session.scalar(
        sa.select(repo.ChatSettings).where(repo.ChatSettings.chat_telegram_id == chat_id)
    )
    if settings and settings.data.get("modes", {}).get("use_global_bans", False):
        # Insert or update GlobalBan
        from redqueen.db.models import GlobalBan
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        
        stmt = pg_insert(GlobalBan).values(
            admin_telegram_id=actor_id,
            user_telegram_id=user_id,
            reason=reason
        ).on_conflict_do_update(
            index_elements=['admin_telegram_id', 'user_telegram_id'],
            set_={'reason': reason}
        )
        await session.execute(stmt)
""")
        in_ban = False

with open(filename, "w") as f:
    f.writelines(new_lines)
