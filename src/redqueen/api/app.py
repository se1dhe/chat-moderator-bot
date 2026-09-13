"""aiohttp application factory for the Mini App API (+ optional static TMA serving)."""
from __future__ import annotations

import logging
import os
from collections.abc import Awaitable, Callable
from pathlib import Path

from aiogram import Bot
from aiohttp import web
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..config import Settings
from .routes import setup_routes

log = logging.getLogger(__name__)

_CORS_HEADERS_BASE = {
    "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Init-Data",
    "Access-Control-Max-Age": "600",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://telegram.org; style-src 'self' 'unsafe-inline'; connect-src 'self' wss: https:; img-src 'self' data: blob: https:;",
}


@web.middleware
async def cors_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
    ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
    origin = request.headers.get("Origin", "")
    cors_headers = {**_CORS_HEADERS_BASE}
    if origin and (origin in ALLOWED_ORIGINS or "*" in ALLOWED_ORIGINS):
        cors_headers["Access-Control-Allow-Origin"] = origin
    else:
        cors_headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS[0] if ALLOWED_ORIGINS else origin
    if request.method == "OPTIONS":
        return web.Response(status=204, headers=cors_headers)
    response = await handler(request)
    response.headers.update(cors_headers)
    return response


def _mount_static(app: web.Application, dist: Path) -> None:
    """Serve the built Mini App under /app with SPA fallback to index.html."""
    index = dist / "index.html"

    async def spa(request: web.Request) -> web.StreamResponse:
        rel = request.match_info.get("tail", "").lstrip("/")
        if rel.startswith("app/"):
            rel = rel[4:]
        
        candidate = (dist / rel).resolve()
        if rel and candidate.is_file() and dist.resolve() in candidate.parents:
            return web.FileResponse(candidate)
        return web.FileResponse(index)

    app.router.add_get("/", spa)
    app.router.add_get("/app", spa)
    app.router.add_get("/{tail:.*}", spa)
    log.info("Serving Mini App from %s", dist)


def create_api_app(
    *,
    bots: dict[int, Bot],
    settings: Settings,
    sessionmaker: async_sessionmaker,
    redis: Redis,
) -> web.Application:
    app = web.Application(middlewares=[cors_middleware], client_max_size=1024**2 * 10)  # 10MB
    # `bots` is keyed by the bot's Telegram id; a request is bound to whichever bot's
    # token validates its initData. `bot` is the primary (first) for legacy references.
    app["bots"] = bots
    app["bot"] = next(iter(bots.values()), None)
    app["settings"] = settings
    app["sessionmaker"] = sessionmaker
    app["redis"] = redis

    setup_routes(app)

    dist = Path(settings.webapp_dist)
    if (dist / "index.html").is_file():
        _mount_static(app, dist)
    else:
        log.info("Mini App bundle not found at %s — API-only (build webapp to enable UI)", dist)

    return app
