"""Repository helpers — thin data-access functions over the async session."""
from __future__ import annotations

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import AIVerdict, Chat, ChatSettings, ModAction, User, Warn


async def get_or_create_chat(
    session: AsyncSession, telegram_id: int, *, type_: str = "group", title: str | None = None
) -> Chat:
    # Eager-load settings: async sessions cannot lazy-load a relationship on access,
    # so a pre-existing chat's `.settings` must be fetched up front.
    chat = await session.scalar(
        select(Chat).where(Chat.telegram_id == telegram_id).options(selectinload(Chat.settings))
    )
    if chat is None:
        chat = Chat(telegram_id=telegram_id, type=type_, title=title)
        chat.settings = ChatSettings()
        session.add(chat)
        await session.flush()
    elif title and chat.title != title:
        chat.title = title
    return chat


async def get_settings(session: AsyncSession, telegram_id: int) -> ChatSettings:
    chat = await get_or_create_chat(session, telegram_id)
    if chat.settings is None:  # safety for legacy rows
        chat.settings = ChatSettings(chat_id=chat.id)
        await session.flush()
    return chat.settings


async def set_warn_limit(session: AsyncSession, chat_telegram_id: int, limit: int) -> None:
    settings = await get_settings(session, chat_telegram_id)
    settings.warn_limit = limit


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    *,
    username: str | None = None,
    full_name: str | None = None,
) -> User:
    user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
    if user is None:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        session.add(user)
        await session.flush()
    else:
        user.username = username or user.username
        user.full_name = full_name or user.full_name
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

async def list_active_chats(session: AsyncSession) -> list[Chat]:
    """All connected chats (the Mini App filters these down to ones the caller admins)."""
    result = await session.scalars(select(Chat).where(Chat.is_active.is_(True)))
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
