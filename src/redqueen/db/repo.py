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
    # Eager-load settings: async sessions cannot lazy-load a relationship on access,
    # so a pre-existing chat's `.settings` must be fetched up front.
    chat = await session.scalar(
        select(Chat).where(Chat.telegram_id == telegram_id).options(selectinload(Chat.settings))
    )
    if chat is None:
        chat = Chat(telegram_id=telegram_id, type=type_, title=title, bot_id=bot_id)
        chat.settings = ChatSettings()
        session.add(chat)
        await session.flush()
    else:
        if title and chat.title != title:
            chat.title = title
        if bot_id and chat.bot_id is None:  # tag legacy rows with their managing bot
            chat.bot_id = bot_id
    return chat


async def upsert_bot_instance(
    session: AsyncSession, *, bot_telegram_id: int, username: str | None, brand: str
) -> BotInstance:
    inst = await session.scalar(
        select(BotInstance).where(BotInstance.bot_telegram_id == bot_telegram_id)
    )
    if inst is None:
        inst = BotInstance(bot_telegram_id=bot_telegram_id, username=username, brand=brand)
        session.add(inst)
    else:
        inst.username = username
        inst.brand = brand
        inst.is_active = True
    return inst


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
    user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
    if user is None:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        if lang:
            user.lang = lang
        session.add(user)
    else:
        if username is not None:
            user.username = username
        if full_name is not None:
            user.full_name = full_name
        if lang is not None:
            user.lang = lang
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


async def search_members(
    session: AsyncSession, chat_telegram_id: int, *, query: str = "", limit: int = 30
) -> list[ChatMember]:
    stmt = select(ChatMember).where(ChatMember.chat_telegram_id == chat_telegram_id)
    q = query.strip().lstrip("@")
    if q:
        like = f"%{q}%"
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
