"""Adaptive trust score: accumulate behavioral signals and let them tune AI strictness.

`User.trust_score` (0..100, default 50) moves with moderation outcomes and now also
nudges the AI confidence threshold: a low-trust (repeatedly-actioned) member is flagged
more readily, a high-trust member gets more benefit of the doubt.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from ..db import repo

BAN = -30
KICK = -15
MUTE = -5
WARN = -5
CAPTCHA_PASS = 2
AI_FALSE_POSITIVE = 3

DEFAULT_SCORE = 50
# How far (percentage points) full trust swing shifts the AI threshold in each direction.
THRESHOLD_SWING = 10
# At/above this global score a member is trusted across the hive and skips join captcha.
CAPTCHA_BYPASS_SCORE = 75


def should_bypass_captcha(trust_score: int) -> bool:
    """A member the Hive already trusts (good standing across chats) skips the gate."""
    return trust_score >= CAPTCHA_BYPASS_SCORE


async def adjust(session: AsyncSession, user_id: int, delta: int, redis: Redis | None = None) -> int:
    if delta > 0 and redis is not None:
        key = f"trust_rl:{user_id}"
        current = await redis.get(key)
        current_val = int(current) if current else 0
        if current_val + delta > 10:
            delta = max(0, 10 - current_val)
        
        if delta > 0:
            await redis.incrby(key, delta)
            if not current:
                await redis.expire(key, 3600)
    
    user = await repo.upsert_user(session, user_id)
    if delta == 0:
        return user.trust_score

    user.trust_score = max(0, min(100, user.trust_score + delta))
    return user.trust_score


async def get_score(session: AsyncSession, user_id: int) -> int:
    """Current trust score (creates the row at the default if the user is new)."""
    user = await repo.upsert_user(session, user_id)
    return user.trust_score


def effective_threshold(base_threshold: int, trust_score: int) -> int:
    """Shift a base AI threshold by trust: low trust lowers it (easier to flag),
    high trust raises it (harder to flag). Clamped to 0..100."""
    shift = round((trust_score - DEFAULT_SCORE) / 50 * THRESHOLD_SWING)
    return max(0, min(100, base_threshold + shift))
