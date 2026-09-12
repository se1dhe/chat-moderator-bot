"""Pro subscription state + Telegram Stars payment recording.

Core moderation is always free. Pro unlocks the higher-leverage automation; the gated
capabilities are listed in `PRO_FEATURES` and enforced at their call sites via `is_pro`.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Payment, Subscription

# Capability keys gated behind Pro (kept in one place so gating stays consistent).
PRO_FEATURES = frozenset({"ai_autoban", "raid_shield", "analytics"})

# Default plan pricing/duration (Telegram Stars). Swappable later / per-plan.
PRO_PRICE_STARS = 500
PRO_PERIOD_DAYS = 30


async def get_subscription(session: AsyncSession, chat_id: int) -> Subscription | None:
    return await session.scalar(
        select(Subscription).where(Subscription.chat_telegram_id == chat_id)
    )


def _active(sub: Subscription | None, *, now: datetime | None = None) -> bool:
    if sub is None or sub.plan != "pro" or sub.active_until is None:
        return False
    return sub.active_until > (now or datetime.now(UTC))


async def is_pro(session: AsyncSession, chat_id: int) -> bool:
    """Whether the chat currently has an active Pro subscription."""
    return _active(await get_subscription(session, chat_id))


async def activate_pro(session: AsyncSession, chat_id: int, *, days: int = PRO_PERIOD_DAYS) -> datetime:
    """Start or extend Pro for `chat_id`. Extends from the later of now / current expiry
    so stacked payments accumulate. Returns the new expiry."""
    now = datetime.now(UTC)
    sub = await get_subscription(session, chat_id)
    if sub is None:
        sub = Subscription(chat_telegram_id=chat_id)
        session.add(sub)
    base = sub.active_until if (sub.active_until and sub.active_until > now) else now
    sub.plan = "pro"
    sub.active_until = base + timedelta(days=days)
    return sub.active_until


async def record_payment(
    session: AsyncSession,
    *,
    chat_id: int,
    payer_id: int,
    stars: int,
    charge_id: str | None,
    days: int = PRO_PERIOD_DAYS,
) -> datetime:
    """Persist a Stars payment (idempotent on charge_id) and activate/extend Pro."""
    if charge_id:
        existing = await session.scalar(
            select(Payment).where(Payment.telegram_payment_charge_id == charge_id)
        )
        if existing is not None:
            sub = await get_subscription(session, chat_id)
            return sub.active_until if sub and sub.active_until else datetime.now(UTC)

    session.add(Payment(
        chat_telegram_id=chat_id, payer_id=payer_id, stars=stars, plan="pro",
        period_days=days, telegram_payment_charge_id=charge_id, status="paid",
    ))
    return await activate_pro(session, chat_id, days=days)
