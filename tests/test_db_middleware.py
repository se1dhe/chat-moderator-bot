"""DbSessionMiddleware must commit (not roll back) when a handler raises SkipHandler.

Regression: captcha writes its CaptchaSession, then raises SkipHandler so the raid
router also sees the join. If the middleware rolled that back, the captcha row vanished
and pressing the answer button did nothing.
"""
from __future__ import annotations

import pytest
from aiogram.dispatcher.event.bases import SkipHandler

from redqueen.middlewares.db import DbSessionMiddleware


class FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


def _mw_with(session):
    def maker():
        return session
    return DbSessionMiddleware(maker)


@pytest.mark.asyncio
async def test_commits_on_success():
    s = FakeSession()
    mw = _mw_with(s)
    async def handler(event, data):
        return "ok"
    assert await mw(handler, object(), {}) == "ok"
    assert s.committed and not s.rolled_back


@pytest.mark.asyncio
async def test_commits_and_reraises_on_skiphandler():
    s = FakeSession()
    mw = _mw_with(s)
    async def handler(event, data):
        raise SkipHandler
    with pytest.raises(SkipHandler):
        await mw(handler, object(), {})
    assert s.committed and not s.rolled_back


@pytest.mark.asyncio
async def test_rolls_back_on_real_error():
    s = FakeSession()
    mw = _mw_with(s)
    async def handler(event, data):
        raise ValueError("boom")
    with pytest.raises(ValueError):
        await mw(handler, object(), {})
    assert s.rolled_back and not s.committed
