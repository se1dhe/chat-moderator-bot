"""HTTP smoke tests for the Mini App API (routing + auth middleware, no DB)."""
from __future__ import annotations

import pytest
from aiohttp.test_utils import TestClient, TestServer

from redqueen.api.app import create_api_app
from redqueen.config import Settings


@pytest.fixture
async def client(fake_redis):
    settings = Settings(_env_file=None)
    settings.bot_token = "123456:TEST"
    app = create_api_app(bot=None, settings=settings, sessionmaker=None, redis=fake_redis)
    async with TestClient(TestServer(app)) as c:
        yield c


@pytest.mark.asyncio
async def test_health_ok(client):
    resp = await client.get("/api/health")
    assert resp.status == 200
    assert (await resp.json())["status"] == "ok"


@pytest.mark.asyncio
async def test_me_without_initdata_is_401(client):
    resp = await client.get("/api/me")
    assert resp.status == 401


@pytest.mark.asyncio
async def test_settings_without_initdata_is_401(client):
    resp = await client.get("/api/chats/123/settings")
    assert resp.status == 401


@pytest.mark.asyncio
async def test_cors_preflight(client):
    resp = await client.options("/api/chats/123/settings")
    assert resp.status == 204
    assert resp.headers["Access-Control-Allow-Origin"] == "*"
