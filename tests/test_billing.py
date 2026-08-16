"""services/billing: Pro status, activation math, payment recording (no real DB)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from redqueen.db.models import Payment, Subscription
from redqueen.services import billing


class FakeSession:
    """Routes scalar() by queried entity; stores one subscription + a payment list."""

    def __init__(self) -> None:
        self.sub: Subscription | None = None
        self.payments: list[Payment] = []

    async def scalar(self, stmt):
        entity = stmt.column_descriptions[0]["entity"]
        if entity is Payment:
            return self.payments[0] if self.payments else None
        return self.sub

    def add(self, obj) -> None:
        if isinstance(obj, Payment):
            self.payments.append(obj)
        else:
            self.sub = obj


@pytest.mark.asyncio
async def test_is_pro_false_without_subscription():
    assert await billing.is_pro(FakeSession(), 1) is False


@pytest.mark.asyncio
async def test_is_pro_false_when_expired():
    s = FakeSession()
    s.sub = Subscription(chat_telegram_id=1, plan="pro",
                         active_until=datetime.now(UTC) - timedelta(days=1))
    assert await billing.is_pro(s, 1) is False


@pytest.mark.asyncio
async def test_activate_creates_and_sets_future_expiry():
    s = FakeSession()
    until = await billing.activate_pro(s, 1, days=30)
    assert s.sub.plan == "pro"
    assert until > datetime.now(UTC) + timedelta(days=29)
    assert await billing.is_pro(s, 1) is True


@pytest.mark.asyncio
async def test_activate_extends_from_current_expiry():
    s = FakeSession()
    first = await billing.activate_pro(s, 1, days=30)
    second = await billing.activate_pro(s, 1, days=30)
    # stacking a second period extends by ~30 more days, not from "now"
    assert second > first + timedelta(days=29)


@pytest.mark.asyncio
async def test_record_payment_adds_and_activates():
    s = FakeSession()
    until = await billing.record_payment(s, chat_id=1, payer_id=7, stars=150, charge_id=None, days=30)
    assert len(s.payments) == 1
    assert s.payments[0].stars == 150
    assert until > datetime.now(UTC) + timedelta(days=29)


@pytest.mark.asyncio
async def test_record_payment_idempotent_on_charge_id():
    s = FakeSession()
    await billing.record_payment(s, chat_id=1, payer_id=7, stars=150, charge_id="chg_1", days=30)
    await billing.record_payment(s, chat_id=1, payer_id=7, stars=150, charge_id="chg_1", days=30)
    assert len(s.payments) == 1  # duplicate charge ignored


def test_pro_feature_set_is_stable():
    # Guard against accidental gating changes: core moderation stays free.
    assert billing.PRO_FEATURES == frozenset({"ai_autoban", "raid_shield", "analytics"})
