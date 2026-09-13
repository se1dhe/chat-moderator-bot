"""Repository helpers — thin data-access functions over the async session."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, or_, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import AIVerdict, BotInstance, Chat, ChatMember, ChatSettings, ModAction, User, Warn


async def get_or_create_chat(
    session: AsyncSession, telegram_id: int, *, type_: str = "group", title: str | None = None,
    bot_id: int | None = None,
) -> Chat:
    # Use atomic INSERT ON CONFLICT DO UPDATE
    stmt = pg_insert(Chat).values(
        telegram_id=telegram_id,
        type=type_,
        title=title,
        bot_id=bot_id,
    )
    
    update_dict = {}
    if title is not None:
        update_dict["title"] = stmt.excluded.title
    if bot_id is not None:
        # Only update bot_id if it's currently null
        update_dict["bot_id"] = func.coalesce(Chat.bot_id, stmt.excluded.bot_id)
        
    if update_dict:
        stmt = stmt.on_conflict_do_update(
            index_elements=["telegram_id"],
            set_=update_dict,
        )
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=["telegram_id"])
        
    stmt = stmt.returning(Chat.id)
    chat_pk = await session.scalar(stmt)
    
    if chat_pk is None:
        chat_pk = await session.scalar(select(Chat.id).where(Chat.telegram_id == telegram_id))
    
    # Eager-load settings: async sessions cannot lazy-load a relationship on access
    chat = await session.scalar(
        select(Chat).where(Chat.id == chat_pk).options(selectinload(Chat.settings))
    )
    
    if chat.settings is None:
        chat.settings = ChatSettings(chat_id=chat.id)
        session.add(chat.settings)
        await session.flush()
        
    return chat


async def upsert_bot_instance(
    session: AsyncSession, *, bot_telegram_id: int, username: str | None, brand: str
) -> BotInstance:
    stmt = pg_insert(BotInstance).values(
        bot_telegram_id=bot_telegram_id,
        username=username,
        brand=brand,
        is_active=True,
    ).on_conflict_do_update(
        index_elements=["bot_telegram_id"],
        set_={
            "username": username,
            "brand": brand,
            "is_active": True,
        },
    ).returning(BotInstance)
    return await session.scalar(stmt)


async def get_settings(session: AsyncSession, telegram_id: int) -> ChatSettings:
    chat = await get_or_create_chat(session, telegram_id)
    if chat.settings is None:  # safety for legacy rows
        chat.settings = ChatSettings(chat_id=chat.id)
        await session.flush()
    return chat.settings


async def set_warn_limit(session: AsyncSession, chat_telegram_id: int, limit: int) -> None:
    settings = await get_settings(session, chat_telegram_id)
    settings.warn_limit = limit


async def get_user(session: AsyncSession, telegram_id: int) -> User | None:
    return await session.scalar(select(User).where(User.telegram_id == telegram_id))


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    *,
    username: str | None = None,
    full_name: str | None = None,
    lang: str | None = None,
) -> User:
    stmt = pg_insert(User).values(
        telegram_id=telegram_id,
        username=username,
        full_name=full_name,
        lang=lang or "en",
    )
    
    update_dict = {}
    if username is not None:
        update_dict["username"] = stmt.excluded.username
    if full_name is not None:
        update_dict["full_name"] = stmt.excluded.full_name
    if lang is not None:
        update_dict["lang"] = stmt.excluded.lang
        
    if update_dict:
        stmt = stmt.on_conflict_do_update(
            index_elements=["telegram_id"],
            set_=update_dict,
        )
    else:
        stmt = stmt.on_conflict_do_nothing(index_elements=["telegram_id"])
        
    stmt = stmt.returning(User)
    user = await session.scalar(stmt)
    if user is None:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
    return user


async def add_warn(
    session: AsyncSession,
    *,
    chat_telegram_id: int,
    user_telegram_id: int,
    issued_by: int,
    reason: str | None,
) -> int:
    session.add(
        Warn(
            chat_telegram_id=chat_telegram_id,
            user_telegram_id=user_telegram_id,
            issued_by=issued_by,
            reason=reason,
        )
    )
    await session.flush()
    return await count_active_warns(session, chat_telegram_id, user_telegram_id)


async def count_active_warns(
    session: AsyncSession, chat_telegram_id: int, user_telegram_id: int
) -> int:
    from sqlalchemy import func

    result = await session.scalar(
        select(func.count())
        .select_from(Warn)
        .where(
            Warn.chat_telegram_id == chat_telegram_id,
            Warn.user_telegram_id == user_telegram_id,
            Warn.active.is_(True),
        )
    )
    return int(result or 0)


async def clear_last_warn(
    session: AsyncSession, chat_telegram_id: int, user_telegram_id: int
) -> int:
    """Deactivate the most recent active warn. Returns remaining count."""
    warn = await session.scalar(
        select(Warn)
        .where(
            Warn.chat_telegram_id == chat_telegram_id,
            Warn.user_telegram_id == user_telegram_id,
            Warn.active.is_(True),
        )
        .order_by(Warn.id.desc())
        .limit(1)
    )
    if warn is not None:
        warn.active = False
        await session.flush()
    return await count_active_warns(session, chat_telegram_id, user_telegram_id)


async def reset_warns(
    session: AsyncSession, chat_telegram_id: int, user_telegram_id: int
) -> None:
    await session.execute(
        update(Warn)
        .where(
            Warn.chat_telegram_id == chat_telegram_id,
            Warn.user_telegram_id == user_telegram_id,
            Warn.active.is_(True),
        )
        .values(active=False)
    )


async def log_action(
    session: AsyncSession,
    *,
    chat_telegram_id: int,
    action: str,
    user_telegram_id: int | None = None,
    actor_id: int | None = None,
    reason: str | None = None,
    meta: dict | None = None,
) -> None:
    session.add(
        ModAction(
            chat_telegram_id=chat_telegram_id,
            user_telegram_id=user_telegram_id,
            actor_id=actor_id,
            action=action,
            reason=reason,
            meta=meta or {},
        )
    )
    
    redis = session.info.get("redis")
    if redis:
        try:
            import json
            chat = await get_or_create_chat(session, chat_telegram_id)
            anonymize = chat.settings.anonymize_events
            
            chat_title = chat.title or "Group"
            user_name = "Unknown"
            
            if user_telegram_id:
                user = await session.scalar(select(User).where(User.telegram_id == user_telegram_id))
                if user:
                    user_name = user.username or user.full_name or "Unknown"
                    
            if anonymize:
                if len(chat_title) > 4:
                    chat_title = chat_title[:2] + "***" + chat_title[-2:]
                else:
                    chat_title = "***"
                    
                if len(user_name) > 3:
                    user_name = user_name[:2] + "***" + user_name[-1:]
                else:
                    user_name = "***"
                    
            await redis.publish("live_events", json.dumps({
                "action": action,
                "reason": reason,
                "chat_title": chat_title,
                "user_name": user_name
            }))
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Failed to publish live event: {e}")


# --- Mini App API reads ---------------------------------------------------------

async def list_active_chats(session: AsyncSession, *, bot_id: int | None = None) -> list[Chat]:
    """Connected chats. When `bot_id` is given, only this brand bot's chats (plus legacy
    rows with no bot_id yet) — white-label isolation for the Mini App listing."""
    stmt = select(Chat).where(Chat.is_active.is_(True))
    if bot_id is not None:
        stmt = stmt.where(or_(Chat.bot_id == bot_id, Chat.bot_id.is_(None)))
    result = await session.scalars(stmt)
    return list(result.all())


async def recent_mod_actions(
    session: AsyncSession, chat_telegram_id: int, *, limit: int = 50
) -> list[ModAction]:
    result = await session.scalars(
        select(ModAction)
        .where(ModAction.chat_telegram_id == chat_telegram_id)
        .order_by(ModAction.id.desc())
        .limit(limit)
    )
    return list(result.all())


async def pending_ai_verdicts(
    session: AsyncSession, chat_telegram_id: int, *, limit: int = 50
) -> list[AIVerdict]:
    result = await session.scalars(
        select(AIVerdict)
        .where(
            AIVerdict.chat_telegram_id == chat_telegram_id,
            AIVerdict.status == "pending",
        )
        .order_by(AIVerdict.id.desc())
        .limit(limit)
    )
    return list(result.all())


async def get_ai_verdict(session: AsyncSession, verdict_id: int) -> AIVerdict | None:
    return await session.scalar(select(AIVerdict).where(AIVerdict.id == verdict_id))


async def record_member(
    session: AsyncSession, *, chat_telegram_id: int, user_telegram_id: int,
    username: str | None, full_name: str | None,
) -> None:
    """Upsert a seen member (bump message_count + last_seen). One statement, no read."""
    stmt = pg_insert(ChatMember).values(
        chat_telegram_id=chat_telegram_id, user_telegram_id=user_telegram_id,
        username=username, full_name=full_name, message_count=1,
    ).on_conflict_do_update(
        constraint="uq_chat_member",
        set_={
            "username": username,
            "full_name": full_name,
            "message_count": ChatMember.message_count + 1,
            "last_seen": func.now(),
        },
    )
    await session.execute(stmt)


async def set_member_state(
    session: AsyncSession, chat_telegram_id: int, user_telegram_id: int,
    *, state: str, muted_until: datetime | None = None,
) -> None:
    """Record a member's last moderation state so the Mini App can offer contextual
    actions. No-op when the user isn't in the roster yet (never wrote a message)."""
    await session.execute(
        update(ChatMember)
        .where(
            ChatMember.chat_telegram_id == chat_telegram_id,
            ChatMember.user_telegram_id == user_telegram_id,
        )
        .values(state=state, muted_until=muted_until)
    )


async def get_member(
    session: AsyncSession, chat_telegram_id: int, user_telegram_id: int
) -> ChatMember | None:
    return await session.scalar(
        select(ChatMember).where(
            ChatMember.chat_telegram_id == chat_telegram_id,
            ChatMember.user_telegram_id == user_telegram_id,
        )
    )

async def count_members(session: AsyncSession, chat_telegram_id: int) -> int:
    result = await session.scalar(
        select(func.count()).select_from(ChatMember).where(ChatMember.chat_telegram_id == chat_telegram_id)
    )
    return int(result or 0)


def _escape_like(q: str) -> str:
    return q.replace("%", "\\%").replace("_", "\\_")

async def search_members(
    session: AsyncSession, chat_telegram_id: int, *, query: str = "", limit: int = 30
) -> list[ChatMember]:
    stmt = select(ChatMember).where(ChatMember.chat_telegram_id == chat_telegram_id)
    q = query.strip().lstrip("@")
    if q:
        escaped_q = _escape_like(q)
        like = f"%{escaped_q}%"
        conds = [ChatMember.username.ilike(like), ChatMember.full_name.ilike(like)]
        if q.isdigit():
            conds.append(ChatMember.user_telegram_id == int(q))
        stmt = stmt.where(or_(*conds))
    stmt = stmt.order_by(ChatMember.last_seen.desc()).limit(limit)
    return list((await session.scalars(stmt)).all())


async def action_counts(
    session: AsyncSession, chat_telegram_id: int
) -> dict[str, int]:
    """Total ModAction rows per action type for a chat (for the stats dashboard)."""
    result = await session.execute(
        select(ModAction.action, func.count())
        .where(ModAction.chat_telegram_id == chat_telegram_id)
        .group_by(ModAction.action)
    )
    return {action: int(n) for action, n in result.all()}


async def actions_timeline(
    session: AsyncSession, chat_telegram_id: int, *, days: int = 14
) -> dict[str, int]:
    """ModAction counts per day (UTC) over the last `days`. Sparse — client fills gaps."""
    since = datetime.now(UTC) - timedelta(days=days)
    day = func.date_trunc("day", ModAction.created_at)
    result = await session.execute(
        select(day.label("d"), func.count())
        .where(ModAction.chat_telegram_id == chat_telegram_id, ModAction.created_at >= since)
        .group_by(day)
        .order_by(day)
    )
    return {d.date().isoformat(): int(n) for d, n in result.all()}


async def verdict_category_counts(
    session: AsyncSession, chat_telegram_id: int
) -> dict[str, int]:
    """AIVerdict counts per category — the AI 'what did we catch' breakdown."""
    result = await session.execute(
        select(AIVerdict.category, func.count())
        .where(AIVerdict.chat_telegram_id == chat_telegram_id)
        .group_by(AIVerdict.category)
    )
    return {cat: int(n) for cat, n in result.all()}
