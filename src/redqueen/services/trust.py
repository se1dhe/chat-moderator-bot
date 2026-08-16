"""Adaptive trust score scaffold (M3): accumulate simple behavioral signals.

`User.trust_score` (0..100, default 50) moves with moderation outcomes. Using the
score to relax/tighten checks is a later milestone (PROJECT_PLAN §4.2) — for now this
module only tracks it so that data exists once enforcement is built.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ..db import repo

BAN = -30
KICK = -15
MUTE = -5
WARN = -5
CAPTCHA_PASS = 2
AI_FALSE_POSITIVE = 3


async def adjust(session: AsyncSession, user_id: int, delta: int) -> int:
    user = await repo.upsert_user(session, user_id)
    user.trust_score = max(0, min(100, user.trust_score + delta))
    return user.trust_score
