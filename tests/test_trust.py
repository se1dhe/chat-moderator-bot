"""services/trust: adaptive trust score accumulation (accumulation-only in M3)."""
from __future__ import annotations

import pytest

from redqueen.db.models import User
from redqueen.services import trust


class FakeSession:
    """Just enough of AsyncSession for trust.adjust: get-or-create a User row."""

    def __init__(self) -> None:
        self.users: dict[int, User] = {}

    async def scalar(self, _stmt):
        # repo.upsert_user only ever selects by telegram_id via this fake store.
        return next(iter(self.users.values()), None)

    def add(self, obj: User) -> None:
        if obj.trust_score is None:  # simulate the DB column default a real flush applies
            obj.trust_score = 50
        self.users[obj.telegram_id] = obj

    async def flush(self) -> None:
        return None


def test_should_bypass_captcha_only_for_high_trust():
    assert trust.should_bypass_captcha(trust.CAPTCHA_BYPASS_SCORE) is True
    assert trust.should_bypass_captcha(100) is True
    assert trust.should_bypass_captcha(trust.DEFAULT_SCORE) is False
    assert trust.should_bypass_captcha(trust.CAPTCHA_BYPASS_SCORE - 1) is False


@pytest.mark.asyncio
async def test_adjust_creates_user_at_default_then_applies_delta():
    session = FakeSession()
    score = await trust.adjust(session, 111, trust.WARN)
    assert score == 45  # default 50 + (-5)


@pytest.mark.asyncio
async def test_adjust_clamps_to_bounds():
    session = FakeSession()
    await trust.adjust(session, 111, -1000)
    score = await trust.adjust(session, 111, -1000)
    assert score == 0

    session2 = FakeSession()
    await trust.adjust(session2, 222, 1000)
    score2 = await trust.adjust(session2, 222, 1000)
    assert score2 == 100
